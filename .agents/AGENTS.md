# Regras do Projeto - HC UTI Manager

## Sincronização de Documentação e Requisitos (Spec-Driven Development)

1. **Análise de Impacto de Novas Funcionalidades:**
   * Sempre que for solicitada a criação de uma nova funcionalidade, nova tela, nova API ou mudança em regras de negócio, o agente **DEVE** obrigatoriamente abrir e analisar os arquivos de especificação de concepção localizados na pasta [docs/projeto_inicial/](./docs/projeto_inicial/), o [README.md](./README.md) principal e os documentos de desenvolvimento de `/docs/` (como `SETUP.md`, `data-model.md` e `ARCHITECTURE.md`) antes de fazer qualquer alteração no código.

2. **Arquivos Críticos a Revisar e Atualizar:**
   * **Requisitos:** [02-requisitos.md](./docs/projeto_inicial/02-requisitos.md) — Adicionar ou atualizar requisitos funcionais (RF) ou não funcionais (RNF).
   * **Casos de Uso:** [03-casos-uso.md](./docs/projeto_inicial/03-casos-uso.md) — Adicionar novos fluxos de usuários ou diagramas Mermaid de fluxo de dados.
   * **Modelo de Dados:** [04-modelo-dados.md](./docs/projeto_inicial/04-modelo-dados.md) — Atualizar entidades, relacionamentos ou payloads JSON do banco.
   * **Interfaces & APIs:** [05-interfaces.md](./docs/projeto_inicial/05-interfaces.md) — Documentar novos endpoints REST, parâmetros e contratos de payload.
   * **Metas e Progresso:** [SPEC.md](./docs/projeto_inicial/SPEC.md) — Manter o Task Breakdown e metas sincronizados.
   * **Manuais e Guias de Desenvolvimento:**
     * [docs/SETUP.md](./docs/SETUP.md) — Manter atualizadas as rotinas e comandos de deploy, backup e configuração do ambiente.
     * [docs/data-model.md](./docs/data-model.md) — Sincronizar qualquer novo campo de reatividade de UI do frontend ou payloads de API.
     * [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — Atualizar regras de segurança e novos fluxos de dados arquiteturais.

3. **Fluxo de Trabalho:**
   * O agente deve propor as atualizações nas especificações em conjunto com o plano de implementação do código, garantindo que o repositório mantenha a verdade da especificação sincronizada com a verdade do código executável.
