# 00 — Diagnóstico e Planejamento

Este diretório reúne métodos, ferramentas, modelos e referências voltados ao **diagnóstico inicial de uma operação de TI** e à construção de um plano estruturado de evolução.

A proposta é criar uma visão objetiva do estado atual da operação antes de definir ações, prioridades, investimentos ou mudanças. O diagnóstico deve servir como ponto de partida para decisões de gestão, governança, melhoria contínua e organização dos serviços de TI.

---

## Objetivo

Apoiar a avaliação da operação de TI de forma estruturada, permitindo identificar:

- pontos fortes;
- fragilidades;
- riscos;
- gargalos;
- dependências;
- ausência de controles;
- oportunidades de melhoria;
- necessidades de padronização;
- prioridades de curto, médio e longo prazo.

O resultado esperado é transformar percepções dispersas em um **diagnóstico organizado, mensurável e acionável**.

---

## Princípio

Antes de melhorar uma operação, é necessário compreender:

> **Onde estamos, o que funciona, o que não funciona, quais riscos existem e onde devemos concentrar esforço.**

O diagnóstico deve preceder a definição do plano de melhoria.

```text
Levantamento
    ↓
Diagnóstico
    ↓
Identificação de gaps
    ↓
Avaliação de riscos
    ↓
Priorização
    ↓
Plano de ação
    ↓
Roadmap
    ↓
Acompanhamento
```

---

## Escopo de avaliação

O diagnóstico pode considerar diferentes dimensões da operação.

### 1. Pessoas

Avaliar aspectos como:

- estrutura da equipe;
- quantidade de profissionais;
- papéis e responsabilidades;
- distribuição das atividades;
- conhecimento técnico;
- matriz de competências;
- dependência de pessoas específicas;
- escalonamento;
- cobertura de horários;
- necessidade de capacitação.

---

### 2. Processos

Verificar se os principais processos estão definidos, executados e controlados.

Exemplos:

- gestão de incidentes;
- gestão de requisições;
- gestão de problemas;
- gestão de mudanças;
- gestão de conhecimento;
- gestão de ativos;
- gestão de configuração;
- monitoramento;
- backup;
- capacidade;
- disponibilidade;
- continuidade;
- gestão de fornecedores.

Avaliar também:

- existência de procedimentos;
- responsáveis;
- entradas e saídas;
- critérios de prioridade;
- regras de escalonamento;
- registros;
- indicadores;
- pontos de controle;
- nível de padronização.

---

### 3. Tecnologia

Avaliar a infraestrutura e as ferramentas utilizadas para sustentar a operação.

Exemplos:

- servidores;
- redes;
- virtualização;
- storage;
- backup;
- datacenter;
- cloud;
- monitoramento;
- ferramentas ITSM;
- inventário;
- CMDB;
- automações;
- integrações;
- segurança.

---

### 4. Serviços

Identificar os serviços efetivamente entregues pela TI.

Avaliar:

- catálogo de serviços;
- criticidade;
- usuários atendidos;
- dependências;
- responsáveis;
- disponibilidade;
- níveis de serviço;
- horários de suporte;
- impactos de indisponibilidade;
- pontos de escalonamento.

---

### 5. Indicadores

Verificar se a operação possui dados suficientes para gestão.

Exemplos:

- volume de chamados;
- backlog;
- cumprimento de SLA;
- satisfação;
- disponibilidade;
- incidentes recorrentes;
- produtividade;
- tempo de atendimento;
- tempo de resolução;
- MTTD;
- MTTA;
- MTTR;
- MTBF;
- capacidade;
- falhas recorrentes.

O diagnóstico deve avaliar não apenas a existência do indicador, mas também:

- definição;
- qualidade dos dados;
- fonte;
- periodicidade;
- responsável;
- meta ou referência;
- interpretação;
- utilização na tomada de decisão.

---

### 6. Governança e controles

Avaliar a existência de mecanismos formais de gestão.

Exemplos:

- políticas;
- procedimentos;
- responsabilidades;
- matriz RACI;
- gestão de riscos;
- reuniões de acompanhamento;
- planos de ação;
- auditorias;
- gestão de fornecedores;
- SLA e OLA;
- registros de decisão;
- melhoria contínua.

---

### 7. Riscos

Identificar situações que possam comprometer a continuidade ou a qualidade dos serviços.

Exemplos:

- ponto único de falha;
- ausência de backup;
- equipamentos sem redundância;
- conhecimento concentrado;
- ativo sem suporte;
- falta de documentação;
- ausência de monitoramento;
- acessos excessivos;
- dependência de fornecedor;
- capacidade próxima do limite;
- processos críticos sem responsável definido.

---

## Estrutura sugerida

```text
00-diagnostico-e-planejamento/
│
├── README.md
├── diagnostico-operacao-ti/
├── assessment-inicial/
├── levantamento-de-riscos/
├── mapa-de-gaps/
├── matriz-de-priorizacao/
├── plano-de-acao/
├── roadmap/
└── evidencias/
```

---

## Ferramentas e artefatos

### Diagnóstico da operação

Documento ou ferramenta destinada a levantar informações sobre:

- equipe;
- processos;
- infraestrutura;
- ferramentas;
- serviços;
- indicadores;
- riscos;
- controles.

---

### Assessment inicial

Checklist estruturado para realizar uma primeira leitura da operação.

Uma escala simples de maturidade pode utilizar respostas como:

```text
0 — Não existe
1 — Existe informalmente
2 — Existe parcialmente
3 — Existe e é executado
4 — Existe, é controlado e medido
5 — Existe, é medido e melhorado continuamente
```

---

### Mapa de gaps

Registro das diferenças entre o estado atual e o estado desejado.

| Tema | Estado atual | Estado desejado | Gap |
|---|---|---|---|
| Monitoramento | Parcial | Serviços críticos monitorados | Cobertura insuficiente |
| Inventário | Desatualizado | Inventário confiável | Falta de processo de atualização |
| SLA | Não acompanhado | Indicadores periódicos | Ausência de medição |

---

### Matriz de riscos

Estrutura mínima sugerida:

| Risco | Probabilidade | Impacto | Nível | Tratamento |
|---|---|---|---|---|
| Falha de componente crítico sem redundância | Alta | Alto | Crítico | Mitigar |
| Inventário desatualizado | Média | Médio | Moderado | Tratar |
| Conhecimento concentrado | Alta | Alto | Crítico | Documentar e capacitar |

---

### Matriz de priorização

As melhorias podem ser avaliadas considerando:

- impacto;
- urgência;
- risco;
- esforço;
- custo;
- dependências;
- benefício esperado.

Uma abordagem simples:

```text
Alta prioridade
    = alto impacto + alta urgência + risco relevante

Média prioridade
    = impacto relevante, mas com menor urgência

Baixa prioridade
    = melhoria desejável, mas sem impacto imediato
```

---

## Plano de ação

Todo item priorizado deve gerar uma ação clara.

Estrutura recomendada:

| Ação | Responsável | Prioridade | Prazo | Status | Evidência |
|---|---|---|---|---|---|
| Implantar monitoramento do serviço crítico | Equipe responsável | Alta | 30 dias | Em andamento | Dashboard |
| Atualizar inventário | Gestão de ativos | Média | 60 dias | Planejado | Base atualizada |

Sempre que possível, utilizar ações:

- específicas;
- mensuráveis;
- atribuídas;
- priorizadas;
- com prazo;
- com evidência de conclusão.

---

## Roadmap

O roadmap transforma ações isoladas em uma sequência coerente de evolução.

Exemplo:

```text
0–30 dias
├── corrigir riscos críticos;
├── estabelecer linha de base;
└── definir responsáveis.

31–90 dias
├── formalizar processos prioritários;
├── estruturar indicadores;
└── melhorar monitoramento.

3–6 meses
├── automatizar atividades;
├── ampliar documentação;
└── evoluir gestão de ativos.

6–12 meses
├── consolidar governança;
├── revisar maturidade;
└── iniciar novo ciclo de melhoria.
```

---

## Evidências

O diagnóstico deve ser sustentado por evidências sempre que possível.

Exemplos:

- relatórios;
- dashboards;
- exportações;
- screenshots;
- inventários;
- logs;
- procedimentos;
- atas;
- contratos;
- registros de chamados;
- entrevistas;
- observação da operação.

A evidência ajuda a reduzir avaliações baseadas apenas em percepção.

---

## Perguntas orientadoras

Algumas perguntas que podem ser utilizadas durante o diagnóstico:

### Operação

- Quais são os principais serviços entregues?
- Quais serviços são críticos?
- Qual é o volume mensal de demandas?
- Existe backlog?
- Quais são os principais motivos de incidentes?
- Existem incidentes recorrentes?

### Pessoas

- Quem é responsável por cada atividade?
- Há dependência excessiva de uma única pessoa?
- Existe cobertura adequada?
- A equipe possui conhecimento documentado?

### Processos

- Os processos estão documentados?
- Existem critérios claros de prioridade?
- Há escalonamento definido?
- Mudanças são controladas?
- Problemas recorrentes são investigados?

### Tecnologia

- Os ativos estão inventariados?
- Existe monitoramento?
- Existem backups testados?
- Há redundância nos componentes críticos?
- Existem ativos sem suporte?

### Gestão

- Existem indicadores?
- Existem metas?
- Os resultados são analisados?
- Existem reuniões periódicas?
- Os riscos são registrados?
- Os planos de ação são acompanhados?

---

## Critérios de avaliação

O diagnóstico deve evitar classificações baseadas exclusivamente em opinião.

Sempre que possível, considerar:

```text
Existência
Formalização
Execução
Controle
Medição
Evidência
Melhoria
```

Exemplo:

| Nível | Situação |
|---|---|
| 0 | Não existe |
| 1 | Prática informal |
| 2 | Parcialmente definida |
| 3 | Definida e executada |
| 4 | Controlada e medida |
| 5 | Otimizada e melhorada continuamente |

---

## Saídas esperadas

Ao final do diagnóstico, recomenda-se possuir pelo menos:

- visão geral da operação;
- pontos fortes;
- principais gaps;
- riscos relevantes;
- oportunidades de melhoria;
- ações prioritárias;
- responsáveis;
- prazos;
- roadmap;
- indicadores para acompanhar a evolução.

---

## Ciclo de melhoria

O diagnóstico não deve ser uma atividade única.

Ele pode ser repetido periodicamente para comparar a evolução:

```text
Diagnóstico inicial
      ↓
Plano de melhoria
      ↓
Implementação
      ↓
Medição
      ↓
Novo diagnóstico
      ↓
Comparação da maturidade
      ↓
Novo ciclo de melhoria
```


---

## Resultado esperado

Uma operação diagnosticada de forma estruturada, com riscos e gaps identificados, prioridades definidas e um **plano de evolução claro, mensurável e acompanhável**.
