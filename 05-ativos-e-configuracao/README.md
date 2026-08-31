# 05 — Ativos e Configuração

Este diretório reúne práticas, modelos, padrões e referências voltados à **gestão de ativos de TI, inventário, itens de configuração e relacionamento entre componentes e serviços**.

A proposta é garantir que a operação conheça os recursos tecnológicos sob sua responsabilidade, saiba onde estão, quem os utiliza, qual seu estado, quais serviços suportam e como se relacionam com outros componentes.

---

## Objetivo

Apoiar a gestão de ativos e configurações de forma estruturada, permitindo:

- manter inventário confiável;
- conhecer localização e responsabilidade dos ativos;
- controlar ciclo de vida;
- identificar ativos sem suporte;
- apoiar auditorias;
- relacionar componentes a serviços;
- melhorar rastreabilidade;
- apoiar análise de impacto;
- melhorar planejamento de renovação;
- apoiar capacidade e segurança;
- reduzir dependência de conhecimento informal.

O resultado esperado é uma base de ativos e configurações **confiável, atualizada, auditável e útil para a operação e para a governança**.

---

## Princípio

Uma operação madura deve conseguir responder:

> **Quais ativos existem, onde estão, quem é responsável, qual é seu estado e quais serviços dependem deles?**

Fluxo simplificado:

```text
Identificar
    ↓
Cadastrar
    ↓
Classificar
    ↓
Relacionar
    ↓
Controlar
    ↓
Auditar
    ↓
Atualizar
    ↓
Renovar ou descartar
```

---

## Estrutura sugerida

```text
05-ativos-e-configuracao/
│
├── README.md
├── inventario/
├── cmdb/
├── netbox/
├── ativos-de-rede/
├── servidores/
├── estacoes/
├── perifericos/
├── software-e-licencas/
├── garantias/
├── contratos/
├── ciclo-de-vida/
├── auditoria/
├── padroes-de-cadastro/
└── relacionamentos/
```

---

## 1. Gestão de Ativos de TI

A gestão de ativos acompanha o ciclo de vida dos recursos utilizados pela organização.

Exemplos:

- notebooks;
- desktops;
- monitores;
- servidores;
- switches;
- roteadores;
- access points;
- storage;
- impressoras;
- dispositivos móveis;
- licenças;
- softwares;
- equipamentos de datacenter.

---

## 2. Informações mínimas de um ativo

Sempre que aplicável, registrar:

- identificador;
- patrimônio;
- fabricante;
- modelo;
- número de série;
- hostname;
- endereço IP;
- endereço MAC;
- sistema operacional;
- localização;
- responsável;
- unidade;
- status;
- data de aquisição;
- garantia;
- contrato;
- fornecedor;
- criticidade;
- serviço relacionado.

---

## 3. Classificação dos ativos

Uma classificação consistente facilita filtros e gestão.

Exemplos:

```text
Rede
Servidor
Estação
Notebook
Periférico
Storage
Telefonia
Software
Licença
Datacenter
```

Também pode ser utilizado:

```text
Produção
Homologação
Desenvolvimento
Reserva
Estoque
Manutenção
Descarte
```

---

## 4. Status

O status deve refletir a situação real do ativo.

Exemplo:

```text
Planejado
Em estoque
Em uso
Em manutenção
Indisponível
Reserva
Em substituição
Descartado
```

Evite manter ativos antigos como ativos em produção após descarte ou substituição.

---

## 5. Inventário

O inventário deve representar o ambiente real.

Pode ser:

- físico;
- lógico;
- automatizado;
- manual;
- híbrido.

### Inventário físico

Confirma existência, localização e condição do ativo.

### Inventário lógico

Confirma informações como:

- hostname;
- IP;
- sistema operacional;
- software;
- configuração;
- status de rede.

---

## 6. Conciliação de inventário

É importante comparar fontes diferentes.

Exemplo:

```text
Inventário patrimonial
        +
NetBox
        +
AD
        +
Ferramenta de monitoramento
        +
CMDB
        ↓
Conciliação
```

Diferenças podem revelar:

- ativo não cadastrado;
- ativo duplicado;
- equipamento desligado;
- hostname incorreto;
- IP desatualizado;
- ativo descartado ainda cadastrado.

---

## 7. CMDB

A **Configuration Management Database** deve representar itens de configuração e seus relacionamentos.

Um CI pode ser:

- servidor;
- aplicação;
- banco;
- switch;
- serviço;
- link;
- equipamento;
- contrato;
- software.

---

## 8. Relacionamentos

O valor da CMDB aumenta quando existem relacionamentos.

Exemplo:

```text
Serviço de e-mail
│
├── Aplicação
│   ├── Servidor APP
│   └── Banco de dados
│
├── Rede
│   ├── Switch
│   └── Firewall
│
└── Storage
```

Isso permite análise de impacto.

---

## 9. Análise de impacto

Quando um componente falha, a operação deve saber:

- quais serviços são afetados;
- quais usuários podem ser impactados;
- qual prioridade deve ser aplicada;
- quais equipes devem ser acionadas.

Exemplo:

```text
Falha no Switch Core
      ↓
Servidores afetados
      ↓
Serviços afetados
      ↓
Usuários impactados
```

---

## 10. NetBox

O NetBox pode ser utilizado para organizar informações de infraestrutura.

Exemplos:

- sites;
- racks;
- dispositivos;
- interfaces;
- endereços IP;
- VLANs;
- circuitos;
- virtualização;
- cabos;
- tenants;
- contatos.

---

## 11. Padronização no NetBox

Definir padrões para:

- nomes;
- status;
- roles;
- sites;
- device types;
- tags;
- interfaces;
- descrições.

Evitar cadastros inconsistentes como:

```text
SWITCH
Switch
switch
Switch Core
CORE-SW
```

sem uma convenção definida.

---

## 12. Ativos de Rede

Para equipamentos de rede, registrar:

- hostname;
- fabricante;
- modelo;
- serial;
- asset tag;
- IP de gerenciamento;
- função;
- localização;
- rack;
- posição;
- firmware;
- status;
- interfaces;
- uplinks;
- garantia.

---

## 13. Servidores

Para servidores físicos ou virtuais:

- hostname;
- IP;
- sistema operacional;
- função;
- CPU;
- memória;
- armazenamento;
- cluster;
- host;
- backup;
- monitoramento;
- criticidade;
- responsável.

---

## 14. Estações de Trabalho

Informações recomendadas:

- patrimônio;
- usuário;
- hostname;
- fabricante;
- modelo;
- serial;
- CPU;
- memória;
- disco;
- sistema operacional;
- localização;
- status;
- garantia.

---

## 15. Software e Licenças

A gestão pode incluir:

- software;
- versão;
- fabricante;
- quantidade contratada;
- quantidade utilizada;
- validade;
- modelo de licenciamento;
- responsável;
- contrato.

---

## 16. Compliance de licenças

A operação deve evitar:

```text
Licenças contratadas < Licenças utilizadas
```

Também deve identificar:

- licenças ociosas;
- softwares sem contrato;
- versões sem suporte;
- produtos descontinuados.

---

## 17. Garantias

Registrar:

- início;
- fim;
- fornecedor;
- tipo;
- SLA;
- cobertura;
- equipamento.

Alertas podem ser criados para:

```text
Garantia vence em 180 dias
Garantia vence em 90 dias
Garantia vence em 30 dias
```

---

## 18. Contratos

Associar ativos a contratos pode ajudar em:

- manutenção;
- suporte;
- renovação;
- garantia;
- fornecedor;
- SLA;
- custo.

---

## 19. Ciclo de Vida

Um ativo deve possuir ciclo de vida conhecido.

```text
Planejamento
    ↓
Aquisição
    ↓
Recebimento
    ↓
Cadastro
    ↓
Implantação
    ↓
Operação
    ↓
Manutenção
    ↓
Substituição
    ↓
Descarte
```

---

## 20. Aquisição

Antes da aquisição, considerar:

- padrão técnico;
- compatibilidade;
- necessidade;
- capacidade;
- suporte;
- garantia;
- ciclo de vida;
- custo total.

---

## 21. Recebimento

No recebimento:

```text
[ ] Conferir modelo
[ ] Conferir quantidade
[ ] Registrar serial
[ ] Registrar patrimônio
[ ] Conferir garantia
[ ] Cadastrar inventário
[ ] Definir localização
```

---

## 22. Movimentação

Toda movimentação deve atualizar o inventário.

Registrar:

- origem;
- destino;
- responsável anterior;
- novo responsável;
- data;
- motivo;
- evidência.

---

## 23. Manutenção

Registrar:

- defeito;
- data;
- fornecedor;
- chamado;
- peça substituída;
- custo;
- período indisponível;
- retorno.

Isso ajuda a identificar ativos com manutenção recorrente.

---

## 24. Substituição

Critérios possíveis:

- fim de garantia;
- fim de suporte;
- baixa capacidade;
- recorrência de falhas;
- incompatibilidade;
- risco;
- custo de manutenção.

---

## 25. Descarte

O descarte deve ser controlado.

Avaliar:

- remoção de dados;
- sanitização;
- patrimônio;
- registro;
- destino;
- descarte ambiental;
- evidência.

---

## 26. Auditoria Física

Auditorias periódicas verificam se o cadastro corresponde ao ambiente.

Pode validar:

```text
Existe?
Está no local correto?
Está com o responsável correto?
Serial confere?
Status confere?
Patrimônio confere?
```

---

## 27. Auditoria Lógica

Pode comparar:

- hostname;
- IP;
- sistema operacional;
- última conexão;
- agente de monitoramento;
- domínio;
- software.

---

## 28. Qualidade dos Dados

Um inventário pode existir e ainda ser pouco confiável.

Indicadores de qualidade:

- ativos sem serial;
- ativos sem localização;
- ativos sem responsável;
- ativos sem status;
- registros duplicados;
- IPs inconsistentes;
- ativos não atualizados.

---

## 29. Fonte da Verdade

Idealmente, deve existir clareza sobre qual sistema é a referência oficial para cada informação.

Exemplo:

| Informação | Fonte oficial |
|---|---|
| Patrimônio | Sistema patrimonial |
| IP | NetBox |
| Usuário | Diretório corporativo |
| Monitoramento | Zabbix |
| Serviço | CMDB |

Evite manter o mesmo dado manualmente em diversas plataformas sem estratégia de sincronização.

---

## 30. Automação

Automação pode apoiar:

- descoberta;
- atualização;
- conciliação;
- criação de ativos;
- coleta de dados;
- validação;
- geração de relatórios.

Exemplo:

```text
API
 ↓
NetBox
 ↓
Inventário
 ↓
Monitoramento
```

---

## 31. Integração com Monitoramento

O inventário pode ser utilizado para verificar cobertura.

Exemplo:

```text
Ativos em produção: 500
Ativos monitorados: 460

Cobertura = 92%
```

Os 40 ativos restantes devem ser avaliados.

---

## 32. Integração com ITSM

Relacionamentos entre ativo e chamado podem ajudar a identificar:

- incidentes recorrentes;
- equipamentos problemáticos;
- custo de suporte;
- impacto;
- histórico de manutenção.

---

## 33. Indicadores

Indicadores possíveis:

### Inventário

- total de ativos;
- ativos por tipo;
- ativos por localização;
- ativos sem responsável.

### Qualidade

- percentual de registros completos;
- duplicidades;
- ativos não conciliados.

### Ciclo de vida

- ativos fora de garantia;
- ativos sem suporte;
- equipamentos a renovar.

### Auditoria

- aderência física;
- divergências;
- tempo para correção.

---

## 34. Exemplo de indicador de completude

```text
Ativos cadastrados: 1.000
Ativos com cadastro completo: 920

Completude = 92%
```

O objetivo deve ser aumentar a confiabilidade da base.

---

## 35. Indicador de cobertura de monitoramento

```text
Ativos críticos: 120
Ativos críticos monitorados: 118

Cobertura = 98,3%
```

---

## 36. Critérios de Maturidade

| Nível | Situação |
|---|---|
| 0 | Ativos desconhecidos |
| 1 | Inventário informal |
| 2 | Cadastro parcial |
| 3 | Inventário padronizado e atualizado |
| 4 | CMDB integrada e auditada |
| 5 | Gestão automatizada, integrada e orientada a serviços |

Avaliar:

- cobertura;
- qualidade;
- atualização;
- relacionamentos;
- integração;
- automação;
- auditoria;
- uso na tomada de decisão.

---

## 37. Perguntas Orientadoras

### Inventário

- Todos os ativos estão cadastrados?
- Existem duplicidades?
- Há ativos sem responsável?
- As localizações estão corretas?

### CMDB

- Existem relacionamentos?
- Os serviços estão associados aos componentes?
- A base é utilizada na análise de impacto?

### Ciclo de vida

- Quais ativos estão sem suporte?
- Quais garantias estão próximas do fim?
- Existe plano de renovação?

### Auditoria

- O inventário é conferido?
- Divergências geram ações?
- Existe periodicidade?

### Dados

- Existe uma fonte oficial?
- Há integração entre sistemas?
- Os dados são confiáveis?

---

## 38. Entregáveis Esperados

Este domínio pode produzir:

- inventário de ativos;
- CMDB;
- padrões de cadastro;
- matriz de criticidade;
- relatórios de auditoria;
- plano de renovação;
- controle de garantias;
- inventário de software;
- mapa de relacionamentos;
- relatórios de qualidade dos dados;
- dashboards;
- integrações;
- procedimentos de entrada, movimentação e descarte.

---

## Resultado esperado

Uma gestão de ativos e configurações capaz de fornecer **informações confiáveis, relacionamentos úteis, rastreabilidade, controle de ciclo de vida e suporte efetivo à operação, à governança e à tomada de decisão**.
