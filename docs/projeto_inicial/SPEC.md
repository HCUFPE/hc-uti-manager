# SPEC.md — Contrato de Desenvolvimento (SDD)

## 1. Visão Geral e Resultados Esperados

Este documento atua como o contrato de desenvolvimento e especificação técnica de entrega do **HC-UTI Manager**. O sistema fornece uma plataforma centralizada e de alta disponibilidade para gestão de vagas e leitos de UTI, operando de forma híbrida integrada com o AGHU.

### Objetivos de Alto Nível
- [x] Implementar autenticação via LDAP/AD Ebserh com fallback seguro.
- [x] Sincronizar cirurgias eletivas programadas a partir do banco PostgreSQL do AGHU.
- [x] Gerenciar a fila dinâmica de prioridades (P1 a P10) de forma automática.
- [x] Garantir controle de concorrência atômico contra duplicidades de alertas.
- [x] Manter uma trilha de auditoria (logs de ações de usuários) imutável.
- [x] Reservar leitos preventivamente para demandas clínicas (Clínico/COB/HEM) com autolimpeza e swap.

---

## 2. Contexto do Projeto (Documentação de Concepção)

As especificações detalhadas de cada etapa do projeto estão distribuídas nos seguintes documentos locais:
*   [Visão](01-visao.md) — Objetivos gerais do produto, contexto de problemas e atores.
*   [Requisitos](02-requisitos.md) — Lista completa de requisitos funcionais (RF) e não funcionais (RNF).
*   [Casos de Uso](03-casos-uso.md) — Fluxos de ações com diagramas Mermaid estruturados.
*   [Modelo de Dados](04-modelo-dados.md) — Modelagem lógica de tabelas SQLite e schemas JSON.
*   [Interfaces](05-interfaces.md) — Definição das telas gráficas, contratos de APIs e hardware.
*   [Arquitetura](06-arquitetura.md) — Stack técnica de deploy (FastAPI, Nginx, Podman, Systemd).
*   [Glossário](07-glossario.md) — Termos técnicos de negócio e referências normativas.

---

## 3. Limites de Escopo e Guardrails (Anti-Patterns)

**O Desenvolvedor / IA DEVE:**
*   Ler obrigatoriamente todas as chaves, DSNs de bancos de dados e chaves JWT a partir do `.env`.
*   Garantir integridade concorrente encapsulando a lógica de geração de alertas em `asyncio.Lock()`.
*   Mapear e testar todas as migrações locais no SQLite via Alembic.
*   Registrar todas as ações do sistema na tabela append-only `historico_acoes`.

**O Desenvolvedor / IA NÃO DEVE:**
*   Escrever qualquer dado no banco de dados externo do AGHU (PostgreSQL). A conexão deve ser estritamente de leitura (`SELECT`).
*   Burlar a injeção de dependências do FastAPI injetando sessões diretas nos Roteadores sem passar pela camada de Provedores.
*   Permitir a criação de solicitações pendentes ativas duplicadas para o mesmo prontuário de paciente.

---

## 4. Task Breakdown (Plano de Implementação Concluído)

### Fase 1: Infraestrutura e Dados
- [x] **[TASK-001]** Mapeamento do banco híbrido (Postgres remoto para AGHU + SQLite local para censo/fila).
- [x] **[TASK-002]** Configuração e isolamento de containers rootless no Podman Compose com Nginx (HTTPS).
- [x] **[TASK-003]** Criação do serviço Systemd (`hc-uti.service`) e liberação de linger para persistência na VM.

### Fase 2: Regras Clínicas e Painéis
- [x] **[TASK-004]** Painel visual de censo (Bed Cards) interativo com 5 estados de leito.
- [x] **[TASK-005]** Fila dinâmica sequencial automática e priorização clínica de pacientes (P1 a P10).
- [x] **[TASK-006]** Mecanismo de mesclagem e substituição de pacientes (Swap) sem gerar leitos fantasmas ou órfãos.
- [x] **[TASK-007]** Módulo do NIR para regulação e liberação física de leitos de UTI pós-alta.

### Fase 3: Concorrência e Confiabilidade
- [x] **[TASK-008]** Correção de condição de corrida em endpoints de alertas no carregamento de telas concorrentes do front.
- [x] **[TASK-009]** Script de backup automático (`backup_db.sh`) diário rotativo do banco SQLite agendado no cron da VM.

### Fase 4: Recursos Avançados e Ajustes
- [x] **[TASK-010]** Implementação de bloqueio e reserva clínica preventiva de leitos (Clínico/COB/HEM) com autolimpeza e swap.

---

## 5. Critérios de Verificação Global

- [x] Build limpo de produção via Podman Compose na VM de produção.
- [x] Cobertura contra duplicidades concorrentes de alertas (zero registros com mesmo microssegundo).
- [x] Registro inalterável e rastreável de todas as ações de auditoria LGPD no banco de dados.
