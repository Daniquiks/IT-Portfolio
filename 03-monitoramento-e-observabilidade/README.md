# 03 — Monitoramento e Observabilidade

Este diretório reúne práticas, ferramentas, métricas, modelos e referências voltados ao **monitoramento, à observabilidade e à confiabilidade dos serviços de TI**.

A proposta é permitir que a operação identifique falhas com rapidez, compreenda o comportamento do ambiente, reduza o tempo de resposta e restauração e utilize dados técnicos para apoiar decisões operacionais e gerenciais.

---

## Objetivo

Apoiar a construção de uma operação capaz de:

- detectar indisponibilidades e degradações;
- identificar sintomas antes de impactos maiores;
- reduzir tempo de detecção;
- reduzir tempo de reconhecimento;
- reduzir tempo de restauração;
- acompanhar disponibilidade;
- acompanhar capacidade e saturação;
- correlacionar eventos;
- melhorar qualidade dos alertas;
- apoiar troubleshooting;
- produzir dados para gestão e melhoria contínua.

O resultado esperado é uma operação mais **proativa, observável, confiável e orientada por evidências**.

---

## Princípio

Monitoramento responde principalmente:

> **Algo está funcionando ou falhou?**

Observabilidade busca responder:

> **Por que o sistema está se comportando dessa forma?**

Uma operação madura deve evoluir de uma visão puramente reativa para uma visão que combine:

```text
Métricas
   +
Logs
   +
Eventos
   +
Alertas
   +
Contexto
   +
Correlação
   ↓
Entendimento do serviço
   ↓
Ação operacional
```

---

## Estrutura sugerida

```text
03-monitoramento-e-observabilidade/
│
├── README.md
├── zabbix/
├── alertas/
├── dashboards/
├── disponibilidade/
├── capacidade/
├── eventos/
├── logs/
├── metricas-mt/
├── sre/
├── observabilidade/
├── thresholds/
├── escalonamento/
├── relatorios/
└── melhoria-continua/
```

---

## 1. Monitoramento

O monitoramento deve acompanhar componentes e serviços relevantes para a operação.

Exemplos:

- servidores;
- switches;
- roteadores;
- links;
- storage;
- máquinas virtuais;
- aplicações;
- serviços Windows/Linux;
- bancos de dados;
- filas;
- certificados;
- espaço em disco;
- CPU;
- memória;
- latência;
- disponibilidade de portas;
- processos;
- backups.

O foco não deve ser monitorar tudo indiscriminadamente, mas monitorar o que realmente possui valor operacional.

---

## 2. Observabilidade

Observabilidade é a capacidade de compreender o estado interno de um sistema a partir de sinais externos.

Os principais pilares são:

### Métricas

Valores numéricos coletados ao longo do tempo.

Exemplos:

- CPU;
- memória;
- latência;
- erros;
- throughput;
- utilização;
- fila;
- sessões;
- disponibilidade.

### Logs

Registros detalhados de eventos e comportamentos do sistema.

Podem apoiar:

- troubleshooting;
- auditoria;
- investigação;
- correlação;
- identificação de causa.

### Traces

Rastreamento de uma transação ou requisição entre diferentes componentes.

Especialmente útil em:

- aplicações distribuídas;
- APIs;
- microsserviços;
- integrações.

---

## 3. Monitoramento de Serviços

O monitoramento não deve se limitar a equipamentos.

Sempre que possível, deve existir uma visão orientada ao serviço.

Exemplo:

```text
Serviço de autenticação
│
├── servidor
├── aplicação
├── banco de dados
├── rede
└── integração externa
```

Uma falha em qualquer componente pode afetar o serviço.

O objetivo é conseguir responder:

- qual serviço foi afetado;
- quais componentes participam dele;
- qual o impacto;
- quais usuários podem ser afetados;
- qual dependência apresentou falha.

---

## 4. Zabbix

O Zabbix pode ser utilizado como plataforma central para:

- coleta de métricas;
- disponibilidade;
- triggers;
- eventos;
- templates;
- dashboards;
- notificações;
- tendências;
- descoberta;
- monitoramento SNMP;
- monitoramento por agente.

### Organização recomendada

```text
zabbix/
├── templates/
├── triggers/
├── discovery/
├── dashboards/
├── itens/
├── documentacao/
└── integracoes/
```

### Boas práticas

- utilizar templates;
- evitar configuração manual repetitiva;
- documentar thresholds;
- utilizar tags;
- definir severidades;
- revisar triggers;
- eliminar alertas sem ação;
- manter nomenclatura padronizada.

---

## 5. Alertas

Um alerta deve representar uma condição que exige atenção ou ação.

Evite transformar qualquer variação de métrica em alerta.

### Um bom alerta deve indicar

- o que aconteceu;
- onde aconteceu;
- severidade;
- impacto provável;
- horário;
- valor atual;
- threshold;
- ação recomendada;
- responsável ou grupo.

Exemplo:

```text
Servidor: SRV-APP-01
Evento: Espaço em disco crítico
Volume: C:
Utilização: 95%
Severidade: Alta
Ação: Verificar consumo e liberar espaço
```

---

## 6. Severidade

Uma classificação possível:

| Severidade | Interpretação |
|---|---|
| Informativa | Evento sem impacto imediato |
| Baixa | Impacto pequeno ou preventivo |
| Média | Degradação relevante |
| Alta | Impacto significativo |
| Crítica | Indisponibilidade ou risco grave |

A severidade técnica pode não ser igual à prioridade do incidente.

A prioridade também deve considerar:

- impacto;
- urgência;
- criticidade do serviço;
- quantidade de usuários;
- horário;
- existência de contingência.

---

## 7. Thresholds

Threshold é o valor utilizado para determinar quando uma condição merece atenção.

Exemplos:

```text
CPU > 90% por 10 minutos
Disco > 85%
Memória disponível < 10%
Latência > 150 ms
Packet loss > 3%
Serviço indisponível por 2 minutos
```

Thresholds devem ser ajustados conforme o comportamento real do ambiente.

Evite:

- limites genéricos para todos os ativos;
- alertas instantâneos para picos curtos;
- thresholds sem justificativa;
- regras que geram alarmes constantes.

---

## 8. Redução de Ruído

Excesso de alertas reduz a eficiência da operação.

Problemas comuns:

- alertas duplicados;
- eventos sem ação;
- severidade exagerada;
- dependências não tratadas;
- thresholds muito sensíveis;
- repetição excessiva.

O objetivo é reduzir **alert fatigue**.

Pergunta importante:

> **Se esse alerta aparecer às 03h, alguém precisa fazer alguma coisa?**

Se a resposta for não, talvez ele deva ser apenas um evento ou métrica.

---

## 9. Dependências e Correlação

Falhas em um único componente podem gerar dezenas de alertas derivados.

Exemplo:

```text
Switch principal indisponível
       ↓
Servidor A indisponível
Servidor B indisponível
Access Point indisponível
Impressora indisponível
```

O ideal é identificar a causa principal e reduzir eventos derivados.

A correlação ajuda a responder:

- qual evento ocorreu primeiro;
- quais eventos são consequência;
- qual componente é causa provável;
- qual serviço está impactado.

---

## 10. Disponibilidade

Disponibilidade mede quanto tempo um serviço permanece disponível dentro de determinado período.

Fórmula conceitual:

```text
Disponibilidade =
Tempo disponível
----------------------- × 100
Tempo total considerado
```

Exemplo:

```text
99,9% de disponibilidade
```

A análise deve considerar:

- período;
- janela de serviço;
- manutenção programada;
- exclusões;
- indisponibilidade total;
- degradação parcial.

---

## 11. Capacidade

Gestão de capacidade busca garantir recursos suficientes para atender demanda atual e futura.

Monitorar:

- CPU;
- memória;
- disco;
- IOPS;
- largura de banda;
- conexões;
- sessões;
- crescimento;
- armazenamento;
- utilização de portas.

### Perguntas

- Qual recurso está próximo do limite?
- Quando o limite pode ser alcançado?
- Existe crescimento constante?
- A capacidade acompanha a demanda?
- É necessário expansão?

---

## 12. Tendências

A análise de tendência permite agir antes da falha.

Exemplo:

```text
Armazenamento

Janeiro   65%
Fevereiro 70%
Março     76%
Abril     82%
```

Mesmo sem alerta crítico, existe uma tendência que exige planejamento.

O monitoramento deve apoiar:

- previsão;
- capacidade;
- orçamento;
- renovação;
- expansão;
- prevenção.

---

## 13. MTTD — Mean Time to Detect

Mede o tempo médio entre o início de uma falha e sua detecção.

```text
Falha
  ↓
[tempo]
  ↓
Detecção
```

Quanto menor, melhor.

### Exemplo

Tempos de detecção:

```text
4 min
6 min
2 min
```

MTTD:

```text
(4 + 6 + 2) / 3 = 4 minutos
```

Um MTTD elevado pode indicar:

- ausência de monitoramento;
- trigger inadequada;
- cobertura insuficiente;
- dependência de usuários reportarem falhas.

---

## 14. MTTA — Mean Time to Acknowledge

Mede o tempo médio entre a geração do alerta e o reconhecimento por alguém da operação.

```text
Alerta
  ↓
[tempo]
  ↓
Reconhecimento
```

Exemplo:

```text
3 min
5 min
1 min
```

MTTA:

```text
3 minutos
```

Pode indicar qualidade de:

- escala;
- notificação;
- NOC;
- responsabilidades;
- escalonamento.

---

## 15. MTTR — Mean Time to Restore

Mede o tempo médio necessário para restaurar o serviço após uma falha.

```text
Falha
  ↓
Detecção
  ↓
Diagnóstico
  ↓
Ação
  ↓
Restauração
```

Exemplo:

```text
25 min
35 min
30 min
```

MTTR:

```text
30 minutos
```

Um MTTR elevado pode indicar:

- troubleshooting demorado;
- ausência de procedimento;
- escalonamento lento;
- falta de conhecimento;
- arquitetura complexa;
- ausência de contingência.

---

## 16. MTBF — Mean Time Between Failures

Mede o tempo médio de funcionamento entre falhas de um componente ou serviço reparável.

Exemplo:

```text
25 dias
30 dias
35 dias
```

MTBF:

```text
30 dias
```

Quanto maior, maior a confiabilidade entre falhas.

---

## 17. MTTF — Mean Time to Failure

Mede o tempo médio até a falha, sendo utilizado principalmente para componentes não reparáveis ou para análise de vida útil.

Pode apoiar:

- renovação;
- manutenção;
- gestão de hardware;
- planejamento de substituição.

---

## 18. Relação entre Métricas MT

Uma visão simplificada:

```text
Falha
  ↓
MTTD
  ↓
Detecção
  ↓
MTTA
  ↓
Reconhecimento
  ↓
Diagnóstico e atuação
  ↓
MTTR
  ↓
Serviço restaurado
```

Já o MTBF observa o intervalo entre falhas.

Essas métricas ajudam a avaliar não apenas tecnologia, mas também:

- monitoramento;
- responsabilidades;
- comunicação;
- processos;
- resiliência;
- confiabilidade;
- capacidade operacional.

---

## 19. Eventos

Nem todo evento precisa gerar alerta.

Exemplos de eventos:

- serviço reiniciado;
- backup concluído;
- interface alterou estado;
- usuário conectado;
- processo iniciado;
- alteração de configuração.

O evento pode ser:

```text
registrado
correlacionado
analisado
descartado
transformado em alerta
```

conforme relevância.

---

## 20. Logs

Logs devem possuir retenção e organização adequadas.

Avaliar:

- origem;
- nível;
- timestamp;
- retenção;
- acesso;
- armazenamento;
- correlação;
- integridade.

Níveis comuns:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Em produção, o nível deve equilibrar:

- visibilidade;
- armazenamento;
- desempenho;
- segurança.

---

## 21. Dashboards

Dashboards devem responder perguntas específicas.

### Dashboard operacional

Pode apresentar:

- disponibilidade atual;
- alertas ativos;
- eventos críticos;
- hosts indisponíveis;
- capacidade;
- serviços degradados.

### Dashboard gerencial

Pode apresentar:

- disponibilidade mensal;
- MTTD;
- MTTA;
- MTTR;
- quantidade de incidentes;
- principais causas;
- tendência;
- cumprimento de metas.

Evite dashboards com muitos dados sem propósito.

---

## 22. SRE

Práticas de **Site Reliability Engineering (SRE)** podem complementar o monitoramento.

Conceitos relevantes:

- SLI;
- SLO;
- error budget;
- confiabilidade;
- automação;
- toil;
- post-mortem;
- engenharia de resiliência.

---

## 23. SLI

**Service Level Indicator** é uma medida do comportamento real de um serviço.

Exemplos:

- disponibilidade;
- latência;
- taxa de sucesso;
- erros.

---

## 24. SLO

**Service Level Objective** define o objetivo esperado para um SLI.

Exemplo:

```text
SLI: disponibilidade

SLO:
99,9% de disponibilidade mensal
```

---

## 25. Error Budget

O error budget representa a margem de indisponibilidade ou erro permitida dentro de um objetivo.

Exemplo conceitual:

```text
SLO = 99,9%

Error Budget = 0,1%
```

Esse conceito ajuda a equilibrar:

- confiabilidade;
- mudanças;
- inovação;
- risco.

---

## 26. Post-mortem

Incidentes relevantes devem gerar aprendizado.

Um post-mortem pode conter:

- resumo;
- impacto;
- duração;
- linha do tempo;
- detecção;
- causa;
- fatores contribuintes;
- resolução;
- lições aprendidas;
- ações preventivas;
- responsáveis;
- prazos.

O foco deve ser aprendizado e melhoria.

---

## 27. Escalonamento

Alertas críticos devem possuir fluxo definido.

Exemplo:

```text
Alerta
  ↓
N1
  ↓
N2
  ↓
N3
  ↓
Gestão
```

O escalonamento pode considerar:

- severidade;
- tempo;
- impacto;
- serviço;
- ausência de reconhecimento.

---

## 28. Integração com ITSM

Uma integração entre monitoramento e ITSM pode permitir:

```text
Zabbix detecta falha
      ↓
Evento é classificado
      ↓
Chamado é criado
      ↓
Equipe é acionada
      ↓
Evento é atualizado
      ↓
Serviço é restaurado
      ↓
Chamado é encerrado
```

Cuidados:

- evitar chamados duplicados;
- correlacionar recuperação;
- definir regras de abertura;
- registrar origem;
- manter rastreabilidade.

---

## 29. Indicadores

Indicadores possíveis:

### Cobertura

- percentual de ativos monitorados;
- percentual de serviços críticos monitorados;
- quantidade de ativos sem monitoramento.

### Alertas

- alertas por período;
- alertas críticos;
- falsos positivos;
- alertas recorrentes;
- alertas sem ação.

### Confiabilidade

- MTTD;
- MTTA;
- MTTR;
- MTBF;
- disponibilidade.

### Capacidade

- ativos próximos do limite;
- crescimento;
- saturação;
- utilização média.

---

## 30. Critérios de Maturidade

| Nível | Situação |
|---|---|
| 0 | Não existe monitoramento |
| 1 | Monitoramento pontual |
| 2 | Cobertura parcial e reativa |
| 3 | Monitoramento padronizado |
| 4 | Monitoramento integrado e medido |
| 5 | Observabilidade, correlação e melhoria contínua |

A avaliação pode considerar:

- cobertura;
- padronização;
- alertas;
- documentação;
- correlação;
- automação;
- métricas;
- integração;
- melhoria.

---

## 31. Perguntas Orientadoras

### Cobertura

- Quais serviços críticos estão monitorados?
- Existem ativos sem monitoramento?
- A cobertura acompanha o inventário?

### Alertas

- Os alertas são acionáveis?
- Existem falsos positivos?
- Há excesso de alertas?
- Severidades estão corretas?

### Resposta

- Quem recebe o alerta?
- Existe escalonamento?
- O tempo de reconhecimento é medido?
- O MTTR é acompanhado?

### Capacidade

- Existem tendências conhecidas?
- Algum recurso está próximo do limite?
- Há previsão de crescimento?

### Gestão

- Existem dashboards?
- Há relatórios periódicos?
- Os dados geram ações?
- Incidentes relevantes geram post-mortem?

---

## 32. Entregáveis Esperados

Este domínio pode produzir:

- matriz de monitoramento;
- inventário de itens monitorados;
- templates;
- triggers;
- dashboards;
- catálogo de alertas;
- matriz de severidade;
- matriz de escalonamento;
- relatórios de disponibilidade;
- relatórios de capacidade;
- indicadores MT;
- post-mortems;
- SLI/SLO;
- planos de melhoria;
- integrações com ITSM.

---

## Resultado esperado

Uma operação capaz de **detectar falhas rapidamente, compreender seu contexto, reduzir tempos de resposta e restauração, acompanhar capacidade e confiabilidade e transformar sinais técnicos em ações operacionais e gerenciais**.
