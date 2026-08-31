# 01 — Governança e Gestão

Este diretório reúne práticas, modelos, controles, indicadores e referências voltados à **governança e à gestão da operação de TI**.

A proposta é estruturar mecanismos que permitam orientar, supervisionar e controlar a operação de forma consistente, garantindo alinhamento entre serviços, responsabilidades, riscos, desempenho, fornecedores e objetivos organizacionais.

---

## Objetivo

Apoiar a construção de uma operação de TI com:

- responsabilidades claras;
- processos definidos;
- riscos conhecidos;
- decisões registradas;
- níveis de serviço acompanhados;
- indicadores confiáveis;
- controles proporcionais;
- planos de ação monitorados;
- melhoria contínua;
- alinhamento com objetivos do negócio.

Governança e gestão devem transformar a operação em um ambiente **previsível, controlado, mensurável e orientado por valor**.

---

## Princípio

A governança responde principalmente a perguntas como:

> **Estamos fazendo as coisas certas, com os controles adequados, riscos conhecidos e responsabilidades definidas?**

A gestão responde a perguntas como:

> **Estamos executando corretamente, acompanhando resultados e corrigindo desvios?**

Fluxo simplificado:

```text
Direcionar
    ↓
Definir responsabilidades
    ↓
Planejar
    ↓
Executar
    ↓
Monitorar
    ↓
Medir
    ↓
Avaliar
    ↓
Corrigir
    ↓
Melhorar continuamente
```

---

## Escopo

Este domínio pode abranger:

- governança de TI;
- gestão de serviços;
- gestão de riscos;
- gestão de fornecedores;
- políticas;
- procedimentos;
- controles internos;
- SLA e OLA;
- matriz RACI;
- gestão de desempenho;
- melhoria contínua;
- conformidade;
- auditoria;
- reuniões de governança;
- registros de decisão;
- planos de ação.

---

## Estrutura sugerida

```text
01-governanca-e-gestao/
│
├── README.md
├── governanca/
├── gestao-de-servicos/
├── riscos/
├── controles/
├── politicas/
├── procedimentos/
├── sla-e-ola/
├── raci/
├── fornecedores/
├── indicadores/
├── reunioes-de-governanca/
├── planos-de-acao/
├── melhoria-continua/
└── auditoria-e-conformidade/
```

---

## 1. Governança de TI

A governança estabelece mecanismos para orientar e supervisionar a utilização da Tecnologia da Informação.

Deve considerar:

- alinhamento estratégico;
- geração de valor;
- riscos;
- recursos;
- desempenho;
- responsabilidades;
- conformidade;
- tomada de decisão.

### Perguntas orientadoras

- Quais objetivos da organização a TI suporta?
- Quais serviços são mais críticos?
- Quem decide sobre prioridades?
- Quais riscos são aceitos?
- Como o desempenho é acompanhado?
- Existem fóruns de decisão?
- As responsabilidades estão formalizadas?
- Os resultados são avaliados periodicamente?

---

## 2. Gestão de Serviços de TI

A gestão de serviços organiza a forma como os serviços são planejados, entregues, suportados e melhorados.

Pode envolver:

- catálogo de serviços;
- incidentes;
- requisições;
- problemas;
- mudanças;
- conhecimento;
- configuração;
- ativos;
- disponibilidade;
- capacidade;
- continuidade;
- níveis de serviço;
- experiência do usuário.

### Artefatos recomendados

- catálogo de serviços;
- matriz de criticidade;
- matriz de prioridade;
- fluxos de atendimento;
- critérios de escalonamento;
- procedimentos;
- indicadores;
- relatórios mensais.

---

## 3. Papéis e Responsabilidades

Uma operação controlada precisa saber claramente:

- quem executa;
- quem aprova;
- quem é consultado;
- quem deve ser informado;
- quem responde pelo resultado.

Uma ferramenta útil é a **matriz RACI**.

| Atividade | Responsável | Aprovador | Consultado | Informado |
|---|---|---|---|---|
| Tratamento de incidente crítico | Operação | Gestor | Especialistas | Áreas impactadas |
| Aprovação de mudança | Equipe técnica | Gestor/CAB | Segurança | Usuários afetados |
| Atualização de inventário | Gestão de ativos | Gestor | Infraestrutura | Auditoria |

---

## 4. Gestão de Riscos

Riscos devem ser identificados, avaliados, tratados e acompanhados.

### Estrutura mínima

| Risco | Probabilidade | Impacto | Nível | Tratamento | Responsável |
|---|---|---|---|---|---|
| Falha de componente crítico | Alta | Alto | Crítico | Mitigar | Infraestrutura |
| Dependência de conhecimento individual | Média | Alto | Alto | Reduzir | Gestão |
| Inventário desatualizado | Média | Médio | Moderado | Tratar | Ativos |

### Estratégias de tratamento

- evitar;
- mitigar;
- transferir;
- aceitar.

Todo risco relevante deve possuir:

- descrição;
- causa;
- impacto;
- probabilidade;
- nível;
- tratamento;
- responsável;
- prazo;
- status.

---

## 5. Políticas e Procedimentos

Políticas definem princípios e regras.

Procedimentos descrevem como as atividades devem ser executadas.

### Exemplos de políticas

- política de backup;
- política de acesso;
- política de mudanças;
- política de ativos;
- política de segurança;
- política de retenção de logs.

### Exemplos de procedimentos

- tratamento de incidente crítico;
- criação de usuário;
- restauração de backup;
- substituição de equipamento;
- escalonamento de chamados;
- atualização de inventário.

---

## 6. Controles Operacionais

Controles ajudam a garantir que atividades críticas sejam executadas de forma consistente.

Exemplos:

- dupla validação;
- aprovação prévia;
- registro obrigatório;
- checklist;
- segregação de funções;
- logs;
- reconciliação;
- auditoria;
- revisão periódica.

Um controle deve possuir:

- objetivo;
- responsável;
- frequência;
- evidência;
- critério de sucesso;
- tratamento de exceções.

---

## 7. SLA e OLA

### SLA — Service Level Agreement

Define níveis de serviço acordados com clientes ou usuários.

Exemplos:

- prazo de atendimento;
- prazo de resolução;
- disponibilidade;
- tempo de resposta;
- horário de suporte.

### OLA — Operational Level Agreement

Define compromissos internos entre equipes que sustentam o SLA.

Exemplo:

```text
SLA com usuário: resolução em até 8 horas

OLA interno:
N1 → triagem em 30 minutos
N2 → análise em até 2 horas
N3 → atuação técnica em até 4 horas
```

### Boas práticas

- metas claras;
- fórmula definida;
- fonte confiável;
- exclusões documentadas;
- revisão periódica;
- acompanhamento por tendência.

---

## 8. Gestão de Fornecedores

A operação pode depender de contratos e fornecedores externos.

Deve-se acompanhar:

- escopo;
- responsabilidades;
- SLA;
- indicadores;
- penalidades;
- riscos;
- entregas;
- chamados;
- reuniões;
- pendências;
- qualidade.

### Artefatos úteis

- matriz de fornecedores;
- relatório de desempenho;
- registro de não conformidades;
- plano de ação;
- atas de reunião;
- controle de SLA contratual.

---

## 9. Indicadores de Gestão

Indicadores devem apoiar decisões.

Exemplos:

### Operacionais

- volume de chamados;
- backlog;
- tempo médio;
- taxa de resolução;
- taxa de escalonamento.

### Serviço

- SLA;
- disponibilidade;
- satisfação;
- recorrência;
- reabertura.

### Confiabilidade

- MTTD;
- MTTA;
- MTTR;
- MTBF.

### Gestão

- riscos abertos;
- planos de ação vencidos;
- fornecedores fora da meta;
- mudanças com falha;
- auditorias pendentes.

Todo indicador deve possuir:

- definição;
- fórmula;
- fonte;
- periodicidade;
- responsável;
- meta;
- interpretação.

---

## 10. Reuniões de Governança

Reuniões devem gerar decisões e ações, não apenas apresentação de números.

### Agenda sugerida

```text
1. Indicadores
2. Incidentes relevantes
3. Riscos
4. SLA
5. Fornecedores
6. Mudanças importantes
7. Planos de ação
8. Decisões
9. Pendências
```

### Registro mínimo

- data;
- participantes;
- indicadores discutidos;
- decisões;
- responsáveis;
- prazos;
- pendências.

---

## 11. Planos de Ação

Toda não conformidade, risco ou oportunidade relevante pode gerar um plano de ação.

| Ação | Responsável | Prazo | Prioridade | Status | Evidência |
|---|---|---|---|---|---|
| Implantar monitoramento | Infraestrutura | 30 dias | Alta | Em andamento | Dashboard |
| Atualizar procedimento | Governança | 15 dias | Média | Planejado | Documento |
| Revisar SLA | Gestão | 20 dias | Alta | Aberto | Nova versão |

Boas práticas:

- ação específica;
- responsável único;
- prazo definido;
- prioridade;
- evidência;
- status atualizado.

---

## 12. Melhoria Contínua

A melhoria contínua deve transformar dados em ação.

Fluxo:

```text
Medir
    ↓
Identificar desvio
    ↓
Analisar causa
    ↓
Definir ação
    ↓
Implementar
    ↓
Validar resultado
    ↓
Padronizar
```

Fontes de melhoria:

- indicadores;
- auditorias;
- incidentes;
- problemas;
- feedback;
- pesquisas de satisfação;
- riscos;
- fornecedores;
- avaliações de maturidade.

---

## 13. Auditoria e Conformidade

A governança deve garantir evidências suficientes para demonstrar que os controles existem e funcionam.

Exemplos de evidências:

- logs;
- relatórios;
- registros de chamados;
- aprovações;
- atas;
- inventários;
- dashboards;
- procedimentos;
- registros de mudança;
- testes de backup;
- relatórios de acesso.

---

## 14. Critérios de Maturidade

Uma escala simples pode ser utilizada:

| Nível | Situação |
|---|---|
| 0 | Não existe |
| 1 | Informal |
| 2 | Parcialmente definido |
| 3 | Definido e executado |
| 4 | Controlado e medido |
| 5 | Otimizado e melhorado continuamente |

A avaliação deve considerar:

- formalização;
- execução;
- controle;
- medição;
- evidência;
- melhoria.

---

## 15. Perguntas Orientadoras

### Governança

- Existem fóruns de decisão?
- Os objetivos da TI estão alinhados ao negócio?
- Os riscos são conhecidos?
- Existem responsabilidades formalizadas?

### Gestão

- Os processos são acompanhados?
- Existem metas?
- Os desvios geram ações?
- Os indicadores são confiáveis?

### Serviços

- Existe catálogo?
- Os serviços críticos são conhecidos?
- Os níveis de serviço são definidos?
- A experiência do usuário é medida?

### Riscos

- Existe registro formal?
- Há responsável?
- Existe plano de tratamento?
- Os riscos são revisados periodicamente?

### Fornecedores

- O desempenho é medido?
- Existem reuniões periódicas?
- Há controle de SLA?
- Pendências são acompanhadas?

---

## 16. Entregáveis Esperados

Ao longo deste domínio, podem ser produzidos:

- modelo de governança;
- matriz RACI;
- matriz de riscos;
- catálogo de serviços;
- SLA e OLA;
- políticas;
- procedimentos;
- controles;
- dashboards;
- relatórios;
- atas;
- planos de ação;
- avaliação de maturidade;
- plano de melhoria contínua.

---

## Relação com o IT Portfolio

Este domínio recebe insumos do diagnóstico e transforma os achados em controles, responsabilidades e mecanismos de gestão.

Relacionamentos principais:

- **00 — Diagnóstico e Planejamento**: identifica gaps e prioridades;
- **02 — Operação e Serviços**: executa os processos;
- **03 — Monitoramento e Observabilidade**: fornece evidências e alertas;
- **04 — Infraestrutura**: aplica controles técnicos;
- **05 — Ativos e Configuração**: mantém base de ativos;
- **06 — Automação e Integrações**: reduz esforço manual;
- **07 — Dados e Indicadores**: mede desempenho;
- **08 — Governança de IA**: estende os controles para uso de IA.

---

## Resultado esperado

Uma operação com **direcionamento claro, responsabilidades definidas, riscos controlados, processos acompanhados, indicadores confiáveis e ciclos formais de melhoria contínua**.
