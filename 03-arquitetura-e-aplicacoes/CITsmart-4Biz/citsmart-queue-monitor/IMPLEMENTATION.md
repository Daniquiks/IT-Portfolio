# Guia de Implementação — CITSmart Queue Monitor

Este documento orienta a instalação, configuração, adaptação e validação do **CITSmart Queue Monitor** em um novo ambiente.

A ferramenta utiliza **Python**, **Tkinter**, **Playwright** e **SQLite** para monitorar uma fila do CITSmart/4Biz, identificar situações operacionais relevantes e apresentar indicadores em uma interface gráfica.

---

## 1. Estrutura esperada do projeto

```text
citsmart-queue-monitor/
│
├── README.md
├── IMPLEMENTATION.md
├── .gitignore
├── .env.example
├── requirements.txt
│
├── assets/
│   └── dashboard.png
│
└── src/
    └── main.py
```

O arquivo `main.py` contém a aplicação.

As configurações específicas do ambiente devem ficar no arquivo `.env`.

O arquivo `.env` **não deve ser enviado ao GitHub**.

---

## 2. Pré-requisitos

Antes da implementação, verifique se a máquina possui:

- Python 3.10 ou superior;
- Google Chrome ou Chromium;
- acesso de rede ao CITSmart/4Biz;
- usuário com permissão para visualizar a fila;
- acesso ao Smart Reports, caso o módulo INS seja utilizado.

No Windows, o Tkinter normalmente acompanha a instalação oficial do Python.

---

## 3. Criar o ambiente Python

Abra o terminal na raiz do projeto.

### Windows / PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Instalar as dependências

Execute:

```bash
pip install -r requirements.txt
```

Depois instale o navegador utilizado pelo Playwright:

```bash
playwright install chromium
```

Se o projeto estiver configurado com:

```env
CHROME_CHANNEL=chrome
```

o Google Chrome deverá estar instalado.

---

## 5. Criar o arquivo `.env`

Copie:

```text
.env.example
```

para:

```text
.env
```

### Windows

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Depois preencha o `.env` com os dados reais do ambiente.

---

## 6. Configuração mínima

Para utilizar somente o monitor principal da fila, configure:

```env
CITSMART_USERNAME=
CITSMART_PASSWORD=
CITSMART_QUEUE_URL=
```

Exemplo conceitual:

```env
CITSMART_USERNAME=usuario
CITSMART_PASSWORD=senha
CITSMART_QUEUE_URL=https://servidor.exemplo/...
```

Nunca publique os valores reais.

---

## 7. Variáveis principais

### Monitoramento

```env
CHECK_INTERVAL_SECONDS=15
SOFT_REFRESH_EVERY_SECONDS=120
RECONNECT_EVERY_SECONDS=60
OUT_OF_QUEUE_GRACE_SECONDS=10
MISSING_CONFIRMATIONS=3
```

Descrição:

- `CHECK_INTERVAL_SECONDS`: intervalo entre leituras da fila;
- `SOFT_REFRESH_EVERY_SECONDS`: intervalo entre atualizações leves da página;
- `RECONNECT_EVERY_SECONDS`: intervalo utilizado nas tentativas de reconexão;
- `OUT_OF_QUEUE_GRACE_SECONDS`: tolerância para situações temporárias fora da página esperada;
- `MISSING_CONFIRMATIONS`: quantidade de leituras consecutivas necessárias antes de confirmar a saída de um chamado.

---

## 8. Alertas

```env
UNASSIGNED_ALERT_AFTER_MINUTES=8
UNASSIGNED_REPEAT_MINUTES=5
DUE_SOON_MINUTES=30
DUE_ALERT_REPEAT_MINUTES=10
SUSPENDED_ALERT_DAYS=14
ERROR_ALERT_COOLDOWN_MINUTES=10
```

Esses parâmetros controlam:

- alertas para chamados sem responsável;
- repetição dos alertas;
- janela de SLA "a vencer";
- alertas de SLA vencido;
- suspensão prolongada;
- repetição de alertas de erro.

---

## 9. Navegador

```env
HEADLESS=false
BRING_TO_FRONT_ON_ALERT=true
CHROME_CHANNEL=chrome
```

Durante a implantação e os testes, recomenda-se:

```env
HEADLESS=false
LOG_FILE_LEVEL=DEBUG
```

Isso permite observar visualmente o navegador e analisar o log.

Após a homologação, o ambiente pode utilizar:

```env
LOG_FILE_LEVEL=INFO
```

---

## 10. Executar a aplicação

Na raiz do projeto:

```bash
python src/main.py
```

O fluxo esperado é:

```text
Aplicação inicia
      ↓
Interface gráfica é aberta
      ↓
Playwright inicia o navegador
      ↓
CITSmart é acessado
      ↓
Autenticação ocorre
      ↓
Fila é localizada
      ↓
Linha de base é criada
      ↓
Monitoramento periódico começa
```

---

## 11. Validação da autenticação

A implementação deve ser validada contra a tela de login do ambiente real.

Verifique se os elementos usados pelo código continuam válidos.

Exemplos comuns:

```text
#username
#password
#kc-login
```

Caso a organização utilize:

- SSO;
- MFA;
- certificado;
- autenticação integrada;
- login customizado;

o fluxo de autenticação poderá precisar de adaptação.

---

## 12. Validar a estrutura da fila

O sistema utiliza automação de interface.

Por isso, versões diferentes ou customizações do CITSmart podem alterar o HTML.

O implementador deve abrir a fila manualmente e verificar o DOM com as ferramentas de desenvolvedor do navegador.

A implementação deve conseguir identificar:

- linha do chamado;
- número do chamado;
- solicitação;
- grupo;
- responsável;
- situação;
- data de criação;
- data limite;
- SLA.

---

## 13. Seletores que devem ser conferidos

A implementação atual pode utilizar estruturas semelhantes a:

```text
div.tableless-tr.request-item
.request-id
.responsavel
.solicitacao
.grupo
.situacao
.dataCriacao
.dataLimite
```

Se algum dado não aparecer corretamente, revise primeiro os seletores HTML antes de alterar as regras de negócio.

Funções relacionadas normalmente incluem:

```text
find_queue_frame()
wait_for_queue_context()
read_tickets()
extract_owner()
extract_sla_text()
extract_creation_date()
extract_limit_date()
extract_sla_status()
```

---

## 14. Validar responsável

Teste pelo menos os seguintes cenários:

```text
Chamado sem responsável
Chamado já atribuído
Chamado que recebe responsável
Chamado que perde responsável
```

A aplicação deve conseguir diferenciar corretamente um responsável vazio de um responsável preenchido.

Isso é essencial para os eventos de captura e para os alertas de chamados sem responsável.

---

## 15. Validar SLA

Teste pelo menos:

```text
SLA normal
SLA a vencer
SLA vencido
Chamado suspenso
```

Confirme:

1. o valor apresentado pelo CITSmart;
2. o valor lido pela aplicação;
3. a classificação gerada pela aplicação;
4. o alerta apresentado.

O fato de o texto do SLA aparecer na tela não significa que a interpretação esteja correta.

---

## 16. Validar linha de base

Ao iniciar o monitor, os chamados que já estão na fila devem formar a linha de base.

Exemplo:

```text
Fila possui 20 chamados
Monitor é iniciado
Presentes na abertura = 20
Entradas detectadas = 0
```

Os chamados existentes antes da inicialização não devem ser tratados como novas entradas.

---

## 17. Validar entrada

Depois da criação da linha de base, faça entrar um novo chamado.

Resultado esperado:

```text
Novo chamado aparece
Entrada é registrada
Indicador de entradas aumenta
Fila atual é atualizada
Alertas são avaliados
```

---

## 18. Validar captura

Utilize um chamado sem responsável.

Depois atribua um responsável.

Resultado esperado:

```text
Responsável vazio
      ↓
Responsável atribuído
      ↓
Captura detectada
      ↓
Tempo até captura calculado
      ↓
Indicadores atualizados
```

---

## 19. Validar reentrada

Um chamado que já saiu pode retornar à fila.

Nesse caso, a aplicação deve registrar uma **reentrada**, e não uma nova entrada inicial.

---

## 20. Validar saída da fila

O CITSmart pode remover temporariamente elementos do HTML durante atualização da página.

Por isso, a aplicação utiliza confirmações sucessivas.

Exemplo:

```env
MISSING_CONFIRMATIONS=3
```

Isso significa que um chamado precisa permanecer ausente por várias leituras antes de ser considerado realmente fora da fila.

Teste:

- refresh normal;
- chamado realmente removido;
- chamado que desaparece e retorna;
- perda temporária de conexão.

---

## 21. Validar suspensão

Teste:

```text
Chamado entra em suspensão
Chamado permanece suspenso
Chamado sai da suspensão
Chamado permanece suspenso acima do limite
```

O limite é configurado em:

```env
SUSPENDED_ALERT_DAYS=14
```

---

## 22. Banco SQLite

A aplicação utiliza SQLite para registrar eventos observados.

Entre os eventos podem existir:

```text
BASELINE
ENTRY
REENTRY
CAPTURE
RESOLUTION
QUEUE_EXIT
SUSPENSION
```

O banco local não deve ser enviado ao GitHub.

O `.gitignore` deve bloquear:

```text
*.db
*.db-shm
*.db-wal
*.sqlite
*.sqlite3
```

---

## 23. Logs

Durante a implantação utilize:

```env
LOG_FILE_LEVEL=DEBUG
```

Depois da homologação:

```env
LOG_FILE_LEVEL=INFO
```

O log deve ser utilizado para investigar:

- falhas de login;
- falhas de localização da fila;
- problemas de seletores;
- reconexões;
- erros de leitura;
- inconsistências de atualização.

---

## 24. Módulo D-1

O módulo D-1 é opcional.

Configure somente se ele for utilizado:

```env
CITSMART_D1_REQUEST_URL=
D1_REQUESTER_NAME=
D1_REQUESTER_EMAIL=
D1_CONTACT_ORIGIN=
D1_ACTIVITY=
D1_CONTACT_METHOD=
D1_SERVICE_TEAM=
D1_STATE=
D1_LOCATION=
D1_IS_MANAGER=
```

O implementador também deve validar os campos HTML do formulário.

Se o CITSmart da organização utilizar IDs ou estruturas diferentes, os seletores deverão ser adaptados.

---

## 25. Módulo INS / Smart Reports

O módulo INS também é opcional.

Exemplo de parâmetros:

```env
CITSMART_SMART_REPORTS_URL=
INS_PESQUISA_REPORT_ID=
INS_TIT_REPORT_ID=
INS_TMS_REPORT_ID=
INS_CONTRACT_ID=
INS_GROUP_IDS=
```

Os valores são específicos de cada ambiente.

Não utilize IDs de outro ambiente sem validação.

Teste separadamente:

```text
PESQUISA
TIT
TMS
```

Confirme:

- relatório correto;
- período;
- filtros;
- KPIs;
- resumo;
- detalhes;
- exportação.

---

## 26. Segurança

Nunca envie para o GitHub:

```text
.env
senhas
usuários reais
tokens
cookies
sessões do navegador
bancos SQLite reais
logs reais
CSV exportados da operação
URLs internas sensíveis
```

Antes do `git push`, execute:

```bash
git status
```

e revise todos os arquivos.

Também pode ser útil:

```bash
git grep -n -i "password"
git grep -n -i "username"
git grep -n -i "http"
git grep -n -i "@"
```

Analise manualmente os resultados antes de publicar.

---

## 27. Homologação

Checklist mínimo:

```text
[ ] Ambiente Python criado
[ ] Dependências instaladas
[ ] Playwright configurado
[ ] .env criado
[ ] .env ignorado pelo Git
[ ] URL da fila validada
[ ] Autenticação validada
[ ] Fila localizada
[ ] Iframes validados
[ ] Número do chamado validado
[ ] Responsável validado
[ ] Solicitação validada
[ ] Grupo validado
[ ] Situação validada
[ ] Data de criação validada
[ ] Data limite validada
[ ] SLA normal validado
[ ] SLA a vencer validado
[ ] SLA vencido validado
[ ] Suspensão validada
[ ] Linha de base validada
[ ] Entrada validada
[ ] Captura validada
[ ] Reentrada validada
[ ] Saída validada
[ ] Banco SQLite validado
[ ] Indicadores validados
[ ] Alertas validados
[ ] Reconexão validada
[ ] Interface validada
[ ] Nenhum dado sensível está versionado
```

---

## 28. Critério de aceite

A implementação pode ser considerada concluída quando:

- a fila é lida de forma consistente;
- os campos são extraídos corretamente;
- não existem falsas saídas durante atualizações normais;
- responsável é identificado corretamente;
- SLA é classificado corretamente;
- alertas são gerados nos momentos esperados;
- eventos são persistidos corretamente;
- indicadores refletem os eventos observados;
- reconexão funciona após falhas temporárias;
- nenhum segredo está versionado.

---

## 29. Estratégia recomendada de implantação

```text
1. Instalação
      ↓
2. Configuração do .env
      ↓
3. Teste de autenticação
      ↓
4. Teste de leitura da fila
      ↓
5. Validação dos campos
      ↓
6. Validação do SLA
      ↓
7. Validação dos eventos
      ↓
8. Validação do histórico
      ↓
9. Validação dos indicadores
      ↓
10. Validação de reconexão
      ↓
11. Módulos opcionais
      ↓
12. Homologação
      ↓
13. Uso operacional
```

Não configure os módulos opcionais antes de estabilizar o monitoramento básico da fila.

---

## 30. Manutenção

Após qualquer atualização relevante do CITSmart, valide novamente:

- autenticação;
- iframe/contexto da fila;
- estrutura das linhas;
- responsável;
- SLA;
- situação;
- datas;
- atualização automática;
- Smart Reports;
- formulário D-1.

Como a solução depende da interface do sistema, alterações no DOM podem exigir manutenção dos seletores.
