## Why

1. Atualmente, o sistema permite a criação de múltiplas solicitações de leito para o mesmo prontuário de paciente de forma simultânea (duplicidade), gerando inconsistências no censo e fila.
2. Ao cadastrar uma solicitação sem prioridade manual definida, o sincronizador de prioridades acaba omitindo o registro em foco do bucket por causa de um bug de exclusão na ordenação, fazendo com que a prioridade dele fique em branco/nula.

## What Changes

- Implementação de validação em `criar_solicitacao` para rejeitar o cadastro de um prontuário que possua uma solicitação ativa com status "Pendente" ou "Reservado".
- Correção no método `_sincronizar_prioridades` para não excluir a solicitação em foco do bucket quando não há prioridade manual desejada no sincronismo.

## Capabilities

### New Capabilities

<!-- Nenhuma nova capability está sendo introduzida -->

### Modified Capabilities

- `solicitacao-leitos`: O cadastro de solicitação deve impedir a duplicidade para prontuários com solicitações ativas e a ordenação de prioridades deve ser consistente para novos cadastros sem prioridade manual pré-definida.

## Impact

- Afeta `criar_solicitacao` e `_sincronizar_prioridades` em `src/controllers/solicitacao_leito_controller.py`.
