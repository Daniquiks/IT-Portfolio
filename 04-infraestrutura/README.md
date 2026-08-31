# 04 — Infraestrutura

Este diretório reúne práticas, padrões, controles, modelos e referências voltados à **infraestrutura de TI que sustenta os serviços e operações da organização**.

A proposta é organizar os principais domínios de infraestrutura de forma estruturada, permitindo documentar, padronizar, monitorar e evoluir o ambiente tecnológico com foco em disponibilidade, capacidade, segurança, continuidade e manutenibilidade.

---

## Objetivo

Apoiar a gestão técnica da infraestrutura de TI, permitindo:

- conhecer o ambiente existente;
- reduzir riscos operacionais;
- padronizar configurações;
- documentar componentes críticos;
- melhorar disponibilidade;
- acompanhar capacidade;
- reduzir pontos únicos de falha;
- estruturar redundância;
- melhorar segurança;
- apoiar continuidade;
- organizar manutenção e renovação;
- facilitar troubleshooting;
- gerar evidências para auditoria e governança.

O resultado esperado é uma infraestrutura **conhecida, documentada, controlada, monitorada e sustentável**.

---

## Princípio

A infraestrutura deve ser tratada como base de sustentação dos serviços.

Uma operação madura deve conseguir responder:

> **Quais componentes sustentam cada serviço, qual é o estado deles, quais riscos existem e o que acontece se um deles falhar?**

Fluxo simplificado:

```text
Inventariar
    ↓
Documentar
    ↓
Padronizar
    ↓
Monitorar
    ↓
Proteger
    ↓
Manter
    ↓
Medir
    ↓
Planejar capacidade
    ↓
Renovar e melhorar
```

---

## Estrutura sugerida

```text
04-infraestrutura/
│
├── README.md
├── redes/
├── servidores/
├── virtualizacao/
├── datacenter/
├── storage/
├── backup/
├── cloud/
├── sistemas-operacionais/
├── energia-e-climatizacao/
├── cabeamento/
├── seguranca/
├── capacidade/
├── continuidade/
├── documentacao/
└── padroes/
```

---

# 1. Redes

A infraestrutura de rede deve garantir conectividade, desempenho, segmentação, disponibilidade e segurança.

## Escopo

- switches;
- roteadores;
- firewalls;
- access points;
- controladoras;
- links;
- VLANs;
- roteamento;
- DNS;
- DHCP;
- VPN;
- ACLs;
- Wi-Fi;
- cabeamento estruturado;
- endereçamento IP.

---

## Informações recomendadas

Para cada equipamento de rede, registrar:

- hostname;
- fabricante;
- modelo;
- serial;
- patrimônio;
- localização;
- endereço IP de gerenciamento;
- firmware;
- função;
- status;
- uplinks;
- interfaces principais;
- VLANs;
- garantia;
- responsável.

---

## Documentação lógica

Deve ser possível compreender:

```text
Internet / WAN
      ↓
Firewall
      ↓
Core
      ↓
Distribuição
      ↓
Acesso
      ↓
Usuários / Servidores / APs
```

Documentos úteis:

- diagrama lógico;
- diagrama físico;
- mapa de VLANs;
- plano de endereçamento;
- lista de links;
- matriz de portas;
- documentação de ACLs;
- inventário de equipamentos.

---

# 2. Switching

Os switches devem seguir padrões de configuração e gerenciamento.

## Controles recomendados

- hostname padronizado;
- IP de gerenciamento;
- VLAN de gerenciamento;
- NTP;
- SNMP;
- syslog;
- autenticação;
- ACL de gerenciamento;
- firmware controlado;
- portas documentadas;
- portas não utilizadas desabilitadas;
- backup de configuração.

---

## Stack e redundância

Quando houver stack ou equipamentos redundantes, documentar:

- membros;
- prioridade;
- versão;
- enlaces;
- comportamento em falha;
- alimentação;
- uplinks redundantes.

---

# 3. Wi-Fi

A rede sem fio deve ser tratada como parte da infraestrutura corporativa.

Avaliar:

- cobertura;
- interferência;
- capacidade;
- canais;
- potência;
- autenticação;
- segmentação;
- roaming;
- densidade;
- quantidade de clientes.

## Informações úteis

- SSID;
- finalidade;
- VLAN associada;
- autenticação;
- localização dos APs;
- modelo;
- firmware;
- canal;
- potência;
- quantidade de clientes.

---

# 4. Servidores

Os servidores devem possuir configuração, responsabilidade e criticidade conhecidas.

## Registrar

- hostname;
- IP;
- fabricante/modelo;
- físico ou virtual;
- sistema operacional;
- versão;
- função;
- serviços executados;
- CPU;
- memória;
- armazenamento;
- localização;
- criticidade;
- backup;
- monitoramento;
- responsável;
- suporte;
- garantia.

---

## Classificação

Uma classificação pode considerar:

```text
Produção
Homologação
Desenvolvimento
Infraestrutura
Gerenciamento
Backup
```

Também deve ser definida a criticidade:

```text
Baixa
Média
Alta
Crítica
```

---

# 5. Sistemas Operacionais

A gestão dos sistemas operacionais deve considerar:

- versão;
- ciclo de vida;
- atualizações;
- hardening;
- antivírus/EDR;
- logs;
- serviços;
- contas;
- acesso remoto;
- monitoramento.

## Controles

- patching periódico;
- remoção de software desnecessário;
- atualização de agentes;
- revisão de serviços;
- contas administrativas controladas;
- horário e NTP corretos;
- logs centralizados quando aplicável.

---

# 6. Virtualização

Ambientes virtualizados devem ser documentados tanto no nível físico quanto lógico.

## Itens

- hosts;
- clusters;
- hypervisors;
- VMs;
- redes virtuais;
- storage;
- snapshots;
- replicação;
- alta disponibilidade;
- capacidade.

---

## Perguntas

- Existe cluster?
- Há redundância de host?
- Qual a capacidade disponível?
- Existe overcommit?
- Como ocorre recuperação de uma VM?
- Existe replicação?
- Snapshots possuem controle?
- Há dependência de um único datastore?

---

# 7. Storage

O armazenamento deve ser acompanhado quanto a:

- capacidade;
- desempenho;
- redundância;
- saúde;
- crescimento;
- conectividade;
- disponibilidade.

## Indicadores

- espaço utilizado;
- espaço livre;
- IOPS;
- latência;
- throughput;
- crescimento;
- falhas de disco;
- estado de RAID.

---

## Capacidade

Exemplo:

```text
Capacidade total: 20 TB
Utilizado: 16 TB
Livre: 4 TB
Utilização: 80%
```

Além do valor atual, acompanhar tendência de crescimento.

---

# 8. Backup

Backup deve ser tratado como processo de continuidade, não apenas como tarefa automática.

## Deve ser conhecido

- o que é protegido;
- frequência;
- retenção;
- destino;
- responsável;
- criptografia;
- cópia externa;
- resultado;
- procedimento de restauração.

---

## Regra importante

> **Backup sem teste de restauração não comprova capacidade de recuperação.**

---

## Checklist

```text
[ ] Job executado
[ ] Dados protegidos
[ ] Retenção correta
[ ] Destino disponível
[ ] Erros analisados
[ ] Restauração testada
[ ] Evidência registrada
```

---

# 9. Continuidade e Recuperação

A infraestrutura deve considerar cenários de falha.

Exemplos:

- falha de servidor;
- falha de storage;
- perda de link;
- falha elétrica;
- indisponibilidade de datacenter;
- perda de equipamento;
- falha de sistema operacional.

---

## Conceitos relevantes

### RTO — Recovery Time Objective

Tempo máximo esperado para restaurar o serviço.

### RPO — Recovery Point Objective

Quantidade máxima aceitável de perda de dados.

Exemplo:

```text
RTO = 4 horas
RPO = 1 hora
```

---

# 10. Datacenter

O ambiente físico deve possuir condições adequadas para suportar os equipamentos.

## Avaliar

- acesso;
- racks;
- organização;
- cabeamento;
- energia;
- UPS;
- climatização;
- temperatura;
- umidade;
- incêndio;
- limpeza;
- identificação;
- segurança física.

---

## Rack

Verificar:

- fixação;
- organização;
- patch panels;
- identificação;
- espaço disponível;
- ventilação;
- distribuição elétrica;
- cabos;
- equipamentos apoiados incorretamente.

---

## Boas práticas

- identificar cabos;
- utilizar patch panels;
- separar energia e dados quando possível;
- utilizar organizadores;
- evitar cabos tensionados;
- manter espaço para ventilação;
- documentar portas e conexões.

---

# 11. Energia

A infraestrutura elétrica deve suportar os equipamentos críticos.

## Avaliar

- circuitos;
- carga;
- UPS;
- autonomia;
- gerador;
- aterramento;
- redundância;
- PDU;
- proteção contra surtos.

---

## Perguntas

- Qual a autonomia do UPS?
- Existe gerador?
- Equipamentos críticos possuem fontes redundantes?
- As fontes redundantes estão ligadas em circuitos diferentes?
- Existe monitoramento da energia?

---

# 12. Climatização

Equipamentos de TI dependem de temperatura adequada.

Monitorar:

- temperatura;
- umidade;
- funcionamento dos equipamentos;
- redundância;
- manutenção;
- fluxo de ar.

Evitar:

- bloqueio de ventilação;
- racks fechados sem circulação;
- equipamentos próximos a fontes de calor;
- ausência de monitoramento térmico.

---

# 13. Cabeamento Estruturado

O cabeamento deve permitir manutenção, rastreabilidade e expansão.

## Registrar

- origem;
- destino;
- patch panel;
- porta do switch;
- ponto lógico;
- categoria;
- identificação.

---

## Problemas comuns

- cabos sem etiqueta;
- cabos diretamente conectados sem organização;
- excesso de comprimento;
- cabos danificados;
- categoria inadequada;
- ausência de patch panel.

---

# 14. Cloud

Ambientes em nuvem devem ser tratados com o mesmo rigor de infraestrutura física.

## Avaliar

- contas/subscriptions;
- regiões;
- redes;
- máquinas;
- storage;
- backups;
- identidade;
- permissões;
- logs;
- custos;
- segurança;
- disponibilidade.

---

## Controles

- menor privilégio;
- MFA;
- tagging;
- orçamento;
- logs;
- backups;
- criptografia;
- revisão de acessos;
- políticas;
- inventário.

---

# 15. Segurança de Infraestrutura

A infraestrutura deve aplicar controles técnicos adequados.

Exemplos:

- segmentação;
- firewall;
- ACL;
- hardening;
- patching;
- autenticação;
- MFA;
- criptografia;
- logging;
- backup;
- gestão de vulnerabilidades.

---

## Gerenciamento

Interfaces de administração não devem ficar desnecessariamente expostas.

Avaliar:

- origem permitida;
- protocolo;
- autenticação;
- logging;
- segregação;
- VPN;
- VLAN de gerenciamento.

---

# 16. Gestão de Vulnerabilidades

A infraestrutura deve possuir mecanismo de identificação e tratamento de vulnerabilidades.

Fluxo:

```text
Identificação
    ↓
Classificação
    ↓
Priorização
    ↓
Correção
    ↓
Validação
    ↓
Encerramento
```

Considerar:

- criticidade;
- exposição;
- exploração conhecida;
- importância do ativo;
- impacto da correção.

---

# 17. Patching

Atualizações devem ser controladas.

## Processo

```text
Atualização disponível
      ↓
Análise
      ↓
Teste
      ↓
Aprovação
      ↓
Implementação
      ↓
Validação
```

Registrar:

- versão anterior;
- versão nova;
- ativo;
- responsável;
- data;
- impacto;
- resultado.

---

# 18. Firmware

Equipamentos de infraestrutura também precisam de gestão de firmware.

Exemplos:

- switches;
- firewalls;
- APs;
- storage;
- servidores;
- controladoras.

Evitar:

- versões obsoletas;
- atualizações sem backup;
- salto de versão não suportado;
- firmware sem validação de compatibilidade.

---

# 19. Capacidade

Capacidade deve ser analisada antes de se tornar incidente.

## Recursos

- CPU;
- memória;
- disco;
- storage;
- largura de banda;
- portas;
- rack;
- energia;
- licenças.

---

## Tendência

Exemplo:

```text
Utilização do link

Janeiro:   45%
Fevereiro: 52%
Março:     64%
Abril:     73%
```

A tendência pode justificar expansão antes da saturação.

---

# 20. Disponibilidade

Infraestrutura crítica deve possuir requisitos claros de disponibilidade.

Avaliar:

- redundância;
- MTBF;
- falhas;
- manutenção;
- dependências;
- contingência.

---

## Exemplo

```text
Serviço crítico
│
├── 2 servidores
├── storage redundante
├── 2 switches
├── 2 links
└── UPS
```

A redundância deve ser real e testada.

---

# 21. Ponto Único de Falha

Um **Single Point of Failure (SPOF)** é um componente cuja falha interrompe todo o serviço.

Exemplos:

- único switch;
- único link;
- único servidor;
- único storage;
- única fonte elétrica.

Todo SPOF relevante deve ser:

```text
Identificado
    ↓
Avaliado
    ↓
Aceito ou tratado
```

---

# 22. Manutenção Preventiva

Atividades preventivas podem incluir:

- atualização;
- limpeza;
- revisão de logs;
- testes de backup;
- teste de redundância;
- análise de capacidade;
- inspeção física;
- revisão de cabos;
- atualização de documentação.

---

# 23. Ciclo de Vida

Todo ativo deve possuir um ciclo de vida conhecido.

```text
Planejamento
    ↓
Aquisição
    ↓
Implantação
    ↓
Operação
    ↓
Manutenção
    ↓
Renovação
    ↓
Descarte
```

Avaliar:

- fim de garantia;
- End of Sale;
- End of Support;
- compatibilidade;
- custo de manutenção;
- risco.

---

# 24. Padronização

Padronização reduz complexidade operacional.

Exemplos:

- nomenclatura;
- modelos homologados;
- versões;
- configuração base;
- endereçamento;
- documentação;
- procedimentos.

---

## Exemplo de hostname

```text
TIPO-LOCAL-NUMERO

SW-PFO-01
SRV-POA-02
AP-BGE-03
```

O padrão deve ser definido conforme a organização.

---

# 25. Documentação Técnica

Documentar o ambiente reduz dependência de conhecimento informal.

Documentos úteis:

- diagrama de rede;
- inventário;
- mapa de rack;
- plano de IP;
- VLANs;
- serviços;
- dependências;
- procedimentos;
- configurações;
- contatos;
- contratos.

---

## Regra

A documentação deve acompanhar a mudança.

```text
Alteração técnica
      ↓
Validação
      ↓
Atualização da documentação
```

---

# 26. Monitoramento

Infraestrutura crítica deve possuir monitoramento adequado.

Exemplos:

- disponibilidade;
- CPU;
- memória;
- disco;
- temperatura;
- interfaces;
- erros;
- energia;
- storage;
- serviços.

Relacionar este conteúdo com:

```text
03-monitoramento-e-observabilidade/
```

---

# 27. Indicadores

Indicadores possíveis:

### Disponibilidade

- disponibilidade por equipamento;
- disponibilidade por serviço;
- quantidade de indisponibilidades.

### Capacidade

- utilização média;
- ativos acima de threshold;
- crescimento.

### Manutenção

- ativos atualizados;
- firmware desatualizado;
- patches pendentes.

### Backup

- taxa de sucesso;
- falhas;
- testes de restauração.

### Ativos

- ativos sem suporte;
- ativos próximos do fim de garantia.

---

# 28. Critérios de Maturidade

| Nível | Situação |
|---|---|
| 0 | Ambiente desconhecido |
| 1 | Conhecimento informal |
| 2 | Inventário/documentação parcial |
| 3 | Infraestrutura padronizada e monitorada |
| 4 | Capacidade, risco e disponibilidade controlados |
| 5 | Infraestrutura otimizada, automatizada e continuamente melhorada |

Avaliar:

- documentação;
- inventário;
- padronização;
- monitoramento;
- capacidade;
- segurança;
- continuidade;
- automação;
- melhoria.

---

# 29. Perguntas Orientadoras

## Redes

- A topologia está documentada?
- Existem equipamentos sem gerenciamento?
- Há redundância?
- As VLANs estão documentadas?
- Existem ACLs de gerenciamento?

## Servidores

- Todos possuem responsável?
- Sistemas estão suportados?
- Backups estão configurados?
- O patching está atualizado?

## Datacenter

- Os racks estão organizados?
- A climatização é suficiente?
- Existe controle de acesso?
- Há autonomia elétrica?

## Continuidade

- Existe backup?
- A restauração é testada?
- Existem SPOFs?
- Existe contingência?

## Capacidade

- Quais recursos estão próximos do limite?
- Existe tendência de crescimento?
- Existe plano de expansão?

---

# 30. Entregáveis Esperados

Este domínio pode produzir:

- inventário técnico;
- diagramas;
- padrões de configuração;
- documentação de rede;
- mapas de rack;
- plano de endereçamento;
- matriz de capacidade;
- matriz de criticidade;
- mapa de SPOFs;
- plano de atualização;
- plano de renovação;
- procedimentos;
- checklists;
- relatórios de disponibilidade;
- relatórios de capacidade;
- planos de continuidade.

---

# Relação com o IT Portfolio

- **00 — Diagnóstico e Planejamento** identifica riscos e gaps;
- **01 — Governança e Gestão** define controles e responsabilidades;
- **02 — Operação e Serviços** utiliza a infraestrutura para entregar serviços;
- **03 — Monitoramento e Observabilidade** acompanha disponibilidade e desempenho;
- **05 — Ativos e Configuração** mantém inventário e relacionamentos;
- **06 — Automação e Integrações** automatiza atividades de infraestrutura;
- **07 — Governança de IA** pode apoiar controles relacionados à infraestrutura utilizada por soluções de IA.

---

# Resultado esperado

Uma infraestrutura de TI **documentada, padronizada, segura, monitorada e preparada para suportar os serviços com níveis adequados de disponibilidade, capacidade, continuidade e confiabilidade**.
