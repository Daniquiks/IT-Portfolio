# 06 — Automação e Integrações

Este diretório reúne práticas, padrões, scripts, modelos e referências voltados à **automação de atividades operacionais e à integração entre sistemas, plataformas e ferramentas de TI**.

A proposta é reduzir tarefas manuais, eliminar retrabalho, aumentar consistência, melhorar rastreabilidade e permitir que diferentes componentes da operação troquem informações de forma controlada e confiável.

---

## Objetivo

Apoiar a evolução da operação por meio de automações e integrações capazes de:

- reduzir atividades repetitivas;
- diminuir erros manuais;
- acelerar fluxos operacionais;
- integrar ferramentas;
- eliminar digitação duplicada;
- melhorar qualidade dos dados;
- automatizar notificações;
- coletar indicadores;
- atualizar inventários;
- criar registros automaticamente;
- melhorar rastreabilidade;
- apoiar decisões operacionais.

O resultado esperado é uma operação mais **eficiente, integrada, previsível e menos dependente de execução manual**.

---

## Princípio

Automação não deve existir apenas porque uma tarefa pode ser automatizada.

Antes de automatizar, deve-se avaliar:

> **O processo está suficientemente definido, controlado e estável para ser automatizado?**

Fluxo recomendado:

```text
Identificar atividade manual
        ↓
Entender o processo
        ↓
Padronizar
        ↓
Avaliar risco
        ↓
Automatizar
        ↓
Registrar logs
        ↓
Monitorar
        ↓
Medir resultado
        ↓
Melhorar
```

---

## Estrutura sugerida

```text
06-automacao-e-integracoes/
│
├── README.md
├── python/
├── powershell/
├── APIs/
├── webhooks/
├── integracoes/
├── automacoes/
├── jobs/
├── ETL/
├── bots-operacionais/
├── notificacoes/
├── monitoramento/
├── seguranca/
├── exemplos/
└── documentacao/
```

---

# 1. Automação Operacional

Automação operacional busca executar tarefas recorrentes de forma padronizada.

Exemplos:

- coleta de informações;
- geração de relatórios;
- verificação de disponibilidade;
- atualização de inventário;
- criação de usuários;
- validação de configurações;
- aplicação de rotinas;
- consolidação de dados;
- envio de notificações.

---

## Critérios para automatizar

Uma atividade tende a ser boa candidata quando:

- é repetitiva;
- possui regras claras;
- ocorre com frequência;
- consome tempo da equipe;
- possui baixo grau de subjetividade;
- apresenta risco de erro manual;
- exige rastreabilidade.

---

# 2. Python

Python pode ser utilizado para:

- APIs;
- processamento de dados;
- automação web;
- integração entre plataformas;
- geração de relatórios;
- ETL;
- monitoramento;
- tarefas agendadas.

## Estrutura sugerida

```text
python/
├── scripts/
├── libs/
├── tests/
├── config/
├── logs/
└── README.md
```

---

## Boas práticas

- utilizar ambiente virtual;
- utilizar requirements.txt ou equivalente;
- separar configuração do código;
- validar entradas;
- tratar exceções;
- utilizar logging;
- evitar credenciais hardcoded;
- documentar dependências;
- criar testes quando aplicável.

---

# 3. PowerShell

PowerShell é especialmente útil em ambientes Microsoft.

Casos comuns:

- Active Directory;
- Windows Server;
- Hyper-V;
- arquivos;
- serviços;
- usuários;
- permissões;
- inventário;
- automação administrativa.

---

## Boas práticas

- utilizar parâmetros;
- validar permissões;
- registrar execução;
- evitar credenciais no script;
- utilizar tratamento de erros;
- documentar requisitos.

---

# 4. APIs

APIs permitem integração estruturada entre sistemas.

Exemplo:

```text
Sistema A
   ↓
API
   ↓
Sistema B
```

Podem ser utilizadas para:

- consultar dados;
- criar registros;
- atualizar informações;
- excluir registros;
- executar ações;
- integrar workflows.

---

## Métodos HTTP comuns

```text
GET     → consultar
POST    → criar
PUT     → atualizar
PATCH   → alterar parcialmente
DELETE  → remover
```

---

## Pontos de controle

Toda integração por API deve considerar:

- autenticação;
- autorização;
- endpoint;
- timeout;
- retries;
- logs;
- versionamento;
- limites de requisição;
- tratamento de erro.

---

# 5. Autenticação

Formas comuns:

- API Key;
- Token;
- OAuth 2.0;
- Basic Auth;
- certificados;
- service accounts.

As credenciais devem ser armazenadas fora do código.

Exemplo:

```text
.env
Secret Manager
Credential Manager
Vault
```

---

# 6. Webhooks

Webhooks permitem que um sistema envie eventos a outro automaticamente.

Exemplo:

```text
Evento no sistema
       ↓
Webhook
       ↓
Aplicação recebe
       ↓
Executa ação
```

Casos de uso:

- alertas;
- abertura de chamados;
- notificações;
- atualização de status;
- sincronização.

---

# 7. Integração Monitoramento x ITSM

Uma integração típica:

```text
Zabbix detecta falha
      ↓
Evento é validado
      ↓
Chamado é criado
      ↓
Equipe é notificada
      ↓
Serviço é restaurado
      ↓
Evento recupera
      ↓
Chamado é atualizado
```

---

## Cuidados

- evitar chamados duplicados;
- utilizar identificador do evento;
- tratar recuperação;
- definir severidade;
- controlar reabertura;
- registrar origem automática.

---

# 8. Integração com Inventário

Exemplo:

```text
NetBox
  ↓
API
  ↓
Script
  ↓
Ferramenta de monitoramento
```

A automação pode:

- criar hosts;
- atualizar IP;
- validar dispositivos;
- sincronizar status;
- remover ativos desativados.

---

# 9. ETL

ETL significa:

```text
Extract
Transform
Load
```

Pode ser utilizado para consolidar informações de diferentes fontes.

Exemplo:

```text
ITSM
 +
Zabbix
 +
Inventário
 +
Planilhas
   ↓
ETL
   ↓
Base consolidada
   ↓
Dashboard
```

---

# 10. Jobs e Agendamento

Automação pode ser executada:

- manualmente;
- por agendamento;
- por evento;
- por webhook;
- por fila.

Ferramentas possíveis:

- Task Scheduler;
- cron;
- systemd timers;
- pipelines;
- orquestradores.

---

## Cuidados

Todo job deve possuir:

- identificação;
- frequência;
- responsável;
- log;
- status;
- mecanismo de falha;
- notificação.

---

# 11. Bots Operacionais

Bots podem executar tarefas repetitivas dentro de plataformas.

Exemplos:

- consultar filas;
- preencher formulários;
- coletar informações;
- gerar alertas;
- consolidar indicadores.

Sempre avaliar:

- autorização;
- política da plataforma;
- robustez;
- manutenção;
- risco de alteração da interface;
- segurança das credenciais.

---

# 12. Automação Web

Automação via navegador pode ser utilizada quando não existe API adequada.

Ferramentas comuns:

- Playwright;
- Selenium.

Exemplo:

```text
Login autorizado
      ↓
Acesso à página
      ↓
Leitura do DOM
      ↓
Execução da ação
```

---

## Limitações

Automação baseada em interface tende a ser mais frágil porque depende de:

- seletores;
- HTML;
- comportamento visual;
- mudanças de versão;
- sessão.

Sempre que possível, priorizar integração por API oficial.

---

# 13. Logs

Automação sem logs é difícil de operar.

Registrar:

- início;
- fim;
- resultado;
- erro;
- objeto processado;
- duração;
- usuário técnico;
- timestamp.

Exemplo:

```text
2026-08-31 10:00:01 INFO Job iniciado
2026-08-31 10:00:03 INFO 120 registros processados
2026-08-31 10:00:04 ERROR Falha ao atualizar ativo 381
```

---

# 14. Níveis de Log

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Em produção, evitar DEBUG permanente quando gerar excesso de informação.

---

# 15. Tratamento de Erros

Uma automação deve prever falhas.

Exemplos:

- API indisponível;
- timeout;
- credencial inválida;
- registro inexistente;
- formato inesperado;
- indisponibilidade de rede.

Fluxo:

```text
Erro
 ↓
Captura
 ↓
Registro
 ↓
Retry, quando aplicável
 ↓
Notificação
 ↓
Encerramento controlado
```

---

# 16. Retry

Retries podem ser úteis para falhas transitórias.

Exemplo:

```text
Tentativa 1
   ↓ falha
aguarda 5s
   ↓
Tentativa 2
   ↓ falha
aguarda 15s
   ↓
Tentativa 3
```

Evitar retry infinito.

---

# 17. Idempotência

Uma automação idempotente pode ser executada novamente sem gerar efeitos duplicados indesejados.

Exemplo ruim:

```text
Executou duas vezes
→ criou dois chamados
```

Exemplo desejado:

```text
Evento já possui chamado
→ atualizar chamado existente
```

---

# 18. Controle de Estado

Algumas automações precisam saber o que aconteceu na execução anterior.

Pode ser armazenado em:

- SQLite;
- banco de dados;
- arquivo;
- cache;
- API externa.

Exemplos:

- último evento processado;
- último horário;
- IDs já tratados;
- status anterior.

---

# 19. Banco Local

SQLite pode ser adequado para ferramentas pequenas ou locais.

Pode armazenar:

- histórico;
- eventos;
- configurações;
- estado;
- resultados.

Para sistemas maiores, avaliar banco centralizado.

---

# 20. Segurança

Automação frequentemente possui acesso privilegiado.

Aplicar:

- menor privilégio;
- contas técnicas;
- segregação;
- rotação de credenciais;
- logs;
- controle de acesso;
- criptografia.

---

## Nunca armazenar diretamente no código

```text
senha
token
API key
credencial
segredo
```

---

# 21. Variáveis de Ambiente

Exemplo:

```env
API_URL=
API_TOKEN=
LOG_LEVEL=INFO
CHECK_INTERVAL_SECONDS=60
```

O arquivo real de credenciais deve ser protegido.

---

# 22. .gitignore

Arquivos sensíveis ou temporários não devem ser versionados.

Exemplo:

```gitignore
.env
*.log
*.db
__pycache__/
.venv/
venv/
sessions/
```

---

# 23. Configuração

Separar:

```text
Código
   ≠
Configuração
   ≠
Segredo
```

Isso permite executar a mesma aplicação em ambientes diferentes.

---

# 24. Ambientes

Quando necessário, considerar:

```text
DEV
HML
PRD
```

Cada ambiente pode ter:

- URL diferente;
- credencial diferente;
- configuração diferente;
- nível de log diferente.

---

# 25. Versionamento

Toda automação relevante deve utilizar controle de versão.

Registrar:

- alterações;
- correções;
- novas funcionalidades;
- mudanças incompatíveis.

---

# 26. Documentação

Toda integração deve responder:

```text
O que faz?
Por que existe?
Quem é responsável?
Quais sistemas utiliza?
Quais permissões precisa?
Como instalar?
Como configurar?
Como executar?
Como validar?
Como resolver falhas?
```

---

# 27. Diagrama de Integração

Exemplo:

```text
┌─────────┐
│ Zabbix  │
└────┬────┘
     │ API/Webhook
     ↓
┌─────────────┐
│ Integração  │
└──────┬──────┘
       ↓
┌─────────────┐
│ ITSM        │
└─────────────┘
```

Documentar:

- origem;
- destino;
- protocolo;
- autenticação;
- frequência;
- responsável.

---

# 28. Monitoramento das Automações

Automação também precisa ser monitorada.

Indicadores:

- última execução;
- sucesso;
- falha;
- duração;
- quantidade processada;
- retries;
- backlog.

---

## Exemplo

```text
Job: sincronizacao-netbox
Última execução: 10:00
Status: OK
Duração: 28s
Registros: 450
Erros: 0
```

---

# 29. Health Check

Serviços de integração podem expor verificação de saúde.

Exemplo:

```text
/health
```

Resposta:

```json
{
  "status": "ok"
}
```

---

# 30. Notificações

Notificações devem indicar:

- automação;
- erro;
- horário;
- impacto;
- tentativa;
- próxima ação.

Evitar alertas sem contexto.

---

# 31. Testes

Sempre que possível, criar testes.

Tipos:

- unitário;
- integração;
- funcional;
- smoke test.

---

## Smoke Test

Um smoke test verifica rapidamente se o fluxo principal funciona após alteração ou implantação.

Exemplo:

```text
Aplicação inicia
   ↓
Autentica
   ↓
Consulta API
   ↓
Processa registro
   ↓
Finaliza sem erro
```

---

# 32. Homologação

Antes de implantar uma automação crítica:

```text
Desenvolver
   ↓
Testar
   ↓
Homologar
   ↓
Documentar
   ↓
Implantar
   ↓
Monitorar
```

---

# 33. Rollback

Mudanças em automações devem permitir retorno quando possível.

Registrar:

- versão anterior;
- backup;
- configuração;
- procedimento de reversão.

---

# 34. Dependências

Dependências devem ser controladas.

Exemplo Python:

```text
requirements.txt
```

Evitar depender de bibliotecas sem controle de versão em aplicações críticas.

---

# 35. Observabilidade da Automação

Além de logs, pode-se utilizar:

- métricas;
- traces;
- dashboards;
- alertas.

Indicadores possíveis:

- execuções por hora;
- falhas;
- latência;
- throughput;
- filas;
- tempo de processamento.

---

# 36. Indicadores de Automação

### Eficiência

- horas economizadas;
- tarefas automatizadas;
- redução de execução manual.

### Qualidade

- erros evitados;
- taxa de sucesso;
- falhas por execução.

### Desempenho

- duração;
- throughput;
- latência.

### Confiabilidade

- disponibilidade;
- falhas;
- retries.

---

# 37. Medição de Benefício

Exemplo:

```text
Atividade manual:
10 minutos × 100 execuções/mês
= 1.000 minutos

Após automação:
2 minutos de supervisão × 100
= 200 minutos

Economia:
800 minutos/mês
≈ 13,3 horas
```

---

# 38. Critérios de Maturidade

| Nível | Situação |
|---|---|
| 0 | Atividades totalmente manuais |
| 1 | Scripts isolados |
| 2 | Automações pontuais documentadas |
| 3 | Integrações padronizadas e monitoradas |
| 4 | Automação integrada com logs, métricas e controles |
| 5 | Operação altamente automatizada e continuamente otimizada |

Avaliar:

- padronização;
- documentação;
- segurança;
- monitoramento;
- integração;
- confiabilidade;
- mensuração de benefício;
- manutenção.

---

# 39. Perguntas Orientadoras

## Processo

- A atividade está padronizada?
- Existe regra clara?
- Automatizar reduz esforço?
- Existe risco de automatizar erro?

## Segurança

- A credencial está protegida?
- O acesso utiliza menor privilégio?
- Existe conta técnica?

## Operação

- Há logs?
- Existe monitoramento?
- Quem recebe falhas?
- Existe retry?

## Arquitetura

- Existe API oficial?
- A integração é desacoplada?
- Existe dependência de interface gráfica?

## Gestão

- O benefício é medido?
- Existe responsável?
- A automação está documentada?
- Existe plano de manutenção?

---

# 40. Entregáveis Esperados

Este domínio pode produzir:

- scripts;
- APIs;
- webhooks;
- integrações;
- jobs;
- automações;
- bibliotecas;
- documentação;
- diagramas;
- arquivos de configuração;
- modelos `.env.example`;
- logs;
- dashboards;
- health checks;
- testes;
- procedimentos de implantação;
- planos de rollback;
- indicadores de automação.

---

# Relação com o IT Portfolio

- **00 — Diagnóstico e Planejamento** identifica atividades candidatas à automação;
- **01 — Governança e Gestão** define controles e responsabilidades;
- **02 — Operação e Serviços** recebe automações para fluxos de atendimento;
- **03 — Monitoramento e Observabilidade** gera eventos e monitora integrações;
- **04 — Infraestrutura** fornece plataformas e ambientes;
- **05 — Ativos e Configuração** fornece dados para sincronização;
- **07 — Dados e Indicadores** utiliza automações para coleta e consolidação;
- **08 — Governança de IA** define controles quando IA fizer parte da automação.

---

# Resultado esperado

Uma operação com **menos tarefas manuais, integrações mais confiáveis, maior rastreabilidade, redução de erros, melhor aproveitamento da equipe e automações implementadas com segurança, controle e capacidade de manutenção**.
