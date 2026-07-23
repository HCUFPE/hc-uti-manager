## Why

Quando um operador cria ou edita uma solicitação de leito na UTI, é possível que o prontuário selecionado já esteja ocupando fisicamente um leito na UTI. Permitir uma nova solicitação nesses casos é um erro operacional que gera duplicidades desnecessárias e poluição visual na fila.

## What Changes

- Validação no ato de criação de solicitação: Caso o prontuário fornecido já possua um leito ocupado no censo em tempo real do AGHu, a criação da solicitação será bloqueada com a mensagem: "O paciente deste prontuário já ocupa o Leito X da UTI! A solicitação não poderá ser criada."
- Validação no ato de edição/troca de prontuário em solicitação existente: O mesmo bloqueio deve se aplicar se houver troca de prontuário por um que já ocupa leito.

## Capabilities

### New Capabilities
<!-- Capabilities being introduced. Replace <name> with kebab-case identifier (e.g., user-auth, data-export, api-rate-limiting). Each creates specs/<name>/spec.md -->
- `prevent-duplicate-bed-request`: Validação em tempo real com base no censo do AGHu para impedir novas solicitações de leito para pacientes que já estão internados na UTI.

### Modified Capabilities
<!-- Existing capabilities whose REQUIREMENTS are changing (not just implementation).
     Only list here if spec-level behavior changes. Each needs a delta spec file.
     Use existing spec names from openspec/specs/. Leave empty if no requirement changes. -->

## Impact

- Modificações no `SolicitacaoLeitoController` (métodos `criar_solicitacao` e `editar_solicitacao`).
- Modificação na injeção de dependências no `get_solicitacao_leito_controller` do `dependencies.py` para fornecer o `LeitoAghuProvider`.
