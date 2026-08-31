
# IT Operations Assessment

Aplicação local em Python/Streamlit para realizar um diagnóstico inicial da Operação de TI.


## Descrição da aplicação

A aplicação realiza uma **avaliação inicial e prática da Operação de TI**, com foco em identificar pontos estruturados, lacunas, riscos e prioridades.

### Base metodológica

O modelo utiliza uma **metodologia própria e simplificada**, inspirada principalmente em:

- **COBIT** — governança, controle, desempenho e capacidade;
- **ITIL** — práticas de gestão e operação de serviços de TI.

A escala utilizada varia de **0 a 5**:

| Nível | Interpretação |
|---:|---|
| 0 | Inexistente |
| 1 | Informal ou inadequado |
| 2 | Parcial |
| 3 | Implementado / definido |
| 4 | Controlado |
| 5 | Medido e melhorado |

> O diagnóstico não representa avaliação ou certificação oficial COBIT ou ITIL.

### Fluxo de uso

```text
Definir escopo
    ↓
Definir nível-alvo
    ↓
Responder checklist
    ↓
Salvar avaliação
    ↓
Analisar relatório
    ↓
Gerar PDF
```

## Funcionalidades

- 9 abas de avaliação:
  1. Organização da Operação
  2. Ativos e Inventário
  3. Infraestrutura
  4. Aplicações e Serviços Críticos
  5. Backup e Continuidade
  6. Segurança e Acessos
  7. Monitoramento
  8. Documentação e Processos
  9. Suporte e Atendimento
- Inclusão/exclusão de qualquer área do escopo.
- Nível-alvo configurável por área.
- Respostas padronizadas em escala de 0 a 5.
- Perguntas específicas, como situação do inventário.
- Bloco de avaliação do usuário dentro de Suporte e Atendimento.
- Perguntas condicionais para pesquisa de satisfação.
- Observações por pergunta.
- Salvamento e retomada de avaliações em SQLite.
- Progresso do preenchimento.
- Relatório consolidado na tela.
- Quadro de desempenho por área.
- Identificação de constatações críticas.
- Geração de relatório em PDF.

## Metodologia inicial

A primeira versão utiliza uma escala própria de estruturação/capacidade:

| Nível | Interpretação |
|---:|---|
| 0 | Inexistente |
| 1 | Informal ou inadequado |
| 2 | Parcial |
| 3 | Implementado / definido |
| 4 | Controlado |
| 5 | Medido e melhorado |

Cada área possui um nível-alvo configurável.

A situação da área considera o gap entre o nível atual e o nível-alvo:

- **Adequado:** atual >= alvo e sem deficiência crítica;
- **Atenção:** gap entre 0 e -1;
- **Insuficiente:** gap inferior a -1;
- **Crítico:** existe pelo menos uma questão crítica avaliada em 0 ou 1.

O índice percentual é apenas a conversão do nível médio de 0–5 para 0–100%.

> Esta metodologia é um modelo próprio inicial. Não representa avaliação ou certificação oficial COBIT, ITIL, ISO ou outro referencial. A matriz de perguntas, critérios e classificações deve ser calibrada posteriormente com literatura e validação prática.

## Instalação

Requer Python 3.10 ou superior.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executar

```bash
streamlit run app.py
```

O navegador abrirá a aplicação local.

## Salvamento

As avaliações são armazenadas no arquivo local:

```text
it_assessment.db
```

Esse arquivo é criado automaticamente na primeira execução.

## Estrutura

```text
IT-Operations-Assessment/
├── app.py
├── requirements.txt
└── README.md
```

## Próximas evoluções sugeridas

- mover o banco de perguntas para YAML/JSON;
- criar perfis/modelos de avaliação;
- permitir anexar evidências;
- incluir plano de ação automático;
- incluir recomendações por resposta;
- adicionar histórico de avaliações da mesma organização;
- comparar diagnóstico atual com diagnóstico anterior;
- fundamentar cada grupo de perguntas em referências bibliográficas;
- calibrar pesos, níveis-alvo e critérios com literatura e uso real.

## Licença

Este projeto é disponibilizado sob a licença MIT.

Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.


## Autor

**Daniel Diehl**

- E-mail: consultortiglobal@gmail.com
- LinkedIn: https://www.linkedin.com/in/danieldiehl90/
- GitHub: https://github.com/Daniquiks
- PIX para doação: `consultortiglobal@gmail.com`
