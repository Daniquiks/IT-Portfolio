# 08 — Continuidade, Backup e Recuperação

Este diretório reúne práticas, modelos, controles, indicadores e referências voltados à **continuidade dos serviços de TI, proteção de dados, backup, restauração e recuperação após falhas ou desastres**.

A proposta é estruturar mecanismos que permitam à organização proteger informações críticas, reduzir impactos operacionais e restabelecer serviços dentro de tempos e níveis de perda aceitáveis.

---

## Objetivo

Apoiar a construção de uma estratégia de continuidade e recuperação capaz de:

- proteger dados e sistemas críticos;
- definir políticas de backup;
- estabelecer RPO e RTO;
- organizar rotinas de backup;
- validar a capacidade real de restauração;
- reduzir risco de perda de dados;
- criar cópias offsite;
- utilizar imutabilidade quando aplicável;
- preparar recuperação contra ransomware;
- definir procedimentos de contingência;
- estruturar Disaster Recovery;
- monitorar jobs e falhas;
- acompanhar indicadores;
- produzir evidências para auditoria e governança.

O resultado esperado é uma operação capaz de **recuperar dados e serviços de forma previsível, testada e alinhada à criticidade do negócio**.

---

## Princípio

Backup não é o objetivo final.

O objetivo é conseguir **recuperar** o que a organização precisa dentro de condições aceitáveis.

Uma estratégia madura deve responder:

> **O que precisa ser protegido, com que frequência, por quanto tempo, onde será armazenado e em quanto tempo precisa ser recuperado?**

Fluxo simplificado:

```text
Identificar serviços e dados críticos
              ↓
Definir criticidade
              ↓
Definir RPO e RTO
              ↓
Criar estratégia de backup
              ↓
Executar backups
              ↓
Monitorar resultados
              ↓
Testar restauração
              ↓
Validar recuperação
              ↓
Revisar e melhorar
```

---

## Estrutura sugerida

```text
08-continuidade-backup-e-recuperacao/
│
├── README.md
├── politica-de-backup/
├── estrategia-de-backup/
├── inventario-de-backups/
├── jobs-e-rotinas/
├── retencao/
├── armazenamento/
├── backup-offsite/
├── imutabilidade/
├── restauracao/
├── testes-de-restauracao/
├── rpo-e-rto/
├── continuidade/
├── disaster-recovery/
├── contingencia/
├── ransomware-recovery/
├── monitoramento/
├── indicadores/
├── auditoria/
└── procedimentos/
```

---

# 1. Política de Backup

A política de backup estabelece regras para proteção e retenção das informações.

Pode definir:

- escopo;
- sistemas protegidos;
- responsabilidades;
- frequência;
- retenção;
- tipos de backup;
- destino;
- criptografia;
- armazenamento externo;
- imutabilidade;
- testes;
- restauração;
- exceções;
- auditoria.

---

## Perguntas orientadoras

- Quais dados devem ser protegidos?
- Qual frequência é necessária?
- Qual retenção é exigida?
- Onde as cópias serão armazenadas?
- Existe cópia fora do ambiente principal?
- Quem é responsável pelo backup?
- Quem pode restaurar?
- Quando os testes são realizados?

---

# 2. Inventário de Backups

A organização deve possuir uma visão clara do que está protegido.

Exemplo:

| Sistema | Tipo | Frequência | Retenção | Destino | Responsável |
|---|---|---|---|---|---|
| ERP | VM + Banco | Diário | 30 dias | Storage Backup | Infraestrutura |
| Fileserver | Arquivos | Diário | 90 dias | Repositório secundário | Infraestrutura |
| Banco crítico | Banco | A cada 1h | 30 dias | Backup dedicado | DBA |

---

## Informações recomendadas

Para cada item protegido, registrar:

- nome;
- serviço relacionado;
- servidor;
- origem;
- tipo de dado;
- criticidade;
- política;
- frequência;
- retenção;
- destino;
- criptografia;
- responsável;
- RPO;
- RTO;
- último teste de restauração.

---

# 3. Criticidade

Nem todos os dados precisam da mesma estratégia.

Uma classificação pode considerar:

```text
Baixa
Média
Alta
Crítica
```

Critérios:

- impacto financeiro;
- impacto operacional;
- impacto legal;
- quantidade de usuários;
- dependência do negócio;
- possibilidade de reconstrução;
- tolerância à perda.

---

# 4. RPO — Recovery Point Objective

RPO representa a quantidade máxima aceitável de perda de dados medida em tempo.

Exemplo:

```text
RPO = 1 hora
```

Isso significa que a organização aceita perder, no máximo, aproximadamente uma hora de dados.

---

## Relação com frequência

Exemplo:

```text
Backup diário
→ RPO potencial de até 24 horas

Backup a cada 1 hora
→ RPO potencial próximo de 1 hora
```

O RPO deve orientar a frequência de proteção.

---

# 5. RTO — Recovery Time Objective

RTO representa o tempo máximo desejado para restabelecer um serviço após uma interrupção.

Exemplo:

```text
RTO = 4 horas
```

A estratégia de recuperação deve ser capaz de atender esse prazo.

---

## Exemplo combinado

```text
Serviço crítico

RPO = 30 minutos
RTO = 2 horas
```

Isso significa:

- perda máxima aceitável de dados: 30 minutos;
- tempo máximo desejado para recuperação: 2 horas.

---

# 6. Relação entre RPO e RTO

```text
Falha ocorre
    ↓
Último ponto recuperável
    ↑
    │ RPO
    │
Falha
    ↓
    │ RTO
    ↓
Serviço restaurado
```

RPO trata de **perda de dados**.

RTO trata de **tempo de recuperação**.

---

# 7. Tipos de Backup

## Backup Completo

Realiza cópia de todos os dados selecionados.

Vantagens:

- restauração mais simples;
- menor dependência de cadeia.

Desvantagens:

- maior tempo;
- maior consumo de armazenamento.

---

## Backup Incremental

Copia apenas alterações desde o último backup realizado.

Vantagens:

- mais rápido;
- menor armazenamento.

Desvantagens:

- restauração pode depender de uma cadeia maior.

---

## Backup Diferencial

Copia alterações desde o último backup completo.

Representa um equilíbrio entre completo e incremental.

---

# 8. Estratégia de Backup

A estratégia deve combinar:

- criticidade;
- volume;
- RPO;
- RTO;
- retenção;
- custo;
- capacidade;
- segurança;
- tempo de restauração.

Exemplo:

```text
Backup completo semanal
        +
Incremental diário
        +
Cópia offsite
        +
Imutabilidade
        +
Teste mensal de restauração
```

---

# 9. Regra 3-2-1

Uma estratégia amplamente utilizada pode seguir o princípio:

```text
3 cópias dos dados
2 tipos diferentes de mídia ou armazenamento
1 cópia fora do ambiente principal
```

Uma evolução pode considerar:

```text
3-2-1-1-0
```

onde:

- 3 cópias;
- 2 mídias;
- 1 cópia offsite;
- 1 cópia offline ou imutável;
- 0 erros após validação.

A adoção deve ser ajustada ao contexto e aos riscos da organização.

---

# 10. Armazenamento

Backups podem ser armazenados em:

- storage dedicado;
- appliance;
- fita;
- object storage;
- nuvem;
- repositório secundário;
- site remoto.

Avaliar:

- capacidade;
- desempenho;
- segurança;
- disponibilidade;
- custo;
- retenção;
- isolamento.

---

# 11. Backup Offsite

Uma cópia fora do ambiente principal reduz risco em eventos como:

- incêndio;
- inundação;
- falha física;
- comprometimento do datacenter;
- ransomware;
- sabotagem.

O ambiente remoto deve possuir controles próprios.

---

# 12. Imutabilidade

Backup imutável não pode ser alterado ou excluído durante determinado período.

Pode ajudar a proteger contra:

- ransomware;
- exclusão acidental;
- comprometimento de credenciais;
- sabotagem.

---

## Princípio

```text
Produção comprometida
        ↓
Backup principal comprometido
        ↓
Cópia imutável permanece disponível
        ↓
Recuperação
```

---

# 13. Backup Offline

Cópias offline ficam desconectadas do ambiente de produção durante parte do tempo.

Exemplos:

- fita;
- mídia removível;
- repositório isolado.

Isso reduz a superfície de ataque.

---

# 14. Criptografia

Backups podem conter grande volume de informação sensível.

Avaliar:

- criptografia em trânsito;
- criptografia em repouso;
- gestão das chaves;
- acesso;
- armazenamento das credenciais.

---

# 15. Controle de Acesso

Nem todo administrador precisa poder excluir backups.

Aplicar:

- menor privilégio;
- segregação;
- contas específicas;
- MFA;
- logs;
- aprovação para ações críticas.

---

# 16. Contas de Serviço

Serviços de backup devem utilizar contas controladas.

Boas práticas:

- credenciais dedicadas;
- menor privilégio;
- rotação;
- não reutilização;
- monitoramento;
- MFA quando suportado.

---

# 17. Jobs de Backup

Todo job deve possuir:

- identificação;
- origem;
- destino;
- frequência;
- janela;
- retenção;
- responsável;
- status;
- último sucesso;
- último erro.

---

# 18. Janela de Backup

A janela deve considerar:

- duração;
- impacto;
- rede;
- storage;
- horário de pico;
- outros jobs;
- replicação.

Se o backup não termina dentro da janela, pode indicar problema de capacidade ou estratégia.

---

# 19. Monitoramento

Backups precisam ser monitorados continuamente.

Situações relevantes:

```text
Sucesso
Sucesso com alerta
Falha
Job não executado
Duração anormal
Destino indisponível
Capacidade crítica
```

---

# 20. Falha de Backup

Toda falha deve gerar tratamento.

Fluxo:

```text
Falha
  ↓
Alerta
  ↓
Análise
  ↓
Correção
  ↓
Nova execução
  ↓
Validação
```

Uma falha recorrente deve gerar investigação de causa.

---

# 21. Restauração

O backup somente demonstra valor quando consegue ser restaurado.

Tipos de restauração:

- arquivo;
- pasta;
- banco;
- VM;
- servidor;
- aplicação;
- ambiente completo.

---

# 22. Teste de Restauração

Testes devem ser realizados periodicamente.

Exemplo:

```text
Selecionar backup
      ↓
Executar restauração
      ↓
Validar integridade
      ↓
Validar aplicação
      ↓
Medir tempo
      ↓
Registrar evidência
```

---

## Registro de teste

| Item | Resultado |
|---|---|
| Sistema | Fileserver |
| Backup utilizado | 30/08/2026 |
| Data do teste | 31/08/2026 |
| Resultado | Sucesso |
| Tempo de restauração | 42 min |
| RTO esperado | 2h |
| Evidência | Registro do teste |

---

# 23. Frequência de Testes

A frequência deve considerar criticidade.

Exemplo:

```text
Crítico → mensal
Alto → trimestral
Médio → semestral
Baixo → anual
```

Os valores devem ser definidos conforme o contexto da organização.

---

# 24. Validação da Restauração

Não basta o software indicar “restore completed”.

É importante validar:

- arquivo abre;
- banco inicia;
- VM sobe;
- aplicação funciona;
- permissões estão corretas;
- dados são consistentes.

---

# 25. Disaster Recovery

Disaster Recovery trata da recuperação da infraestrutura e dos serviços após eventos graves.

Exemplos:

- perda de datacenter;
- falha generalizada;
- desastre físico;
- ataque cibernético;
- indisponibilidade extensa.

---

## Componentes de um plano

- serviços prioritários;
- RPO;
- RTO;
- contatos;
- responsabilidades;
- infraestrutura alternativa;
- backups;
- procedimentos;
- comunicação;
- sequência de recuperação;
- validação.

---

# 26. Ordem de Recuperação

Serviços possuem dependências.

Exemplo:

```text
Energia
  ↓
Rede
  ↓
Storage
  ↓
Virtualização
  ↓
Banco de Dados
  ↓
Aplicação
  ↓
Usuários
```

A ordem deve ser conhecida antes de uma crise.

---

# 27. Mapa de Dependências

Cada serviço crítico deve possuir dependências conhecidas.

Exemplo:

```text
Sistema de Atendimento
│
├── Banco de dados
├── Servidor de aplicação
├── DNS
├── Active Directory
├── Rede
└── Storage
```

Esse mapa ajuda a planejar a recuperação.

---

# 28. Plano de Continuidade

Continuidade é mais ampla que backup.

O objetivo é manter ou recuperar atividades críticas durante interrupções.

Pode envolver:

- pessoas;
- processos;
- tecnologia;
- instalações;
- fornecedores;
- comunicação.

---

# 29. Contingência

Uma contingência permite operar temporariamente de outra forma.

Exemplo:

```text
Sistema indisponível
      ↓
Ativação de processo manual
      ↓
Registro temporário
      ↓
Serviço principal restaurado
      ↓
Conciliação
```

---

# 30. Procedimentos de Emergência

Procedimentos precisam ser objetivos.

Exemplo:

```text
1. Confirmar incidente
2. Acionar responsável
3. Avaliar impacto
4. Declarar contingência
5. Iniciar recuperação
6. Comunicar áreas
7. Validar serviço
8. Encerrar contingência
```

---

# 31. Comunicação

Durante uma indisponibilidade grave, deve existir plano de comunicação.

Registrar:

- responsáveis;
- grupos;
- contatos;
- periodicidade;
- mensagens;
- canais alternativos.

---

# 32. Ransomware Recovery

Cenários de ransomware devem fazer parte da estratégia de recuperação.

Avaliar:

- backups imutáveis;
- isolamento;
- credenciais;
- cópia offline;
- ambiente limpo;
- ponto de recuperação;
- validação de integridade.

---

## Fluxo conceitual

```text
Ataque identificado
      ↓
Isolamento
      ↓
Contenção
      ↓
Identificação do ponto seguro
      ↓
Restauração em ambiente limpo
      ↓
Validação
      ↓
Retorno controlado
```

---

# 33. Proteção contra exclusão

Controles possíveis:

- MFA;
- segregação de função;
- retenção bloqueada;
- imutabilidade;
- aprovação;
- logs.

---

# 34. Capacidade do Repositório

O ambiente de backup deve possuir capacidade suficiente.

Monitorar:

- utilizado;
- livre;
- crescimento;
- taxa de deduplicação;
- compressão;
- retenção.

---

## Tendência

Exemplo:

```text
Janeiro   62%
Fevereiro 68%
Março     75%
Abril     82%
```

A capacidade deve ser ampliada antes da saturação.

---

# 35. Retenção

Retenção determina por quanto tempo as cópias são mantidas.

Pode variar conforme:

- criticidade;
- legislação;
- contrato;
- negócio;
- capacidade.

Exemplo:

```text
Diário → 30 dias
Semanal → 12 semanas
Mensal → 12 meses
Anual → 5 anos
```

Os períodos devem ser definidos conforme necessidade real.

---

# 36. GFS

Estratégias do tipo **Grandfather-Father-Son (GFS)** podem utilizar:

```text
Diário
Semanal
Mensal
Anual
```

para criar diferentes níveis de retenção.

---

# 37. Banco de Dados

Backups de banco podem exigir estratégias específicas.

Exemplos:

- full;
- incremental;
- transaction logs;
- snapshots consistentes;
- dump.

Avaliar:

- consistência;
- ponto no tempo;
- recuperação;
- integração com aplicação.

---

# 38. Máquinas Virtuais

Backups de VM podem proteger:

- disco;
- configuração;
- estado;
- aplicação.

Avaliar integração com:

- hypervisor;
- snapshots;
- quiescence;
- aplicações.

---

# 39. Arquivos

Backups de arquivos devem considerar:

- permissões;
- versões;
- nomes;
- metadados;
- compartilhamentos.

---

# 40. SaaS

Serviços SaaS também podem exigir estratégia própria.

Perguntas:

- O fornecedor realiza backup?
- Qual retenção?
- É possível restaurar individualmente?
- Existe exportação?
- Há necessidade de solução externa?

---

# 41. Cloud

Ambientes cloud exigem entendimento do modelo de responsabilidade compartilhada.

Avaliar:

- snapshots;
- object storage;
- versionamento;
- regiões;
- contas;
- recuperação;
- cópias entre regiões;
- imutabilidade.

---

# 42. Evidências

Manter evidências de:

- execução;
- sucesso;
- falha;
- restauração;
- teste;
- aprovação;
- incidente;
- capacidade.

Isso facilita:

- auditoria;
- governança;
- investigação;
- melhoria.

---

# 43. Auditoria

Uma auditoria de backup pode verificar:

```text
[ ] Sistemas críticos protegidos
[ ] Frequência conforme política
[ ] Retenção conforme política
[ ] Falhas tratadas
[ ] Cópias offsite
[ ] Imutabilidade, quando prevista
[ ] Criptografia
[ ] Testes de restauração
[ ] RPO e RTO definidos
[ ] Evidências disponíveis
```

---

# 44. Indicadores

## Execução

- jobs executados;
- jobs com sucesso;
- jobs com falha;
- jobs não executados.

---

## Taxa de sucesso

```text
Taxa de sucesso =
Jobs concluídos com sucesso
--------------------------- × 100
Jobs executados
```

---

## Restauração

- testes executados;
- testes com sucesso;
- tempo médio de restauração;
- aderência ao RTO.

---

## Proteção

- percentual de sistemas críticos protegidos;
- percentual com cópia offsite;
- percentual com backup imutável.

---

## RPO

- sistemas dentro do RPO;
- violações de RPO;
- tempo desde último ponto válido.

---

# 45. Indicador de Cobertura

Exemplo:

```text
Sistemas críticos: 50
Sistemas críticos protegidos: 49

Cobertura = 98%
```

O sistema restante representa risco que deve ser avaliado.

---

# 46. Indicador de Teste

```text
Backups críticos: 30
Backups testados no período: 27

Cobertura de teste = 90%
```

---

# 47. Indicador de Sucesso

Exemplo:

```text
Jobs executados: 10.000
Jobs com sucesso: 9.850

Taxa de sucesso = 98,5%
```

A taxa deve ser analisada junto com criticidade e reincidência.

---

# 48. Critérios de Maturidade

| Nível | Situação |
|---|---|
| 0 | Não existe estratégia formal |
| 1 | Backups manuais ou pontuais |
| 2 | Rotinas definidas, mas pouco testadas |
| 3 | Política, monitoramento e testes regulares |
| 4 | RPO/RTO, offsite, imutabilidade e DR controlados |
| 5 | Continuidade integrada, testada e continuamente melhorada |

Avaliar:

- cobertura;
- política;
- retenção;
- segurança;
- testes;
- RPO;
- RTO;
- monitoramento;
- contingência;
- DR;
- melhoria contínua.

---

# 49. Perguntas Orientadoras

## Cobertura

- Todos os sistemas críticos estão protegidos?
- Existe inventário de backups?
- Há dados fora da política?

## Segurança

- Existe cópia imutável?
- Existe cópia offsite?
- Credenciais são segregadas?
- Há MFA?

## Restauração

- Os backups são testados?
- O tempo de restauração é medido?
- O RTO é atendido?
- O RPO é atendido?

## Continuidade

- Existe plano de contingência?
- A sequência de recuperação é conhecida?
- Dependências estão documentadas?
- Existe plano de comunicação?

## Gestão

- Falhas geram ação?
- Indicadores são acompanhados?
- Existem revisões periódicas?
- A estratégia acompanha mudanças no ambiente?

---

# 50. Entregáveis Esperados

Este domínio pode produzir:

- política de backup;
- inventário de backups;
- matriz de criticidade;
- matriz de RPO/RTO;
- calendário de backup;
- matriz de retenção;
- procedimentos de restauração;
- registros de testes;
- plano de contingência;
- plano de Disaster Recovery;
- mapa de dependências;
- runbooks;
- dashboards;
- relatórios;
- indicadores;
- checklists;
- planos de melhoria.

---

# Resultado esperado

Uma operação capaz de **proteger dados críticos, detectar falhas de backup, validar restaurações, cumprir objetivos de recuperação e restabelecer serviços de forma controlada, testada e alinhada ao risco e à criticidade da organização**.
