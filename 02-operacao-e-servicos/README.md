# 02 — Operação e Serviços

Este diretório reúne práticas, processos, modelos, indicadores e referências voltados à **operação diária dos serviços de TI**.

A proposta é organizar o atendimento, a sustentação e o controle das demandas de forma previsível, rastreável e orientada à qualidade do serviço.

---

## Objetivo

Apoiar a estruturação e evolução da operação de serviços de TI, permitindo:

- organizar fluxos de atendimento;
- reduzir tempo de resposta e resolução;
- melhorar priorização;
- reduzir backlog;
- padronizar escalonamentos;
- diminuir recorrência de falhas;
- melhorar a experiência do usuário;
- acompanhar desempenho operacional;
- criar base de conhecimento;
- estabelecer mecanismos de melhoria contínua.

O resultado esperado é uma operação mais **estável, previsível, mensurável e orientada ao usuário**.

---

## Princípio

A operação de serviços deve responder de forma consistente a perguntas como:

> **O que aconteceu, quem está responsável, qual o impacto, qual o prazo e qual é a próxima ação?**

Fluxo simplificado:

```text
Demanda recebida
      ↓
Registro
      ↓
Classificação
      ↓
Priorização
      ↓
Atendimento
      ↓
Escalonamento, se necessário
      ↓
Solução
      ↓
Validação
      ↓
Encerramento
      ↓
Medição e melhoria
```

---

## Estrutura sugerida

```text
02-operacao-e-servicos/
│
├── README.md
├── incidentes/
├── requisicoes/
├── problemas/
├── mudancas/
├── conhecimento/
├── major-incidents/
├── fila-de-atendimento/
├── escalonamento/
├── catalogo-de-servicos/
├── procedimentos-operacionais/
├── experiencia-do-usuario/
├── comunicacao/
└── melhoria-continua/
```

---

## 1. Gestão de Incidentes

A gestão de incidentes tem como objetivo restaurar o serviço normal o mais rapidamente possível e reduzir o impacto sobre os usuários e o negócio.

### Informações mínimas

Um incidente deve possuir, sempre que aplicável:

- identificação;
- data e hora;
- serviço afetado;
- usuário ou área afetada;
- impacto;
- urgência;
- prioridade;
- responsável;
- grupo de atendimento;
- descrição;
- ações realizadas;
- solução;
- tempo de atendimento;
- tempo de resolução.

### Perguntas orientadoras

- Qual serviço foi afetado?
- Quantos usuários foram impactados?
- Existe indisponibilidade total ou parcial?
- Há solução de contorno?
- Existe incidente semelhante conhecido?
- Qual equipe deve atuar?
- É necessário escalonamento?
- O incidente deve ser tratado como crítico?

---

## 2. Priorização

Prioridade deve ser definida de forma consistente e não apenas pela percepção do solicitante.

Uma abordagem comum considera:

```text
Prioridade = Impacto × Urgência
```

Exemplo:

| Impacto | Urgência | Prioridade |
|---|---|---|
| Alto | Alta | Crítica |
| Alto | Média | Alta |
| Médio | Média | Média |
| Baixo | Baixa | Baixa |

Os critérios devem ser definidos conforme o contexto da organização.

---

## 3. Incidentes Críticos

Incidentes com grande impacto podem exigir um fluxo específico de **Major Incident Management**.

### Características

- alto impacto;
- indisponibilidade de serviço crítico;
- múltiplos usuários afetados;
- risco operacional relevante;
- necessidade de coordenação entre equipes;
- necessidade de comunicação executiva.

### Fluxo sugerido

```text
Detecção
   ↓
Classificação como crítico
   ↓
Acionamento das equipes
   ↓
Coordenação técnica
   ↓
Comunicação periódica
   ↓
Restauração
   ↓
Validação
   ↓
Post-mortem
```

### Artefatos recomendados

- registro do incidente;
- linha do tempo;
- responsáveis;
- comunicações;
- causa;
- solução;
- ações preventivas;
- post-mortem.

---

## 4. Gestão de Requisições

Requisições são demandas normalmente padronizadas, previsíveis e repetitivas.

Exemplos:

- criação de usuário;
- concessão de acesso;
- instalação de software;
- desbloqueio de conta;
- solicitação de equipamento;
- configuração de estação;
- informação ou relatório.

### Boas práticas

- definir catálogo;
- padronizar informações necessárias;
- automatizar quando possível;
- estabelecer aprovação;
- definir prazo;
- definir responsável;
- criar procedimentos reutilizáveis.

---

## 5. Catálogo de Serviços

O catálogo ajuda a organizar os serviços e requisições oferecidos pela TI.

Cada item pode conter:

- nome do serviço;
- descrição;
- público atendido;
- responsável;
- horário de atendimento;
- dependências;
- SLA;
- requisitos;
- procedimento;
- canal de solicitação;
- criticidade.

Exemplo:

| Serviço | Responsável | Horário | SLA | Criticidade |
|---|---|---|---|---|
| Acesso corporativo | Suporte | Comercial | 4h | Alta |
| Instalação de software | Suporte | Comercial | 8h | Média |
| Rede corporativa | Infraestrutura | 24x7 | Conforme criticidade | Crítica |

---

## 6. Gestão de Problemas

A gestão de problemas busca identificar e tratar causas de incidentes recorrentes ou relevantes.

### Objetivos

- reduzir reincidência;
- identificar causa raiz;
- documentar erros conhecidos;
- criar soluções de contorno;
- gerar ações preventivas.

### Fluxo

```text
Incidentes recorrentes
      ↓
Problema identificado
      ↓
Investigação
      ↓
Causa raiz
      ↓
Solução de contorno
      ↓
Ação definitiva
      ↓
Validação
```

### Técnicas úteis

- 5 Porquês;
- Ishikawa;
- análise de tendência;
- Pareto;
- análise de logs;
- correlação de eventos.

---

## 7. Erros Conhecidos

Quando uma causa já é conhecida, mas ainda não existe solução definitiva, pode ser criado um registro de erro conhecido.

Esse registro pode conter:

- descrição;
- sintomas;
- causa;
- solução de contorno;
- serviços afetados;
- procedimento;
- referência ao problema;
- status da solução definitiva.

Isso reduz tempo de diagnóstico em novos incidentes.

---

## 8. Gestão de Mudanças

Mudanças devem ser controladas para reduzir risco de indisponibilidade ou impacto inesperado.

### Informações mínimas

- descrição;
- justificativa;
- responsável;
- serviço afetado;
- risco;
- impacto;
- janela;
- plano de implementação;
- plano de teste;
- plano de rollback;
- aprovação;
- resultado.

### Classificação possível

```text
Mudança padrão
Mudança normal
Mudança emergencial
```

### Checklist básico

```text
[ ] Impacto avaliado
[ ] Risco avaliado
[ ] Responsável definido
[ ] Janela definida
[ ] Backup realizado, quando aplicável
[ ] Plano de teste definido
[ ] Rollback definido
[ ] Aprovação registrada
[ ] Comunicação realizada
[ ] Resultado documentado
```

---

## 9. Gestão de Conhecimento

O conhecimento operacional não deve depender exclusivamente da memória das pessoas.

### Conteúdos recomendados

- procedimentos;
- FAQs;
- soluções;
- erros conhecidos;
- scripts;
- diagramas;
- troubleshooting;
- configurações;
- lições aprendidas.

### Estrutura de um artigo

```text
Título
Objetivo
Sintoma
Causa
Pré-requisitos
Procedimento
Validação
Rollback
Observações
Responsável
Data da revisão
```

### Resultado esperado

Redução de:

- tempo de diagnóstico;
- dependência de especialistas;
- retrabalho;
- erros;
- escalonamentos desnecessários.

---

## 10. Fila de Atendimento

A fila deve permitir visão clara da situação operacional.

Indicadores relevantes:

- quantidade atual;
- sem responsável;
- a vencer;
- vencidos;
- suspensos;
- idade do backlog;
- entradas;
- saídas;
- reentradas.

### Perguntas operacionais

- Qual chamado precisa de atenção agora?
- Existe chamado sem responsável?
- Há SLA próximo do vencimento?
- Qual é o chamado mais antigo?
- Existem chamados suspensos por muito tempo?
- A fila está crescendo?
- A capacidade da equipe está adequada?

---

## 11. Escalonamento

O escalonamento deve possuir critérios claros.

### Escalonamento funcional

Quando o chamado exige conhecimento de outro nível ou equipe.

Exemplo:

```text
N1
 ↓
N2
 ↓
N3
```

### Escalonamento hierárquico

Quando é necessário envolver gestão devido a:

- risco;
- impacto;
- atraso;
- indisponibilidade;
- ausência de resposta;
- incidente crítico.

### Regras recomendadas

- definir gatilho;
- definir destinatário;
- definir prazo;
- registrar motivo;
- manter rastreabilidade.

---

## 12. SLA

O acompanhamento de SLA deve permitir atuação antes do vencimento.

Situações típicas:

```text
Normal
A vencer
Vencido
Suspenso
```

A operação deve conhecer:

- meta;
- tempo restante;
- regra de suspensão;
- prioridade;
- responsável;
- consequência do descumprimento.

Indicadores possíveis:

- percentual dentro do SLA;
- quantidade vencida;
- quantidade a vencer;
- tempo médio;
- distribuição por prioridade;
- reincidência de violações.

---

## 13. Backlog

Backlog não deve ser analisado apenas pela quantidade total.

Também deve considerar:

- idade;
- prioridade;
- responsável;
- serviço;
- status;
- SLA;
- causa da permanência.

### Faixas de envelhecimento

Exemplo:

```text
0–1 dia
2–3 dias
4–7 dias
8–15 dias
16–30 dias
+30 dias
```

O objetivo é evitar acumulação silenciosa de demandas antigas.

---

## 14. Comunicação com Usuários

Boa operação também depende de comunicação.

Recomendações:

- linguagem clara;
- informar impacto;
- indicar próxima atualização;
- evitar jargão excessivo;
- registrar comunicação;
- comunicar indisponibilidades;
- informar restauração;
- orientar o usuário quando necessário.

### Incidentes críticos

Uma comunicação pode conter:

```text
Serviço afetado
Impacto
Início do incidente
Situação atual
Ações em andamento
Previsão, se conhecida
Próxima atualização
```

---

## 15. Experiência e Satisfação do Usuário

A experiência do usuário ajuda a avaliar a qualidade percebida do serviço.

Podem ser acompanhados:

- satisfação;
- facilidade de atendimento;
- clareza da comunicação;
- percepção de prazo;
- qualidade da solução.

A análise deve observar também a **representatividade da amostra**, não apenas a nota média.

---

## 16. Indicadores Operacionais

### Volume

- chamados no período;
- entradas;
- saídas;
- backlog.

### Tempo

- tempo de primeira resposta;
- tempo de atendimento;
- tempo de resolução;
- tempo até captura.

### SLA

- cumprimento;
- violações;
- chamados a vencer.

### Qualidade

- reabertura;
- recorrência;
- satisfação;
- resolução no primeiro contato.

### Confiabilidade

- MTTD;
- MTTA;
- MTTR;
- MTBF.

---

## 17. Relatório Operacional

Um relatório periódico pode conter:

```text
Resumo executivo
Volume
Backlog
SLA
Indicadores de tempo
Incidentes relevantes
Problemas recorrentes
Mudanças
Satisfação
Riscos
Planos de ação
Tendência
```

O objetivo é explicar não apenas **o que aconteceu**, mas também:

- por que aconteceu;
- qual o impacto;
- qual a tendência;
- qual ação será tomada.

---

## 18. Capacidade da Operação

A demanda deve ser comparada com a capacidade disponível.

Avaliar:

- volume por período;
- distribuição por horário;
- quantidade por responsável;
- complexidade;
- escalonamentos;
- backlog;
- sazonalidade.

Perguntas:

- A equipe consegue absorver a demanda?
- Existem horários críticos?
- Existem gargalos por especialidade?
- Há concentração excessiva em determinados responsáveis?

---

## 19. Automatização

Processos repetitivos devem ser avaliados para automação.

Exemplos:

- classificação;
- notificações;
- abertura automática;
- atualização de status;
- coleta de indicadores;
- relatórios;
- integração com monitoramento;
- atualização de inventário.

A automação deve reduzir esforço sem remover controles essenciais.

---

## 20. Melhoria Contínua

A operação deve utilizar dados para identificar oportunidades.

Fluxo:

```text
Operar
   ↓
Medir
   ↓
Identificar desvio
   ↓
Analisar causa
   ↓
Implementar melhoria
   ↓
Medir novamente
```

Fontes de melhoria:

- incidentes;
- problemas;
- reclamações;
- SLA;
- backlog;
- satisfação;
- auditorias;
- métricas;
- feedback da equipe.

---

## 21. Critérios de Maturidade

| Nível | Situação |
|---|---|
| 0 | Processo inexistente |
| 1 | Execução informal |
| 2 | Parcialmente definido |
| 3 | Definido e executado |
| 4 | Medido e controlado |
| 5 | Otimizado e melhorado continuamente |

A avaliação pode considerar:

- definição;
- documentação;
- execução;
- responsabilidade;
- medição;
- evidência;
- automação;
- melhoria.

---

## 22. Perguntas Orientadoras

### Atendimento

- A fila possui responsável?
- Existem critérios claros de prioridade?
- Os chamados são classificados corretamente?
- Existe escalonamento definido?

### SLA

- Os prazos são acompanhados?
- Existem alertas antes do vencimento?
- Violações são analisadas?

### Problemas

- Incidentes recorrentes geram investigação?
- Existem erros conhecidos?
- A causa raiz é registrada?

### Mudanças

- Existe avaliação de risco?
- Há rollback?
- Mudanças com falha são analisadas?

### Conhecimento

- Procedimentos estão documentados?
- O conhecimento é atualizado?
- A equipe consegue localizar soluções rapidamente?

---

## 23. Entregáveis Esperados

Este domínio pode produzir:

- fluxos operacionais;
- procedimentos;
- catálogo de serviços;
- matriz de prioridade;
- regras de escalonamento;
- base de conhecimento;
- dashboards;
- relatórios;
- indicadores;
- post-mortems;
- modelos de incidente;
- modelos de mudança;
- registros de problemas;
- planos de melhoria.

---

## Resultado esperado

Uma operação de serviços de TI **organizada, rastreável, mensurável e orientada à restauração rápida, qualidade do atendimento e melhoria contínua**.
