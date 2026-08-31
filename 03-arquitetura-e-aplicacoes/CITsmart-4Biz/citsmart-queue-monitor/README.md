# CITSmart Queue Monitor

Ferramenta local desenvolvida em Python para monitoramento operacional
de filas de atendimento no CITSmart.

## Objetivo

Centralizar informações operacionais da fila e fornecer visibilidade
sobre chamados que demandam atenção, permitindo acompanhamento contínuo
da operação.

## Principais funcionalidades

- Monitoramento automático da fila
- Identificação de chamados sem responsável
- Alertas de SLA a vencer
- Identificação de chamados vencidos
- Controle de chamados suspensos
- Histórico de entradas e saídas
- Indicadores operacionais
- Tempo médio até captura
- Ranking mensal por responsável
- Exportação de dados para CSV
- Persistência local com SQLite
- Automação de navegador com Playwright

## Tecnologias

- Python
- Tkinter
- Playwright
- SQLite
- CITSmart
- CSV

## Arquitetura

A aplicação executa localmente e utiliza automação de navegador para
coletar informações da fila. Os eventos observados são registrados em
SQLite e apresentados em uma interface de acompanhamento operacional.

## Segurança

Credenciais e parâmetros específicos do ambiente não fazem parte do
repositório.

Utilize `.env.example` como referência para configurar sua instalação.

## Licença

Este projeto é disponibilizado sob a licença MIT.

Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
