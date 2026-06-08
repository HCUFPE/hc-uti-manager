## Why

Atualmente, ao criar uma nova solicitação de leito, a prioridade selecionada pelo usuário no formulário de criação (payload contendo o campo `prioridade`, ex: `"P3"`) não é gravada no banco de dados e nem passada como foco para a ordenação automática. Isso faz com que a prioridade inicial seja sempre sobrescrita puramente de forma cronológica, e o usuário precise editar a solicitação logo após criá-la para ajustar a prioridade desejada.

## What Changes

- Gravação da prioridade enviada no payload ao criar uma nova solicitação de leito.
- Passagem do id da nova solicitação e da prioridade desejada ao chamar o método `_sincronizar_prioridades` ao final da criação da solicitação.

## Capabilities

### New Capabilities

<!-- Nenhuma nova capability está sendo introduzida -->

### Modified Capabilities

- `solicitacao-leitos`: A prioridade manual definida pelo usuário no ato de criação de uma solicitação de leito deve ser considerada e preservada na fila.

## Impact

- Afeta `criar_solicitacao` em `src/controllers/solicitacao_leito_controller.py`.
