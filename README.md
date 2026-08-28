# Information Technology

Repositório técnico destinado a servir como **fonte única de referência para planejamento, estruturação, implementação, operação, controle, avaliação e melhoria da Tecnologia da Informação** em diferentes contextos organizacionais.

A proposta é reunir conhecimento aplicável: políticas, processos, procedimentos, modelos operacionais, controles, indicadores, checklists, templates, configurações, exemplos e critérios de implementação que possam ser reutilizados e adaptados em diferentes ambientes de TI.

---

# Finalidade

Este repositório foi desenvolvido para responder a questões práticas como:

- O que precisa existir em determinada área de TI?
- O que deve ser avaliado antes de uma implementação?
- Quais políticas precisam ser definidas?
- Quais processos e procedimentos precisam existir?
- Quais papéis e responsabilidades precisam ser estabelecidos?
- Quais controles devem ser implementados?
- Quais indicadores devem ser acompanhados?
- Quais documentos precisam ser produzidos?
- Qual nível de estrutura é adequado para determinada organização?
- Como adaptar uma prática para ambientes simples, intermediários ou complexos?
- Como avaliar se o que foi implementado está funcionando?
- Como evoluir a maturidade posteriormente?

O conteúdo deve permitir partir de um cenário inexistente ou pouco estruturado até um modelo operacional documentado, controlado, mensurável e passível de melhoria contínua.

---

# Princípios

## Aplicabilidade

O conteúdo deve possuir utilidade prática e apoiar decisões, planejamento, implementação ou operação.

## Adaptabilidade

Não existe um único modelo adequado para todas as organizações.

As implementações devem considerar fatores como:

- complexidade tecnológica;
- criticidade dos serviços;
- exigências regulatórias;
- maturidade organizacional;
- porte da organização;
- quantidade de usuários;
- recursos disponíveis;
- riscos;
- tamanho da equipe;
- volume operacional.

## Contexto

Uma prática não deve ser implementada apenas porque um framework ou norma a menciona.

A implementação deve considerar a necessidade da organização, seus riscos, sua capacidade operacional e os resultados esperados.

## Escalabilidade

Os modelos devem permitir evolução progressiva, evitando tanto controles insuficientes quanto burocracia desnecessária.

## Padronização

Conteúdos semelhantes devem seguir uma estrutura comum para facilitar consulta, comparação e reutilização.

## Rastreabilidade

Sempre que possível, políticas, controles, processos e recomendações devem indicar os referenciais que os fundamentam.

---

# Ciclo de Implementação

A utilização desta base segue, de forma geral, o seguinte ciclo:

```text
Entender o contexto
        ↓
Realizar diagnóstico
        ↓
Identificar necessidades e riscos
        ↓
Avaliar maturidade
        ↓
Definir prioridades
        ↓
Selecionar o modelo adequado
        ↓
Definir o modelo-alvo
        ↓
Planejar
        ↓
Documentar
        ↓
Implementar
        ↓
Operar
        ↓
Controlar
        ↓
Medir
        ↓
Avaliar
        ↓
Melhorar
```

---

# Estrutura

```text
Information-Technology/
│
├── README.md
│
├── 00-planejamento-e-implementacao/
├── 01-governanca-e-gestao/
├── 02-gestao-de-servicos/
├── 03-arquitetura-e-aplicacoes/
├── 04-infraestrutura/
├── 05-dados/
├── 06-ativos-e-configuracao/
├── 07-monitoramento-e-observabilidade/
├── 08-seguranca-e-continuidade/
└── 90-modelos-e-templates/
```

---

# 00 — Planejamento e Implementação

Reúne métodos e instrumentos utilizados para compreender uma organização, avaliar seu ambiente atual e planejar a implantação ou evolução de capacidades de TI.

```text
00-planejamento-e-implementacao/
├── avaliacao-de-contexto/
├── diagnostico/
├── levantamento-do-ambiente/
├── maturidade/
├── modelos-de-implementacao/
├── modelo-alvo/
├── papeis-e-responsabilidades/
├── priorizacao/
└── roadmap/
```

## Avaliação de Contexto

Identificação das características que influenciam o desenho da estrutura de TI.

Principais fatores:

- complexidade;
- criticidade;
- dependências;
- maturidade;
- obrigações regulatórias;
- porte;
- recursos;
- riscos;
- tamanho da equipe;
- volume operacional.

## Diagnóstico

Avaliação da situação atual e identificação de lacunas entre o ambiente existente e o ambiente desejado.

## Levantamento do Ambiente

Coleta estruturada de informações sobre:

- aplicações;
- arquitetura;
- ativos;
- contratos;
- dados;
- documentação;
- infraestrutura;
- pessoas;
- processos;
- serviços;
- sistemas;
- tecnologias.

## Maturidade

Avaliação do nível atual de estruturação de uma capacidade e definição dos próximos níveis de evolução.

## Modelos de Implementação

As capacidades poderão possuir diferentes níveis de implementação.

### Essencial

Modelo simplificado, com controles mínimos necessários para proporcionar organização e rastreabilidade.

Normalmente adequado a ambientes:

- com baixa complexidade;
- com baixo volume operacional;
- com equipes pequenas;
- com estrutura hierárquica simples.

### Intermediário

Modelo com maior formalização, definição de responsabilidades, controles e indicadores.

### Avançado

Modelo voltado a ambientes de maior complexidade, criticidade, escala, regulação ou necessidade de segregação de responsabilidades.

> O porte da organização é apenas um dos critérios para seleção do modelo.

## Modelo-Alvo

Descrição de como determinada capacidade deverá funcionar após sua implementação.

## Papéis e Responsabilidades

Definição de:

- autoridades;
- executores;
- gestores;
- responsáveis;
- segregação de funções.

## Priorização

Critérios para decidir o que deve ser implementado primeiro considerando valor, impacto, esforço, risco e dependências.

## Roadmap

Planejamento da evolução das capacidades ao longo do tempo.

---

# 01 — Governança e Gestão

Reúne estruturas utilizadas para direcionar, controlar, avaliar e acompanhar a Tecnologia da Informação.

```text
01-governanca-e-gestao/
├── conformidade/
├── governanca-de-ia/
├── governanca-de-ti/
├── indicadores-e-desempenho/
├── planejamento-de-ti/
├── politicas-e-diretrizes/
└── riscos-e-controles/
```

## Conformidade

Estruturação dos mecanismos utilizados para identificar, acompanhar e demonstrar atendimento a requisitos internos, contratuais, regulatórios e normativos.

## Governança de Inteligência Artificial

Estruturação da governança necessária para utilização responsável de Inteligência Artificial.

Principais componentes:

- controles;
- gestão de riscos;
- inventário de sistemas de IA;
- monitoramento;
- papéis e responsabilidades;
- políticas;
- prestação de contas;
- supervisão;
- transparência.

## Governança de TI

Estruturação dos mecanismos pelos quais a organização avalia, direciona e acompanha a utilização da Tecnologia da Informação.

Principais componentes:

- alinhamento estratégico;
- direitos decisórios;
- estruturas de governança;
- prestação de contas;
- responsabilidades;
- riscos;
- valor gerado pela TI.

## Indicadores e Desempenho

Definição de mecanismos utilizados para acompanhar resultados e apoiar decisões.

## Planejamento de TI

Abrange:

- objetivos;
- planos;
- prioridades;
- projetos;
- recursos;
- roadmap tecnológico;
- alinhamento organizacional.

## Políticas e Diretrizes

Definição e manutenção dos documentos utilizados para estabelecer princípios, regras, responsabilidades e expectativas organizacionais.

## Riscos e Controles

Identificação, avaliação, tratamento e acompanhamento de riscos relacionados à Tecnologia da Informação.

---

# 02 — Gestão de Serviços

Reúne as capacidades necessárias para planejar, entregar, suportar, controlar e melhorar os serviços de Tecnologia da Informação.

```text
02-gestao-de-servicos/
├── catalogo-de-servicos/
├── gestao-de-incidentes/
├── gestao-de-mudancas/
├── gestao-de-nivel-de-servico/
├── gestao-de-problemas/
├── gestao-de-requisicoes/
├── gestao-do-conhecimento/
├── melhoria-continua/
└── satisfacao-e-experiencia/
```

## Catálogo de Serviços

Estruturação e manutenção das informações sobre os serviços disponibilizados pela TI.

## Gestão de Incidentes

Estruturação da capacidade necessária para restaurar serviços e minimizar impactos decorrentes de interrupções ou degradações.

Pode abranger:

- categorização;
- comunicação;
- escalonamento;
- impacto;
- incidentes críticos;
- indicadores;
- política;
- priorização;
- responsabilidades;
- resolução;
- urgência.

## Gestão de Mudanças

Estruturação dos mecanismos utilizados para avaliar, autorizar, planejar, executar e revisar mudanças.

Pode abranger:

- avaliação de impacto;
- avaliação de risco;
- autoridades de mudança;
- comunicação;
- controles;
- indicadores;
- janelas de mudança;
- plano de implementação;
- plano de retorno;
- política;
- revisão pós-implementação;
- tipos de mudança.

### Exemplos de modelos

#### Essencial

Uma organização com ambiente simples pode adotar:

```text
Solicitação
    ↓
Avaliação técnica
    ↓
Avaliação de impacto e risco
    ↓
Aprovação da chefia ou responsável
    ↓
Agendamento
    ↓
Implementação
    ↓
Validação
    ↓
Encerramento
```

#### Intermediário

Pode estabelecer diferentes autoridades conforme risco, impacto ou tipo de mudança.

#### Avançado

Pode incorporar:

- autoridade colegiada;
- automação;
- CAB quando necessário;
- fluxo específico para emergências;
- maior segregação de responsabilidades;
- múltiplos níveis de autorização.

## Gestão de Nível de Serviço

Estruturação dos compromissos, objetivos e mecanismos utilizados para acompanhar a qualidade dos serviços.

## Gestão de Problemas

Estruturação da identificação e tratamento das causas de incidentes atuais ou potenciais.

Pode abranger:

- análise de causa raiz;
- erros conhecidos;
- prevenção;
- registro de problemas;
- soluções de contorno.

## Gestão de Requisições

Estruturação do recebimento, tratamento e atendimento de solicitações padronizadas.

## Gestão do Conhecimento

Estruturação dos mecanismos para criação, organização, manutenção, compartilhamento e utilização do conhecimento.

## Melhoria Contínua

Identificação, priorização, acompanhamento e avaliação de oportunidades de melhoria.

## Satisfação e Experiência

Avaliação da percepção dos usuários em relação aos serviços prestados.

Pode abranger:

- experiência do usuário;
- pesquisa de satisfação;
- representatividade;
- satisfação do usuário;
- taxa de resposta.

---

# 03 — Arquitetura e Aplicações

Reúne práticas relacionadas à organização, implementação, integração, sustentação e evolução das aplicações.

```text
03-arquitetura-e-aplicacoes/
├── aplicacoes/
│   ├── ambientes/
│   ├── automacao/
│   ├── ciclo-de-vida/
│   ├── configuracao/
│   └── integracoes/
└── arquitetura-de-sistemas/
```

## Aplicações

Abrange a gestão técnica e operacional das aplicações utilizadas pela organização.

### Ambientes

Estruturação e separação de ambientes como:

- desenvolvimento;
- homologação;
- produção;
- testes.

### Automação

Aplicação de scripts e workflows para reduzir atividades manuais e aumentar consistência operacional.

### Ciclo de Vida

Acompanhamento das aplicações desde sua necessidade até sua retirada.

### Configuração

Gestão das configurações necessárias para funcionamento adequado das aplicações.

### Integrações

Estruturação da comunicação entre aplicações e serviços.

Pode abranger:

- APIs;
- autenticação;
- filas;
- integrações entre sistemas;
- JSON;
- mensageria;
- middleware;
- webhooks.

## Arquitetura de Sistemas

Definição da estrutura, componentes, dependências e relações entre aplicações e serviços.

---

# 04 — Infraestrutura

Reúne os componentes físicos e lógicos utilizados para sustentar aplicações, dados e serviços.

```text
04-infraestrutura/
├── alta-disponibilidade/
├── armazenamento/
├── backup-e-recuperacao/
├── datacenter/
├── redes/
├── servidores/
└── virtualizacao/
```

## Alta Disponibilidade

Implementação de mecanismos destinados a reduzir indisponibilidade e pontos únicos de falha.

## Armazenamento

Planejamento e administração dos recursos destinados ao armazenamento de dados.

## Backup e Recuperação

Estruturação de:

- políticas de backup;
- retenção;
- testes de restauração;
- recuperação;
- responsabilidades;
- RPO;
- RTO.

## Datacenter

Planejamento e organização de ambientes destinados à hospedagem de infraestrutura tecnológica.

Pode abranger:

- cabeamento;
- climatização;
- energia;
- organização física;
- racks;
- segurança física.

## Redes

Planejamento, implementação, documentação e operação das redes.

Pode abranger:

- DHCP;
- DNS;
- endereçamento;
- redes sem fio;
- roteamento;
- segmentação;
- switching;
- VLAN.

## Servidores

Planejamento, instalação, configuração, atualização, documentação e operação de servidores.

Pode abranger:

- hardware;
- Linux;
- Windows Server.

## Virtualização

Planejamento e gerenciamento de infraestrutura virtualizada.

---

# 05 — Dados

Reúne práticas relacionadas à organização, armazenamento, administração, proteção e utilização dos dados.

```text
05-dados/
├── administracao/
├── bancos-de-dados/
├── governanca-de-dados/
├── modelagem/
├── protecao-e-recuperacao/
├── qualidade-de-dados/
└── sql/
```

## Administração

Práticas utilizadas para administrar plataformas e serviços de dados.

## Bancos de Dados

Planejamento, implantação, configuração e operação de Sistemas Gerenciadores de Bancos de Dados.

## Governança de Dados

Estruturação das responsabilidades, regras e controles relacionados aos dados.

## Modelagem

Definição das estruturas e relações necessárias para representação adequada das informações.

## Proteção e Recuperação

Mecanismos destinados à segurança, disponibilidade e recuperação dos dados.

## Qualidade de Dados

Controles utilizados para acompanhar:

- completude;
- consistência;
- integridade;
- precisão;
- atualização.

## SQL

Consultas, procedimentos e exemplos relacionados à utilização de SQL.

---

# 06 — Ativos e Configuração

Reúne práticas utilizadas para identificar, registrar, controlar, relacionar e acompanhar recursos tecnológicos.

```text
06-ativos-e-configuracao/
├── cmdb/
├── gestao-de-ativos/
├── gestao-de-configuracao/
├── inventario/
└── netbox/
```

## CMDB

Estruturação e utilização de bases destinadas ao registro de itens de configuração e seus relacionamentos.

## Gestão de Ativos

Controle dos ativos durante seu ciclo de vida.

Pode abranger:

- aquisição;
- descarte;
- garantia;
- hardware;
- licenciamento;
- movimentação;
- propriedade;
- software.

## Gestão de Configuração

Identificação e manutenção das informações necessárias para compreender os componentes utilizados na entrega dos serviços.

## Inventário

Descoberta, identificação, registro e atualização dos recursos tecnológicos.

## NetBox

Aplicação do NetBox para documentação e gestão de informações relacionadas à infraestrutura e aos recursos de rede.

---

# 07 — Monitoramento e Observabilidade

Reúne mecanismos utilizados para acompanhar o estado, desempenho, disponibilidade e comportamento dos ambientes tecnológicos.

```text
07-monitoramento-e-observabilidade/
├── dashboards/
├── disponibilidade/
├── eventos-e-alertas/
├── logs/
├── metricas/
├── monitoramento/
├── observabilidade/
├── sre/
└── zabbix/
```

## Dashboards

Estruturação das informações utilizadas para acompanhamento operacional e gerencial.

## Disponibilidade

Medição e acompanhamento da disponibilidade de componentes e serviços.

## Eventos e Alertas

Definição de mecanismos utilizados para detectar e comunicar condições relevantes.

## Logs

Coleta, armazenamento, consulta e análise de registros produzidos pelos sistemas.

## Métricas

Pode abranger:

- disponibilidade;
- latência;
- MTBF;
- MTTA;
- MTTD;
- MTTF;
- MTTR;
- utilização;
- volume.

## Monitoramento

Implementação do acompanhamento contínuo dos recursos tecnológicos.

## Observabilidade

Estruturação da capacidade de compreender o comportamento interno dos sistemas a partir das informações por eles produzidas.

## SRE

Práticas relacionadas à confiabilidade, disponibilidade, desempenho e resiliência dos serviços.

## Zabbix

Implementação e utilização do Zabbix para monitoramento de infraestrutura, aplicações e serviços.

---

# 08 — Segurança e Continuidade

Reúne práticas utilizadas para proteger recursos tecnológicos e manter a capacidade de operação diante de falhas, incidentes ou interrupções.

```text
08-seguranca-e-continuidade/
├── continuidade/
├── identidade-e-acesso/
├── resposta-a-incidentes/
├── riscos-de-seguranca/
├── seguranca-de-infraestrutura/
└── vulnerabilidades/
```

## Continuidade

Planejamento da manutenção ou recuperação das operações diante de eventos disruptivos.

## Identidade e Acesso

Estruturação dos mecanismos utilizados para controlar quem pode acessar quais recursos.

Pode abranger:

- autenticação;
- autorização;
- contas privilegiadas;
- identidade;
- revisão de acessos;
- segregação de funções.

## Resposta a Incidentes

Estruturação das ações necessárias para identificar, conter, tratar e recuperar ambientes afetados por incidentes de segurança.

## Riscos de Segurança

Identificação, avaliação, tratamento e monitoramento dos riscos relacionados à segurança.

## Segurança de Infraestrutura

Proteção dos componentes de infraestrutura.

Pode abranger:

- endpoints;
- redes;
- servidores;
- serviços;
- sistemas operacionais.

## Vulnerabilidades

Identificação, classificação, priorização, correção e acompanhamento de vulnerabilidades.

---

# 90 — Modelos e Templates

Biblioteca reutilizável de documentos e artefatos destinados a apoiar implementações.

```text
90-modelos-e-templates/
├── checklists/
├── dashboards/
├── fluxos/
├── formularios/
├── matrizes/
├── planos/
├── politicas/
├── procedimentos/
├── raci/
└── roadmaps/
```

## Checklists

Listas utilizadas para diagnóstico, implementação, validação e revisão.

## Dashboards

Modelos de acompanhamento operacional e gerencial.

## Fluxos

Representações de processos e decisões.

## Formulários

Modelos para coleta e registro estruturado de informações.

## Matrizes

Pode incluir:

- impacto × urgência;
- priorização;
- responsabilidades;
- riscos.

## Planos

Pode incluir:

- implantação;
- melhoria;
- recuperação;
- tratamento de riscos.

## Políticas

Modelos reutilizáveis de políticas organizacionais.

## Procedimentos

Modelos para documentação de atividades operacionais.

## RACI

Modelos para definição de responsabilidades.

## Roadmaps

Modelos utilizados para planejamento da evolução das capacidades.

---

# Estrutura Padrão de uma Capacidade

Sempre que aplicável, os conteúdos deverão seguir uma estrutura semelhante:

```text
capacidade/
├── README.md
├── politica/
├── processo/
├── papeis-e-responsabilidades/
├── classificacoes-e-criterios/
├── controles/
├── indicadores/
├── modelos-de-implementacao/
├── procedimentos/
├── templates/
└── referencias/
```

Nem todas as áreas precisarão possuir todos esses elementos.

As pastas devem ser criadas apenas quando houver conteúdo suficiente para justificar sua existência.

---

# Modelos de Implementação

Uma mesma capacidade pode possuir implementações diferentes.

Exemplo:

```text
modelos-de-implementacao/
├── essencial.md
├── intermediario.md
└── avancado.md
```

A escolha deve considerar o contexto da organização.

```text
Complexidade
+
Criticidade
+
Maturidade
+
Porte
+
Regulação
+
Recursos
+
Riscos
+
Tamanho da equipe
+
Volume operacional
        ↓
Modelo de implementação
```

O objetivo é evitar dois extremos:

- implementação insuficiente para os riscos existentes;
- implementação excessivamente burocrática para o ambiente.

---

# Referenciais

Frameworks, métodos e modelos de gestão utilizados como suporte conceitual às implementações são tratados separadamente no repositório:

**Frameworks-and-Methods**

Exemplos:

- Agile
- COBIT
- ITIL
- Kanban
- Lean
- PMBOK
- PRINCE2
- Scrum

O `Information-Technology` utiliza esses referenciais quando necessário, mas permanece organizado pelas **capacidades que precisam ser estruturadas e implementadas**, e não pelo framework que as descreve.

---

# Relação entre os Repositórios

```text
Frameworks-and-Methods
        ↓
Princípios, frameworks, métodos e práticas
        ↓
Information-Technology
        ↓
Planejamento e aplicação no ambiente
        ↓
Projetos específicos
        ↓
Implementação técnica
```

---

# Critério para Inclusão de Conteúdo

Antes de adicionar um conteúdo, deve-se considerar:

> Este material me ajuda a avaliar, planejar, estruturar, implementar, documentar, operar, controlar, medir ou melhorar uma capacidade de Tecnologia da Informação?

Se a resposta for positiva, o conteúdo possui aderência à proposta deste repositório.

---

# Status

Este repositório está em **desenvolvimento contínuo**.

A estrutura será ampliada de forma progressiva conforme novos conteúdos forem desenvolvidos e novas necessidades de implementação forem identificadas.

O objetivo é manter uma base técnica reutilizável, organizada e suficientemente flexível para apoiar diferentes organizações e ambientes de Tecnologia da Informação.
