# Information Technology

Fonte única de consulta para **planejar, estruturar, implementar, operar e melhorar ambientes de Tecnologia da Informação**.

> Use este repositório como ponto de partida para encontrar políticas, processos, procedimentos, checklists, modelos, indicadores e orientações de implementação.

---

## Índice

| Área | Conteúdo |
|---|---|
| [00 — Planejamento e Implementação](./00-planejamento-e-implementacao/) | Diagnóstico, maturidade, priorização, roadmap e modelos de implementação |
| [01 — Governança e Gestão](./01-governanca-e-gestao/) | Governança de TI, governança de IA, planejamento, riscos e controles |
| [02 — Gestão de Serviços](./02-gestao-de-servicos/) | Incidentes, mudanças, problemas, requisições, SLA, conhecimento e melhoria |
| [03 — Arquitetura e Aplicações](./03-arquitetura-e-aplicacoes/) | Aplicações, arquitetura, automação e integrações |
| [04 — Infraestrutura](./04-infraestrutura/) | Datacenter, redes, servidores, storage, backup e virtualização |
| [05 — Dados](./05-dados/) | Bancos de dados, governança, modelagem, proteção e SQL |
| [06 — Ativos e Configuração](./06-ativos-e-configuracao/) | Ativos, CMDB, configuração, inventário e NetBox |
| [07 — Monitoramento e Observabilidade](./07-monitoramento-e-observabilidade/) | Alertas, disponibilidade, logs, métricas, SRE e Zabbix |
| [08 — Segurança e Continuidade](./08-seguranca-e-continuidade/) | Acessos, continuidade, incidentes de segurança, riscos e vulnerabilidades |

---

# 00 — Planejamento e Implementação

Antes de implementar uma área ou capacidade:

- Avaliação de contexto
- Diagnóstico
- Levantamento do ambiente
- Maturidade
- Modelo-alvo
- Modelos de implementação
- Papéis e responsabilidades
- Priorização
- Roadmap

### Modelos de implementação

As implementações podem ser adaptadas ao contexto:

| Modelo | Aplicação |
|---|---|
| **Essencial** | Estrutura mínima, simples e funcional |
| **Intermediário** | Maior formalização, controles e responsabilidades |
| **Avançado** | Ambientes complexos, críticos, regulados ou de maior escala |

A escolha deve considerar:

`Complexidade` · `Criticidade` · `Maturidade` · `Porte` · `Regulação` · `Recursos` · `Riscos` · `Volume`

---

# 01 — Governança e Gestão

- Conformidade
- Governança de IA
- Governança de TI
- Indicadores e desempenho
- Planejamento de TI
- Políticas e diretrizes
- Riscos e controles

---

# 02 — Gestão de Serviços

- Catálogo de serviços
- Gestão de incidentes
- Gestão de mudanças
- Gestão de nível de serviço
- Gestão de problemas
- Gestão de requisições
- Gestão do conhecimento
- Melhoria contínua
- Satisfação e experiência do usuário

### Exemplo — Gestão de Mudanças

Pode incluir:

- Aprovações
- Avaliação de impacto
- Avaliação de risco
- Autoridades de mudança
- Controles
- Indicadores
- Política
- Processo
- Tipos de mudança

Modelos diferentes podem ser utilizados conforme o ambiente.

**Essencial**

```text
Solicitação
    ↓
Avaliação
    ↓
Aprovação da chefia
    ↓
Implementação
    ↓
Validação
```

**Intermediário**

```text
Aprovação conforme risco e impacto
```

**Avançado**

```text
Autoridades específicas
CAB quando necessário
Fluxo emergencial
Segregação de responsabilidades
```

---

# 03 — Arquitetura e Aplicações

- Ambientes
- Aplicações
- Arquitetura de sistemas
- Automação
- Ciclo de vida
- Configuração
- Integrações

### Integrações

- APIs
- Autenticação
- JSON
- Mensageria
- Middleware
- Webhooks

### Automação

- PowerShell
- Python
- Scripts
- Workflows

---

# 04 — Infraestrutura

- Alta disponibilidade
- Armazenamento
- Backup e recuperação
- Datacenter
- Redes
- Servidores
- Virtualização

### Redes

- DHCP
- DNS
- Endereçamento
- Routing
- Switching
- VLAN
- Wireless

### Servidores

- Hardware
- Linux
- Windows Server

---

# 05 — Dados

- Administração
- Bancos de dados
- Governança de dados
- Modelagem
- Proteção e recuperação
- Qualidade de dados
- SQL

---

# 06 — Ativos e Configuração

- CMDB
- Gestão de ativos
- Gestão de configuração
- Inventário
- NetBox

---

# 07 — Monitoramento e Observabilidade

- Dashboards
- Disponibilidade
- Eventos e alertas
- Logs
- Métricas
- Monitoramento
- Observabilidade
- SRE
- Zabbix

### Métricas

- MTBF — Mean Time Between Failures
- MTTA — Mean Time to Acknowledge
- MTTD — Mean Time to Detect
- MTTF — Mean Time to Failure
- MTTR — Mean Time to Restore

---

# 08 — Segurança e Continuidade

- Continuidade
- Identidade e acesso
- Resposta a incidentes
- Riscos de segurança
- Segurança de infraestrutura
- Vulnerabilidades

---

# Estrutura

```text
Information-Technology/
├── 00-planejamento-e-implementacao/
├── 01-governanca-e-gestao/
├── 02-gestao-de-servicos/
├── 03-arquitetura-e-aplicacoes/
├── 04-infraestrutura/
├── 05-dados/
├── 06-ativos-e-configuracao/
├── 07-monitoramento-e-observabilidade/
└── 08-seguranca-e-continuidade/
```


O `Information-Technology` é voltado principalmente para **aplicação prática e implementação**.
