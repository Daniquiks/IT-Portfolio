# 07 — Governança de IA

Este diretório reúne práticas, controles, modelos e referências voltados à **governança do uso de Inteligência Artificial em ambientes organizacionais e operações de TI**.

A proposta é estabelecer mecanismos para que soluções de IA sejam avaliadas, aprovadas, utilizadas, monitoradas e descontinuadas de forma controlada, considerando valor, risco, segurança, privacidade, transparência, responsabilidade e supervisão humana.

---

## Objetivo

Apoiar a adoção responsável de Inteligência Artificial, permitindo:

- identificar onde IA está sendo utilizada;
- registrar casos de uso;
- definir responsáveis;
- avaliar riscos antes da implantação;
- controlar dados utilizados;
- avaliar fornecedores e modelos;
- estabelecer critérios de aprovação;
- definir supervisão humana;
- monitorar desempenho e comportamento;
- registrar incidentes;
- controlar mudanças;
- documentar decisões;
- acompanhar o ciclo de vida;
- apoiar conformidade e auditoria;
- promover melhoria contínua.

O resultado esperado é uma utilização de IA **controlada, rastreável, proporcional ao risco e alinhada aos objetivos da organização**.

---

## Princípio

Governança de IA não deve ser tratada apenas como uma questão tecnológica.

Uma solução pode envolver simultaneamente:

```text
Pessoas
  +
Processos
  +
Dados
  +
Modelos
  +
Fornecedores
  +
Infraestrutura
  +
Segurança
  +
Riscos
  +
Decisões
```

A pergunta central não deve ser apenas:

> **A IA funciona?**

Também deve ser possível responder:

> **Por que ela está sendo utilizada, com quais dados, sob quais controles, quem é responsável e quais riscos são aceitáveis?**

---

## Estrutura sugerida

```text
07-governanca-de-ia/
│
├── README.md
├── politica-de-ia/
├── inventario-de-ia/
├── casos-de-uso/
├── avaliacao-de-risco/
├── avaliacao-de-modelos/
├── dados-e-privacidade/
├── seguranca/
├── fornecedores/
├── controles/
├── supervisao-humana/
├── transparencia/
├── monitoramento/
├── incidentes-de-ia/
├── ciclo-de-vida/
├── auditoria/
├── templates/
└── referencias/
```

---

# 1. Política de IA

A organização pode estabelecer uma política para orientar o uso de Inteligência Artificial.

A política pode definir:

- objetivos;
- escopo;
- usos permitidos;
- usos restritos;
- responsabilidades;
- classificação de risco;
- tratamento de dados;
- segurança;
- supervisão humana;
- aprovação;
- monitoramento;
- registro;
- auditoria.

---

## Perguntas básicas

- Quem pode utilizar ferramentas de IA?
- Para quais finalidades?
- Quais dados podem ser inseridos?
- Quais ferramentas estão autorizadas?
- Quais usos precisam de aprovação?
- Quem responde pelo resultado?
- Como incidentes devem ser tratados?

---

# 2. Inventário de IA

Uma organização deve conhecer as soluções de IA utilizadas em seu ambiente.

O inventário pode incluir:

- nome da solução;
- finalidade;
- área responsável;
- fornecedor;
- modelo utilizado;
- tipo de IA;
- usuários;
- dados processados;
- integrações;
- criticidade;
- classificação de risco;
- status;
- data de aprovação;
- responsável.

---

## Exemplo

| Solução | Finalidade | Responsável | Dados | Risco | Status |
|---|---|---|---|---|---|
| Assistente interno | Apoio documental | TI | Dados internos controlados | Médio | Aprovado |
| Classificador de chamados | Triagem | Operação | Dados de chamados | Baixo | Produção |
| Modelo analítico | Previsão | Dados | Dados corporativos | Médio | Piloto |

---

# 3. Casos de Uso

Cada utilização de IA deve possuir finalidade clara.

Exemplos:

- classificação de chamados;
- sumarização;
- geração de documentação;
- copilotos;
- pesquisa em base de conhecimento;
- análise de tendências;
- apoio ao diagnóstico;
- automação assistida;
- previsão de capacidade;
- detecção de anomalias;
- análise documental.

---

## Registro de caso de uso

Um caso de uso pode conter:

```text
Nome
Objetivo
Área
Responsável
Problema que pretende resolver
Usuários
Dados utilizados
Modelo/fornecedor
Benefício esperado
Riscos
Controles
Critério de sucesso
Status
```

---

# 4. Avaliação de Necessidade

Antes de implantar IA, verificar se ela realmente é necessária.

Perguntas:

- O problema está claramente definido?
- Uma automação convencional resolveria?
- Existe dado suficiente?
- O benefício esperado é mensurável?
- Existe risco desproporcional?
- A solução exige IA ou apenas regras bem definidas?

---

# 5. Classificação de Risco

Nem todo uso de IA possui o mesmo nível de risco.

Uma classificação simples pode considerar:

```text
Baixo
Moderado
Alto
Crítico
```

A classificação pode avaliar:

- impacto sobre pessoas;
- criticidade da decisão;
- autonomia;
- sensibilidade dos dados;
- exposição externa;
- segurança;
- possibilidade de erro;
- reversibilidade;
- dependência operacional.

---

## Exemplo

| Critério | Baixo risco | Alto risco |
|---|---|---|
| Decisão | Apenas apoio | Decisão crítica |
| Dados | Públicos | Sensíveis/confidenciais |
| Autonomia | Sugestão | Ação automática |
| Impacto | Limitado | Significativo |
| Reversibilidade | Fácil | Difícil |

---

# 6. Avaliação de Risco

Cada caso relevante pode possuir um registro formal de risco.

Estrutura possível:

| Risco | Probabilidade | Impacto | Nível | Controle | Responsável |
|---|---|---|---|---|---|
| Resposta incorreta | Média | Alto | Alto | Validação humana | Área responsável |
| Exposição de dados | Baixa | Alto | Alto | Restrição de dados | Segurança |
| Dependência de fornecedor | Média | Médio | Moderado | Plano de contingência | TI |

---

## Categorias de risco

- segurança;
- privacidade;
- qualidade;
- viés;
- erro;
- alucinação;
- disponibilidade;
- dependência de fornecedor;
- propriedade intelectual;
- uso inadequado;
- falta de transparência;
- automação excessiva;
- perda de rastreabilidade.

---

# 7. Dados

O uso de IA depende diretamente dos dados utilizados.

Avaliar:

- origem;
- qualidade;
- classificação;
- finalidade;
- autorização;
- retenção;
- compartilhamento;
- armazenamento;
- acesso.

---

## Perguntas

- O dado pode ser enviado para essa ferramenta?
- O fornecedor utiliza o conteúdo para treinamento?
- Onde o dado é processado?
- Existe retenção?
- É possível excluir?
- Existem dados pessoais?
- Existem informações confidenciais?

---

# 8. Privacidade

Casos que envolvam dados pessoais precisam de controles proporcionais.

Considerar:

- minimização;
- finalidade;
- necessidade;
- acesso;
- retenção;
- compartilhamento;
- anonimização ou pseudonimização quando aplicável.

A utilização de IA não elimina os requisitos de governança já existentes para dados.

---

# 9. Segurança

Soluções de IA também devem fazer parte da arquitetura de segurança.

Avaliar:

- autenticação;
- autorização;
- MFA;
- integração;
- APIs;
- logs;
- tokens;
- credenciais;
- isolamento;
- vulnerabilidades;
- exposição externa.

---

## Segredos

Nunca armazenar diretamente em prompts, código ou repositórios públicos:

```text
Senhas
Tokens
API Keys
Credenciais
Segredos
Dados confidenciais
```

---

# 10. Prompt Injection

Sistemas baseados em modelos de linguagem podem ser expostos a tentativas de manipulação das instruções.

Controles podem incluir:

- validação de entrada;
- isolamento de ferramentas;
- limitação de permissões;
- filtragem;
- supervisão;
- logs;
- confirmação de ações críticas.

---

# 11. Menor Privilégio

Uma IA integrada a ferramentas corporativas deve receber apenas as permissões necessárias.

Exemplo:

```text
Necessidade:
Consultar chamados

Permissão desejada:
Leitura de chamados

Evitar:
Acesso administrativo completo
```

---

# 12. Fornecedores

A avaliação de fornecedores pode considerar:

- empresa responsável;
- modelo;
- localização do processamento;
- termos de uso;
- segurança;
- privacidade;
- retenção;
- suporte;
- disponibilidade;
- portabilidade;
- encerramento do serviço.

---

## Perguntas para fornecedores

- Quais dados são armazenados?
- Por quanto tempo?
- Os dados são utilizados para treinamento?
- Existe isolamento entre clientes?
- Quais certificações existem?
- Há logs?
- Existe SLA?
- Como ocorre exclusão de dados?
- Como ocorre encerramento do contrato?

---

# 13. Avaliação de Modelos

Modelos podem ser avaliados conforme o uso pretendido.

Critérios possíveis:

- precisão;
- consistência;
- relevância;
- segurança;
- latência;
- custo;
- estabilidade;
- explicabilidade;
- robustez.

---

## Benchmark

Quando possível, criar conjunto de testes representativo.

Exemplo:

```text
50 perguntas reais
      ↓
Executar no modelo
      ↓
Avaliar respostas
      ↓
Registrar resultado
      ↓
Comparar versões
```

---

# 14. Critério de Aceitação

Antes da implantação, definir o que representa desempenho aceitável.

Exemplo:

```text
Acurácia mínima: 90%
Taxa máxima de erro: 5%
Revisão humana: obrigatória
Tempo máximo de resposta: 10s
```

Os valores devem depender do caso de uso.

---

# 15. Supervisão Humana

Nem toda saída de IA deve gerar uma ação automática.

Modelos possíveis:

```text
Human in the Loop
Human on the Loop
Human out of the Loop
```

---

## Human in the Loop

Uma pessoa valida antes da decisão ou execução.

Adequado quando:

- impacto é relevante;
- erro pode causar dano;
- decisão exige julgamento;
- risco é elevado.

---

# 16. Automação de Decisões

Quanto maior a autonomia da solução, maior tende a ser a necessidade de controle.

Exemplo:

```text
IA sugere categoria
→ menor autonomia

IA altera prioridade
→ autonomia intermediária

IA executa ação em produção
→ maior autonomia
```

A governança deve ser proporcional ao impacto.

---

# 17. Transparência

Usuários devem compreender, quando relevante:

- que existe IA envolvida;
- qual é sua finalidade;
- quais são suas limitações;
- como contestar ou revisar uma decisão;
- quem é responsável.

---

# 18. Explicabilidade

Nem todo sistema precisa do mesmo nível de explicação.

Quanto maior o impacto da decisão, maior pode ser a necessidade de compreender:

- quais informações foram utilizadas;
- como a resposta foi produzida;
- quais limitações existem;
- quais critérios influenciaram o resultado.

---

# 19. Rastreabilidade

Sempre que tecnicamente e juridicamente apropriado, manter registros de:

- modelo;
- versão;
- configuração;
- prompt;
- resultado;
- usuário;
- data;
- ação realizada.

Isso ajuda em:

- auditoria;
- investigação;
- reprodução;
- melhoria.

---

# 20. Logs

Logs de soluções de IA podem registrar:

```text
Timestamp
Usuário
Caso de uso
Modelo
Versão
Resultado
Erro
Ação executada
```

Os próprios logs podem conter dados sensíveis e devem possuir controles de acesso e retenção.

---

# 21. Monitoramento

A solução deve continuar sendo avaliada após implantação.

Monitorar:

- erros;
- qualidade;
- disponibilidade;
- latência;
- custo;
- volume;
- reclamações;
- incidentes;
- mudanças de comportamento.

---

# 22. Drift

O comportamento ou desempenho de uma solução pode mudar ao longo do tempo.

Podem ocorrer:

- data drift;
- concept drift;
- mudanças de modelo;
- mudanças de contexto;
- alterações do fornecedor.

Por isso, avaliações periódicas são necessárias.

---

# 23. Mudança de Modelo

Alterar modelo ou versão pode alterar significativamente os resultados.

Fluxo recomendado:

```text
Nova versão
    ↓
Teste
    ↓
Comparação
    ↓
Avaliação de risco
    ↓
Aprovação
    ↓
Implantação
    ↓
Monitoramento
```

---

# 24. Gestão de Mudanças

Mudanças relevantes devem ser controladas.

Exemplos:

- novo modelo;
- novo fornecedor;
- mudança de prompt principal;
- alteração de dados;
- nova integração;
- aumento de autonomia;
- nova finalidade.

---

# 25. Incidentes de IA

A organização deve possuir mecanismo para tratar comportamentos inadequados.

Exemplos:

- exposição de informação;
- resposta incorreta com impacto;
- execução indevida;
- indisponibilidade;
- uso não autorizado;
- comportamento inesperado.

---

## Registro

```text
Data
Solução
Descrição
Impacto
Usuários afetados
Dados envolvidos
Ação imediata
Causa
Correção
Responsável
```

---

# 26. Kill Switch

Soluções críticas podem precisar de mecanismo para interrupção rápida.

Exemplo:

```text
Comportamento inadequado
        ↓
Desativar automação
        ↓
Retornar processo manual
        ↓
Investigar
```

---

# 27. Contingência

A organização deve avaliar o que ocorre se a solução de IA ficar indisponível.

Perguntas:

- Existe processo manual?
- Existe modelo alternativo?
- Existe fornecedor alternativo?
- O serviço depende completamente da IA?

---

# 28. Ciclo de Vida

O ciclo de vida pode ser estruturado como:

```text
Ideia
  ↓
Caso de uso
  ↓
Avaliação
  ↓
Risco
  ↓
Piloto
  ↓
Homologação
  ↓
Aprovação
  ↓
Produção
  ↓
Monitoramento
  ↓
Revisão
  ↓
Descontinuação
```

---

# 29. Piloto

Antes de utilização ampla, pode ser útil executar um piloto.

Objetivos:

- validar benefício;
- identificar riscos;
- medir qualidade;
- avaliar aceitação;
- entender custo;
- testar controles.

---

# 30. Homologação

A homologação pode incluir:

```text
[ ] Caso de uso aprovado
[ ] Responsável definido
[ ] Risco avaliado
[ ] Dados avaliados
[ ] Segurança avaliada
[ ] Modelo testado
[ ] Critério de sucesso atingido
[ ] Supervisão definida
[ ] Logs configurados
[ ] Plano de contingência definido
```

---

# 31. Aprovação

A aprovação deve ser proporcional ao risco.

Exemplo:

```text
Baixo risco
→ aprovação da área

Moderado
→ área + TI

Alto
→ governança + segurança + responsável pelo negócio

Crítico
→ instância executiva adequada
```

A estrutura real depende da organização.

---

# 32. Papéis e Responsabilidades

Possíveis papéis:

- patrocinador;
- proprietário do caso de uso;
- responsável técnico;
- segurança;
- privacidade;
- dados;
- governança;
- usuário;
- auditoria.

---

## RACI

Exemplo:

| Atividade | Área de Negócio | TI | Segurança | Governança |
|---|---|---|---|---|
| Propor caso de uso | R | C | I | I |
| Avaliar arquitetura | C | R | C | I |
| Avaliar risco | C | C | R | A |
| Aprovar produção | R | C | C | A |

---

# 33. Comitê de IA

Organizações com maior utilização podem criar fórum específico.

Possíveis responsabilidades:

- avaliar casos relevantes;
- revisar riscos;
- definir padrões;
- acompanhar incidentes;
- avaliar fornecedores;
- revisar políticas;
- priorizar melhorias.

---

# 34. Inventário de Modelos

Além do inventário de soluções, pode existir inventário dos modelos.

Registrar:

- fornecedor;
- modelo;
- versão;
- finalidade;
- casos de uso;
- data de adoção;
- status;
- restrições.

---

# 35. Custos

O uso de IA também deve ser acompanhado financeiramente.

Indicadores:

- custo mensal;
- custo por usuário;
- custo por requisição;
- tokens;
- infraestrutura;
- licenças.

---

# 36. Benefícios

O valor deve ser mensurado sempre que possível.

Exemplos:

- tempo economizado;
- redução de backlog;
- melhoria de qualidade;
- aumento de produtividade;
- redução de tempo de análise;
- diminuição de erros.

---

## Exemplo

```text
Processo manual:
20 minutos

Processo com apoio de IA:
8 minutos

Redução:
12 minutos por execução
```

---

# 37. Indicadores

### Adoção

- casos de uso ativos;
- usuários;
- áreas utilizando IA.

### Risco

- casos por classificação;
- riscos abertos;
- controles pendentes.

### Qualidade

- precisão;
- erro;
- revisão humana;
- incidentes.

### Operação

- disponibilidade;
- latência;
- volume;
- custo.

### Governança

- casos inventariados;
- casos aprovados;
- casos sem responsável;
- revisões pendentes.

---

# 38. Shadow AI

Ferramentas utilizadas sem conhecimento ou aprovação podem gerar riscos.

Exemplos:

- contas pessoais;
- envio de documentos internos;
- ferramentas não homologadas;
- integrações não registradas.

Controles possíveis:

- política;
- conscientização;
- inventário;
- ferramentas homologadas;
- monitoramento;
- canais para solicitação de novos usos.

---

# 39. Uso Aceitável

Uma política pode diferenciar:

```text
Permitido
Permitido com restrições
Exige aprovação
Proibido
```

Exemplo:

| Uso | Classificação |
|---|---|
| Revisão de texto público | Permitido |
| Processamento de dados internos | Restrito |
| Dados sensíveis em ferramenta pública | Proibido |
| Decisão crítica automatizada | Exige avaliação |

---

# 40. Treinamento e Capacitação

Usuários precisam compreender:

- limitações;
- risco de erro;
- proteção de dados;
- verificação de respostas;
- uso de prompts;
- responsabilidade;
- regras organizacionais.

---

# 41. Documentação

Cada solução relevante deve possuir documentação suficiente.

Exemplo:

```text
Objetivo
Arquitetura
Modelo
Dados
Responsável
Riscos
Controles
Integrações
Critérios de uso
Monitoramento
Contingência
```

---

# 42. Auditoria

Auditoria pode verificar:

- inventário;
- aprovações;
- riscos;
- logs;
- controles;
- responsáveis;
- dados;
- fornecedores;
- revisões.

---

# 43. Evidências

Exemplos:

- registros de aprovação;
- avaliações de risco;
- contratos;
- testes;
- logs;
- relatórios;
- atas;
- inventário;
- registros de incidente;
- métricas.

---

# 44. Referências de Governança

Este domínio pode utilizar como referência frameworks e normas reconhecidos, como:

- ISO/IEC 42001;
- NIST AI Risk Management Framework;
- princípios de governança de dados;
- gestão de riscos corporativos;
- segurança da informação;
- privacidade;
- práticas de governança de TI.

As referências devem ser adaptadas ao contexto da organização, ao nível de risco e às obrigações aplicáveis.

---

# 45. Critérios de Maturidade

| Nível | Situação |
|---|---|
| 0 | Uso de IA desconhecido e não controlado |
| 1 | Uso pontual e informal |
| 2 | Inventário e regras básicas |
| 3 | Casos avaliados, aprovados e documentados |
| 4 | Riscos, métricas e ciclo de vida controlados |
| 5 | Governança integrada, mensurada e continuamente melhorada |

A avaliação pode considerar:

- política;
- inventário;
- risco;
- dados;
- segurança;
- responsáveis;
- monitoramento;
- auditoria;
- melhoria contínua.

---

# 46. Perguntas Orientadoras

## Estratégia

- Por que a IA está sendo utilizada?
- Qual benefício é esperado?
- Existe alternativa mais simples?

## Risco

- Qual o impacto de uma resposta incorreta?
- Existe revisão humana?
- O processo é reversível?

## Dados

- Quais dados são utilizados?
- Eles podem ser enviados ao fornecedor?
- Existe retenção?

## Segurança

- Quais permissões a solução possui?
- Há credenciais ou integrações?
- Existem logs?

## Operação

- Quem é responsável?
- Como falhas são tratadas?
- Existe contingência?

## Governança

- O caso está inventariado?
- Foi aprovado?
- Existe revisão periódica?
- Os resultados são medidos?

---

# 47. Entregáveis Esperados

Este domínio pode produzir:

- política de IA;
- inventário de IA;
- catálogo de casos de uso;
- matriz de risco;
- checklist de avaliação;
- formulário de aprovação;
- matriz RACI;
- inventário de modelos;
- avaliação de fornecedores;
- registro de incidentes;
- modelos de homologação;
- dashboards;
- indicadores;
- relatórios;
- procedimentos de revisão;
- plano de descontinuação.

---

# Resultado esperado

Uma organização capaz de utilizar Inteligência Artificial de forma **planejada, rastreável e proporcional ao risco**, com casos de uso conhecidos, responsáveis definidos, dados protegidos, controles estabelecidos, resultados monitorados e mecanismos formais de revisão e melhoria contínua.
