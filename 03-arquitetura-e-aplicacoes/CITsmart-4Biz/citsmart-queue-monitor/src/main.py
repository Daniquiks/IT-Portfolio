import csv
import json
import logging
import os
import re
import sqlite3
import threading
import time
import tkinter as tk
import uuid

from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from logging.handlers import RotatingFileHandler
from pathlib import Path
from queue import Empty, Queue
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List, Optional, Tuple

try:
    import winsound
except ImportError:
    winsound = None

from dotenv import load_dotenv
from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent if SCRIPT_DIR.name.lower() == "src" else SCRIPT_DIR
APP_VERSION = "5.12"

# O arquivo .env real fica fora do Git. Em uma estrutura com src/main.py,
# ele deve ficar na raiz do projeto. O segundo carregamento mantém
# compatibilidade caso o script seja executado diretamente de outra pasta.
load_dotenv(PROJECT_DIR / ".env")
load_dotenv(SCRIPT_DIR / ".env")
load_dotenv()


def env_int(name: str, default: int, minimum: int = 0) -> int:
    try:
        value = int(os.getenv(name, str(default)))
        return max(minimum, value)
    except (TypeError, ValueError):
        return default


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "sim", "yes", "on"}


def env_csv(name: str) -> Tuple[str, ...]:
    return tuple(
        item.strip()
        for item in os.getenv(name, "").split(",")
        if item.strip()
    )


CITSMART_USERNAME = os.getenv("CITSMART_USERNAME", "").strip()
CITSMART_PASSWORD = os.getenv("CITSMART_PASSWORD", "").strip()
CITSMART_QUEUE_URL = os.getenv("CITSMART_QUEUE_URL", "").strip()
CITSMART_AUTH_HOST = os.getenv("CITSMART_AUTH_HOST", "").strip().lower()
SMART_REPORTS_URL = os.getenv("CITSMART_SMART_REPORTS_URL", "").strip()
D1_REQUEST_URL = os.getenv("CITSMART_D1_REQUEST_URL", "").strip()
QUEUE_RECORDS_PER_PAGE = 50

CHECK_INTERVAL_SECONDS = env_int("CHECK_INTERVAL_SECONDS", 15, 5)
SOFT_REFRESH_EVERY_SECONDS = env_int("SOFT_REFRESH_EVERY_SECONDS", 120, 30)
RECONNECT_EVERY_SECONDS = env_int("RECONNECT_EVERY_SECONDS", 60, 10)
OUT_OF_QUEUE_GRACE_SECONDS = env_int("OUT_OF_QUEUE_GRACE_SECONDS", 10, 1)

UNASSIGNED_ALERT_AFTER_MINUTES = env_int(
    "UNASSIGNED_ALERT_AFTER_MINUTES",
    8,
    0,
)
UNASSIGNED_REPEAT_MINUTES = env_int(
    "UNASSIGNED_REPEAT_MINUTES",
    5,
    1,
)

DUE_SOON_MINUTES = env_int("DUE_SOON_MINUTES", 30, 1)
SUSPENDED_ALERT_DAYS = env_int("SUSPENDED_ALERT_DAYS", 14, 1)
DUE_ALERT_REPEAT_MINUTES = env_int("DUE_ALERT_REPEAT_MINUTES", 10, 1)
ERROR_ALERT_COOLDOWN_MINUTES = env_int("ERROR_ALERT_COOLDOWN_MINUTES", 10, 1)
MISSING_CONFIRMATIONS = env_int("MISSING_CONFIRMATIONS", 3, 2)

HEADLESS = env_bool("HEADLESS", False)
BRING_TO_FRONT_ON_ALERT = env_bool("BRING_TO_FRONT_ON_ALERT", True)
CHROME_CHANNEL = os.getenv("CHROME_CHANNEL", "chrome").strip()
LOG_FILE_LEVEL = os.getenv("LOG_FILE_LEVEL", "INFO").upper()

LOG_PATH = Path(os.getenv("LOG_FILE", str(SCRIPT_DIR / "citsmart_monitor.log")))
DB_PATH = Path(
    os.getenv("DATABASE_FILE", str(SCRIPT_DIR / "citsmart_monitor.db"))
)
STATE_PATH = Path(
    os.getenv("STATE_FILE", str(SCRIPT_DIR / "citsmart_monitor_state.json"))
)
BROWSER_SESSION_DIR = Path(
    os.getenv("BROWSER_SESSION_DIR", str(SCRIPT_DIR / "browser_session"))
)
INS_BROWSER_SESSION_DIR = Path(
    os.getenv(
        "INS_BROWSER_SESSION_DIR",
        str(SCRIPT_DIR / "browser_session_ins"),
    )
)
D1_BROWSER_SESSION_DIR = Path(
    os.getenv(
        "D1_BROWSER_SESSION_DIR",
        str(SCRIPT_DIR / "browser_session_d1"),
    )
)

QUEUE_URL_MARKER = "servicerequestincident.load"
SMART_REPORTS_URL_MARKER = "smartreports.load"

# Configurações específicas do fluxo D-1. Não há dados pessoais ou valores
# do ambiente gravados no código-fonte; tudo é fornecido pelo .env local.
D1_REQUESTER_NAME = os.getenv("D1_REQUESTER_NAME", "").strip()
D1_REQUESTER_EMAIL = os.getenv("D1_REQUESTER_EMAIL", "").strip()
D1_CONTACT_ORIGIN = os.getenv("D1_CONTACT_ORIGIN", "").strip()
D1_ACTIVITY = os.getenv("D1_ACTIVITY", "").strip()
D1_CONTACT_METHOD = os.getenv("D1_CONTACT_METHOD", "").strip()
D1_SERVICE_TEAM = os.getenv("D1_SERVICE_TEAM", "").strip()
D1_STATE = os.getenv("D1_STATE", "").strip()
D1_LOCATION = os.getenv("D1_LOCATION", "").strip()
D1_IS_MANAGER = os.getenv("D1_IS_MANAGER", "").strip()

# Identificadores do Smart Reports também dependem de cada ambiente.
INS_PESQUISA_REPORT_ID = env_int("INS_PESQUISA_REPORT_ID", 0, 0)
INS_TIT_REPORT_ID = env_int("INS_TIT_REPORT_ID", 0, 0)
INS_TMS_REPORT_ID = env_int("INS_TMS_REPORT_ID", 0, 0)
INS_CONTRACT_ID = os.getenv("INS_CONTRACT_ID", "").strip()
INS_GROUP_IDS = env_csv("INS_GROUP_IDS")

INS_CONNECTION_SAFETY_DELAY_SECONDS = 2
INS_REPORT_ORDER = ("pesquisa", "tit", "tms")
TMS_TARGETS_BY_HOUR = {
    1: 90.0,
    2: 90.0,
    4: 93.0,
    8: 93.0,
    24: 95.0,
}

# Script exibido no navegador visível da fila. Ele mantém a atualização
# automática ativa, avisa quando a página está incorreta e destaca chamados
# sem responsável. A execução anterior é encerrada antes de uma nova injeção.
QUEUE_BROWSER_MONITOR_SCRIPT = r"""
(() => {
  const AUTO_BUTTON_ID = "button-list-atualizacao-automatica";
  const RECORDS_INPUT_ID = "records-by-page";
  const RECORDS_PER_PAGE = "50";
  const CELL_SELECTOR = "div.tableless-td.ellipsis.responsavel";
  const SCAN_MS = 3000;
  const AUTO_CHECK_MS = 60000;
  const PAGE_CHECK_MS = 10000;
  const POPUP_MS = 2000;
  const SOUND_GAIN = 0.25;
  const HIGHLIGHT = true;
  const HOST_W = window;
  const HOST_DOC = document;

  try { HOST_W.__CITSmartStop?.(); } catch {}

  const normalizeText = value =>
    (value ?? "")
      .toString()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();

  const collectDocuments = () => {
    const documents = [];
    const visited = new Set();
    const collect = win => {
      try {
        if (!win || visited.has(win)) return;
        visited.add(win);
        documents.push(win.document);
        win.document.querySelectorAll("iframe, frame").forEach(frame => {
          try {
            if (frame.contentWindow) collect(frame.contentWindow);
          } catch {}
        });
      } catch {}
    };
    collect(HOST_W);
    return documents;
  };

  const findAutoButton = () => {
    for (const doc of collectDocuments()) {
      try {
        const button = doc.getElementById(AUTO_BUTTON_ID);
        if (button) return { doc, button };
      } catch {}
    }
    return null;
  };

  const findRecordsInput = () => {
    for (const doc of collectDocuments()) {
      try {
        const input = doc.getElementById(RECORDS_INPUT_ID);
        if (input) return input;
      } catch {}
    }
    return null;
  };

  const isQueuePage = () => Boolean(findAutoButton());
  const findGridDocument = () => {
    for (const doc of collectDocuments()) {
      try {
        if (doc.querySelector(CELL_SELECTOR)) return doc;
      } catch {}
    }
    return null;
  };

  const removeInterface = () => {
    [
      "citsmart-monitor-style",
      "citsmart-monitor-status",
      "citsmart-monitor-popup",
      "citsmart-page-warning"
    ].forEach(id => HOST_DOC.getElementById(id)?.remove());
  };
  removeInterface();

  const style = HOST_DOC.createElement("style");
  style.id = "citsmart-monitor-style";
  style.textContent = `
    @keyframes citsmart-blink {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: .55; transform: scale(.96); }
    }
    @keyframes citsmart-popup-show {
      from { opacity: 0; transform: translate(-50%, -50%) scale(.85); }
      to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    }
    #citsmart-monitor-status {
      position: fixed; top: 15px; right: 15px; z-index: 2147483647;
      display: flex; align-items: center; gap: 8px; padding: 9px 13px;
      border: 2px solid #16a34a; border-radius: 30px; background: #fff;
      color: #166534; box-shadow: 0 3px 12px rgba(0,0,0,.30);
      font: bold 13px Arial,sans-serif; animation: citsmart-blink 1.4s infinite;
    }
    #citsmart-monitor-status .status-dot {
      width: 11px; height: 11px; border-radius: 50%; background: #22c55e;
    }
    #citsmart-monitor-popup {
      position: fixed; top: 50%; left: 50%; z-index: 2147483647;
      display: none; min-width: 340px; max-width: 80%; padding: 25px 35px;
      border: 3px solid #dc2626; border-radius: 14px; background: #fff;
      color: #991b1b; box-shadow: 0 15px 50px rgba(0,0,0,.40);
      text-align: center; font-family: Arial,sans-serif; pointer-events: none;
    }
    #citsmart-monitor-popup.show {
      display: block; animation: citsmart-popup-show .2s ease-out;
    }
    #citsmart-monitor-popup .popup-icon { margin-bottom: 10px; font-size: 45px; }
    #citsmart-monitor-popup .popup-title { margin-bottom: 8px; font-size: 23px; font-weight: bold; }
    #citsmart-monitor-popup .popup-body { color: #333; font-size: 17px; }
    #citsmart-page-warning {
      position: fixed; top: 65px; right: 15px; z-index: 2147483647;
      display: none; padding: 10px 14px; border: 2px solid #dc2626;
      border-radius: 8px; background: #fff1f2; color: #991b1b;
      box-shadow: 0 3px 12px rgba(0,0,0,.25); font: bold 13px Arial,sans-serif;
    }
    #citsmart-page-warning.show { display: block; }
  `;

  const status = HOST_DOC.createElement("div");
  status.id = "citsmart-monitor-status";
  status.innerHTML = `<span class="status-dot"></span><span class="status-text">Monitor ativo</span>`;
  const popup = HOST_DOC.createElement("div");
  popup.id = "citsmart-monitor-popup";
  popup.innerHTML = `<div class="popup-icon">🔔</div><div class="popup-title"></div><div class="popup-body"></div>`;
  const pageWarning = HOST_DOC.createElement("div");
  pageWarning.id = "citsmart-page-warning";
  pageWarning.textContent = "⚠ Retorne para a página da fila de chamados.";
  (HOST_DOC.head || HOST_DOC.documentElement).appendChild(style);
  (HOST_DOC.body || HOST_DOC.documentElement).append(status, popup, pageWarning);

  const updateStatus = correctPage => {
    const dot = status.querySelector(".status-dot");
    const text = status.querySelector(".status-text");
    if (correctPage) {
      status.style.borderColor = "#16a34a";
      status.style.color = "#166534";
      dot.style.background = "#22c55e";
      text.textContent = "Monitor ativo";
      pageWarning.classList.remove("show");
    } else {
      status.style.borderColor = "#dc2626";
      status.style.color = "#991b1b";
      dot.style.background = "#ef4444";
      text.textContent = "Página incorreta";
      pageWarning.classList.add("show");
    }
  };

  let popupTimeout = null;
  const showPopup = (title, body) => {
    popup.querySelector(".popup-title").textContent = title;
    popup.querySelector(".popup-body").textContent = body;
    popup.classList.remove("show");
    void popup.offsetWidth;
    popup.classList.add("show");
    if (popupTimeout) HOST_W.clearTimeout(popupTimeout);
    popupTimeout = HOST_W.setTimeout(() => popup.classList.remove("show"), POPUP_MS);
  };

  let audioContext = null;
  const getAudioContext = async () => {
    const AudioContext = HOST_W.AudioContext || HOST_W.webkitAudioContext;
    if (!AudioContext) return null;
    if (!audioContext) audioContext = new AudioContext();
    if (audioContext.state === "suspended") {
      try { await audioContext.resume(); } catch {}
    }
    return audioContext;
  };
  const playNote = async (frequency, durationMs, type = "sine", delayMs = 0, volume = SOUND_GAIN) => {
    try {
      const context = await getAudioContext();
      if (!context) return;
      const oscillator = context.createOscillator();
      const gain = context.createGain();
      const start = context.currentTime + delayMs / 1000;
      const end = start + durationMs / 1000;
      oscillator.type = type;
      oscillator.frequency.value = frequency;
      gain.gain.setValueAtTime(.0001, start);
      gain.gain.linearRampToValueAtTime(volume, start + .02);
      gain.gain.exponentialRampToValueAtTime(.0001, end);
      oscillator.connect(gain).connect(context.destination);
      oscillator.start(start);
      oscillator.stop(end + .03);
    } catch {}
  };
  const playTicketSound = () => {
    playNote(880, 220);
    playNote(1319, 220, "sine", 240);
  };
  const playWrongPageSound = () => {
    playNote(650, 250, "square", 0, .35);
    playNote(450, 300, "square", 300, .35);
  };
  const unlockAudio = () => {
    getAudioContext();
    HOST_DOC.removeEventListener("click", unlockAudio, true);
    HOST_DOC.removeEventListener("keydown", unlockAudio, true);
  };
  HOST_DOC.addEventListener("click", unlockAudio, true);
  HOST_DOC.addEventListener("keydown", unlockAudio, true);

  let lastAutoClick = 0;
  const validateAutoUpdate = () => {
    const data = findAutoButton();
    if (!data) {
      console.warn("[CITSmart] Botão Atualização automática não encontrado.");
      return false;
    }
    const { button } = data;
    if (button.classList.contains("active")) return true;
    const now = Date.now();
    if (now - lastAutoClick < 5000) return false;
    lastAutoClick = now;
    try {
      button.click();
      HOST_W.setTimeout(() => {
        const current = findAutoButton()?.button;
        console.log(current?.classList.contains("active")
          ? "[CITSmart] Atualização automática ativada com sucesso."
          : "[CITSmart] O botão ainda não possui a classe active.");
      }, 1000);
      return true;
    } catch (error) {
      console.error("[CITSmart] Erro ao ativar o botão.", error);
      return false;
    }
  };

  const validateRecordsPerPage = () => {
    const input = findRecordsInput();
    if (!input) {
      console.warn(
        "[CITSmart] Campo Registro por página não encontrado."
      );
      return false;
    }
    if ((input.value || "").trim() === RECORDS_PER_PAGE) {
      return true;
    }

    try {
      const inputWindow = input.ownerDocument.defaultView || HOST_W;
      const setter = Object.getOwnPropertyDescriptor(
        inputWindow.HTMLInputElement.prototype,
        "value"
      )?.set;
      input.focus();
      if (setter) setter.call(input, RECORDS_PER_PAGE);
      else input.value = RECORDS_PER_PAGE;
      input.dispatchEvent(new inputWindow.Event("input", { bubbles: true }));
      input.dispatchEvent(new inputWindow.Event("change", { bubbles: true }));
      input.dispatchEvent(new inputWindow.KeyboardEvent("keydown", {
        key: "Enter",
        code: "Enter",
        keyCode: 13,
        which: 13,
        bubbles: true
      }));
      input.dispatchEvent(new inputWindow.KeyboardEvent("keyup", {
        key: "Enter",
        code: "Enter",
        keyCode: 13,
        which: 13,
        bubbles: true
      }));
      input.blur();
      console.log("[CITSmart] Registro por página ajustado para 50.");
      return true;
    } catch (error) {
      console.error(
        "[CITSmart] Erro ao ajustar Registro por página.",
        error
      );
      return false;
    }
  };

  let lastPageState = null;
  const validateQueuePage = () => {
    const correctPage = isQueuePage();
    updateStatus(correctPage);
    if (!correctPage) {
      console.warn("[CITSmart] Fora da página da fila.");
      playWrongPageSound();
    } else if (lastPageState === false) {
      validateAutoUpdate();
    }
    lastPageState = correctPage;
    return correctPage;
  };

  const seen = new Map();
  let initialScanFinished = false;
  const isEmptyCell = cell => {
    if (!cell) return true;
    let responsible = null;
    try { responsible = cell.querySelector(":scope div[title]"); }
    catch { responsible = cell.querySelector("div[title]"); }
    if (!responsible) return true;
    return !normalizeText(responsible.getAttribute("title"));
  };
  const getRow = cell =>
    cell.closest?.('[role="row"], .tableless-tr, .ui-grid-row, tr, [ng-repeat]') || cell;
  const getRowKey = row => {
    const id = row?.getAttribute?.("id") || row?.dataset?.id || row?.dataset?.rowKey;
    if (id) return `id:${id}`;
    const text = normalizeText(row?.textContent);
    const ticketNumber = text.match(/\b\d{5,}\b/)?.[0];
    return ticketNumber ? `ticket:${ticketNumber}` : `texto:${text.slice(0, 200)}`;
  };
  const handleCell = cell => {
    const row = getRow(cell);
    const key = getRowKey(row);
    const empty = isEmptyCell(cell);
    const previous = seen.get(key);
    if (HIGHLIGHT && cell?.style) cell.style.outline = empty ? "2px dashed red" : "";
    if (!initialScanFinished) {
      seen.set(key, { empty });
      return;
    }
    if (!previous) {
      seen.set(key, { empty });
      if (empty) {
        showPopup("Novo chamado sem responsável", "Verifique a fila de atendimento.");
        playTicketSound();
      }
      return;
    }
    if (!previous.empty && empty) {
      showPopup("Chamado ficou sem responsável", "Verifique a fila de atendimento.");
      playTicketSound();
    }
    seen.set(key, { empty });
  };
  const scanTickets = () => {
    const doc = findGridDocument();
    if (!doc) return;
    const cells = doc.querySelectorAll(CELL_SELECTOR);
    cells.forEach(handleCell);
    if (!initialScanFinished) {
      initialScanFinished = true;
      console.log(`[CITSmart] Scan inicial: ${cells.length} registros.`);
    }
  };

  validateQueuePage();
  validateAutoUpdate();
  validateRecordsPerPage();
  HOST_W.setTimeout(scanTickets, 3000);
  const scanInterval = HOST_W.setInterval(scanTickets, SCAN_MS);
  const autoInterval = HOST_W.setInterval(() => {
    validateAutoUpdate();
    validateRecordsPerPage();
  }, AUTO_CHECK_MS);
  const pageInterval = HOST_W.setInterval(validateQueuePage, PAGE_CHECK_MS);

  HOST_W.__CITSmartStop = () => {
    HOST_W.clearInterval(scanInterval);
    HOST_W.clearInterval(autoInterval);
    HOST_W.clearInterval(pageInterval);
    if (popupTimeout) HOST_W.clearTimeout(popupTimeout);
    HOST_DOC.removeEventListener("click", unlockAudio, true);
    HOST_DOC.removeEventListener("keydown", unlockAudio, true);
    removeInterface();
    if (audioContext && audioContext.state !== "closed") audioContext.close().catch(() => {});
    delete HOST_W.__CITSmartStop;
    console.log("[CITSmart] Monitor encerrado.");
  };
  console.log("[CITSmart] Monitor iniciado.");
})();
"""

INS_REPORT_CONFIG = {
    "pesquisa": {
        "id": INS_PESQUISA_REPORT_ID,
        "label": "PESQUISA",
        "wrap": ".smart-report-content .psq-wrap",
        "subtitle": ".psq-subtitle",
        "filters_container": ".psq-filters",
        "chips": ".psq-filters .psq-chip",
        "kpi_cards": ".psq-kpis .psq-card.kpi",
        "expected_kpis": (
            "Pesquisas Registradas",
            "Com Resposta",
            "Sem Resposta",
            "Pontos (meta ≥ 4)",
        ),
        "form_filters": (
            (
                "Contrato",
                'select[name="PARAM.contrato"]',
                INS_CONTRACT_ID,
            ),
            (
                "Grupo Executor",
                'select[name="PARAM.grupo"]',
                INS_GROUP_IDS,
            ),
            (
                "Nota",
                'select[name="PARAM.nota"]',
                ("-1",),
            ),
            (
                "Situação",
                'select[name="PARAM.situacao"]',
                ("4", "6"),
            ),
            (
                "Prioridade",
                'select[name="PARAM.prioridade"]',
                ("-1",),
            ),
            (
                "Layout",
                'select[name="PARAM.layoutNovo"]',
                "S",
            ),
        ),
    },
    "tit": {
        "id": INS_TIT_REPORT_ID,
        "label": "TIT",
        "wrap": ".smart-report-content .nti-wrap",
        "subtitle": ".nti-subtitle",
        "filters_container": ".nti-filters",
        "chips": ".nti-filters .nti-chip",
        "kpi_cards": ".nti-kpis .nti-card.kpi",
        "expected_kpis": (
            "Total de Chamados",
            "Dentro do Prazo",
            "Fora do Prazo",
            "% Atendimento",
        ),
        "form_filters": (
            (
                "Contrato",
                'select[name="PARAM.contrato"]',
                INS_CONTRACT_ID,
            ),
            (
                "Grupo de Captura",
                'select[name="PARAM.grupo"]',
                INS_GROUP_IDS,
            ),
            (
                "Complemento",
                'select[name="PARAM.complemento"]',
                ("-1",),
            ),
            (
                "Tipo de Demanda",
                'select[name="PARAM.tipo_demanda"]',
                "-1",
            ),
            (
                "Prioridade",
                'select[name="PARAM.prioridade"]',
                ("-1",),
            ),
            (
                "Situação",
                'select[name="PARAM.situacao"]',
                ("4", "6"),
            ),
            (
                "Prazo",
                'select[name="PARAM.prazo"]',
                "-1",
            ),
            (
                "Fase",
                'select[name="PARAM.fase"]',
                "1",
            ),
            (
                "Layout",
                'select[name="PARAM.layoutNovo"]',
                "S",
            ),
        ),
    },
    "tms": {
        "id": INS_TMS_REPORT_ID,
        "label": "TMS",
        "wrap": ".smart-report-content .tms-wrap",
        "subtitle": ".tms-subtitle",
        "filters_container": ".tms-filters",
        "chips": ".tms-filters .tms-chip",
        "kpi_cards": ".tms-kpis .tms-card.kpi",
        "expected_kpis": (
            "Total de Chamados",
            "Dentro do Prazo",
            "Fora do Prazo",
            "% Atendimento",
        ),
        "form_filters": (
            (
                "Contrato",
                'select[name="PARAM.contrato"]',
                INS_CONTRACT_ID,
            ),
            (
                "Grupo de Captura",
                'select[name="PARAM.grupo"]',
                INS_GROUP_IDS,
            ),
            (
                "Complemento",
                'select[name="PARAM.complemento"]',
                ("-1",),
            ),
            (
                "Tipo de Demanda",
                'select[name="PARAM.tipo_demanda"]',
                "-1",
            ),
            (
                "Prioridade",
                'select[name="PARAM.prioridade"]',
                ("-1",),
            ),
            (
                "Situação",
                'select[name="PARAM.situacao"]',
                ("4", "6"),
            ),
            (
                "Prazo",
                'select[name="PARAM.prazo"]',
                "-1",
            ),
            (
                "Layout",
                'select[name="PARAM.layoutNovo"]',
                "S",
            ),
        ),
    },
}

# Seletores ordenados do contador exibido pelo CITSmart. O primeiro grupo
# aponta para o binding Angular que apresenta valores como "8:10".
SLA_SELECTORS = (
    (
        "div.tableless-td.ellipsis.dataLimite "
        "[ng-if*='request.prazohh']"
    ),
    (
        "div.tableless-td.ellipsis.dataLimite "
        "[data-ng-if*='request.prazohh']"
    ),
    # O binding pode aparecer sem uma classe fixa na célula, conforme o
    # layout/ordem de colunas configurado pelo usuário no CITSmart.
    "div[ng-if*='request.prazohh']",
    "div[data-ng-if*='request.prazohh']",
    "div.tableless-td.ellipsis.dataLimite .ng-binding",
    "div.tableless-td.ellipsis.sla .ng-binding",
    "div.tableless-td.ellipsis.prazo .ng-binding",
    ".tempo-restante",
    ".remaining-time",
    "[title*='SLA']",
)


# ==========================================================
# LOG E COMUNICAÇÃO COM A JANELA
# ==========================================================

ui_queue: Queue = Queue()
ins_command_queue: Queue = Queue()
queue_command_queue: Queue = Queue()
d1_command_queue: Queue = Queue()

log = logging.getLogger("citsmart-monitor")
log.setLevel(logging.DEBUG)
log.handlers = []

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

try:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        LOG_PATH,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(getattr(logging, LOG_FILE_LEVEL, logging.INFO))
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
except OSError:
    log.exception("Não foi possível criar o arquivo de log.")

log.propagate = False


def emit_ui(event_type: str, **payload) -> None:
    ui_queue.put({"type": event_type, **payload})


def set_monitor_status(text: str, state: str) -> None:
    emit_ui("status", text=text, state=state)


def beep_alert(level: str = "warning") -> None:
    if winsound is None:
        return

    try:
        if level == "critical":
            winsound.Beep(1300, 400)
            winsound.Beep(1300, 400)
        elif level == "info":
            winsound.Beep(850, 250)
        else:
            winsound.Beep(1050, 350)
    except Exception:
        pass


def local_alert(
    title: str,
    message: str,
    *,
    level: str = "warning",
    sound: bool = True,
) -> None:
    emit_ui(
        "alert",
        title=title,
        message=message,
        level=level,
        alert_at=datetime.now(),
        ticket_id=extract_alert_ticket_id(title, message),
    )
    if sound:
        beep_alert(level)


last_error_alert_at: Optional[datetime] = None


def rate_limited_error_alert(title: str, message: str) -> None:
    global last_error_alert_at

    now = datetime.now()
    cooldown = timedelta(minutes=ERROR_ALERT_COOLDOWN_MINUTES)

    if last_error_alert_at is None or now - last_error_alert_at >= cooldown:
        last_error_alert_at = now
        local_alert(title, message, level="critical")
    else:
        log.warning("Alerta de erro suprimido pelo intervalo de segurança: %s", title)


# ==========================================================
# MODELOS E HISTÓRICO
# ==========================================================

@dataclass
class Ticket:
    ticket_id: str
    request_name: str = ""
    grupo: str = ""
    task_status: str = ""
    owner_text: str = ""
    owner_empty: bool = True
    sla_text: str = ""
    remaining_seconds: Optional[int] = None
    creation_date: str = ""
    limit_date: str = ""
    sla_status: str = ""

    @property
    def suspended(self) -> bool:
        text = normalize_text(self.task_status)
        return "suspens" in text

    @property
    def sla_state(self) -> str:
        if self.suspended:
            return "suspended"

        status = normalize_text(self.sla_status).replace(" ", "")
        if "vencid" in status:
            return "overdue"
        if "avencer" in status:
            return "due_soon"
        if status == "normal":
            return "ok"
        if self.remaining_seconds is None:
            return "unknown"
        if self.remaining_seconds <= 0:
            return "overdue"
        if self.remaining_seconds <= DUE_SOON_MINUTES * 60:
            return "due_soon"
        return "ok"

    @property
    def displayed_sla_status(self) -> str:
        if self.suspended:
            return "Suspenso"
        return self.sla_status or "N/D"

    @property
    def displayed_sla_text(self) -> str:
        if self.suspended:
            return "Suspenso"
        return format_remaining(self.remaining_seconds, self.sla_text)


@dataclass
class ActiveTicket:
    ticket: Ticket
    first_seen: datetime
    first_seen_without_owner: Optional[datetime] = None
    suspended_since: Optional[datetime] = None
    last_unassigned_alert_at: Optional[datetime] = None
    last_due_alert_at: Optional[datetime] = None
    last_due_alert_kind: str = ""


@dataclass
class ExitEvent:
    ticket_id: str
    exited_at: str
    reason: str
    request_name: str
    grupo: str
    owner_text: str
    task_status: str
    sla_text: str
    time_in_queue: str
    creation_date: str = ""
    limit_date: str = ""
    sla_status: str = ""


class StopRequested(Exception):
    pass


def normalize_text(value: str) -> str:
    replacements = str.maketrans(
        "áàâãéèêíìîóòôõúùûç",
        "aaaaeeeiiioooouuuc",
    )
    return (value or "").lower().translate(replacements).strip()


def format_duration(seconds: int) -> str:
    seconds = max(0, int(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    if hours >= 24:
        days, hours = divmod(hours, 24)
        return f"{days}d {hours:02d}h {minutes:02d}min"

    return f"{hours:02d}h {minutes:02d}min {secs:02d}s"


def format_remaining(seconds: Optional[int], fallback: str = "") -> str:
    # Exibe exatamente o valor apresentado pelo CITSmart (por exemplo, 8:10).
    # A conversão para segundos continua sendo usada apenas internamente para
    # classificar o chamado como normal, a vencer ou vencido.
    original_text = (fallback or "").strip()
    if original_text:
        return original_text

    if seconds is None:
        return "N/D"

    absolute_seconds = abs(int(seconds))
    hours, remainder = divmod(absolute_seconds, 3600)
    minutes = remainder // 60
    compact = f"{hours}:{minutes:02d}"
    return f"VENCIDO {compact}" if seconds <= 0 else compact


# ==========================================================
# BANCO LOCAL DE ENTRADAS E CAPTURAS
# ==========================================================

EVENT_LABELS = {
    "BASELINE": "Presente na abertura",
    "ENTRY": "Entrada detectada",
    "REENTRY": "Reentrada detectada",
    "CAPTURE": "Captura detectada",
    "RESOLUTION": "Resolução observada",
    "QUEUE_EXIT": "Saída da fila",
    "SUSPENSION": "Suspensão observada",
}


def local_iso(value: Optional[datetime] = None) -> str:
    moment = value or datetime.now()
    return moment.astimezone().isoformat(timespec="seconds")


def database_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(DB_PATH), timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    with database_connection() as connection:
        connection.execute("PRAGMA journal_mode = WAL")
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS monitor_sessions (
                session_id TEXT PRIMARY KEY,
                started_at TEXT NOT NULL,
                ended_at TEXT
            );

            CREATE TABLE IF NOT EXISTS ticket_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                ticket_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_at TEXT NOT NULL,
                request_name TEXT,
                grupo TEXT,
                task_status TEXT,
                owner_text TEXT,
                sla_text TEXT,
                creation_date TEXT,
                limit_date TEXT,
                sla_status TEXT,
                remaining_seconds INTEGER,
                sla_state TEXT,
                overdue_at_detection INTEGER NOT NULL DEFAULT 0,
                capture_seconds INTEGER,
                notes TEXT,
                FOREIGN KEY (session_id)
                    REFERENCES monitor_sessions(session_id)
            );

            CREATE INDEX IF NOT EXISTS idx_ticket_events_ticket
                ON ticket_events(ticket_id, event_at);

            CREATE INDEX IF NOT EXISTS idx_ticket_events_session
                ON ticket_events(session_id, event_type, event_at);

            CREATE TABLE IF NOT EXISTS ticket_monitor_state (
                ticket_id TEXT PRIMARY KEY,
                suspended_since TEXT
            );
            """
        )

        # Versões anteriores gravavam avisos no SQLite. A partir da versão
        # 5.2 eles existem somente na memória enquanto a janela está aberta.
        connection.execute("DROP TABLE IF EXISTS alert_history")

        # Migração automática de bancos criados por versões anteriores.
        event_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(ticket_events)"
            ).fetchall()
        }
        for column_name in ("creation_date", "limit_date", "sla_status"):
            if column_name not in event_columns:
                connection.execute(
                    f"ALTER TABLE ticket_events ADD COLUMN {column_name} TEXT"
                )


def extract_alert_ticket_id(title: str, message: str) -> str:
    match = re.search(
        r"\bchamado\s*#?\s*(\d+)\b",
        f"{title}\n{message}",
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else ""


def start_database_session(session_id: str, started_at: datetime) -> None:
    with database_connection() as connection:
        connection.execute(
            """
            INSERT INTO monitor_sessions (session_id, started_at)
            VALUES (?, ?)
            """,
            (session_id, local_iso(started_at)),
        )


def finish_database_session(session_id: str, ended_at: datetime) -> None:
    try:
        with database_connection() as connection:
            connection.execute(
                """
                UPDATE monitor_sessions
                SET ended_at = ?
                WHERE session_id = ?
                """,
                (local_iso(ended_at), session_id),
            )
    except sqlite3.Error:
        log.exception("Não foi possível finalizar a sessão no banco local.")


def record_ticket_event(
    session_id: str,
    event_type: str,
    ticket: Ticket,
    event_at: datetime,
    *,
    capture_seconds: Optional[int] = None,
    notes: str = "",
) -> bool:
    try:
        with database_connection() as connection:
            connection.execute(
                """
                INSERT INTO ticket_events (
                    session_id,
                    ticket_id,
                    event_type,
                    event_at,
                    request_name,
                    grupo,
                    task_status,
                    owner_text,
                    sla_text,
                    creation_date,
                    limit_date,
                    sla_status,
                    remaining_seconds,
                    sla_state,
                    overdue_at_detection,
                    capture_seconds,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    ticket.ticket_id,
                    event_type,
                    local_iso(event_at),
                    ticket.request_name,
                    ticket.grupo,
                    ticket.task_status,
                    ticket.owner_text,
                    ticket.displayed_sla_text,
                    ticket.creation_date,
                    ticket.limit_date,
                    ticket.displayed_sla_status,
                    ticket.remaining_seconds,
                    ticket.sla_state,
                    1 if ticket.sla_state == "overdue" else 0,
                    capture_seconds,
                    notes,
                ),
            )
        return True
    except sqlite3.Error as exc:
        log.exception(
            "Falha ao registrar o evento %s do chamado %s.",
            event_type,
            ticket.ticket_id,
        )
        rate_limited_error_alert(
            "Falha no histórico local",
            f"Não foi possível registrar o chamado {ticket.ticket_id}: {exc}",
        )
        return False


def load_suspended_since(ticket_id: str) -> Optional[datetime]:
    try:
        with database_connection() as connection:
            row = connection.execute(
                """
                SELECT suspended_since
                FROM ticket_monitor_state
                WHERE ticket_id = ?
                """,
                (ticket_id,),
            ).fetchone()
        if not row or not row["suspended_since"]:
            return None
        value = datetime.fromisoformat(row["suspended_since"])
        return value.replace(tzinfo=None) if value.tzinfo is not None else value
    except (sqlite3.Error, TypeError, ValueError):
        log.exception(
            "Falha ao recuperar o início da suspensão do chamado %s.",
            ticket_id,
        )
        return None


def save_suspended_since(
    ticket_id: str,
    suspended_since: Optional[datetime],
) -> None:
    try:
        with database_connection() as connection:
            if suspended_since is None:
                connection.execute(
                    "DELETE FROM ticket_monitor_state WHERE ticket_id = ?",
                    (ticket_id,),
                )
                return

            connection.execute(
                """
                INSERT INTO ticket_monitor_state (ticket_id, suspended_since)
                VALUES (?, ?)
                ON CONFLICT(ticket_id) DO UPDATE SET
                    suspended_since = excluded.suspended_since
                """,
                (ticket_id, suspended_since.isoformat(timespec="seconds")),
            )
    except sqlite3.Error:
        log.exception(
            "Falha ao salvar o início da suspensão do chamado %s.",
            ticket_id,
        )


def ticket_was_observed_in_session(
    session_id: str,
    ticket_id: str,
) -> bool:
    try:
        with database_connection() as connection:
            row = connection.execute(
                """
                SELECT 1
                FROM ticket_events
                WHERE session_id = ?
                  AND ticket_id = ?
                  AND event_type IN ('BASELINE', 'ENTRY', 'REENTRY')
                LIMIT 1
                """,
                (session_id, ticket_id),
            ).fetchone()
        return row is not None
    except sqlite3.Error:
        log.exception("Falha ao consultar observações anteriores do chamado.")
        return False


def query_ticket_history(ticket_id: str) -> List[dict]:
    with database_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                session_id,
                ticket_id,
                event_type,
                event_at,
                request_name,
                grupo,
                task_status,
                owner_text,
                sla_text,
                creation_date,
                limit_date,
                sla_status,
                remaining_seconds,
                sla_state,
                overdue_at_detection,
                capture_seconds,
                notes
            FROM ticket_events
            WHERE ticket_id = ?
            ORDER BY event_at, id
            """,
            (ticket_id,),
        ).fetchall()

    return [dict(row) for row in rows]


def event_is_suspended(event: dict) -> bool:
    return "suspens" in normalize_text(event.get("task_status") or "")


def displayed_event_sla_status(event: dict) -> str:
    if event_is_suspended(event):
        return "Suspenso"
    return event.get("sla_status") or "N/D"


def displayed_event_sla_text(event: dict) -> str:
    if event_is_suspended(event):
        return "Suspenso"
    return event.get("sla_text") or "N/D"


def build_ticket_summary(events: List[dict]) -> dict:
    empty_summary = {
        "ticket_id": "N/D",
        "observation_type": "N/D",
        "entry_at": "N/D",
        "creation_date": "N/D",
        "limit_date": "N/D",
        "sla_at_entry": "N/D",
        "sla_status": "N/D",
        "arrived_overdue": "N/D",
        "capture_at": "Não observada",
        "captured_by": "N/D",
        "capture_time": "N/D",
        "resolution_at": "Não observada",
        "resolved_by": "N/D",
        "request_name": "N/D",
        "grupo": "N/D",
        "task_status": "N/D",
    }
    if not events:
        return empty_summary

    observations = [
        event
        for event in events
        if event["event_type"] in {"BASELINE", "ENTRY", "REENTRY"}
    ]
    observation = observations[-1] if observations else events[0]
    observation_index = events.index(observation)
    capture = next(
        (
            event
            for event in events[observation_index + 1 :]
            if event["event_type"] == "CAPTURE"
        ),
        None,
    )
    resolution = next(
        (
            event
            for event in events[observation_index + 1 :]
            if event["event_type"] == "RESOLUTION"
        ),
        None,
    )

    summary = {
        "ticket_id": observation["ticket_id"],
        "observation_type": EVENT_LABELS.get(
            observation["event_type"],
            observation["event_type"],
        ),
        "entry_at": format_database_datetime(observation["event_at"]),
        "creation_date": observation.get("creation_date") or "N/D",
        "limit_date": observation.get("limit_date") or "N/D",
        "sla_at_entry": displayed_event_sla_text(observation),
        "sla_status": displayed_event_sla_status(observation),
        "arrived_overdue": (
            "Sim" if observation["overdue_at_detection"] else "Não"
        ),
        "capture_at": "Não observada",
        "captured_by": "N/D",
        "capture_time": "N/D",
        "resolution_at": "Não observada",
        "resolved_by": "N/D",
        "request_name": observation["request_name"] or "N/D",
        "grupo": observation["grupo"] or "N/D",
        "task_status": observation["task_status"] or "N/D",
    }

    if capture:
        summary["capture_at"] = format_database_datetime(capture["event_at"])
        summary["captured_by"] = capture["owner_text"] or "N/D"
        if capture["capture_seconds"] is not None:
            summary["capture_time"] = format_duration(
                capture["capture_seconds"]
            )
        summary["task_status"] = capture["task_status"] or summary["task_status"]

    if resolution:
        summary["resolution_at"] = format_database_datetime(
            resolution["event_at"]
        )
        summary["resolved_by"] = resolution["owner_text"] or "N/D"
        summary["task_status"] = (
            resolution["task_status"] or summary["task_status"]
        )

    return summary


def format_database_datetime(value: str) -> str:
    try:
        return datetime.fromisoformat(value).strftime("%d/%m/%Y %H:%M:%S")
    except (TypeError, ValueError):
        return value or "N/D"


def query_session_indicators(session_id: str) -> dict:
    month_prefix = datetime.now().strftime("%Y-%m")
    indicators = {
        "baseline": 0,
        "entries": 0,
        "reentries": 0,
        "captures": 0,
        "resolutions": 0,
        "arrived_overdue": 0,
        "average_capture_seconds": None,
        "max_capture_seconds": None,
        "by_owner": [],
    }

    try:
        with database_connection() as connection:
            totals = connection.execute(
                """
                SELECT
                    COUNT(DISTINCT CASE
                        WHEN event_type = 'BASELINE' THEN ticket_id
                    END)
                        AS baseline,
                    COUNT(DISTINCT CASE
                        WHEN event_type = 'ENTRY' THEN ticket_id
                    END)
                        AS entries,
                    COUNT(DISTINCT CASE
                        WHEN event_type = 'REENTRY' THEN ticket_id
                    END)
                        AS reentries,
                    COUNT(DISTINCT CASE
                        WHEN event_type = 'CAPTURE' THEN ticket_id
                    END)
                        AS captures,
                    COUNT(DISTINCT CASE
                        WHEN event_type = 'RESOLUTION' THEN ticket_id
                    END)
                        AS resolutions,
                    COUNT(DISTINCT
                        CASE
                            WHEN event_type IN ('ENTRY', 'REENTRY')
                             AND overdue_at_detection = 1
                            THEN ticket_id
                        END
                    ) AS arrived_overdue,
                    AVG(
                        CASE
                            WHEN event_type = 'CAPTURE'
                            THEN capture_seconds
                        END
                    ) AS average_capture_seconds,
                    MAX(
                        CASE
                            WHEN event_type = 'CAPTURE'
                            THEN capture_seconds
                        END
                    ) AS max_capture_seconds
                FROM ticket_events
                WHERE session_id = ?
                """,
                (session_id,),
            ).fetchone()

            owner_rows = connection.execute(
                """
                SELECT
                    COALESCE(NULLIF(owner_text, ''), 'N/D') AS owner,
                    COUNT(DISTINCT CASE
                        WHEN event_type = 'CAPTURE' THEN ticket_id
                    END) AS captures,
                    COUNT(DISTINCT CASE
                        WHEN event_type = 'RESOLUTION' THEN ticket_id
                    END) AS resolutions,
                    COUNT(DISTINCT ticket_id) AS total
                FROM ticket_events
                WHERE event_at LIKE ?
                  AND event_type IN ('CAPTURE', 'RESOLUTION')
                  AND COALESCE(owner_text, '') != ''
                GROUP BY COALESCE(NULLIF(owner_text, ''), 'N/D')
                ORDER BY resolutions DESC, captures DESC, total DESC, owner
                """,
                (f"{month_prefix}%",),
            ).fetchall()

        if totals:
            indicators.update(
                {
                    "baseline": totals["baseline"] or 0,
                    "entries": totals["entries"] or 0,
                    "reentries": totals["reentries"] or 0,
                    "captures": totals["captures"] or 0,
                    "resolutions": totals["resolutions"] or 0,
                    "arrived_overdue": totals["arrived_overdue"] or 0,
                    "average_capture_seconds": totals[
                        "average_capture_seconds"
                    ],
                    "max_capture_seconds": totals["max_capture_seconds"],
                }
            )
        indicators["by_owner"] = [dict(row) for row in owner_rows]
    except sqlite3.Error:
        log.exception("Falha ao calcular os indicadores da sessão.")

    return indicators


def export_current_month_csv(destination: str) -> int:
    month_prefix = datetime.now().strftime("%Y-%m")

    with database_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                ticket_id,
                event_type,
                event_at,
                creation_date,
                limit_date,
                sla_text,
                sla_status,
                sla_state,
                overdue_at_detection,
                owner_text,
                capture_seconds,
                grupo,
                task_status,
                request_name,
                session_id
            FROM ticket_events
            WHERE event_at LIKE ?
            ORDER BY event_at, id
            """,
            (f"{month_prefix}%",),
        ).fetchall()

    headers = [
        "chamado",
        "evento",
        "data_hora",
        "data_criacao",
        "data_limite",
        "sla",
        "status_sla",
        "estado_sla",
        "chegou_vencido",
        "responsavel",
        "tempo_ate_captura_segundos",
        "grupo",
        "situacao",
        "solicitacao",
        "sessao",
    ]

    with open(destination, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(headers)
        for row in rows:
            suspended = (
                "suspens" in normalize_text(row["task_status"] or "")
            )
            writer.writerow(
                [
                    row["ticket_id"],
                    EVENT_LABELS.get(row["event_type"], row["event_type"]),
                    format_database_datetime(row["event_at"]),
                    row["creation_date"],
                    row["limit_date"],
                    "Suspenso" if suspended else row["sla_text"],
                    "Suspenso" if suspended else row["sla_status"],
                    "suspended" if suspended else row["sla_state"],
                    (
                        "Não"
                        if suspended
                        else (
                            "Sim"
                            if row["overdue_at_detection"]
                            else "Não"
                        )
                    ),
                    row["owner_text"],
                    row["capture_seconds"],
                    row["grupo"],
                    row["task_status"],
                    row["request_name"],
                    row["session_id"],
                ]
            )

    return len(rows)


def load_daily_exits() -> List[ExitEvent]:
    try:
        if not STATE_PATH.exists():
            return []

        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        if data.get("date") != date.today().isoformat():
            return []

        # Mantém apenas uma saída por número de chamado. Isso também limpa
        # duplicidades gravadas por versões anteriores do monitor.
        unique_events: Dict[str, ExitEvent] = {}
        for item in data.get("exits", []):
            event = ExitEvent(**item)
            unique_events.pop(event.ticket_id, None)
            unique_events[event.ticket_id] = event

        return list(unique_events.values())
    except Exception:
        log.exception("Não foi possível ler o histórico diário.")
        return []


def save_daily_exits(events: List[ExitEvent]) -> None:
    try:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "date": date.today().isoformat(),
            "exits": [asdict(event) for event in events[-2000:]],
        }
        temp_path = STATE_PATH.with_suffix(STATE_PATH.suffix + ".tmp")
        temp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(temp_path, STATE_PATH)
    except Exception:
        log.exception("Não foi possível salvar o histórico diário.")


def interruptible_sleep(seconds: int, stop_event: threading.Event) -> None:
    if stop_event.wait(seconds):
        raise StopRequested()


# ==========================================================
# EXTRAÇÃO DO CITSMART
# ==========================================================

def is_browser_closed_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return any(
        text in message
        for text in (
            "target closed",
            "browser has been closed",
            "connection closed",
            "context closed",
            "page closed",
            "event loop is closed",
        )
    )


def is_logged_out(page) -> bool:
    url = (page.url or "").lower()
    keycloak_login = "/openid-connect/auth" in url
    configured_auth_host = (
        bool(CITSMART_AUTH_HOST) and CITSMART_AUTH_HOST in url
    )
    return keycloak_login or configured_auth_host


def is_on_queue_page(page) -> bool:
    return QUEUE_URL_MARKER in (page.url or "").lower()


def login_if_needed(page, destination_url: Optional[str] = None) -> None:
    if not is_logged_out(page):
        return

    if not CITSMART_USERNAME or not CITSMART_PASSWORD:
        raise RuntimeError(
            "A sessão do CITSmart exige login, mas CITSMART_USERNAME ou "
            "CITSMART_PASSWORD não está definido no arquivo .env."
        )

    set_monitor_status("Autenticando no CITSmart...", "connecting")
    log.warning("Sessão ausente ou expirada. Fazendo autenticação.")

    for attempt in range(1, 4):
        try:
            page.wait_for_selector("#username", timeout=15000)
            page.fill("#username", CITSMART_USERNAME)
            page.fill("#password", CITSMART_PASSWORD)
            page.click("#kc-login")
            page.wait_for_load_state("domcontentloaded", timeout=30000)

            page.goto(
                destination_url or CITSMART_QUEUE_URL,
                wait_until="domcontentloaded",
            )
            if is_logged_out(page):
                raise RuntimeError("O CITSmart retornou novamente para a autenticação.")

            log.info("Autenticação realizada.")
            return
        except Exception:
            if attempt == 3:
                raise
            log.exception("Tentativa %s de autenticação falhou.", attempt)
            time.sleep(3)


def extract_text(row, selector: str) -> str:
    try:
        locator = row.locator(selector).first
        if locator.count() == 0:
            return ""
        return (locator.inner_text() or "").strip()
    except Exception:
        return ""


def extract_text_or_title(row, selector: str) -> str:
    try:
        locator = row.locator(selector).first
        if locator.count() == 0:
            return ""

        visible = (locator.inner_text() or "").strip()
        title = (locator.get_attribute("title") or "").strip()

        child = locator.locator("[title]").first
        child_title = ""
        if child.count() > 0:
            child_title = (child.get_attribute("title") or "").strip()

        return title or child_title or visible
    except Exception:
        return ""


def extract_owner(row) -> Tuple[bool, str]:
    text = extract_text_or_title(
        row,
        "div.tableless-td.ellipsis.responsavel",
    )
    return not bool(text), text


def normalize_sla_counter_text(value: str) -> str:
    clean = " ".join((value or "").split())
    if not clean:
        return ""

    # Data limite é uma coluna própria e nunca deve aparecer como contador.
    if re.search(
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b",
        clean,
    ):
        return ""

    normalized = normalize_text(clean)
    if re.fullmatch(
        r"(?:vencid[oa]\s+)?-?\d{1,4}:\d{2}"
        r"(?::\d{2})?",
        normalized,
    ):
        return clean

    # Mantém compatibilidade caso o CITSmart passe a escrever a duração
    # usando unidades em vez do contador HH:MM.
    if re.fullmatch(
        r"(?:vencid[oa]\s+)?-?"
        r"(?:(?:\d+\s*(?:d|dia|dias))\s*)?"
        r"(?:(?:\d+\s*(?:h|hora|horas))\s*)?"
        r"(?:(?:\d+\s*(?:min|minuto|minutos))\s*)?"
        r"(?:(?:\d+\s*(?:seg|segundo|segundos))\s*)?",
        normalized,
    ) and any(character.isdigit() for character in normalized):
        return clean

    return ""


def extract_absolute_datetime_text(value: str) -> str:
    clean = " ".join((value or "").split())
    match = re.search(
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}"
        r"(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?\b",
        clean,
    )
    return match.group(0) if match else ""


def extract_sla_text(row) -> str:
    for selector in SLA_SELECTORS:
        try:
            locators = row.locator(selector)
            for index in range(min(locators.count(), 10)):
                locator = locators.nth(index)
                visible = (locator.inner_text() or "").strip()
                title = (
                    locator.get_attribute("title") or ""
                ).strip()
                for candidate in (visible, title):
                    counter = normalize_sla_counter_text(
                        candidate
                    )
                    if counter:
                        return counter
        except Exception:
            continue

    return ""


def extract_creation_date(row) -> str:
    for selector in (
        "div.tableless-td.dataCriacao .ng-binding",
        ".dataCriacao .ng-binding",
        ".dataCriacao",
    ):
        value = extract_text_or_title(row, selector)
        if value:
            return value
    return ""


def extract_limit_date(row) -> str:
    for selector in (
        "div.tableless-td.dataLimite [ng-if*='request.prazohh']",
        "div.tableless-td.dataLimite [data-ng-if*='request.prazohh']",
        "div.tableless-td.dataLimite .ng-binding",
        ".dataLimite .ng-binding",
        ".dataLimite",
    ):
        value = extract_text_or_title(row, selector)
        absolute = extract_absolute_datetime_text(value)
        if absolute:
            return absolute
    return ""


def extract_sla_status(row) -> str:
    for selector in (
        "div.tableless-td.status .badge",
        ".status .badge",
        "div.tableless-td.status",
    ):
        value = extract_text_or_title(row, selector)
        if value:
            return " ".join(value.split())
    return ""


def parse_sla_remaining_seconds(text: str, now: datetime) -> Optional[int]:
    if not text:
        return None

    normalized = normalize_text(text)

    # Data e hora absolutas: 29/07/2026 18:30 ou 29-07-2026 18:30:00.
    absolute_match = re.search(
        r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})"
        r"(?:\s+(?:as\s*)?(\d{1,2}):(\d{2})(?::(\d{2}))?)?",
        normalized,
    )
    if absolute_match:
        day, month, year, hour, minute, second = absolute_match.groups()
        try:
            due_at = datetime(
                int(year),
                int(month),
                int(day),
                int(hour or 23),
                int(minute or 59),
                int(second or (0 if hour is not None else 59)),
            )
            return int((due_at - now).total_seconds())
        except ValueError:
            pass

    overdue = any(
        word in normalized
        for word in ("vencido", "expirado", "estourado", "fora do prazo")
    )

    # Contador HH:MM ou HH:MM:SS. Um sinal negativo indica prazo vencido.
    clock_match = re.search(r"(?<!\d)(-)?(\d{1,4}):(\d{2})(?::(\d{2}))?(?!\d)", normalized)
    if clock_match:
        negative, first, second, third = clock_match.groups()
        hours = int(first)
        minutes = int(second)
        seconds = int(third or 0)
        total = hours * 3600 + minutes * 60 + seconds
        return -total if negative or overdue else total

    days_match = re.search(r"(\d+)\s*(?:d\b|dia(?:s)?)", normalized)
    hours_match = re.search(r"(\d+)\s*(?:h\b|hora(?:s)?)", normalized)
    minutes_match = re.search(r"(\d+)\s*(?:min\b|minuto(?:s)?)", normalized)
    seconds_match = re.search(r"(\d+)\s*(?:seg\b|segundo(?:s)?)", normalized)

    if any((days_match, hours_match, minutes_match, seconds_match)):
        total = (
            int(days_match.group(1)) * 86400 if days_match else 0
        ) + (
            int(hours_match.group(1)) * 3600 if hours_match else 0
        ) + (
            int(minutes_match.group(1)) * 60 if minutes_match else 0
        ) + (
            int(seconds_match.group(1)) if seconds_match else 0
        )
        return -total if overdue else total

    if overdue:
        return 0

    return None


def find_queue_frame(page):
    contexts = [page, *page.frames]

    # Primeiro procura efetivamente as linhas. Isso evita selecionar o page
    # principal quando a tabela está dentro de um iframe.
    for context in contexts:
        try:
            if context.locator("div.tableless-tr.request-item").count() > 0:
                return context
        except Exception as exc:
            if is_browser_closed_error(exc):
                raise
            log.debug(
                "Falha ao inspecionar contexto %s: %s",
                getattr(context, "url", "N/D"),
                exc,
            )

    # Uma fila vazia não possui linhas. Nesse caso, o botão de atualização
    # automática identifica o contexto correto.
    for context in contexts:
        try:
            if context.locator("#button-list-atualizacao-automatica").count() > 0:
                return context
        except Exception as exc:
            if is_browser_closed_error(exc):
                raise
            log.debug("Falha ao procurar o botão da fila: %s", exc)

    # Não retorna somente pela URL: durante um refresh a URL já está correta,
    # mas a tabela ainda não terminou de carregar. Aceitar esse estado como
    # fila vazia causaria falsas saídas em massa.
    return None


def wait_for_queue_context(page, timeout_ms: int = 30000):
    end_time = time.time() + timeout_ms / 1000

    while time.time() < end_time:
        context = find_queue_frame(page)
        if context is not None:
            return context
        time.sleep(1)

    raise PlaywrightTimeoutError(
        "A estrutura da fila não foi encontrada na página ou nos iframes."
    )


def ensure_queue_records_per_page(context) -> bool:
    try:
        records_input = context.locator("#records-by-page").first
        if records_input.count() == 0:
            log.debug("Campo Registro por página não encontrado.")
            return False

        expected = str(QUEUE_RECORDS_PER_PAGE)
        current = (records_input.input_value() or "").strip()
        if current == expected:
            return True

        records_input.fill(expected)
        records_input.press("Enter")
        records_input.evaluate("element => element.blur()")

        # A alteração recarrega a grade via Angular. Aguarda a atualização
        # para a primeira leitura não considerar as linhas 11 a 50 como
        # novos chamados.
        time.sleep(2.5)

        confirmed = (records_input.input_value() or "").strip()
        if confirmed == expected:
            log.info("Registro por página ajustado para %s.", expected)
            return True

        log.warning(
            "O campo Registro por página não confirmou o valor %s; "
            "valor atual: %s.",
            expected,
            confirmed or "vazio",
        )
        return False
    except Exception:
        log.exception("Falha ao ajustar Registro por página para 50.")
        return False


def ensure_auto_refresh_enabled(context) -> bool:
    try:
        button = context.locator("#button-list-atualizacao-automatica").first
        if button.count() == 0:
            log.debug("Botão de atualização automática não encontrado.")
            return False

        classes = (button.get_attribute("class") or "").lower()
        pressed = (button.get_attribute("aria-pressed") or "").lower()
        enabled = "active" in classes or pressed == "true"

        if enabled:
            return True

        button.click()
        time.sleep(0.8)

        classes = (button.get_attribute("class") or "").lower()
        pressed = (button.get_attribute("aria-pressed") or "").lower()
        enabled = "active" in classes or pressed == "true"

        if enabled:
            log.info("Atualização automática da fila foi ativada.")
            return True

        log.warning("O botão foi clicado, mas não aparenta estar ativo.")
        return False
    except Exception:
        log.exception("Falha ao verificar a atualização automática.")
        return False


def read_tickets(context) -> Dict[str, Ticket]:
    rows = context.locator("div.tableless-tr.request-item")
    tickets: Dict[str, Ticket] = {}
    now = datetime.now()

    for index in range(rows.count()):
        try:
            row = rows.nth(index)
            ticket_id = extract_text(row, ".request-id")
            if not ticket_id:
                continue

            owner_empty, owner_text = extract_owner(row)
            raw_sla_text = extract_sla_text(row)
            creation_date = extract_creation_date(row)
            limit_date = extract_limit_date(row)
            remaining_seconds = parse_sla_remaining_seconds(
                limit_date or raw_sla_text,
                now,
            )
            sla_text = raw_sla_text
            if sla_text and re.search(
                r"\d{1,2}[/-]\d{1,2}[/-]\d{4}",
                sla_text,
            ):
                sla_text = format_remaining(remaining_seconds)
            elif not sla_text and re.fullmatch(
                r"-?\d{1,4}:\d{2}(?::\d{2})?",
                limit_date.strip(),
            ):
                sla_text = limit_date.strip()
            elif not sla_text and remaining_seconds is not None:
                sla_text = format_remaining(remaining_seconds)

            tickets[ticket_id] = Ticket(
                ticket_id=ticket_id,
                request_name=extract_text(row, ".solicitacao .ng-binding"),
                grupo=extract_text(row, ".grupo.atual .ng-binding"),
                task_status=extract_text(row, ".situacao .badge"),
                owner_text=owner_text,
                owner_empty=owner_empty,
                sla_text=sla_text,
                remaining_seconds=remaining_seconds,
                creation_date=creation_date,
                limit_date=limit_date,
                sla_status=extract_sla_status(row),
            )
        except Exception:
            log.exception("Falha ao ler uma linha da fila.")

    return tickets


def goto_queue(page):
    if not is_on_queue_page(page):
        page.goto(CITSMART_QUEUE_URL, wait_until="domcontentloaded")

    context = wait_for_queue_context(page, timeout_ms=30000)
    ensure_queue_records_per_page(context)
    return context


# ==========================================================
# NAVEGADOR E RECONEXÃO
# ==========================================================

def create_browser_context(playwright_instance):
    if not CITSMART_QUEUE_URL:
        raise RuntimeError(
            "CITSMART_QUEUE_URL não está configurada no arquivo .env."
        )

    BROWSER_SESSION_DIR.mkdir(parents=True, exist_ok=True)

    launch_options = {
        "user_data_dir": str(BROWSER_SESSION_DIR),
        "headless": HEADLESS,
        "viewport": {"width": 1600, "height": 900},
    }
    if CHROME_CHANNEL:
        launch_options["channel"] = CHROME_CHANNEL

    try:
        browser = playwright_instance.chromium.launch_persistent_context(
            **launch_options
        )
    except Exception:
        if not CHROME_CHANNEL:
            raise

        log.exception(
            "Não foi possível abrir o canal '%s'. Tentando o Chromium padrão.",
            CHROME_CHANNEL,
        )
        launch_options.pop("channel", None)
        browser = playwright_instance.chromium.launch_persistent_context(
            **launch_options
        )

    page = browser.pages[0] if browser.pages else browser.new_page()
    page.set_default_timeout(15000)

    page.goto(CITSMART_QUEUE_URL, wait_until="domcontentloaded")
    login_if_needed(page)
    context = goto_queue(page)
    ensure_auto_refresh_enabled(context)

    return browser, page, context


def close_browser_safely(browser) -> None:
    try:
        if browser:
            browser.close()
    except Exception:
        pass


def launch_visible_browser(playwright_instance):
    launch_options = {"headless": False}
    if CHROME_CHANNEL:
        launch_options["channel"] = CHROME_CHANNEL

    try:
        return playwright_instance.chromium.launch(
            **launch_options
        )
    except Exception:
        if not CHROME_CHANNEL:
            raise
        log.exception(
            "Falha ao abrir o Chrome visível. "
            "Tentando o Chromium padrão."
        )
        launch_options.pop("channel", None)
        return playwright_instance.chromium.launch(
            **launch_options
        )


def inject_queue_browser_monitor(page) -> None:
    page.wait_for_load_state("domcontentloaded", timeout=30000)
    page.evaluate(QUEUE_BROWSER_MONITOR_SCRIPT)
    log.info("Script visual de monitoramento injetado na fila.")


def restore_queue_browser_monitor(page) -> bool:
    try:
        inject_queue_browser_monitor(page)
        return True
    except Exception:
        log.exception(
            "Não foi possível reaplicar o monitor visual da fila."
        )
        return False


def register_queue_browser_init_script(context) -> bool:
    try:
        context.add_init_script(QUEUE_BROWSER_MONITOR_SCRIPT)
        return True
    except Exception:
        log.exception(
            "Não foi possível registrar o monitor visual para "
            "as próximas navegações."
        )
        return False


def reconnect_until_success(
    playwright_instance,
    browser,
    reason: str,
    stop_event: threading.Event,
):
    close_browser_safely(browser)
    rate_limited_error_alert(
        "Conexão com o CITSmart perdida",
        f"O monitor continuará tentando reconectar.\nMotivo: {reason[:300]}",
    )

    while not stop_event.is_set():
        try:
            set_monitor_status("Reconectando ao CITSmart...", "connecting")
            browser, page, context = create_browser_context(playwright_instance)
            set_monitor_status("Monitor ativo", "active")
            emit_ui(
                "alert",
                title="Conexão restabelecida",
                message="O monitor voltou a acompanhar a fila.",
                level="info",
            )
            log.info("Conexão com o CITSmart restabelecida.")
            return browser, page, context
        except StopRequested:
            raise
        except Exception as exc:
            log.exception("Falha na reconexão: %s", exc)
            interruptible_sleep(RECONNECT_EVERY_SECONDS, stop_event)

    raise StopRequested()


# ==========================================================
# REGRAS DE MONITORAMENTO
# ==========================================================

def make_active_ticket(
    ticket: Ticket,
    now: datetime,
    database_ready: bool = False,
) -> ActiveTicket:
    suspended_since = None

    if ticket.suspended:
        if database_ready:
            suspended_since = load_suspended_since(ticket.ticket_id)
        if suspended_since is None:
            suspended_since = now
            if database_ready:
                save_suspended_since(ticket.ticket_id, suspended_since)
    elif database_ready:
        # Remove um estado antigo caso o programa tenha sido encerrado antes
        # de observar que o chamado deixou de estar suspenso.
        save_suspended_since(ticket.ticket_id, None)

    return ActiveTicket(
        ticket=ticket,
        first_seen=now,
        first_seen_without_owner=now if ticket.owner_empty else None,
        suspended_since=suspended_since,
    )


def queue_problem_text(
    active: ActiveTicket,
    now: Optional[datetime] = None,
) -> str:
    ticket = active.ticket
    moment = now or datetime.now()
    problems = []

    if ticket.owner_empty:
        problems.append("Sem responsável")

    if ticket.sla_state == "overdue":
        problems.append("Vencido")
    elif ticket.sla_state == "due_soon":
        problems.append("A vencer")

    if (
        ticket.suspended
        and active.suspended_since is not None
        and moment - active.suspended_since
        >= timedelta(days=SUSPENDED_ALERT_DAYS)
    ):
        problems.append("Susp +2sem")

    return " | ".join(problems)


def classify_exit(active: ActiveTicket) -> str:
    ticket = active.ticket
    if ticket.suspended:
        return "Suspenso"
    if not ticket.owner_empty:
        return "Resolvido após atribuição"
    return "Saiu da fila"


def register_exit(
    active: ActiveTicket,
    daily_exits: List[ExitEvent],
    now: datetime,
    session_id: str,
    database_ready: bool,
) -> None:
    ticket = active.ticket
    reason = classify_exit(active)
    event = ExitEvent(
        ticket_id=ticket.ticket_id,
        exited_at=now.isoformat(timespec="seconds"),
        reason=reason,
        request_name=ticket.request_name or "N/D",
        grupo=ticket.grupo or "N/D",
        owner_text=ticket.owner_text or "Sem responsável",
        task_status=ticket.task_status or "N/D",
        sla_text=ticket.displayed_sla_text,
        time_in_queue=format_duration((now - active.first_seen).total_seconds()),
        creation_date=ticket.creation_date or "N/D",
        limit_date=ticket.limit_date or "N/D",
        sla_status=ticket.displayed_sla_status,
    )
    # A aba "Saíram hoje" representa chamados únicos. Se o mesmo chamado já
    # estiver no histórico, atualiza sua última saída em vez de duplicá-lo.
    daily_exits[:] = [
        previous
        for previous in daily_exits
        if previous.ticket_id != ticket.ticket_id
    ]
    daily_exits.append(event)
    save_daily_exits(daily_exits)

    if database_ready:
        if reason == "Resolvido após atribuição":
            event_type = "RESOLUTION"
            notes = (
                "Resolução gerencial inferida: o chamado saiu da fila "
                "depois de estar atribuído a um responsável."
            )
        elif reason == "Suspenso":
            event_type = "SUSPENSION"
            notes = "Chamado suspenso quando deixou a fila monitorada."
        else:
            event_type = "QUEUE_EXIT"
            notes = "Chamado deixou a fila sem responsável identificado."

        record_ticket_event(
            session_id,
            event_type,
            ticket,
            now,
            notes=notes,
        )

    local_alert(
        f"Chamado {ticket.ticket_id} saiu da fila",
        f"Classificação: {reason}\nSolicitação: {ticket.request_name or 'N/D'}",
        level="info" if reason == "Resolvido após atribuição" else "warning",
    )


def remove_current_tickets_from_history(
    current_ids,
    daily_exits: List[ExitEvent],
) -> None:
    active_ids = set(current_ids)
    if not active_ids or not daily_exits:
        return

    previous_size = len(daily_exits)
    daily_exits[:] = [
        event
        for event in daily_exits
        if event.ticket_id not in active_ids
    ]

    if len(daily_exits) != previous_size:
        removed = previous_size - len(daily_exits)
        save_daily_exits(daily_exits)
        log.info(
            "%s registro(s) antigo(s) removido(s) de 'Saíram hoje' "
            "porque os chamados estão atualmente na fila.",
            removed,
        )


def monitor_ticket_changes(
    active: ActiveTicket,
    current: Ticket,
    now: datetime,
    session_id: str,
    database_ready: bool,
) -> None:
    previous = active.ticket

    if not previous.suspended and current.suspended:
        active.suspended_since = now
        if database_ready:
            save_suspended_since(current.ticket_id, now)
        local_alert(
            f"Chamado {current.ticket_id} suspenso",
            (
                f"Situação: {current.task_status or 'Suspenso'}\n"
                f"Solicitação: {current.request_name or 'N/D'}"
            ),
            level="warning",
        )
    elif previous.suspended and not current.suspended:
        active.suspended_since = None
        if database_ready:
            save_suspended_since(current.ticket_id, None)
    elif current.suspended and active.suspended_since is None:
        active.suspended_since = now
        if database_ready:
            save_suspended_since(current.ticket_id, now)

    if previous.owner_empty and not current.owner_empty:
        capture_seconds = max(
            0,
            int((now - active.first_seen).total_seconds()),
        )
        active.first_seen_without_owner = None
        active.last_unassigned_alert_at = None
        log.info(
            "Chamado %s foi atribuído a %s.",
            current.ticket_id,
            current.owner_text or "responsável identificado",
        )
        if database_ready:
            record_ticket_event(
                session_id,
                "CAPTURE",
                current,
                now,
                capture_seconds=capture_seconds,
                notes="Captura observada durante o monitoramento.",
            )

    if not previous.owner_empty and current.owner_empty:
        active.first_seen_without_owner = now
        active.last_unassigned_alert_at = None
        local_alert(
            f"Chamado {current.ticket_id} ficou sem responsável",
            f"Solicitação: {current.request_name or 'N/D'}",
            level="warning",
        )

    active.ticket = current


def check_unassigned_alert(active: ActiveTicket, now: datetime) -> None:
    ticket = active.ticket

    if not ticket.owner_empty:
        return

    if active.first_seen_without_owner is None:
        active.first_seen_without_owner = now

    elapsed = now - active.first_seen_without_owner
    if elapsed < timedelta(minutes=UNASSIGNED_ALERT_AFTER_MINUTES):
        return

    repeat = timedelta(minutes=UNASSIGNED_REPEAT_MINUTES)
    if (
        active.last_unassigned_alert_at is not None
        and now - active.last_unassigned_alert_at < repeat
    ):
        return

    active.last_unassigned_alert_at = now
    minutes = max(0, int(elapsed.total_seconds() // 60))
    local_alert(
        f"Chamado {ticket.ticket_id} sem responsável",
        (
            f"Está sem responsável há {minutes} minuto(s).\n"
            f"Solicitação: {ticket.request_name or 'N/D'}"
        ),
        level="critical",
    )


def check_due_alert(active: ActiveTicket, now: datetime) -> None:
    ticket = active.ticket
    kind = ticket.sla_state

    if kind not in {"due_soon", "overdue"}:
        active.last_due_alert_kind = ""
        active.last_due_alert_at = None
        return

    repeat = timedelta(minutes=DUE_ALERT_REPEAT_MINUTES)
    changed_kind = kind != active.last_due_alert_kind
    repeat_elapsed = (
        active.last_due_alert_at is None
        or now - active.last_due_alert_at >= repeat
    )

    if not changed_kind and not repeat_elapsed:
        return

    active.last_due_alert_kind = kind
    active.last_due_alert_at = now
    remaining = ticket.displayed_sla_text

    if kind == "overdue":
        title = f"Chamado {ticket.ticket_id} vencido"
        level = "critical"
    else:
        title = f"Chamado {ticket.ticket_id} a vencer"
        level = "warning"

    local_alert(
        title,
        (
            f"Status do SLA: {ticket.displayed_sla_status}\n"
            f"Prazo: {remaining}\n"
            f"Solicitação: {ticket.request_name or 'N/D'}\n"
            f"Responsável: {ticket.owner_text or 'Sem responsável'}"
        ),
        level=level,
    )


def publish_snapshot(
    tracked: Dict[str, ActiveTicket],
    daily_exits: List[ExitEvent],
    updated_at: datetime,
    session_id: str,
    session_started_at: datetime,
    database_ready: bool,
) -> None:
    indicators = (
        query_session_indicators(session_id)
        if database_ready
        else {
            "baseline": 0,
            "entries": 0,
            "reentries": 0,
            "captures": 0,
            "resolutions": 0,
            "arrived_overdue": 0,
            "average_capture_seconds": None,
            "max_capture_seconds": None,
            "by_owner": [],
        }
    )
    indicators.update(
        {
            "current_queue": len(tracked),
            "current_unassigned": sum(
                active.ticket.owner_empty
                for active in tracked.values()
            ),
            "current_due_soon": sum(
                active.ticket.sla_state == "due_soon"
                for active in tracked.values()
            ),
            "current_overdue": sum(
                active.ticket.sla_state == "overdue"
                for active in tracked.values()
            ),
            "current_suspended": sum(
                active.ticket.suspended
                for active in tracked.values()
            ),
        }
    )

    emit_ui(
        "snapshot",
        active=list(tracked.values()),
        exits=list(daily_exits),
        updated_at=updated_at,
        indicators=indicators,
        session_id=session_id,
        session_started_at=session_started_at,
        database_ready=database_ready,
    )


def rollover_history_if_needed(
    history_date: date,
    daily_exits: List[ExitEvent],
) -> date:
    today = date.today()
    if today != history_date:
        daily_exits.clear()
        save_daily_exits(daily_exits)
        log.info("Histórico diário reiniciado para %s.", today.isoformat())
    return today


# ==========================================================
# CHAMADO DE AUDITORIA D-1
# ==========================================================

def d1_reference_date(today: Optional[date] = None) -> date:
    return (today or date.today()) - timedelta(days=1)


def d1_description(reference: Optional[date] = None) -> str:
    reference_day = reference or d1_reference_date()
    return (
        "##Registro_Auditoria_Tecnica\n"
        "Aberto chamado para registrar auditoria dos chamados e "
        "disponibilidade do ambiente referente ao dia "
        f"{reference_day.strftime('%d/%m')}."
    )


def d1_wait_for_context(
    page,
    selector: str,
    timeout_ms: int = 30000,
):
    deadline = time.time() + timeout_ms / 1000
    last_error: Optional[Exception] = None

    while time.time() < deadline:
        for context in [page, *page.frames]:
            try:
                if context.locator(selector).count() > 0:
                    return context
            except Exception as exc:
                if is_browser_closed_error(exc):
                    raise
                last_error = exc
        time.sleep(0.4)

    message = f"Campo do chamado não encontrado: {selector}"
    if last_error is not None:
        message += f". Último erro: {last_error}"
    raise PlaywrightTimeoutError(message)


def d1_select_option(context, selector: str, label: str) -> None:
    select = context.locator(selector).first
    select.wait_for(state="attached", timeout=20000)
    select.select_option(label=label)

    selected_label = select.evaluate(
        "element => element.selectedOptions[0]?.textContent?.trim() || ''"
    )
    if normalize_text(selected_label) != normalize_text(label):
        raise RuntimeError(
            f"O CITSmart não confirmou a opção '{label}'."
        )


def d1_select_requester(context) -> None:
    requester = context.locator("#request-solicitante").first
    requester.wait_for(state="visible", timeout=20000)
    requester.fill(D1_REQUESTER_NAME)
    time.sleep(1.2)

    clicked = False
    candidate_selectors = (
        "ul.dropdown-menu li",
        ".uib-typeahead-match",
        ".ui-autocomplete li",
        "[role='option']",
        ".autocomplete li",
    )
    for selector in candidate_selectors:
        candidates = context.locator(selector).filter(
            has_text=D1_REQUESTER_NAME
        )
        for index in range(min(candidates.count(), 10)):
            candidate = candidates.nth(index)
            try:
                if not candidate.is_visible():
                    continue
                text = " ".join((candidate.inner_text() or "").split())
                normalized = normalize_text(text)
                if normalize_text(D1_REQUESTER_NAME) not in normalized:
                    continue
                candidate.click()
                clicked = True
                break
            except Exception:
                continue
        if clicked:
            break

    if not clicked:
        requester.press("ArrowDown")
        requester.press("Enter")

    deadline = time.time() + 20
    while time.time() < deadline:
        try:
            if requester.is_disabled():
                break
        except Exception:
            pass
        time.sleep(0.4)
    else:
        raise RuntimeError(
            "O solicitante foi digitado, mas o autocomplete do "
            "CITSmart não confirmou a seleção."
        )

    try:
        context.locator(f"text={D1_REQUESTER_EMAIL}").first.wait_for(
            state="visible",
            timeout=10000,
        )
    except Exception:
        log.warning(
            "Solicitante confirmado, mas o e-mail não ficou visível "
            "durante a validação."
        )


def d1_select_activity(context) -> None:
    search = context.locator(
        "#citsmart-service-request-portfolio-search-input"
    ).first
    search.wait_for(state="visible", timeout=20000)
    search.fill(D1_ACTIVITY)
    time.sleep(1.2)

    clicked = False
    candidate_selectors = (
        "div.selected",
        ".citsmart-service-request-portfolio-search-result",
        "ul.dropdown-menu li",
        ".ui-autocomplete li",
        "[role='option']",
        "strong",
    )
    for selector in candidate_selectors:
        candidates = context.locator(selector).filter(has_text=D1_ACTIVITY)
        for index in range(min(candidates.count(), 10)):
            candidate = candidates.nth(index)
            try:
                if candidate.is_visible():
                    candidate.click()
                    clicked = True
                    break
            except Exception:
                continue
        if clicked:
            break

    if not clicked:
        search.press("ArrowDown")
        search.press("Enter")


def d1_fill_description(context, description: str) -> None:
    iframe_locator = context.locator(
        "#cke_textarea-request-descricao iframe.cke_wysiwyg_frame"
    ).first

    try:
        iframe_locator.wait_for(state="attached", timeout=15000)
        iframe_handle = iframe_locator.element_handle()
        editor_frame = (
            iframe_handle.content_frame()
            if iframe_handle is not None
            else None
        )
        if editor_frame is not None:
            body = editor_frame.locator("body").first
            body.wait_for(state="visible", timeout=10000)
            body.fill(description)
            body.press("Tab")
            return
    except Exception:
        log.exception(
            "Não foi possível preencher a descrição pela área visual "
            "do editor. Tentando a integração do CKEditor."
        )

    html = "".join(
        f"<p>{line}</p>" for line in description.splitlines()
    )
    instance_name = context.evaluate(
        """
        payload => {
          const ckeditor = window.CKEDITOR;
          if (!ckeditor || !ckeditor.instances) return '';
          const names = Object.keys(ckeditor.instances);
          const name = names.find(value =>
            value.includes('textarea-request-descricao')
          );
          if (!name) return '';
          ckeditor.instances[name].setData(payload.html);
          return name;
        }
        """,
        {"html": html},
    )
    if not instance_name:
        raise RuntimeError(
            "O editor da descrição foi encontrado, mas não pôde ser "
            "preenchido."
        )

    time.sleep(0.8)
    context.evaluate(
        """
        name => {
          const instance = window.CKEDITOR?.instances?.[name];
          if (!instance) return;
          instance.updateElement();
          instance.fire('change');
          instance.fire('blur');
        }
        """,
        instance_name,
    )


def d1_prepare_request(page) -> date:
    required_config = {
        "CITSMART_D1_REQUEST_URL": D1_REQUEST_URL,
        "D1_REQUESTER_NAME": D1_REQUESTER_NAME,
        "D1_REQUESTER_EMAIL": D1_REQUESTER_EMAIL,
        "D1_CONTACT_ORIGIN": D1_CONTACT_ORIGIN,
        "D1_ACTIVITY": D1_ACTIVITY,
        "D1_CONTACT_METHOD": D1_CONTACT_METHOD,
        "D1_SERVICE_TEAM": D1_SERVICE_TEAM,
        "D1_STATE": D1_STATE,
        "D1_LOCATION": D1_LOCATION,
        "D1_IS_MANAGER": D1_IS_MANAGER,
    }
    missing = [name for name, value in required_config.items() if not value]
    if missing:
        raise RuntimeError(
            "Configuração D-1 incompleta no .env: " + ", ".join(missing)
        )

    reference = d1_reference_date()
    description = d1_description(reference)

    page.goto(D1_REQUEST_URL, wait_until="domcontentloaded")
    login_if_needed(page, destination_url=D1_REQUEST_URL)
    if D1_REQUEST_URL not in (page.url or ""):
        page.goto(D1_REQUEST_URL, wait_until="domcontentloaded")

    requester_context = d1_wait_for_context(
        page,
        "#request-solicitante",
        timeout_ms=45000,
    )
    d1_select_requester(requester_context)
    d1_select_option(
        requester_context,
        "#select-request-origem-atendimento",
        D1_CONTACT_ORIGIN,
    )
    d1_select_activity(requester_context)

    form_context = d1_wait_for_context(
        page,
        "#div-form-builder #abertura_chamado_tecnicoPage",
        timeout_ms=45000,
    )
    d1_select_option(
        form_context,
        '[id="abertura_chamado.forma_atendimento"] select',
        D1_CONTACT_METHOD,
    )
    d1_select_option(
        form_context,
        '[id="abertura_chamado.atendimento_realizado"] select',
        D1_SERVICE_TEAM,
    )
    d1_select_option(
        form_context,
        '[id="abertura_chamado.id_estado"] select',
        D1_STATE,
    )

    complement = form_context.locator(
        '[id="abertura_chamado.id_localidade"] select'
    ).first
    deadline = time.time() + 25
    while time.time() < deadline:
        option = complement.locator("option").filter(has_text=D1_LOCATION)
        if option.count() > 0:
            break
        time.sleep(0.4)
    else:
        raise RuntimeError(
            "A localidade foi selecionada, mas o CITSmart não carregou "
            f"a opção de complemento '{D1_LOCATION}'."
        )

    d1_select_option(
        form_context,
        '[id="abertura_chamado.id_localidade"] select',
        D1_LOCATION,
    )
    d1_select_option(
        form_context,
        '[id="abertura_chamado.chefe"] select',
        D1_IS_MANAGER,
    )

    already_open = form_context.locator(
        '[id="abertura_chamado.ticket_aberto"] input[type="checkbox"]'
    ).first
    if already_open.count() > 0 and already_open.is_checked():
        already_open.uncheck()

    d1_fill_description(form_context, description)
    page.bring_to_front()
    return reference


def d1_create_browser_context(playwright_instance):
    D1_BROWSER_SESSION_DIR.mkdir(parents=True, exist_ok=True)
    launch_options = {
        "user_data_dir": str(D1_BROWSER_SESSION_DIR),
        "headless": False,
        "viewport": {"width": 1600, "height": 900},
    }
    if CHROME_CHANNEL:
        launch_options["channel"] = CHROME_CHANNEL

    try:
        return playwright_instance.chromium.launch_persistent_context(
            **launch_options
        )
    except Exception:
        if not CHROME_CHANNEL:
            raise
        log.exception(
            "Não foi possível abrir o Chrome para o chamado D-1. "
            "Tentando o Chromium padrão."
        )
        launch_options.pop("channel", None)
        return playwright_instance.chromium.launch_persistent_context(
            **launch_options
        )


def d1_worker(stop_event: threading.Event) -> None:
    browser = None

    try:
        with sync_playwright() as playwright_instance:
            while not stop_event.is_set():
                try:
                    command = d1_command_queue.get(timeout=0.5)
                except Empty:
                    continue

                if command.get("action") == "stop":
                    break
                if command.get("action") != "prepare_d1":
                    continue

                try:
                    emit_ui(
                        "d1_status",
                        text="Abrindo o CITSmart e preparando o chamado...",
                        state="working",
                    )
                    if browser is None:
                        browser = d1_create_browser_context(
                            playwright_instance
                        )

                    page = browser.new_page()
                    page.set_default_timeout(20000)
                    reference = d1_prepare_request(page)
                    emit_ui(
                        "d1_status",
                        text=(
                            "Chamado preenchido para revisão. Confira os "
                            "dados no navegador e, se estiverem corretos, "
                            "use Salvar e Avançar no CITSmart."
                        ),
                        state="success",
                        reference=reference.strftime("%d/%m/%Y"),
                    )
                    log.info(
                        "Chamado D-1 preparado para %s, sem envio "
                        "automático.",
                        reference.strftime("%d/%m/%Y"),
                    )
                except Exception as exc:
                    log.exception("Falha ao preparar o chamado D-1.")
                    if is_browser_closed_error(exc):
                        close_browser_safely(browser)
                        browser = None
                    emit_ui(
                        "d1_status",
                        text=f"Falha ao preparar o chamado: {exc}",
                        state="error",
                    )
                finally:
                    emit_ui("d1_ready")
    finally:
        close_browser_safely(browser)
        emit_ui("d1_stopped")


# ==========================================================
# RELATÓRIOS INS — PESQUISA, TIT E TMS
# ==========================================================

def ins_current_period(
    today: Optional[date] = None,
) -> Tuple[str, str]:
    current_day = today or date.today()
    start = current_day.replace(day=1)
    end = current_day - timedelta(days=1)
    if end < start:
        # No primeiro dia do mês ainda não há período D-1 no mês atual.
        # Nesse caso, usa o mês anterior completo como período inicial.
        start = end.replace(day=1)
    return (
        start.strftime("%d/%m/%Y"),
        end.strftime("%d/%m/%Y"),
    )


def ins_validate_period(
    start_text: str,
    end_text: str,
) -> Tuple[str, str]:
    parsed_dates = []
    for label, value in (
        ("Data inicial", start_text),
        ("Data final", end_text),
    ):
        clean = (value or "").strip()
        try:
            parsed_dates.append(
                datetime.strptime(clean, "%d/%m/%Y").date()
            )
        except ValueError as exc:
            raise ValueError(
                f"{label} inválida. Use o formato dd/mm/aaaa."
            ) from exc

    start_date, end_date = parsed_dates
    if start_date > end_date:
        raise ValueError(
            "A Data inicial não pode ser posterior à Data final."
        )

    return (
        start_date.strftime("%d/%m/%Y"),
        end_date.strftime("%d/%m/%Y"),
    )


def ins_emit_status(text: str, state: str = "working") -> None:
    emit_ui("ins_status", text=text, state=state)


def ins_find_context(page, selector: str, timeout_seconds: int = 30):
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        for context in [page, *page.frames]:
            try:
                if context.locator(selector).count() > 0:
                    return context
            except Exception:
                continue
        time.sleep(0.3)

    raise TimeoutError(
        f"Elemento não encontrado no Smart Reports: {selector}"
    )


def ins_selected_values(locator) -> List[str]:
    return locator.evaluate(
        """
        element => Array.from(element.selectedOptions)
            .map(option => option.value)
        """
    )


def ins_set_select_values(context, selector: str, values) -> None:
    locator = context.locator(selector).first
    locator.wait_for(state="attached", timeout=10000)
    locator.select_option(values, timeout=10000)
    locator.evaluate(
        """
        element => {
            element.dispatchEvent(new Event('input', {bubbles: true}));
            element.dispatchEvent(new Event('change', {bubbles: true}));
            if (window.jQuery) {
                window.jQuery(element).trigger('change');
            }
        }
        """
    )


def ins_set_date_value(
    context,
    selector: str,
    expected_value: str,
) -> bool:
    locator = context.locator(selector).first
    locator.wait_for(state="attached", timeout=10000)
    current_value = (locator.input_value(timeout=5000) or "").strip()
    if current_value == expected_value:
        return False

    locator.evaluate(
        """
        (element, value) => {
            const setter = Object.getOwnPropertyDescriptor(
                HTMLInputElement.prototype,
                'value'
            ).set;
            setter.call(element, value);
            element.classList.toggle('filled', Boolean(value));
            element.dispatchEvent(new Event('input', {bubbles: true}));
            element.dispatchEvent(new Event('change', {bubbles: true}));
            element.dispatchEvent(new Event('blur', {bubbles: true}));
            if (window.jQuery) {
                window.jQuery(element)
                    .val(value)
                    .trigger('input')
                    .trigger('change')
                    .trigger('blur');
            }
        }
        """,
        expected_value,
    )

    actual_value = (locator.input_value(timeout=5000) or "").strip()
    if actual_value != expected_value:
        raise RuntimeError(
            f"O CITSmart manteve a data {actual_value or 'vazia'} "
            f"em vez de {expected_value}."
        )
    return True


def ins_login_if_needed(page) -> None:
    if not is_logged_out(page):
        return

    if not CITSMART_USERNAME or not CITSMART_PASSWORD:
        raise RuntimeError(
            "A sessão dos relatórios exige login, mas "
            "CITSMART_USERNAME ou CITSMART_PASSWORD não está "
            "definido no arquivo .env."
        )

    ins_emit_status("Autenticando os relatórios no CITSmart...")
    page.wait_for_selector("#username", timeout=15000)
    page.fill("#username", CITSMART_USERNAME)
    page.fill("#password", CITSMART_PASSWORD)
    page.click("#kc-login")
    page.wait_for_load_state("domcontentloaded", timeout=30000)
    if is_logged_out(page):
        raise RuntimeError(
            "O CITSmart retornou novamente para a autenticação."
        )


def ins_create_browser_context(playwright_instance):
    required_config = {
        "CITSMART_SMART_REPORTS_URL": SMART_REPORTS_URL,
        "INS_PESQUISA_REPORT_ID": INS_PESQUISA_REPORT_ID,
        "INS_TIT_REPORT_ID": INS_TIT_REPORT_ID,
        "INS_TMS_REPORT_ID": INS_TMS_REPORT_ID,
        "INS_CONTRACT_ID": INS_CONTRACT_ID,
        "INS_GROUP_IDS": INS_GROUP_IDS,
    }
    missing = [name for name, value in required_config.items() if not value]
    if missing:
        raise RuntimeError(
            "Configuração INS incompleta no .env: " + ", ".join(missing)
        )

    INS_BROWSER_SESSION_DIR.mkdir(parents=True, exist_ok=True)
    options = {
        "user_data_dir": str(INS_BROWSER_SESSION_DIR),
        "headless": True,
        "viewport": {"width": 1600, "height": 900},
    }
    if CHROME_CHANNEL:
        options["channel"] = CHROME_CHANNEL

    try:
        browser = (
            playwright_instance.chromium.launch_persistent_context(
                **options
            )
        )
    except Exception:
        if not CHROME_CHANNEL:
            raise
        log.exception(
            "Falha ao abrir o Chrome para o INS. "
            "Tentando o Chromium padrão."
        )
        options.pop("channel", None)
        browser = (
            playwright_instance.chromium.launch_persistent_context(
                **options
            )
        )

    page = browser.pages[0] if browser.pages else browser.new_page()
    page.set_default_timeout(15000)
    page.goto(SMART_REPORTS_URL, wait_until="domcontentloaded")
    ins_login_if_needed(page)
    if SMART_REPORTS_URL_MARKER not in (page.url or "").lower():
        page.goto(SMART_REPORTS_URL, wait_until="domcontentloaded")
    return browser, page


def ins_ensure_reports_page(
    playwright_instance,
    browser,
    page,
):
    if browser is None:
        browser, page = ins_create_browser_context(
            playwright_instance
        )

    if page is None or page.is_closed():
        page = browser.new_page()

    if SMART_REPORTS_URL_MARKER not in (page.url or "").lower():
        page.goto(SMART_REPORTS_URL, wait_until="domcontentloaded")

    ins_login_if_needed(page)
    if SMART_REPORTS_URL_MARKER not in (page.url or "").lower():
        page.goto(SMART_REPORTS_URL, wait_until="domcontentloaded")
    return browser, page


def ins_load_report(page, report_key: str):
    config = INS_REPORT_CONFIG[report_key]
    report_id = config["id"]
    generate_selector = (
        f'button[onclick="UtilSmartReport.process({report_id})"]'
    )

    try:
        return ins_find_context(
            page,
            generate_selector,
            timeout_seconds=3,
        )
    except TimeoutError:
        pass

    menu_context = ins_find_context(
        page,
        "#menu_report_category_item_10",
        timeout_seconds=30,
    )
    report_link = menu_context.locator(
        f"#menu_report_category_report_{report_id} a"
    ).first

    if not report_link.is_visible():
        category_link = menu_context.locator(
            "#menu_report_category_item_10 > a"
        ).first
        category_link.evaluate("element => element.click()")
        report_link.wait_for(state="visible", timeout=15000)

    report_link.evaluate("element => element.click()")
    return ins_find_context(
        page,
        generate_selector,
        timeout_seconds=30,
    )


def ins_ensure_filters_panel_open(
    context,
    report_id: int,
) -> None:
    form = context.locator(f"#formSmartReport{report_id}").first
    if form.count() == 0:
        form = context.locator(
            "#smart-reports-container-params"
        ).first
    form.wait_for(state="attached", timeout=15000)

    widget = form.locator(
        '.widget[data-toggle="collapse-widget"]'
    ).first
    if widget.count() == 0:
        widget = context.locator(
            '#smart-reports-container-params '
            '.widget[data-toggle="collapse-widget"]'
        ).first
    widget.wait_for(state="attached", timeout=15000)

    widget_body = widget.locator(".widget-body").first
    start_field = form.locator(
        '[name="PARAM.dataInicio"]'
    ).first
    end_field = form.locator('[name="PARAM.dataFim"]').first

    def panel_is_open() -> bool:
        collapse_state = (
            widget.get_attribute("data-collapse-closed") or ""
        ).strip().lower()
        body_classes = set(
            (widget_body.get_attribute("class") or "").split()
        )
        return (
            collapse_state == "false"
            and "in" in body_classes
            and widget_body.is_visible()
            and start_field.is_visible()
            and end_field.is_visible()
        )

    if panel_is_open():
        return

    collapse_state = (
        widget.get_attribute("data-collapse-closed") or ""
    ).strip().lower()
    if collapse_state != "false":
        toggle = widget.locator(
            ".widget-head .collapse-toggle"
        ).first
        if toggle.count() == 0:
            raise RuntimeError(
                "O botão para abrir os filtros não foi encontrado."
            )
        toggle.evaluate("element => element.click()")

    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if panel_is_open():
            return
        time.sleep(0.2)

    raise TimeoutError(
        "O painel de filtros não ficou aberto com "
        'data-collapse-closed="false".'
    )


def ins_fill_report_filters(
    context,
    report_key: str,
    start_text: str,
    end_text: str,
) -> None:
    config = INS_REPORT_CONFIG[report_key]
    ins_ensure_filters_panel_open(context, config["id"])
    ins_set_date_value(
        context,
        '[name="PARAM.dataInicio"]',
        start_text,
    )
    ins_set_date_value(
        context,
        '[name="PARAM.dataFim"]',
        end_text,
    )

    for label, selector, values in config["form_filters"]:
        ins_set_select_values(context, selector, values)
        expected = (
            list(values)
            if isinstance(values, tuple)
            else [values]
        )
        actual = ins_selected_values(
            context.locator(selector).first
        )
        if sorted(actual) != sorted(expected):
            raise RuntimeError(
                f"Falha ao selecionar {label}. "
                f"Esperado: {expected}; encontrado: {actual}."
            )


def ins_wait_for_report_result(
    context,
    report_key: str,
    old_subtitle: str,
    start_text: str,
    end_text: str,
    timeout_seconds: int = 120,
) -> None:
    config = INS_REPORT_CONFIG[report_key]
    deadline = time.monotonic() + timeout_seconds
    minimum_accept_time = time.monotonic() + 4
    started_at = time.monotonic()
    last_progress_second = -10

    while time.monotonic() < deadline:
        wrap = context.locator(config["wrap"]).first
        if wrap.count() > 0 and wrap.is_visible():
            subtitle = context.locator(
                config["subtitle"]
            ).first
            subtitle_text = (
                (subtitle.inner_text() or "").strip()
                if subtitle.count() > 0
                else ""
            )
            filters = context.locator(
                config["filters_container"]
            ).first
            filters_text = (
                " ".join((filters.inner_text() or "").split())
                if filters.count() > 0
                else ""
            )
            correct_period = (
                start_text in filters_text
                and end_text in filters_text
            )
            changed = (
                not old_subtitle
                or subtitle_text != old_subtitle
            )
            if correct_period and (
                changed
                or time.monotonic() >= minimum_accept_time
            ):
                return

        elapsed = int(time.monotonic() - started_at)
        if elapsed - last_progress_second >= 10:
            last_progress_second = elapsed
            ins_emit_status(
                f"{config['label']}: aguardando o CITSmart... "
                f"{elapsed}s"
            )
        time.sleep(0.5)

    raise TimeoutError(
        f"O relatório {config['label']} não terminou em "
        f"{timeout_seconds} segundos."
    )


def ins_canonical_kpi_label(
    report_key: str,
    label: str,
) -> str:
    normalized = " ".join(label.split()).casefold()
    if report_key == "pesquisa":
        if normalized.startswith("pesquisas registradas"):
            return "Pesquisas Registradas"
        if normalized.startswith("com resposta"):
            return "Com Resposta"
        if normalized.startswith("sem resposta"):
            return "Sem Resposta"
        if normalized.startswith("pontos"):
            return "Pontos (meta ≥ 4)"
    else:
        if normalized.startswith("total de chamados"):
            return "Total de Chamados"
        if normalized.startswith("dentro do prazo"):
            return "Dentro do Prazo"
        if normalized.startswith("fora do prazo"):
            return "Fora do Prazo"
        if normalized.startswith("% atendimento"):
            return "% Atendimento"
    return " ".join(label.split())


def ins_extract_kpis(
    context,
    report_key: str,
    timeout_seconds: int = 20,
) -> Dict[str, str]:
    config = INS_REPORT_CONFIG[report_key]
    deadline = time.monotonic() + timeout_seconds
    last_result: Dict[str, str] = {}

    while time.monotonic() < deadline:
        cards = context.locator(config["kpi_cards"])
        current: Dict[str, str] = {}
        for index in range(cards.count()):
            card = cards.nth(index)
            label_locator = card.locator(".kpi-label").first
            value_locator = card.locator(".kpi-value").first
            if (
                label_locator.count() == 0
                or value_locator.count() == 0
            ):
                continue
            raw_label = " ".join(
                (label_locator.inner_text() or "").split()
            )
            value = " ".join(
                (value_locator.inner_text() or "").split()
            )
            if raw_label and value:
                current[
                    ins_canonical_kpi_label(
                        report_key,
                        raw_label,
                    )
                ] = value

        last_result = current
        if all(
            current.get(label)
            for label in config["expected_kpis"]
        ):
            return current
        time.sleep(0.2)

    missing = [
        label
        for label in config["expected_kpis"]
        if not last_result.get(label)
    ]
    raise RuntimeError(
        "Indicadores não encontrados: "
        + ", ".join(missing)
    )


def ins_extract_filters(
    context,
    report_key: str,
) -> Dict[str, str]:
    chips = context.locator(
        INS_REPORT_CONFIG[report_key]["chips"]
    )
    result: Dict[str, str] = {}

    for index in range(chips.count()):
        chip = chips.nth(index)
        label_locator = chip.locator("b").first
        label = (
            " ".join((label_locator.inner_text() or "").split())
            if label_locator.count() > 0
            else ""
        )
        full_text = " ".join(
            (chip.inner_text() or "").split()
        )
        value = (
            full_text[len(label):].strip()
            if label
            else full_text
        )
        if label:
            result[label] = value
    return result


def ins_read_table_rows(table, minimum_cells: int) -> List[List[str]]:
    return table.evaluate(
        """
        (table, minimumCells) => {
            const readRows = selector =>
                Array.from(table.querySelectorAll(selector))
                    .map(row =>
                        Array.from(row.querySelectorAll('td'))
                            .map(cell =>
                                (cell.innerText || '')
                                    .trim()
                                    .replace(/\\s+/g, ' ')
                            )
                    )
                    .filter(values =>
                        values.length >= minimumCells
                    );
            return [
                ...readRows('tbody tr'),
                ...readRows('tfoot tr')
            ];
        }
        """,
        minimum_cells,
    )


def ins_find_summary_table(context, report_key: str):
    if report_key == "pesquisa":
        table = context.locator("#exportacsv").first
        return table if table.count() > 0 else None

    prefix = "nti" if report_key == "tit" else "tms"
    expected_title = f"resumo por sla {report_key}"
    cards = context.locator(
        f".{prefix}-grid .{prefix}-card"
    )
    for index in range(cards.count()):
        card = cards.nth(index)
        title = card.locator("h3").first
        title_text = (
            " ".join((title.inner_text() or "").split())
            if title.count() > 0
            else ""
        )
        if title_text.casefold().startswith(expected_title):
            table = card.locator(
                f"table.{prefix}-table"
            ).first
            return table if table.count() > 0 else None
    return None


def ins_extract_summary(
    context,
    report_key: str,
) -> List[List[str]]:
    table = ins_find_summary_table(context, report_key)
    if table is None:
        raise RuntimeError(
            f"O resumo do relatório "
            f"{INS_REPORT_CONFIG[report_key]['label']} "
            "não foi encontrado."
        )
    minimum = 3 if report_key == "pesquisa" else 6
    return ins_read_table_rows(table, minimum)


def ins_parse_percentage(value: str) -> Optional[float]:
    match = re.search(
        r"-?\d+(?:[.,]\d+)?",
        (value or "").replace(" ", ""),
    )
    if not match:
        return None
    try:
        return float(match.group(0).replace(",", "."))
    except ValueError:
        return None


def ins_tms_target_percentage(sla_text: str) -> Optional[float]:
    clean = (sla_text or "").strip().casefold()
    clock_match = re.fullmatch(
        r"(\d{1,3}):\d{2}(?::\d{2})?",
        clean,
    )
    if clock_match:
        return TMS_TARGETS_BY_HOUR.get(
            int(clock_match.group(1))
        )

    hour_match = re.search(
        r"\b(\d{1,3})\s*(?:h|hora|horas)\b",
        clean,
    )
    if hour_match:
        return TMS_TARGETS_BY_HOUR.get(
            int(hour_match.group(1))
        )
    return None


def ins_enrich_tms_summary(
    rows: List[List[str]],
) -> List[List[str]]:
    enriched = []
    for source_row in rows:
        row = list(source_row[:6])
        row.extend([""] * (6 - len(row)))
        sla, total, inside, attended, outside, not_attended = row
        target = ins_tms_target_percentage(sla)
        achieved = ins_parse_percentage(attended)

        if target is None:
            target_text = "—"
            result_text = "—"
        else:
            target_text = f"{target:.0f}%"
            result_text = (
                "Meta atingida"
                if achieved is not None and achieved >= target
                else "Abaixo da meta"
            )

        enriched.append(
            [
                sla,
                total,
                inside,
                attended,
                target_text,
                result_text,
                outside,
                not_attended,
            ]
        )
    return enriched


def export_ins_results_to_csv(
    destination,
    results: Dict[str, dict],
    schemas: Dict[str, dict],
    timestamp: Optional[str] = None,
) -> Tuple[List[Path], List[str]]:
    destination_path = Path(destination)
    if not destination_path.is_dir():
        raise NotADirectoryError(
            f"A pasta selecionada não existe: {destination_path}"
        )

    export_timestamp = timestamp or datetime.now().strftime(
        "%Y-%m-%d_%H%M%S_%f"
    )
    exported_paths: List[Path] = []
    failures: List[str] = []

    for report_key in INS_REPORT_ORDER:
        result = results.get(report_key)
        if not result:
            continue

        schema = schemas.get(report_key)
        if not schema:
            failures.append(
                f"{report_key.upper()}: configuração não encontrada"
            )
            continue

        path = destination_path / (
            f"{report_key}_{export_timestamp}.csv"
        )
        temporary_path = destination_path / (
            f".{path.name}.tmp"
        )

        try:
            filters = result.get("filters", {})
            if not isinstance(filters, dict):
                filters = {}
            kpis = result.get("kpis", {})
            if not isinstance(kpis, dict):
                kpis = {}

            with open(
                temporary_path,
                "w",
                newline="",
                encoding="utf-8-sig",
            ) as csv_file:
                writer = csv.writer(
                    csv_file,
                    delimiter=";",
                    lineterminator="\n",
                )
                writer.writerow(
                    ["Relatório", schema.get("title", report_key.upper())]
                )
                writer.writerow(
                    [
                        "Período",
                        (
                            f"{result.get('start_date', '')} a "
                            f"{result.get('end_date', '')}"
                        ),
                    ]
                )
                writer.writerow([])
                writer.writerow(["Filtros"])
                writer.writerow(["Campo", "Valor"])
                for label, value in filters.items():
                    writer.writerow([label, value])
                writer.writerow([])
                writer.writerow(["Indicadores"])
                writer.writerow(["Indicador", "Valor"])
                for label in schema.get("kpis", ()):
                    writer.writerow(
                        [label, kpis.get(label, "N/D")]
                    )
                writer.writerow([])
                writer.writerow(
                    [schema.get("summary_title", "Resumo")]
                )
                writer.writerow(
                    schema.get("summary_headers", ())
                )
                writer.writerows(result.get("summary", []))
                writer.writerow([])
                writer.writerow(["Detalhamento"])
                writer.writerow(
                    schema.get("detail_headers", ())
                )
                writer.writerows(result.get("details", []))

            os.replace(temporary_path, path)
            exported_paths.append(path)
        except Exception as exc:
            log.exception(
                "Falha ao exportar o CSV do relatório %s.",
                report_key.upper(),
            )
            failures.append(
                f"{report_key.upper()}: {exc}"
            )
        finally:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                log.warning(
                    "Não foi possível remover o arquivo temporário %s.",
                    temporary_path,
                )

    return exported_paths, failures


def ins_extract_details(
    context,
    report_key: str,
) -> List[List[str]]:
    if report_key == "pesquisa":
        detail_card = context.locator("#detalheCard").first
        table = context.locator("#exportacsvdet").first
        if (
            detail_card.count() == 0
            or not detail_card.is_visible()
            or table.count() == 0
        ):
            button = context.locator("#btnDetalhado").first
            button.wait_for(state="attached", timeout=30000)
            button.evaluate("element => element.click()")
            table = context.locator("#exportacsvdet").first
        table.wait_for(state="visible", timeout=30000)
        return table.locator("tbody tr").evaluate_all(
            """
            rows => rows.map(row =>
                Array.from(row.querySelectorAll('td'))
                    .map(cell =>
                        (cell.innerText || '')
                            .trim()
                            .replace(/\\s+/g, ' ')
                    )
            ).filter(values => values.length >= 6)
              .map(values => values.slice(0, 6))
            """
        )

    table = context.locator("#exportacsv").first
    table.wait_for(state="attached", timeout=30000)
    if report_key == "tit":
        return table.locator("tbody tr").evaluate_all(
            """
            rows => rows.map(row => {
                const cells = Array.from(
                    row.querySelectorAll('td')
                );
                if (cells.length < 19) {
                    return [];
                }
                const indexes = [
                    0, 2, 11, 12, 13, 14, 15, 16, 17, 18
                ];
                return indexes.map(index =>
                    (cells[index].innerText || '')
                        .trim()
                        .replace(/\\s+/g, ' ')
                );
            }).filter(values => values.length === 10)
            """
        )

    return table.locator("tbody tr").evaluate_all(
        """
        rows => rows.map(row => {
            const cells = Array.from(
                row.querySelectorAll('td')
            );
            if (cells.length < 16) {
                return [];
            }
            const read = index =>
                (cells[index].innerText || '')
                    .trim()
                    .replace(/\\s+/g, ' ');
            return [
                read(0),
                read(2),
                read(5),
                `${read(6)} ${read(7)}`.trim(),
                `${read(8)} ${read(9)}`.trim(),
                read(10),
                read(11),
                read(12),
                read(14),
                read(15)
            ];
        }).filter(values => values.length === 10)
        """
    )


def ins_generate_report(
    page,
    report_key: str,
    start_text: str,
    end_text: str,
) -> dict:
    config = INS_REPORT_CONFIG[report_key]
    context = ins_load_report(page, report_key)
    ins_ensure_filters_panel_open(context, config["id"])

    subtitle = context.locator(config["subtitle"]).first
    old_subtitle = (
        (subtitle.inner_text() or "").strip()
        if subtitle.count() > 0
        else ""
    )

    ins_fill_report_filters(
        context,
        report_key,
        start_text,
        end_text,
    )
    generate_button = context.locator(
        f'button[onclick="UtilSmartReport.process('
        f'{config["id"]})"]'
    ).first
    generate_button.wait_for(state="visible", timeout=15000)
    generate_button.scroll_into_view_if_needed(timeout=5000)
    generate_button.evaluate("element => element.click()")
    ins_wait_for_report_result(
        context,
        report_key,
        old_subtitle,
        start_text,
        end_text,
    )

    return {
        "kpis": ins_extract_kpis(context, report_key),
        "filters": ins_extract_filters(context, report_key),
        "summary": ins_extract_summary(context, report_key),
        "details": ins_extract_details(context, report_key),
    }


def ins_worker(stop_event: threading.Event) -> None:
    browser = None
    page = None
    visible_browser = None
    visible_context = None
    visible_pages: Dict[str, object] = {}
    try:
        with sync_playwright() as playwright_instance:
            while not stop_event.is_set():
                try:
                    command = ins_command_queue.get(timeout=0.25)
                except Empty:
                    continue

                if command.get("action") == "stop":
                    break
                if command.get("action") == "show_report":
                    report_key = command.get("report_key", "")
                    label = INS_REPORT_CONFIG.get(
                        report_key,
                        {},
                    ).get("label", report_key.upper())
                    try:
                        if report_key not in INS_REPORT_CONFIG:
                            raise ValueError(
                                "Relatório INS inválido."
                            )
                        start_text, end_text = ins_validate_period(
                            command.get("start_date", ""),
                            command.get("end_date", ""),
                        )
                        browser, page = ins_ensure_reports_page(
                            playwright_instance,
                            browser,
                            page,
                        )

                        connected = False
                        if visible_browser is not None:
                            try:
                                connected = visible_browser.is_connected()
                            except Exception:
                                connected = False
                        if not connected:
                            close_browser_safely(visible_browser)
                            visible_browser = launch_visible_browser(
                                playwright_instance
                            )
                            visible_context = (
                                visible_browser.new_context(
                                    storage_state=browser.storage_state(),
                                    viewport={
                                        "width": 1600,
                                        "height": 900,
                                    },
                                )
                            )
                            visible_pages.clear()

                        report_page = visible_pages.get(report_key)
                        if (
                            report_page is None
                            or report_page.is_closed()
                        ):
                            report_page = visible_context.new_page()
                            report_page.set_default_timeout(15000)
                            visible_pages[report_key] = report_page

                        emit_ui(
                            "ins_show_status",
                            report_key=report_key,
                            message=(
                                f"Gerando {label} no navegador visível..."
                            ),
                        )
                        report_page.goto(
                            SMART_REPORTS_URL,
                            wait_until="domcontentloaded",
                        )
                        ins_login_if_needed(report_page)
                        if SMART_REPORTS_URL_MARKER not in (
                            report_page.url or ""
                        ).lower():
                            report_page.goto(
                                SMART_REPORTS_URL,
                                wait_until="domcontentloaded",
                            )
                        ins_generate_report(
                            report_page,
                            report_key,
                            start_text,
                            end_text,
                        )
                        report_page.bring_to_front()
                        emit_ui(
                            "ins_report_shown",
                            report_key=report_key,
                            message=(
                                f"{label} aberto no navegador — "
                                f"{start_text} a {end_text}."
                            ),
                        )
                    except Exception as exc:
                        log.exception(
                            "Falha ao mostrar o relatório %s.",
                            label,
                        )
                        emit_ui(
                            "ins_show_error",
                            report_key=report_key,
                            message=str(exc),
                        )
                    finally:
                        emit_ui(
                            "ins_show_ready",
                            report_key=report_key,
                        )
                    continue

                if command.get("action") != "generate":
                    continue

                completed = 0
                failed = 0
                try:
                    start_text, end_text = ins_validate_period(
                        command.get("start_date", ""),
                        command.get("end_date", ""),
                    )
                    browser, page = ins_ensure_reports_page(
                        playwright_instance,
                        browser,
                        page,
                    )
                    ins_emit_status(
                        "Smart Reports conectado. Aguardando "
                        "2 segundos antes de gerar..."
                    )
                    if stop_event.wait(
                        INS_CONNECTION_SAFETY_DELAY_SECONDS
                    ):
                        break

                    for index, report_key in enumerate(
                        INS_REPORT_ORDER,
                        start=1,
                    ):
                        if stop_event.is_set():
                            break
                        label = INS_REPORT_CONFIG[
                            report_key
                        ]["label"]
                        ins_emit_status(
                            f"{index}/3 — Gerando {label} "
                            f"de {start_text} até {end_text}..."
                        )
                        try:
                            result = ins_generate_report(
                                page,
                                report_key,
                                start_text,
                                end_text,
                            )
                            completed += 1
                            emit_ui(
                                "ins_report_result",
                                report_key=report_key,
                                start_date=start_text,
                                end_date=end_text,
                                **result,
                            )
                        except Exception as exc:
                            failed += 1
                            log.exception(
                                "Falha no relatório INS %s.",
                                label,
                            )
                            emit_ui(
                                "ins_report_error",
                                report_key=report_key,
                                message=str(exc),
                            )

                    emit_ui(
                        "ins_complete",
                        completed=completed,
                        failed=failed,
                        start_date=start_text,
                        end_date=end_text,
                    )
                except Exception as exc:
                    log.exception(
                        "Falha ao conectar os relatórios INS."
                    )
                    emit_ui(
                        "ins_status",
                        text=f"Falha no INS: {exc}",
                        state="error",
                    )
                finally:
                    emit_ui("ins_ready")
    finally:
        close_browser_safely(visible_browser)
        close_browser_safely(browser)
        emit_ui("ins_stopped")


# ==========================================================
# LOOP PRINCIPAL
# ==========================================================

def monitor_main(stop_event: threading.Event) -> None:
    tracked: Dict[str, ActiveTicket] = {}
    missing_counts: Dict[str, int] = {}
    daily_exits = load_daily_exits()
    # Regrava o estado já sem eventuais duplicidades antigas.
    save_daily_exits(daily_exits)
    history_date = date.today()
    initialized = False
    browser = None
    visible_queue_browser = None
    visible_queue_context = None
    visible_queue_page = None
    queue_script_on_main_page = False
    queue_init_script_registered = False
    session_id = uuid.uuid4().hex
    session_started_at = datetime.now()
    database_ready = False

    try:
        initialize_database()
        start_database_session(session_id, session_started_at)
        database_ready = True
        log.info(
            "Sessão local de monitoramento iniciada: %s.",
            session_id,
        )
    except sqlite3.Error as exc:
        log.exception("Não foi possível iniciar o banco local.")
        local_alert(
            "Histórico local indisponível",
            (
                "O monitor continuará funcionando, mas não registrará "
                f"entradas e capturas nesta sessão.\nMotivo: {exc}"
            ),
            level="critical",
        )

    if not CITSMART_QUEUE_URL:
        message = "Defina CITSMART_QUEUE_URL no arquivo .env."
        set_monitor_status(message, "error")
        local_alert("Configuração incompleta", message, level="critical")
        if database_ready:
            finish_database_session(session_id, datetime.now())
        return

    with sync_playwright() as playwright_instance:
        try:
            set_monitor_status("Abrindo o CITSmart...", "connecting")
            browser, page, queue_context = create_browser_context(playwright_instance)
            last_soft_refresh = time.time()
            out_of_queue_since: Optional[float] = None
            wrong_page_alerted = False

            def show_queue_in_browser():
                nonlocal visible_queue_browser
                nonlocal visible_queue_context
                nonlocal visible_queue_page
                nonlocal queue_init_script_registered

                if not HEADLESS:
                    if not queue_init_script_registered:
                        queue_init_script_registered = (
                            register_queue_browser_init_script(
                                browser
                            )
                        )
                    target_page = page
                else:
                    connected = False
                    if visible_queue_browser is not None:
                        try:
                            connected = (
                                visible_queue_browser.is_connected()
                            )
                        except Exception:
                            connected = False
                    if not connected:
                        close_browser_safely(visible_queue_browser)
                        visible_queue_browser = launch_visible_browser(
                            playwright_instance
                        )
                        visible_queue_context = (
                            visible_queue_browser.new_context(
                                storage_state=browser.storage_state(),
                                viewport={
                                    "width": 1600,
                                    "height": 900,
                                },
                            )
                        )
                        register_queue_browser_init_script(
                            visible_queue_context
                        )
                        visible_queue_page = None
                    if (
                        visible_queue_page is None
                        or visible_queue_page.is_closed()
                    ):
                        visible_queue_page = (
                            visible_queue_context.new_page()
                        )
                        visible_queue_page.set_default_timeout(15000)
                    target_page = visible_queue_page

                target_page.goto(
                    CITSMART_QUEUE_URL,
                    wait_until="domcontentloaded",
                )
                login_if_needed(target_page)
                target_context = goto_queue(target_page)
                ensure_auto_refresh_enabled(target_context)
                inject_queue_browser_monitor(target_page)
                target_page.bring_to_front()
                return (
                    target_context
                    if target_page is page
                    else None
                )

            set_monitor_status("Monitor ativo", "active")
            log.info("Monitor local iniciado.")

            while not stop_event.is_set():
                try:
                    while True:
                        try:
                            command = queue_command_queue.get_nowait()
                        except Empty:
                            break
                        if command.get("action") != "show_queue":
                            continue
                        try:
                            emit_ui(
                                "queue_browser_status",
                                text=(
                                    "Abrindo a fila e aplicando o "
                                    "monitor visual..."
                                ),
                                finished=False,
                            )
                            opened_context = show_queue_in_browser()
                            if opened_context is not None:
                                queue_context = opened_context
                                queue_script_on_main_page = True
                            emit_ui(
                                "queue_browser_status",
                                text=(
                                    "Fila aberta no navegador com o "
                                    "monitor visual ativo."
                                ),
                                finished=True,
                            )
                        except Exception as exc:
                            log.exception(
                                "Falha ao abrir a fila no navegador."
                            )
                            emit_ui(
                                "queue_browser_status",
                                text=f"Falha ao abrir a fila: {exc}",
                                finished=True,
                                error=True,
                            )

                    history_date = rollover_history_if_needed(
                        history_date,
                        daily_exits,
                    )

                    if is_logged_out(page):
                        login_if_needed(page)
                        queue_context = goto_queue(page)
                        if queue_script_on_main_page:
                            restore_queue_browser_monitor(page)

                    if not is_on_queue_page(page):
                        if out_of_queue_since is None:
                            out_of_queue_since = time.time()

                        elapsed = time.time() - out_of_queue_since
                        if elapsed >= OUT_OF_QUEUE_GRACE_SECONDS:
                            if not wrong_page_alerted:
                                local_alert(
                                    "CITSmart fora da página da fila",
                                    "O monitor retornará automaticamente para a fila.",
                                    level="critical",
                                )
                                wrong_page_alerted = True

                            page.goto(
                                CITSMART_QUEUE_URL,
                                wait_until="domcontentloaded",
                            )
                            queue_context = goto_queue(page)
                            if queue_script_on_main_page:
                                restore_queue_browser_monitor(page)
                            out_of_queue_since = None
                            wrong_page_alerted = False
                        else:
                            interruptible_sleep(
                                CHECK_INTERVAL_SECONDS,
                                stop_event,
                            )
                            continue
                    else:
                        out_of_queue_since = None
                        wrong_page_alerted = False

                    queue_context = wait_for_queue_context(page, timeout_ms=30000)
                    ensure_queue_records_per_page(queue_context)
                    ensure_auto_refresh_enabled(queue_context)

                    if (
                        time.time() - last_soft_refresh
                        >= SOFT_REFRESH_EVERY_SECONDS
                    ):
                        log.debug("Executando atualização leve da fila.")
                        page.reload(wait_until="domcontentloaded")
                        login_if_needed(page)
                        queue_context = goto_queue(page)
                        ensure_auto_refresh_enabled(queue_context)
                        if queue_script_on_main_page:
                            restore_queue_browser_monitor(page)
                        last_soft_refresh = time.time()

                    current = read_tickets(queue_context)
                    now = datetime.now()

                    # As duas abas são mutuamente exclusivas: um chamado que
                    # está na fila não pode permanecer também em "Saíram hoje".
                    # Isso limpa inclusive falsos registros gravados por uma
                    # versão anterior do monitor.
                    remove_current_tickets_from_history(
                        current.keys(),
                        daily_exits,
                    )

                    if not initialized:
                        tracked = {
                            ticket_id: make_active_ticket(
                                ticket,
                                now,
                                database_ready,
                            )
                            for ticket_id, ticket in current.items()
                        }
                        missing_counts.clear()

                        if database_ready:
                            for ticket in current.values():
                                record_ticket_event(
                                    session_id,
                                    "BASELINE",
                                    ticket,
                                    now,
                                    notes=(
                                        "Chamado já presente quando o "
                                        "monitor foi iniciado."
                                    ),
                                )

                        due_soon_count = 0
                        overdue_count = 0
                        for active in tracked.values():
                            if active.ticket.sla_state == "due_soon":
                                due_soon_count += 1
                            elif active.ticket.sla_state == "overdue":
                                overdue_count += 1
                            else:
                                continue

                            # Evita uma sequência de alertas individuais na
                            # primeira leitura. Depois do intervalo configurado,
                            # cada chamado passa a ser lembrado normalmente.
                            active.last_due_alert_kind = active.ticket.sla_state
                            active.last_due_alert_at = now

                        initialized = True
                        log.info(
                            "Linha de base criada com %s chamado(s).",
                            len(tracked),
                        )

                        if due_soon_count or overdue_count:
                            local_alert(
                                "Prazos encontrados na fila inicial",
                                (
                                    f"A vencer: {due_soon_count}\n"
                                    f"Vencidos: {overdue_count}\n"
                                    "Consulte os chamados destacados na aba "
                                    "Fila atual."
                                ),
                                level=(
                                    "critical"
                                    if overdue_count
                                    else "warning"
                                ),
                            )
                    else:
                        previous_ids = set(tracked)
                        current_ids = set(current)

                        if previous_ids and not current_ids:
                            log.warning(
                                "Leitura temporariamente vazia. "
                                "Nenhuma saída será confirmada nesta leitura."
                            )

                        # Um chamado somente é considerado fora da fila após
                        # desaparecer em várias leituras consecutivas. O
                        # refresh nativo do CITSmart remove as linhas do DOM
                        # por alguns segundos e não representa uma saída real.
                        for ticket_id in previous_ids & current_ids:
                            missing_counts.pop(ticket_id, None)

                        for ticket_id in sorted(previous_ids - current_ids):
                            missing_counts[ticket_id] = (
                                missing_counts.get(ticket_id, 0) + 1
                            )

                            if missing_counts[ticket_id] < MISSING_CONFIRMATIONS:
                                log.info(
                                    "Chamado %s ausente na leitura %s/%s; "
                                    "aguardando confirmação.",
                                    ticket_id,
                                    missing_counts[ticket_id],
                                    MISSING_CONFIRMATIONS,
                                )
                                continue

                            active = tracked.pop(ticket_id)
                            missing_counts.pop(ticket_id, None)
                            register_exit(
                                active,
                                daily_exits,
                                now,
                                session_id,
                                database_ready,
                            )

                        for ticket_id in sorted(current_ids - previous_ids):
                            ticket = current[ticket_id]
                            tracked[ticket_id] = make_active_ticket(ticket, now, database_ready)

                            if database_ready:
                                event_type = (
                                    "REENTRY"
                                    if ticket_was_observed_in_session(
                                        session_id,
                                        ticket_id,
                                    )
                                    else "ENTRY"
                                )
                                record_ticket_event(
                                    session_id,
                                    event_type,
                                    ticket,
                                    now,
                                    notes=(
                                        "Chamado detectado na fila durante "
                                        "o período monitorado."
                                    ),
                                )

                            local_alert(
                                f"Novo chamado {ticket_id} na fila",
                                (
                                    f"Solicitação: {ticket.request_name or 'N/D'}\n"
                                    f"Grupo: {ticket.grupo or 'N/D'}\n"
                                    f"Responsável: "
                                    f"{ticket.owner_text or 'Sem responsável'}"
                                ),
                                level="critical" if ticket.owner_empty else "warning",
                            )

                        for ticket_id in sorted(previous_ids & current_ids):
                            monitor_ticket_changes(
                                tracked[ticket_id],
                                current[ticket_id],
                                now,
                                session_id,
                                database_ready,
                            )

                    for active in tracked.values():
                        check_unassigned_alert(active, now)
                        check_due_alert(active, now)

                    publish_snapshot(
                        tracked,
                        daily_exits,
                        now,
                        session_id,
                        session_started_at,
                        database_ready,
                    )
                    interruptible_sleep(CHECK_INTERVAL_SECONDS, stop_event)

                except StopRequested:
                    raise
                except PlaywrightTimeoutError as exc:
                    log.exception("Timeout ao ler a fila: %s", exc)
                    browser, page, queue_context = reconnect_until_success(
                        playwright_instance,
                        browser,
                        f"Timeout: {exc}",
                        stop_event,
                    )
                    if queue_script_on_main_page:
                        queue_init_script_registered = (
                            register_queue_browser_init_script(
                                browser
                            )
                        )
                        restore_queue_browser_monitor(page)
                    last_soft_refresh = time.time()
                except Exception as exc:
                    log.exception("Erro durante o monitoramento: %s", exc)
                    browser, page, queue_context = reconnect_until_success(
                        playwright_instance,
                        browser,
                        str(exc),
                        stop_event,
                    )
                    if queue_script_on_main_page:
                        queue_init_script_registered = (
                            register_queue_browser_init_script(
                                browser
                            )
                        )
                        restore_queue_browser_monitor(page)
                    last_soft_refresh = time.time()

        except StopRequested:
            log.info("Encerramento solicitado.")
        except Exception as exc:
            log.exception("Não foi possível iniciar o monitor: %s", exc)
            set_monitor_status("Falha ao iniciar o monitor", "error")
            local_alert(
                "Falha ao iniciar o monitor",
                str(exc),
                level="critical",
            )
        finally:
            close_browser_safely(visible_queue_browser)
            close_browser_safely(browser)
            if database_ready:
                finish_database_session(session_id, datetime.now())
            set_monitor_status("Monitor desligado", "stopped")
            log.info("Monitor encerrado.")


# ==========================================================
# JANELA
# ==========================================================

def start_control_window() -> None:
    stop_event = threading.Event()
    started_at = datetime.now()

    root = tk.Tk()
    root.title(f"CITSMART — Controle da fila — versão {APP_VERSION}")
    root.geometry("1600x900")
    root.minsize(1180, 700)

    colors = {
        "bg": "#f7f9fc",
        "card": "#ffffff",
        "text": "#13213a",
        "muted": "#667085",
        "blue": "#155eef",
        "blue_hover": "#0f4fd8",
        "green": "#079455",
        "orange": "#f26a00",
        "red": "#d92d20",
        "dark_red": "#b42318",
        "nav": "#06254a",
        "nav_dark": "#041c38",
        "nav_active": "#155eef",
        "border": "#dfe4ea",
        "heading": "#f3f6fa",
    }
    root.configure(bg=colors["bg"])

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Treeview",
        font=("Segoe UI", 9),
        rowheight=30,
        background=colors["card"],
        fieldbackground=colors["card"],
        foreground=colors["text"],
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 9, "bold"),
        background=colors["heading"],
        foreground=colors["text"],
        relief="flat",
        padding=(6, 7),
    )
    style.map(
        "Treeview",
        background=[("selected", colors["blue"])],
        foreground=[("selected", "#ffffff")],
    )
    style.configure("TNotebook", background=colors["bg"], borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        font=("Segoe UI", 10, "bold"),
        padding=(18, 9),
    )

    status_var = tk.StringVar(value="Iniciando monitor...")
    uptime_var = tk.StringVar(value="Tempo ativo: 00h 00min 00s")
    updated_var = tk.StringVar(value="Última leitura: aguardando")
    alert_var = tk.StringVar(value="")
    monitor_state = {"value": "connecting", "blink": False}
    monitor_finished_reported = {"value": False}

    # ------------------------------------------------------
    # ESTRUTURA PRINCIPAL: SIDEBAR + CONTEÚDO
    # ------------------------------------------------------
    app_shell = tk.Frame(root, bg=colors["bg"])
    app_shell.pack(fill="both", expand=True)

    sidebar = tk.Frame(app_shell, bg=colors["nav"], width=190)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    content = tk.Frame(app_shell, bg=colors["bg"])
    content.pack(side="right", fill="both", expand=True)

    brand = tk.Frame(sidebar, bg=colors["nav"])
    brand.pack(fill="x", padx=18, pady=(24, 18))
    tk.Label(
        brand,
        text="◉",
        font=("Segoe UI Symbol", 24, "bold"),
        fg="#2f80ff",
        bg=colors["nav"],
    ).pack(side="left")
    tk.Label(
        brand,
        text="CITSMART",
        font=("Segoe UI", 17, "bold"),
        fg="#ffffff",
        bg=colors["nav"],
    ).pack(side="left", padx=(8, 0))

    tk.Frame(sidebar, bg="#163b63", height=1).pack(fill="x", padx=14, pady=(0, 10))
    sidebar_nav = tk.Frame(sidebar, bg=colors["nav"])
    sidebar_nav.pack(fill="x", padx=10)

    # ------------------------------------------------------
    # CABEÇALHO
    # ------------------------------------------------------
    header = tk.Frame(content, bg=colors["bg"])
    header.pack(fill="x", padx=28, pady=(20, 10))

    header_left = tk.Frame(header, bg=colors["bg"])
    header_left.pack(side="left", fill="x", expand=True)

    title_line = tk.Frame(header_left, bg=colors["bg"])
    title_line.pack(anchor="w")
    tk.Label(
        title_line,
        text="Controle da fila",
        font=("Segoe UI", 23, "bold"),
        fg=colors["text"],
        bg=colors["bg"],
    ).pack(side="left")
    tk.Label(
        title_line,
        text=f"v{APP_VERSION}",
        font=("Segoe UI", 9, "bold"),
        fg=colors["blue"],
        bg="#eef4ff",
        padx=8,
        pady=4,
    ).pack(side="left", padx=(12, 0), pady=(4, 0))

    status_line = tk.Frame(header_left, bg=colors["bg"])
    status_line.pack(anchor="w", pady=(7, 0))

    status_icon = tk.Label(
        status_line,
        text="●",
        font=("Segoe UI", 12, "bold"),
        fg=colors["orange"],
        bg=colors["bg"],
    )
    status_icon.pack(side="left")

    tk.Label(
        status_line,
        textvariable=status_var,
        font=("Segoe UI", 9),
        fg=colors["text"],
        bg=colors["bg"],
    ).pack(side="left", padx=(6, 13))
    tk.Label(
        status_line,
        text="|",
        font=("Segoe UI", 9),
        fg="#b8c0cc",
        bg=colors["bg"],
    ).pack(side="left")
    tk.Label(
        status_line,
        textvariable=uptime_var,
        font=("Segoe UI", 9),
        fg=colors["muted"],
        bg=colors["bg"],
    ).pack(side="left", padx=13)
    tk.Label(
        status_line,
        text="|",
        font=("Segoe UI", 9),
        fg="#b8c0cc",
        bg=colors["bg"],
    ).pack(side="left")
    tk.Label(
        status_line,
        textvariable=updated_var,
        font=("Segoe UI", 9),
        fg=colors["muted"],
        bg=colors["bg"],
    ).pack(side="left", padx=(13, 0))

    def shutdown_monitor() -> None:
        if stop_event.is_set():
            return
        status_var.set("Encerrando monitor...")
        monitor_state["value"] = "stopping"
        stop_event.set()
        ins_command_queue.put({"action": "stop"})
        d1_command_queue.put({"action": "stop"})
        stop_button.configure(state="disabled", text="Encerrando...")

    stop_button = tk.Button(
        header,
        text="⏻  Desligar monitor",
        command=shutdown_monitor,
        font=("Segoe UI", 10, "bold"),
        bg="#d70000",
        fg="#ffffff",
        activebackground=colors["dark_red"],
        activeforeground="#ffffff",
        relief="flat",
        bd=0,
        padx=18,
        pady=10,
        cursor="hand2",
    )
    stop_button.pack(side="right", padx=(12, 0))

    # Alerta temporário: permanece oculto até existir um aviso.
    alert_frame = tk.Frame(
        content,
        bg="#fff7e6",
        highlightbackground="#f5c36a",
        highlightthickness=1,
    )
    alert_label = tk.Label(
        alert_frame,
        textvariable=alert_var,
        font=("Segoe UI", 10, "bold"),
        fg="#7a3e00",
        bg="#fff7e6",
        justify="left",
        anchor="w",
        padx=14,
        pady=10,
    )
    alert_label.pack(fill="x")

    # ------------------------------------------------------
    # CARDS DE RESUMO DA FILA
    # ------------------------------------------------------
    stats_frame = tk.Frame(content, bg=colors["bg"])
    stats_frame.pack(fill="x", padx=28, pady=(2, 12))

    stat_vars = {
        "queue": tk.StringVar(value="0"),
        "unassigned": tk.StringVar(value="0"),
        "due": tk.StringVar(value="0"),
        "overdue": tk.StringVar(value="0"),
        "exits": tk.StringVar(value="0"),
    }

    cards = (
        ("♟", "Na fila", "queue", colors["blue"]),
        ("♟", "Sem responsável", "unassigned", colors["orange"]),
        ("◷", "A vencer", "due", colors["orange"]),
        ("!", "Vencidos", "overdue", colors["red"]),
        ("↪", "Saíram hoje", "exits", colors["green"]),
    )

    for column, (icon, label, key, accent) in enumerate(cards):
        stats_frame.grid_columnconfigure(column, weight=1, uniform="summary")
        card = tk.Frame(
            stats_frame,
            bg=colors["card"],
            highlightbackground=colors["border"],
            highlightthickness=1,
        )
        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(0 if column == 0 else 6, 0 if column == 4 else 6),
            ipady=4,
        )
        icon_label = tk.Label(
            card,
            text=icon,
            font=("Segoe UI Symbol", 20, "bold"),
            fg=accent,
            bg=colors["card"],
            width=3,
        )
        icon_label.pack(side="left", padx=(12, 4), pady=11)
        metric = tk.Frame(card, bg=colors["card"])
        metric.pack(side="left", fill="both", expand=True, pady=8)
        tk.Label(
            metric,
            textvariable=stat_vars[key],
            font=("Segoe UI", 19, "bold"),
            fg=accent,
            bg=colors["card"],
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            metric,
            text=label,
            font=("Segoe UI", 9),
            fg=colors["text"],
            bg=colors["card"],
            anchor="w",
        ).pack(anchor="w")

    # ------------------------------------------------------
    # PÁGINAS: substitui as abas horizontais por navegação lateral
    # ------------------------------------------------------
    page_container = tk.Frame(content, bg=colors["bg"])
    page_container.pack(fill="both", expand=True, padx=28, pady=(0, 20))
    page_container.grid_rowconfigure(0, weight=1)
    page_container.grid_columnconfigure(0, weight=1)

    queue_tab = tk.Frame(page_container, bg=colors["card"])
    exits_tab = tk.Frame(page_container, bg=colors["card"])
    indicators_tab = tk.Frame(page_container, bg=colors["bg"])
    alerts_tab = tk.Frame(page_container, bg=colors["card"])
    d1_tab = tk.Frame(page_container, bg=colors["bg"])
    ins_tab = tk.Frame(page_container, bg=colors["bg"])

    pages = {
        "queue": queue_tab,
        "exits": exits_tab,
        "alerts": alerts_tab,
        "indicators": indicators_tab,
        "d1": d1_tab,
        "ins": ins_tab,
    }
    for page in pages.values():
        page.grid(row=0, column=0, sticky="nsew")

    sidebar_buttons = {}

    def show_page(page_key: str) -> None:
        page = pages.get(page_key)
        if page is None:
            return
        page.tkraise()
        for key, button in sidebar_buttons.items():
            selected = key == page_key
            button.configure(
                bg=colors["nav_active"] if selected else colors["nav"],
                activebackground=(
                    colors["nav_active"] if selected else colors["nav_dark"]
                ),
            )

    nav_items = (
        ("☷", "Fila atual", "queue"),
        ("↗", "Saíram hoje", "exits"),
        ("♧", "Histórico de avisos", "alerts"),
        ("◔", "Indicadores", "indicators"),
        ("▤", "Chamado D-1", "d1"),
        ("◇", "INS", "ins"),
    )

    for icon, label, key in nav_items:
        button = tk.Button(
            sidebar_nav,
            text=f"{icon}   {label}",
            command=lambda page_key=key: show_page(page_key),
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg=colors["nav"],
            activeforeground="#ffffff",
            activebackground=colors["nav_dark"],
            relief="flat",
            bd=0,
            anchor="w",
            padx=14,
            pady=12,
            cursor="hand2",
        )
        button.pack(fill="x", pady=2)
        sidebar_buttons[key] = button

    # Abre em Indicadores para reproduzir a composição da referência.
    show_page("indicators")

    def make_tree(
        parent,
        columns: Tuple[str, ...],
        headings: Dict[str, str],
        widths: Dict[str, int],
        anchors: Optional[Dict[str, str]] = None,
    ):
        frame = tk.Frame(parent, bg=colors["card"])
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        vertical = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        horizontal = ttk.Scrollbar(
            frame,
            orient="horizontal",
            command=tree.xview,
        )
        tree.configure(
            yscrollcommand=vertical.set,
            xscrollcommand=horizontal.set,
        )

        tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        for column in columns:
            tree.heading(column, text=headings[column])
            tree.column(
                column,
                width=widths[column],
                minwidth=70,
                anchor=(anchors or {}).get(column, "w"),
                stretch=column in {"request", "group"},
            )

        return tree

    queue_toolbar = tk.Frame(queue_tab, bg=colors["card"])
    queue_toolbar.pack(fill="x", padx=10, pady=(10, 6))
    queue_browser_button = tk.Button(
        queue_toolbar,
        text="Abrir fila no navegador",
        command=lambda: request_queue_browser(),
        font=("Segoe UI", 9, "bold"),
        bg=colors["blue"],
        fg="#ffffff",
        activebackground="#1d4ed8",
        activeforeground="#ffffff",
        disabledforeground="#e5e7eb",
        relief="flat",
        padx=12,
        pady=7,
        cursor="hand2",
    )
    queue_browser_button.pack(side="left")
    queue_browser_status_var = tk.StringVar(
        value=(
            "Abre a fila e ativa o monitor visual dentro do navegador."
        )
    )
    tk.Label(
        queue_toolbar,
        textvariable=queue_browser_status_var,
        font=("Segoe UI", 9),
        fg=colors["muted"],
        bg=colors["card"],
    ).pack(side="left", padx=(12, 0))

    queue_columns = (
        "ticket",
        "problem",
        "sla",
        "creation",
        "limit",
        "request",
        "group",
        "owner",
        "status",
        "entered",
    )
    queue_tree = make_tree(
        queue_tab,
        queue_columns,
        {
            "ticket": "Chamado",
            "problem": "Alerta",
            "request": "Solicitação",
            "group": "Grupo",
            "owner": "Responsável",
            "status": "Situação",
            "creation": "Data criação",
            "limit": "Data limite",
            "sla": "SLA",
            "entered": "Detectado às",
        },
        {
            "ticket": 90,
            "problem": 155,
            "request": 330,
            "group": 165,
            "owner": 165,
            "status": 120,
            "creation": 155,
            "limit": 155,
            "sla": 90,
            "entered": 130,
        },
        {"ticket": "center", "problem": "center", "entered": "center"},
    )

    queue_tree.tag_configure("normal", background="#ffffff")
    queue_tree.tag_configure("unassigned", background="#fff7ed")
    queue_tree.tag_configure("suspended", background="#f3e8ff")
    queue_tree.tag_configure(
        "suspended_long",
        background="#ead7ff",
        foreground="#6b21a8",
    )
    queue_tree.tag_configure("due_soon", background="#fef3c7")
    queue_tree.tag_configure(
        "overdue",
        background="#fee2e2",
        foreground=colors["dark_red"],
    )

    exit_columns = (
        "time",
        "ticket",
        "reason",
        "request",
        "group",
        "owner",
        "status",
        "creation",
        "limit",
        "sla_status",
        "sla",
        "duration",
    )
    exits_tree = make_tree(
        exits_tab,
        exit_columns,
        {
            "time": "Horário",
            "ticket": "Chamado",
            "reason": "Classificação",
            "request": "Solicitação",
            "group": "Grupo",
            "owner": "Último responsável",
            "status": "Última situação",
            "creation": "Data criação",
            "limit": "Data limite",
            "sla_status": "Status do SLA",
            "sla": "SLA",
            "duration": "Tempo observado",
        },
        {
            "time": 85,
            "ticket": 90,
            "reason": 150,
            "request": 300,
            "group": 160,
            "owner": 160,
            "status": 125,
            "creation": 155,
            "limit": 155,
            "sla_status": 115,
            "sla": 90,
            "duration": 125,
        },
        {"time": "center", "ticket": "center", "duration": "center"},
    )
    exits_tree.tag_configure("Suspenso", background="#f3e8ff")
    exits_tree.tag_configure("Saiu da fila", background="#fff7ed")
    exits_tree.tag_configure("Capturado / atribuído", background="#ecfdf3")
    exits_tree.tag_configure("Resolvido após atribuição", background="#ecfdf3")

    # ------------------------------------------------------
    # ABA DE INDICADORES DA SESSÃO ATUAL
    # ------------------------------------------------------

    indicator_vars = {
        "baseline": tk.StringVar(value="0"),
        "entries": tk.StringVar(value="0"),
        "reentries": tk.StringVar(value="0"),
        "captures": tk.StringVar(value="0"),
        "resolutions": tk.StringVar(value="0"),
        "arrived_overdue": tk.StringVar(value="0"),
        "average_capture": tk.StringVar(value="N/D"),
        "max_capture": tk.StringVar(value="N/D"),
        "suspended": tk.StringVar(value="0"),
    }

    indicator_header = tk.Frame(indicators_tab, bg=colors["bg"])
    indicator_header.pack(fill="x", padx=12, pady=(12, 8))

    tk.Label(
        indicator_header,
        text="Indicadores do período monitorado",
        font=("Segoe UI", 14, "bold"),
        fg=colors["text"],
        bg=colors["bg"],
    ).pack(side="left")

    indicator_note_var = tk.StringVar(
        value=(
            "Os números começam quando o programa é aberto e contam "
            "chamados únicos."
        )
    )
    tk.Label(
        indicator_header,
        textvariable=indicator_note_var,
        font=("Segoe UI", 9),
        fg=colors["muted"],
        bg=colors["bg"],
    ).pack(side="left", padx=(14, 0))

    indicator_cards_frame = tk.Frame(indicators_tab, bg=colors["bg"])
    indicator_cards_frame.pack(fill="x", padx=12, pady=(0, 10))

    indicator_cards = (
        ("Presentes na abertura", "baseline", colors["muted"]),
        ("Entradas detectadas", "entries", colors["blue"]),
        ("Reentradas", "reentries", colors["orange"]),
        ("Capturas detectadas", "captures", colors["green"]),
        ("Resolvidos observados", "resolutions", colors["green"]),
        ("Entraram vencidos", "arrived_overdue", colors["red"]),
        ("Tempo médio até captura", "average_capture", colors["blue"]),
        ("Maior tempo até captura", "max_capture", colors["orange"]),
        ("Suspensos agora", "suspended", "#7e22ce"),
    )

    for index, (label, key, accent) in enumerate(indicator_cards):
        row, column = divmod(index, 4)
        indicator_cards_frame.grid_columnconfigure(column, weight=1)

        card = tk.Frame(
            indicator_cards_frame,
            bg=colors["card"],
            highlightbackground="#d0d5dd",
            highlightthickness=1,
        )
        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=5,
            pady=5,
        )
        tk.Label(
            card,
            textvariable=indicator_vars[key],
            font=("Segoe UI", 18, "bold"),
            fg=accent,
            bg=colors["card"],
        ).pack(pady=(10, 1))
        tk.Label(
            card,
            text=label,
            font=("Segoe UI", 9),
            fg=colors["muted"],
            bg=colors["card"],
        ).pack(pady=(0, 10))

    indicator_bottom = tk.Frame(indicators_tab, bg=colors["bg"])
    indicator_bottom.pack(fill="both", expand=True, padx=17, pady=(0, 12))

    owner_panel = tk.Frame(
        indicator_bottom,
        bg=colors["card"],
        highlightbackground="#d0d5dd",
        highlightthickness=1,
    )
    owner_panel.pack(side="left", fill="both", expand=True, padx=(0, 6))

    tk.Label(
        owner_panel,
        text=(
            "Ranking mensal por responsável — capturas e resoluções "
            "observadas"
        ),
        font=("Segoe UI", 10, "bold"),
        fg=colors["text"],
        bg=colors["card"],
    ).pack(anchor="w", padx=10, pady=(9, 5))

    tk.Label(
        owner_panel,
        text=(
            "Resolvido = chamado que deixou a fila depois de estar "
            "atribuído a um responsável."
        ),
        font=("Segoe UI", 8),
        fg=colors["muted"],
        bg=colors["card"],
    ).pack(anchor="w", padx=10, pady=(0, 5))

    owner_tree_frame = tk.Frame(owner_panel, bg=colors["card"])
    owner_tree_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
    owner_tree = ttk.Treeview(
        owner_tree_frame,
        columns=("rank", "owner", "captures", "resolutions", "total"),
        show="headings",
        height=6,
    )
    owner_tree.heading("rank", text="#")
    owner_tree.heading("owner", text="Responsável")
    owner_tree.heading("captures", text="Capturados")
    owner_tree.heading("resolutions", text="Resolvidos")
    owner_tree.heading("total", text="Total único")
    owner_tree.column("rank", width=45, anchor="center", stretch=False)
    owner_tree.column("owner", width=260, stretch=True)
    owner_tree.column("captures", width=90, anchor="center", stretch=False)
    owner_tree.column("resolutions", width=90, anchor="center", stretch=False)
    owner_tree.column("total", width=90, anchor="center", stretch=False)
    owner_scroll = ttk.Scrollbar(
        owner_tree_frame,
        orient="vertical",
        command=owner_tree.yview,
    )
    owner_tree.configure(yscrollcommand=owner_scroll.set)
    owner_tree.pack(side="left", fill="both", expand=True)
    owner_scroll.pack(side="right", fill="y")

    export_panel = tk.Frame(
        indicator_bottom,
        bg=colors["card"],
        width=320,
        highlightbackground="#d0d5dd",
        highlightthickness=1,
    )
    export_panel.pack(side="right", fill="y", padx=(6, 0))
    export_panel.pack_propagate(False)

    tk.Label(
        export_panel,
        text="Relatório local",
        font=("Segoe UI", 11, "bold"),
        fg=colors["text"],
        bg=colors["card"],
    ).pack(anchor="w", padx=14, pady=(14, 5))
    tk.Label(
        export_panel,
        text=(
            "Exporta somente os eventos de entrada, reentrada, "
            "presença inicial e captura do mês atual."
        ),
        font=("Segoe UI", 9),
        fg=colors["muted"],
        bg=colors["card"],
        justify="left",
        wraplength=285,
    ).pack(anchor="w", padx=14, pady=(0, 12))

    export_status_var = tk.StringVar(value="")
    export_button = tk.Button(
        export_panel,
        text="Exportar mês atual (CSV)",
        command=lambda: export_month_from_ui(),
        font=("Segoe UI", 9, "bold"),
        bg=colors["blue"],
        fg="#ffffff",
        activebackground="#1d4ed8",
        activeforeground="#ffffff",
        relief="flat",
        padx=12,
        pady=8,
        cursor="hand2",
    )
    export_button.pack(fill="x", padx=14)
    tk.Label(
        export_panel,
        textvariable=export_status_var,
        font=("Segoe UI", 8),
        fg=colors["muted"],
        bg=colors["card"],
        justify="left",
        wraplength=285,
    ).pack(anchor="w", padx=14, pady=(10, 0))

    # ------------------------------------------------------
    # ABA CHAMADO D-1
    # ------------------------------------------------------

    d1_initial_reference = d1_reference_date()
    d1_reference_var = tk.StringVar(
        value=(
            "Referência automática: "
            + d1_initial_reference.strftime("%d/%m/%Y")
        )
    )
    d1_description_var = tk.StringVar(
        value=d1_description(d1_initial_reference)
    )
    d1_status_var = tk.StringVar(
        value=(
            "O navegador será aberto com os campos preenchidos. "
            "O envio permanece manual para conferência."
        )
    )

    d1_header = tk.Frame(d1_tab, bg=colors["bg"])
    d1_header.pack(fill="x", padx=18, pady=(18, 10))
    d1_header_left = tk.Frame(d1_header, bg=colors["bg"])
    d1_header_left.pack(side="left", fill="x", expand=True)
    tk.Label(
        d1_header_left,
        text="Preparar chamado de auditoria D-1",
        font=("Segoe UI", 15, "bold"),
        fg=colors["text"],
        bg=colors["bg"],
    ).pack(anchor="w")
    tk.Label(
        d1_header_left,
        textvariable=d1_reference_var,
        font=("Segoe UI", 10, "bold"),
        fg=colors["blue"],
        bg=colors["bg"],
    ).pack(anchor="w", pady=(3, 0))

    d1_prepare_button = tk.Button(
        d1_header,
        text="Abrir e preencher chamado D-1",
        command=lambda: request_d1_ticket(),
        font=("Segoe UI", 10, "bold"),
        bg=colors["green"],
        fg="#ffffff",
        activebackground="#15803d",
        activeforeground="#ffffff",
        disabledforeground="#e5e7eb",
        relief="flat",
        padx=16,
        pady=9,
        cursor="hand2",
    )
    d1_prepare_button.pack(side="right", padx=(12, 0))

    d1_card = tk.Frame(
        d1_tab,
        bg=colors["card"],
        highlightbackground="#d0d5dd",
        highlightthickness=1,
    )
    d1_card.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    d1_status_label = tk.Label(
        d1_card,
        textvariable=d1_status_var,
        font=("Segoe UI", 10),
        fg=colors["muted"],
        bg=colors["card"],
        justify="left",
        anchor="w",
        wraplength=1120,
    )
    d1_status_label.pack(fill="x", padx=18, pady=(16, 14))

    d1_fields = (
        ("Solicitante", D1_REQUESTER_NAME),
        ("Origem do contato", D1_CONTACT_ORIGIN),
        ("Atividade", D1_ACTIVITY),
        ("Forma de contato", D1_CONTACT_METHOD),
        ("Atendimento", D1_SERVICE_TEAM),
        ("Localidade", D1_STATE),
        ("Complemento", D1_LOCATION),
        ("Chefe ou substituto", D1_IS_MANAGER),
    )
    d1_fields_frame = tk.Frame(d1_card, bg=colors["card"])
    d1_fields_frame.pack(fill="x", padx=18)
    for row_index, (field_label, field_value) in enumerate(d1_fields):
        tk.Label(
            d1_fields_frame,
            text=field_label + ":",
            font=("Segoe UI", 9, "bold"),
            fg=colors["muted"],
            bg=colors["card"],
            anchor="w",
            width=22,
        ).grid(row=row_index, column=0, sticky="w", pady=3)
        tk.Label(
            d1_fields_frame,
            text=field_value,
            font=("Segoe UI", 9),
            fg=colors["text"],
            bg=colors["card"],
            anchor="w",
        ).grid(row=row_index, column=1, sticky="w", pady=3)

    tk.Label(
        d1_card,
        text="Descrição gerada:",
        font=("Segoe UI", 9, "bold"),
        fg=colors["muted"],
        bg=colors["card"],
    ).pack(anchor="w", padx=18, pady=(16, 4))
    tk.Label(
        d1_card,
        textvariable=d1_description_var,
        font=("Consolas", 10),
        fg=colors["text"],
        bg="#f8fafc",
        justify="left",
        anchor="nw",
        padx=12,
        pady=10,
    ).pack(fill="x", padx=18, pady=(0, 18))

    # ------------------------------------------------------
    # ABA INS — PESQUISA, TIT E TMS
    # ------------------------------------------------------

    ins_results: Dict[str, dict] = {}
    ins_busy = {"value": False}
    ins_show_busy = set()
    ins_default_start, ins_default_end = ins_current_period()
    ins_start_date_var = tk.StringVar(value=ins_default_start)
    ins_end_date_var = tk.StringVar(value=ins_default_end)
    ins_status_var = tk.StringVar(
        value=(
            "Os relatórios serão gerados automaticamente ao abrir. "
            "Altere o período e use o botão para gerar novamente."
        )
    )
    ins_period_var = tk.StringVar(value="Período: aguardando coleta")

    ins_header = tk.Frame(ins_tab, bg=colors["bg"])
    ins_header.pack(fill="x", padx=12, pady=(12, 8))

    ins_header_left = tk.Frame(ins_header, bg=colors["bg"])
    ins_header_left.pack(side="left", fill="x", expand=True)
    tk.Label(
        ins_header_left,
        text="Indicadores INS",
        font=("Segoe UI", 14, "bold"),
        fg=colors["text"],
        bg=colors["bg"],
    ).pack(anchor="w")
    tk.Label(
        ins_header_left,
        textvariable=ins_status_var,
        font=("Segoe UI", 9),
        fg=colors["muted"],
        bg=colors["bg"],
        anchor="w",
    ).pack(anchor="w", pady=(2, 0))
    tk.Label(
        ins_header_left,
        textvariable=ins_period_var,
        font=("Segoe UI", 9, "bold"),
        fg=colors["blue"],
        bg=colors["bg"],
        anchor="w",
    ).pack(anchor="w", pady=(2, 0))

    ins_update_button = tk.Button(
        ins_header,
        text="Conectar e atualizar relatórios",
        command=lambda: request_ins_update(),
        font=("Segoe UI", 9, "bold"),
        bg=colors["green"],
        fg="#ffffff",
        activebackground="#15803d",
        activeforeground="#ffffff",
        relief="flat",
        padx=12,
        pady=8,
        cursor="hand2",
    )
    ins_update_button.pack(side="left", padx=(10, 0))

    ins_export_button = tk.Button(
        ins_header,
        text="Exportar CSVs",
        command=lambda: export_ins_csvs(),
        font=("Segoe UI", 9, "bold"),
        bg=colors["blue"],
        fg="#ffffff",
        activebackground="#1d4ed8",
        activeforeground="#ffffff",
        disabledforeground="#e5e7eb",
        relief="flat",
        padx=12,
        pady=8,
        cursor="hand2",
        state="disabled",
    )
    ins_export_button.pack(side="left", padx=(8, 0))

    ins_period_controls = tk.Frame(ins_tab, bg=colors["bg"])
    ins_period_controls.pack(fill="x", padx=12, pady=(0, 8))

    tk.Label(
        ins_period_controls,
        text="Data inicial:",
        font=("Segoe UI", 9, "bold"),
        fg=colors["text"],
        bg=colors["bg"],
    ).pack(side="left")
    ins_start_date_entry = tk.Entry(
        ins_period_controls,
        textvariable=ins_start_date_var,
        font=("Segoe UI", 10),
        width=12,
        justify="center",
        relief="solid",
        bd=1,
    )
    ins_start_date_entry.pack(side="left", padx=(6, 14), ipady=4)

    tk.Label(
        ins_period_controls,
        text="Data final:",
        font=("Segoe UI", 9, "bold"),
        fg=colors["text"],
        bg=colors["bg"],
    ).pack(side="left")
    ins_end_date_entry = tk.Entry(
        ins_period_controls,
        textvariable=ins_end_date_var,
        font=("Segoe UI", 10),
        width=12,
        justify="center",
        relief="solid",
        bd=1,
    )
    ins_end_date_entry.pack(side="left", padx=(6, 10), ipady=4)

    tk.Label(
        ins_period_controls,
        text="Formato: dd/mm/aaaa",
        font=("Segoe UI", 8),
        fg=colors["muted"],
        bg=colors["bg"],
    ).pack(side="left")

    ins_schemas = {
        "pesquisa": {
            "title": "PESQUISA",
            "kpis": (
                "Pesquisas Registradas",
                "Com Resposta",
                "Sem Resposta",
                "Pontos (meta ≥ 4)",
            ),
            "summary_title": "Quantitativo por avaliação",
            "summary_columns": (
                "evaluation",
                "quantity",
                "percentage",
            ),
            "summary_headers": (
                "Avaliação",
                "Quantidade de solicitações",
                "%",
            ),
            "summary_widths": (430, 250, 150),
            "detail_columns": (
                "ticket",
                "activity",
                "group",
                "closed_at",
                "survey_date",
                "rating",
            ),
            "detail_headers": (
                "Nº Ticket",
                "Atividade",
                "Grupo Executor",
                "Encerramento",
                "Data da Pesquisa",
                "Avaliação",
            ),
            "detail_widths": (100, 360, 230, 155, 135, 150),
        },
        "tit": {
            "title": "TIT",
            "kpis": (
                "Total de Chamados",
                "Dentro do Prazo",
                "Fora do Prazo",
                "% Atendimento",
            ),
            "summary_title": "Resumo por SLA TIT",
            "summary_columns": (
                "sla",
                "total",
                "outside",
                "outside_percentage",
                "inside",
                "inside_percentage",
            ),
            "summary_headers": (
                "SLA TIT",
                "Total",
                "Fora",
                "% Não Atend.",
                "Dentro",
                "% Atend.",
            ),
            "summary_widths": (190, 110, 110, 145, 110, 130),
            "detail_columns": (
                "ticket",
                "activity",
                "forwarded_at",
                "first_capture_at",
                "responsible",
                "group",
                "goal",
                "capture_time",
                "within_deadline",
                "closed_at",
            ),
            "detail_headers": (
                "Nº Ticket",
                "Atividade",
                "Encaminhamento",
                "1ª Captura",
                "Responsável pela 1ª Captura",
                "Grupo Executor",
                "Meta TIT",
                "Tempo de Captura",
                "No Prazo",
                "Encerramento",
            ),
            "detail_widths": (
                100,
                330,
                155,
                155,
                240,
                230,
                100,
                135,
                90,
                155,
            ),
        },
        "tms": {
            "title": "TMS",
            "kpis": (
                "Total de Chamados",
                "Dentro do Prazo",
                "Fora do Prazo",
                "% Atendimento",
            ),
            "summary_title": "Resumo por SLA TMS — metas",
            "summary_columns": (
                "sla",
                "total",
                "inside",
                "inside_percentage",
                "target",
                "target_result",
                "outside",
                "outside_percentage",
            ),
            "summary_headers": (
                "SLA TMS",
                "Total",
                "Dentro",
                "% Atend.",
                "Meta",
                "Resultado",
                "Fora",
                "% Não Atend.",
            ),
            "summary_widths": (
                145,
                90,
                90,
                110,
                90,
                145,
                90,
                125,
            ),
            "detail_columns": (
                "ticket",
                "activity",
                "sla",
                "started_at",
                "finished_at",
                "service_time",
                "suspension_time",
                "within_deadline",
                "group",
                "technician",
            ),
            "detail_headers": (
                "Nº Ticket",
                "Atividade",
                "SLA",
                "Início do Atendimento",
                "Fim do Atendimento",
                "Tempo de Atendimento",
                "Tempo de Suspensão",
                "No Prazo",
                "Grupo Executor",
                "Técnico Responsável",
            ),
            "detail_widths": (
                100,
                330,
                100,
                155,
                155,
                145,
                145,
                90,
                230,
                240,
            ),
        },
    }

    def make_ins_tree(
        parent,
        columns: Tuple[str, ...],
        headers: Tuple[str, ...],
        widths: Tuple[int, ...],
        *,
        height: int = 5,
    ):
        frame = tk.Frame(parent, bg=colors["card"])
        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=height,
        )
        vertical = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=tree.yview,
        )
        horizontal = ttk.Scrollbar(
            frame,
            orient="horizontal",
            command=tree.xview,
        )
        tree.configure(
            yscrollcommand=vertical.set,
            xscrollcommand=horizontal.set,
        )
        tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        for column, header_text, width in zip(
            columns,
            headers,
            widths,
        ):
            tree.heading(column, text=header_text)
            tree.column(
                column,
                width=width,
                minwidth=75,
                anchor=(
                    "center"
                    if column
                    not in {
                        "activity",
                        "group",
                        "responsible",
                        "technician",
                        "evaluation",
                    }
                    else "w"
                ),
                stretch=column in {
                    "activity",
                    "group",
                    "responsible",
                    "technician",
                    "evaluation",
                },
            )
        return frame, tree

    ins_subnotebook = ttk.Notebook(ins_tab)
    ins_subnotebook.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=(0, 12),
    )
    ins_views: Dict[str, dict] = {}
    kpi_accents = (
        colors["blue"],
        colors["green"],
        colors["red"],
        colors["orange"],
    )

    for report_key in INS_REPORT_ORDER:
        schema = ins_schemas[report_key]
        page = tk.Frame(ins_subnotebook, bg=colors["card"])
        ins_subnotebook.add(page, text=schema["title"])

        report_line = tk.Frame(page, bg=colors["card"])
        report_line.pack(fill="x", padx=10, pady=(8, 4))
        report_status_var = tk.StringVar(
            value="Aguardando geração."
        )
        report_status_label = tk.Label(
            report_line,
            textvariable=report_status_var,
            font=("Segoe UI", 9, "bold"),
            fg=colors["muted"],
            bg=colors["card"],
        )
        report_status_label.pack(side="left")
        show_report_button = tk.Button(
            report_line,
            text="Mostrar no navegador",
            command=(
                lambda key=report_key: request_ins_show(key)
            ),
            font=("Segoe UI", 8, "bold"),
            bg=colors["blue"],
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            disabledforeground="#e5e7eb",
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            state="disabled",
        )
        show_report_button.pack(side="right")
        filter_var = tk.StringVar(
            value="Filtros ainda não carregados."
        )
        tk.Label(
            report_line,
            textvariable=filter_var,
            font=("Segoe UI", 8),
            fg=colors["muted"],
            bg=colors["card"],
            anchor="w",
        ).pack(side="left", padx=(14, 0), fill="x", expand=True)

        kpi_frame = tk.Frame(page, bg=colors["card"])
        kpi_frame.pack(fill="x", padx=8, pady=(0, 6))
        kpi_vars = {}
        for index, label in enumerate(schema["kpis"]):
            kpi_frame.grid_columnconfigure(index, weight=1)
            variable = tk.StringVar(value="—")
            kpi_vars[label] = variable
            card = tk.Frame(
                kpi_frame,
                bg="#f8fafc",
                highlightbackground="#d0d5dd",
                highlightthickness=1,
            )
            card.grid(
                row=0,
                column=index,
                sticky="ew",
                padx=4,
            )
            tk.Label(
                card,
                textvariable=variable,
                font=("Segoe UI", 15, "bold"),
                fg=kpi_accents[index],
                bg="#f8fafc",
            ).pack(pady=(5, 0))
            tk.Label(
                card,
                text=label,
                font=("Segoe UI", 8),
                fg=colors["muted"],
                bg="#f8fafc",
            ).pack(pady=(0, 5))

        tk.Label(
            page,
            text=schema["summary_title"],
            font=("Segoe UI", 9, "bold"),
            fg=colors["text"],
            bg=colors["card"],
        ).pack(anchor="w", padx=10, pady=(0, 3))
        summary_frame, summary_tree = make_ins_tree(
            page,
            schema["summary_columns"],
            schema["summary_headers"],
            schema["summary_widths"],
            height=5,
        )
        summary_frame.pack(fill="x", padx=8, pady=(0, 5))
        summary_tree.tag_configure(
            "total",
            background="#e5e7eb",
            foreground=colors["text"],
        )
        summary_tree.tag_configure(
            "target_met",
            background="#ecfdf3",
            foreground="#166534",
        )
        summary_tree.tag_configure(
            "target_missed",
            background="#fee2e2",
            foreground=colors["dark_red"],
        )

        tk.Label(
            page,
            text="Detalhamento",
            font=("Segoe UI", 9, "bold"),
            fg=colors["text"],
            bg=colors["card"],
        ).pack(anchor="w", padx=10, pady=(0, 3))
        detail_frame, detail_tree = make_ins_tree(
            page,
            schema["detail_columns"],
            schema["detail_headers"],
            schema["detail_widths"],
        )
        detail_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0, 8),
        )

        ins_views[report_key] = {
            "kpi_vars": kpi_vars,
            "filter_var": filter_var,
            "status_var": report_status_var,
            "status_label": report_status_label,
            "show_button": show_report_button,
            "summary_tree": summary_tree,
            "detail_tree": detail_tree,
        }

    def request_ins_update() -> None:
        if (
            ins_busy["value"]
            or ins_show_busy
            or stop_event.is_set()
        ):
            return

        try:
            start_text, end_text = ins_validate_period(
                ins_start_date_var.get(),
                ins_end_date_var.get(),
            )
        except ValueError as exc:
            ins_status_var.set(str(exc))
            ins_period_var.set("Período: verifique as datas informadas")
            ins_start_date_entry.focus_set()
            return

        ins_start_date_var.set(start_text)
        ins_end_date_var.set(end_text)
        ins_results.clear()
        ins_busy["value"] = True
        ins_update_button.configure(state="disabled")
        ins_export_button.configure(state="disabled")
        ins_start_date_entry.configure(state="disabled")
        ins_end_date_entry.configure(state="disabled")
        ins_status_var.set(
            "Conectando ao Smart Reports em segundo plano..."
        )
        ins_period_var.set(
            f"Período solicitado: {start_text} a {end_text}"
        )
        for report_key in INS_REPORT_ORDER:
            view = ins_views[report_key]
            view["status_var"].set("Aguardando geração...")
            view["status_label"].configure(fg=colors["muted"])
            view["show_button"].configure(state="disabled")
        ins_command_queue.put(
            {
                "action": "generate",
                "start_date": start_text,
                "end_date": end_text,
            }
        )

    def request_ins_show(report_key: str) -> None:
        if (
            ins_busy["value"]
            or report_key in ins_show_busy
            or stop_event.is_set()
        ):
            return

        result = ins_results.get(report_key)
        if not result:
            ins_status_var.set(
                "Gere o relatório antes de mostrá-lo no navegador."
            )
            return

        view = ins_views[report_key]
        label = ins_schemas[report_key]["title"]
        ins_show_busy.add(report_key)
        view["show_button"].configure(state="disabled")
        view["status_var"].set(
            f"Abrindo {label} no navegador..."
        )
        view["status_label"].configure(fg=colors["blue"])
        ins_command_queue.put(
            {
                "action": "show_report",
                "report_key": report_key,
                "start_date": result.get("start_date", ""),
                "end_date": result.get("end_date", ""),
            }
        )

    def refresh_ins_report(
        report_key: str,
        event: dict,
    ) -> None:
        schema = ins_schemas[report_key]
        view = ins_views[report_key]
        summary_rows = event.get("summary", [])
        if report_key == "tms":
            summary_rows = ins_enrich_tms_summary(summary_rows)
        result = {
            "start_date": event.get("start_date", ""),
            "end_date": event.get("end_date", ""),
            "kpis": event.get("kpis", {}),
            "filters": event.get("filters", {}),
            "summary": summary_rows,
            "details": event.get("details", []),
        }
        ins_results[report_key] = result

        for label, variable in view["kpi_vars"].items():
            variable.set(result["kpis"].get(label, "N/D"))

        view["filter_var"].set(
            " | ".join(
                f"{label}: {value}"
                for label, value in result["filters"].items()
            )
            or "Filtros não identificados."
        )

        summary_tree = view["summary_tree"]
        summary_tree.delete(*summary_tree.get_children())
        for row in result["summary"]:
            first_value = row[0].strip() if row else ""
            if first_value.casefold() in {"total", "totais"}:
                tags = ("total",)
            elif (
                report_key == "tms"
                and len(row) > 5
                and row[5] in {
                    "Meta atingida",
                    "Abaixo da meta",
                }
            ):
                tags = (
                    ("target_met",)
                    if row[5] == "Meta atingida"
                    else ("target_missed",)
                )
            else:
                tags = ()
            summary_tree.insert(
                "",
                "end",
                values=tuple(
                    row[:len(schema["summary_columns"])]
                ),
                tags=tags,
            )

        detail_tree = view["detail_tree"]
        detail_tree.delete(*detail_tree.get_children())
        for row in result["details"]:
            detail_tree.insert(
                "",
                "end",
                values=tuple(
                    row[:len(schema["detail_columns"])]
                ),
            )

        view["status_var"].set(
            f"Concluído: {len(result['details'])} registro(s)."
        )
        view["status_label"].configure(fg=colors["green"])
        view["show_button"].configure(state="normal")

    def export_ins_csvs() -> None:
        if not ins_results:
            message = (
                "Nenhum relatório concluído está disponível. "
                "Gere os indicadores antes de exportar."
            )
            ins_status_var.set(message)
            messagebox.showwarning(
                "Exportar CSVs",
                message,
                parent=root,
            )
            return

        try:
            root.attributes("-topmost", False)
            root.lift()
            root.update_idletasks()
            destination = filedialog.askdirectory(
                parent=root,
                title="Escolher pasta para salvar os CSVs do INS",
                mustexist=True,
            )
        except tk.TclError as exc:
            log.exception(
                "Falha ao abrir a seleção da pasta dos CSVs."
            )
            message = f"Não foi possível escolher a pasta: {exc}"
            ins_status_var.set(message)
            messagebox.showerror(
                "Exportar CSVs",
                message,
                parent=root,
            )
            return

        if not destination:
            ins_status_var.set("Exportação dos CSVs cancelada.")
            return

        ins_export_button.configure(state="disabled")
        ins_status_var.set("Gerando os arquivos CSV...")
        root.configure(cursor="watch")
        root.update_idletasks()

        try:
            exported_paths, failures = export_ins_results_to_csv(
                destination,
                dict(ins_results),
                ins_schemas,
            )
        except Exception as exc:
            log.exception("Falha geral na exportação dos CSVs.")
            exported_paths = []
            failures = [str(exc)]
        finally:
            root.configure(cursor="")
            ins_export_button.configure(
                state=("normal" if ins_results else "disabled")
            )

        if exported_paths and not failures:
            filenames = "\n".join(
                f"• {path.name}" for path in exported_paths
            )
            message = (
                f"{len(exported_paths)} arquivo(s) exportado(s) "
                f"com sucesso para:\n{destination}\n\n{filenames}"
            )
            ins_status_var.set(
                f"{len(exported_paths)} CSV(s) exportado(s) "
                f"com sucesso."
            )
            messagebox.showinfo(
                "Exportação concluída",
                message,
                parent=root,
            )
            return

        if exported_paths:
            message = (
                f"{len(exported_paths)} arquivo(s) foram salvos, "
                "mas ocorreram falhas:\n\n"
                + "\n".join(failures)
            )
            ins_status_var.set(
                "Exportação concluída parcialmente."
            )
            messagebox.showwarning(
                "Exportação parcial",
                message,
                parent=root,
            )
            return

        message = (
            "Nenhum CSV foi criado.\n\n"
            + (
                "\n".join(failures)
                if failures
                else "Não havia relatórios disponíveis."
            )
        )
        ins_status_var.set("Falha ao exportar os CSVs.")
        messagebox.showerror(
            "Falha na exportação",
            message,
            parent=root,
        )

    # ------------------------------------------------------
    # ABA DE AVISOS TEMPORÁRIOS DA EXECUÇÃO ATUAL
    # ------------------------------------------------------

    alert_history_header = tk.Frame(alerts_tab, bg=colors["card"])
    alert_history_header.pack(fill="x", padx=14, pady=(14, 8))

    tk.Label(
        alert_history_header,
        text="Avisos da execução atual",
        font=("Segoe UI", 10, "bold"),
        fg=colors["text"],
        bg=colors["card"],
    ).pack(side="left")

    alert_history_count_var = tk.StringVar(
        value=(
            "Nenhum aviso nesta execução. O conteúdo não é salvo ao "
            "fechar o programa."
        )
    )
    tk.Label(
        alert_history_header,
        textvariable=alert_history_count_var,
        font=("Segoe UI", 9),
        fg=colors["muted"],
        bg=colors["card"],
    ).pack(side="left", padx=(14, 0))

    alert_history_tree = make_tree(
        alerts_tab,
        ("date", "ticket", "level", "title", "message"),
        {
            "date": "Data e hora",
            "ticket": "Chamado",
            "level": "Nível",
            "title": "Aviso",
            "message": "Detalhes",
        },
        {
            "date": 155,
            "ticket": 100,
            "level": 95,
            "title": 290,
            "message": 650,
        },
        {"date": "center", "ticket": "center", "level": "center"},
    )
    alert_level_labels = {
        "info": "Informativo",
        "warning": "Atenção",
        "critical": "Crítico",
    }

    def request_queue_browser() -> None:
        if stop_event.is_set():
            return
        queue_browser_button.configure(state="disabled")
        queue_browser_status_var.set(
            "Solicitando abertura da fila..."
        )
        queue_command_queue.put({"action": "show_queue"})

    def request_d1_ticket() -> None:
        if stop_event.is_set():
            return

        reference = d1_reference_date()
        d1_reference_var.set(
            "Referência automática: "
            + reference.strftime("%d/%m/%Y")
        )
        d1_description_var.set(d1_description(reference))
        d1_status_var.set(
            "Solicitando a abertura e o preenchimento do chamado..."
        )
        d1_status_label.configure(fg=colors["blue"])
        d1_prepare_button.configure(state="disabled")
        d1_command_queue.put({"action": "prepare_d1"})

    def copy_ticket_id(event) -> None:
        tree = event.widget
        item_id = tree.identify_row(event.y)
        if not item_id:
            return
        values = tree.item(item_id, "values")
        if not values:
            return
        ticket_id = values[0] if tree is queue_tree else values[1]
        root.clipboard_clear()
        root.clipboard_append(ticket_id)
        status_var.set(f"Chamado {ticket_id} copiado")

    queue_tree.bind("<Double-1>", copy_ticket_id)
    exits_tree.bind("<Double-1>", copy_ticket_id)

    def queue_severity(active: ActiveTicket) -> Tuple[int, int, str]:
        ticket = active.ticket
        remaining = ticket.remaining_seconds
        problem = queue_problem_text(active)

        if ticket.sla_state == "overdue":
            return 0, remaining or 0, ticket.ticket_id
        if ticket.sla_state == "due_soon":
            return 1, remaining or 0, ticket.ticket_id
        if "Susp +2sem" in problem:
            return 2, 0, ticket.ticket_id
        if ticket.owner_empty:
            return 3, 0, ticket.ticket_id
        if ticket.suspended:
            return 4, 0, ticket.ticket_id
        return 5, 0, ticket.ticket_id

    def refresh_queue_tree(active_items: List[ActiveTicket]) -> None:
        queue_tree.delete(*queue_tree.get_children())

        now = datetime.now()

        for active in sorted(active_items, key=queue_severity):
            ticket = active.ticket
            problem = queue_problem_text(active, now)

            if ticket.sla_state == "overdue":
                tag = "overdue"
            elif ticket.sla_state == "due_soon":
                tag = "due_soon"
            elif "Susp +2sem" in problem:
                tag = "suspended_long"
            elif ticket.owner_empty:
                tag = "unassigned"
            elif ticket.suspended:
                tag = "suspended"
            else:
                tag = "normal"

            queue_tree.insert(
                "",
                "end",
                values=(
                    ticket.ticket_id,
                    problem,
                    ticket.displayed_sla_text,
                    ticket.creation_date or "N/D",
                    ticket.limit_date or "N/D",
                    ticket.request_name or "N/D",
                    ticket.grupo or "N/D",
                    ticket.owner_text or "Sem responsável",
                    ticket.task_status or "N/D",
                    active.first_seen.strftime("%d/%m/%Y %H:%M:%S"),
                ),
                tags=(tag,),
            )

        stat_vars["queue"].set(str(len(active_items)))
        stat_vars["unassigned"].set(
            str(sum(item.ticket.owner_empty for item in active_items))
        )
        stat_vars["due"].set(
            str(sum(item.ticket.sla_state == "due_soon" for item in active_items))
        )
        stat_vars["overdue"].set(
            str(sum(item.ticket.sla_state == "overdue" for item in active_items))
        )

    def refresh_exits_tree(events: List[ExitEvent]) -> None:
        exits_tree.delete(*exits_tree.get_children())

        for event in reversed(events):
            try:
                event_time = datetime.fromisoformat(event.exited_at).strftime("%H:%M:%S")
            except ValueError:
                event_time = event.exited_at

            exits_tree.insert(
                "",
                "end",
                values=(
                    event_time,
                    event.ticket_id,
                    event.reason,
                    event.request_name,
                    event.grupo,
                    event.owner_text,
                    event.task_status,
                    event.creation_date,
                    event.limit_date,
                    event.sla_status,
                    event.sla_text,
                    event.time_in_queue,
                ),
                tags=(event.reason,),
            )

        stat_vars["exits"].set(str(len(events)))

    def refresh_indicators(
        indicators: dict,
        session_started_at: Optional[datetime],
        database_ready: bool,
    ) -> None:
        indicator_vars["baseline"].set(str(indicators.get("baseline", 0)))
        indicator_vars["entries"].set(str(indicators.get("entries", 0)))
        indicator_vars["reentries"].set(str(indicators.get("reentries", 0)))
        indicator_vars["captures"].set(str(indicators.get("captures", 0)))
        indicator_vars["resolutions"].set(
            str(indicators.get("resolutions", 0))
        )
        indicator_vars["arrived_overdue"].set(
            str(indicators.get("arrived_overdue", 0))
        )
        indicator_vars["suspended"].set(
            str(indicators.get("current_suspended", 0))
        )

        average = indicators.get("average_capture_seconds")
        maximum = indicators.get("max_capture_seconds")
        indicator_vars["average_capture"].set(
            format_duration(int(average))
            if average is not None
            else "N/D"
        )
        indicator_vars["max_capture"].set(
            format_duration(int(maximum))
            if maximum is not None
            else "N/D"
        )

        owner_tree.delete(*owner_tree.get_children())
        for rank, owner in enumerate(indicators.get("by_owner", []), start=1):
            owner_tree.insert(
                "",
                "end",
                values=(
                    rank,
                    owner.get("owner", "N/D"),
                    owner.get("captures", 0),
                    owner.get("resolutions", 0),
                    owner.get("total", 0),
                ),
            )

        if not owner_tree.get_children():
            owner_tree.insert(
                "",
                "end",
                values=(
                    "-",
                    "Nenhuma captura ou resolução observada",
                    "0",
                    "0",
                    "0",
                ),
            )

        if isinstance(session_started_at, datetime):
            started_text = session_started_at.strftime("%d/%m/%Y %H:%M:%S")
            database_text = (
                "histórico local ativo"
                if database_ready
                else "histórico local indisponível"
            )
            indicator_note_var.set(
                f"Sessão iniciada em {started_text} — {database_text}."
            )

    alert_history_tree.tag_configure("info", background="#eff6ff")
    alert_history_tree.tag_configure("warning", background="#fff7ed")
    alert_history_tree.tag_configure(
        "critical",
        background="#fee2e2",
        foreground=colors["dark_red"],
    )

    def export_month_from_ui() -> None:
        default_name = (
            "eventos_citsmart_"
            + datetime.now().strftime("%Y-%m")
            + ".csv"
        )
        destination = filedialog.asksaveasfilename(
            parent=root,
            title="Exportar eventos do mês atual",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=(("Arquivo CSV", "*.csv"),),
        )
        if not destination:
            return

        try:
            initialize_database()
            total = export_current_month_csv(destination)
            export_status_var.set(
                f"{total} evento(s) exportado(s) para:\n{destination}"
            )
        except (OSError, sqlite3.Error) as exc:
            export_status_var.set(f"Falha na exportação: {exc}")

    alert_after_id = {"value": None}
    alert_blink_remaining = {"value": 0}
    alert_base_color = {"value": "#fff7e6"}

    def hide_alert() -> None:
        alert_after_id["value"] = None
        alert_blink_remaining["value"] = 0
        alert_frame.pack_forget()

    def blink_alert() -> None:
        if alert_blink_remaining["value"] <= 0:
            alert_frame.configure(bg=alert_base_color["value"])
            alert_label.configure(bg=alert_base_color["value"])
            return

        current = alert_frame.cget("bg")
        base = alert_base_color["value"]
        alternate = "#ffffff"
        next_color = alternate if current == base else base
        alert_frame.configure(bg=next_color)
        alert_label.configure(bg=next_color)
        alert_blink_remaining["value"] -= 1
        root.after(280, blink_alert)

    def show_alert(title: str, message: str, level: str) -> None:
        palettes = {
            "info": ("#dbeafe", "#1e3a8a"),
            "warning": ("#fff7e6", "#7a3e00"),
            "critical": ("#fee2e2", colors["dark_red"]),
        }
        background, foreground = palettes.get(level, palettes["warning"])
        alert_base_color["value"] = background

        alert_var.set(f"{title}\n{message}")
        alert_frame.configure(bg=background)
        alert_label.configure(bg=background, fg=foreground)

        if not alert_frame.winfo_ismapped():
            alert_frame.pack(
                fill="x",
                padx=28,
                pady=(0, 12),
                before=stats_frame,
            )

        if alert_after_id["value"] is not None:
            root.after_cancel(alert_after_id["value"])
        alert_after_id["value"] = root.after(15000, hide_alert)

        alert_blink_remaining["value"] = 6
        blink_alert()

        if BRING_TO_FRONT_ON_ALERT:
            try:
                root.deiconify()
                root.lift()
                root.attributes("-topmost", True)
                root.after(1200, lambda: root.attributes("-topmost", False))
            except tk.TclError:
                pass

    def append_current_alert(event: dict) -> None:
        level = event.get("level", "warning")
        alert_at = event.get("alert_at")
        if isinstance(alert_at, datetime):
            alert_at_text = alert_at.strftime("%d/%m/%Y %H:%M:%S")
        else:
            alert_at_text = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        alert_history_tree.insert(
            "",
            0,
            values=(
                alert_at_text,
                event.get("ticket_id") or "Geral",
                alert_level_labels.get(level, level),
                event.get("title", "Alerta"),
                " ".join((event.get("message") or "").split()),
            ),
            tags=(level,),
        )
        total = len(alert_history_tree.get_children())
        alert_history_count_var.set(
            f"{total} aviso(s) desde a abertura do programa. "
            "Este conteúdo é temporário."
        )

    def process_ui_events() -> None:
        while True:
            try:
                event = ui_queue.get_nowait()
            except Empty:
                break

            event_type = event.get("type")

            if event_type == "status":
                status_var.set(event.get("text", ""))
                monitor_state["value"] = event.get("state", "active")
            elif event_type == "alert":
                append_current_alert(event)
                show_alert(
                    event.get("title", "Alerta"),
                    event.get("message", ""),
                    event.get("level", "warning"),
                )
            elif event_type == "snapshot":
                active_items = event.get("active", [])
                exits = event.get("exits", [])
                refresh_queue_tree(active_items)
                refresh_exits_tree(exits)
                refresh_indicators(
                    event.get("indicators", {}),
                    event.get("session_started_at"),
                    event.get("database_ready", False),
                )

                updated_at = event.get("updated_at")
                if isinstance(updated_at, datetime):
                    updated_var.set(
                        "Última leitura: "
                        + updated_at.strftime("%d/%m/%Y %H:%M:%S")
                    )
            elif event_type == "queue_browser_status":
                queue_browser_status_var.set(
                    event.get("text", "")
                )
                if event.get("finished"):
                    queue_browser_button.configure(state="normal")
            elif event_type == "d1_status":
                d1_status_var.set(event.get("text", ""))
                d1_state = event.get("state", "working")
                d1_status_label.configure(
                    fg={
                        "success": colors["green"],
                        "error": colors["red"],
                        "working": colors["blue"],
                    }.get(d1_state, colors["muted"])
                )
                reference = event.get("reference")
                if reference:
                    d1_reference_var.set(
                        f"Referência preparada: {reference}"
                    )
            elif event_type == "d1_ready":
                d1_prepare_button.configure(state="normal")
            elif event_type == "d1_stopped":
                if stop_event.is_set():
                    d1_status_var.set("Preparador de chamado encerrado.")
            elif event_type == "ins_status":
                ins_status_var.set(event.get("text", ""))
            elif event_type == "ins_report_result":
                refresh_ins_report(
                    event.get("report_key", ""),
                    event,
                )
            elif event_type == "ins_report_error":
                report_key = event.get("report_key", "")
                if report_key in ins_views:
                    view = ins_views[report_key]
                    view["status_var"].set(
                        "Falha: " + event.get("message", "erro")
                    )
                    view["status_label"].configure(
                        fg=colors["red"]
                    )
                    view["show_button"].configure(
                        state="disabled"
                    )
                    ins_results.pop(report_key, None)
            elif event_type == "ins_show_status":
                report_key = event.get("report_key", "")
                if report_key in ins_views:
                    view = ins_views[report_key]
                    view["status_var"].set(
                        event.get("message", "Abrindo no navegador...")
                    )
                    view["status_label"].configure(
                        fg=colors["blue"]
                    )
            elif event_type == "ins_report_shown":
                report_key = event.get("report_key", "")
                if report_key in ins_views:
                    view = ins_views[report_key]
                    view["status_var"].set(
                        event.get("message", "Aberto no navegador.")
                    )
                    view["status_label"].configure(
                        fg=colors["green"]
                    )
            elif event_type == "ins_show_error":
                report_key = event.get("report_key", "")
                if report_key in ins_views:
                    view = ins_views[report_key]
                    view["status_var"].set(
                        "Falha ao abrir: "
                        + event.get("message", "erro")
                    )
                    view["status_label"].configure(
                        fg=colors["red"]
                    )
            elif event_type == "ins_show_ready":
                report_key = event.get("report_key", "")
                ins_show_busy.discard(report_key)
                if report_key in ins_views:
                    ins_views[report_key][
                        "show_button"
                    ].configure(
                        state=(
                            "normal"
                            if report_key in ins_results
                            else "disabled"
                        )
                    )
            elif event_type == "ins_complete":
                completed = event.get("completed", 0)
                failed = event.get("failed", 0)
                start_date = event.get("start_date", "")
                end_date = event.get("end_date", "")
                ins_period_var.set(
                    f"Período: {start_date} a {end_date}"
                )
                ins_status_var.set(
                    f"INS concluído: {completed} relatório(s); "
                    f"{failed} falha(s)."
                )
            elif event_type == "ins_ready":
                ins_busy["value"] = False
                ins_update_button.configure(state="normal")
                ins_start_date_entry.configure(state="normal")
                ins_end_date_entry.configure(state="normal")
                for report_key, view in ins_views.items():
                    view["show_button"].configure(
                        state=(
                            "normal"
                            if report_key in ins_results
                            else "disabled"
                        )
                    )
                ins_export_button.configure(
                    state=(
                        "normal"
                        if ins_results
                        else "disabled"
                    )
                )
            elif event_type == "ins_stopped":
                if stop_event.is_set():
                    ins_status_var.set("Coletor INS encerrado.")

        if root.winfo_exists():
            root.after(250, process_ui_events)

    def update_uptime() -> None:
        elapsed = int((datetime.now() - started_at).total_seconds())
        uptime_var.set(f"Tempo ativo: {format_duration(elapsed)}")
        if root.winfo_exists():
            root.after(1000, update_uptime)

    def blink_status_icon() -> None:
        monitor_state["blink"] = not monitor_state["blink"]
        state = monitor_state["value"]

        if state == "active":
            color = colors["green"] if monitor_state["blink"] else "#86efac"
        elif state in {"error", "stopped"}:
            color = colors["red"]
        elif state == "stopping":
            color = colors["dark_red"]
        else:
            color = colors["orange"] if monitor_state["blink"] else "#fed7aa"

        status_icon.configure(fg=color)
        if root.winfo_exists():
            root.after(650, blink_status_icon)

    monitor_thread = threading.Thread(
        target=monitor_main,
        args=(stop_event,),
        daemon=True,
        name="citsmart-monitor",
    )
    monitor_thread.start()

    d1_thread = threading.Thread(
        target=d1_worker,
        args=(stop_event,),
        daemon=True,
        name="citsmart-d1",
    )
    d1_thread.start()

    ins_thread = threading.Thread(
        target=ins_worker,
        args=(stop_event,),
        daemon=True,
        name="citsmart-ins",
    )
    ins_thread.start()
    root.after(900, request_ins_update)

    def check_monitor_thread() -> None:
        if not monitor_thread.is_alive():
            if stop_event.is_set():
                root.after(500, root.destroy)
                return

            if not monitor_finished_reported["value"]:
                monitor_finished_reported["value"] = True
                monitor_state["value"] = "error"
                status_var.set("Monitor interrompido")
                stop_button.configure(state="disabled", text="Monitor encerrado")

        if root.winfo_exists():
            root.after(1000, check_monitor_thread)

    def on_close() -> None:
        shutdown_monitor()

    root.protocol("WM_DELETE_WINDOW", on_close)

    process_ui_events()
    update_uptime()
    blink_status_icon()
    check_monitor_thread()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        shutdown_monitor()


if __name__ == "__main__":
    start_control_window()

