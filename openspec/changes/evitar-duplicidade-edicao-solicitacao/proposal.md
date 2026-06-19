## Why

Atualmente, ao editar uma solicitação ativa com status "Reservado" para alterar o prontuário do paciente (fluxo de troca de paciente), o sistema cria um novo registro de solicitação sem validar se o paciente de destino já possui uma solicitação ativa ("Pendente" ou "Reservado"). Isso gera duplicidade de solicitações ativas para o mesmo prontuário no banco de dados.

## What Changes

- **Detecção de Duplicidade na Edição**: O sistema irá verificar se o novo prontuário informado já possui uma solicitação ativa ("Pendente" ou "Reservado") na base de dados.
- **Mesclagem Inteligente (Merge)**: 
  - Se o novo paciente já possuir uma solicitação "Pendente" ativa, essa solicitação existente será promovida para "Reservado" (vinculando-a ao leito de destino). A solicitação do paciente de origem será alterada para "Cancelada" e a sua reserva de leito física será transferida no banco de dados.
  - Caso contrário (se não houver solicitação ativa para o novo paciente), o sistema criará uma nova solicitação "Reservado" para ele, cancelando a do paciente de origem (comportamento atual).
- **Registro no Histórico**: O fluxo de mesclagem registrará adequadamente as movimentações e o cancelamento correspondente no histórico de ações.

## Capabilities

### New Capabilities

*(Nenhuma nova funcionalidade será introduzida)*

### Modified Capabilities

- `solicitacao-leitos`: O fluxo de edição de solicitação (`editar_solicitacao`) passa a validar duplicidades e a mesclar de forma inteligente solicitações pendentes preexistentes do paciente de destino ao transferir reservas de leitos.

## Impact

- **Backend (`solicitacao_leito_controller.py`)**:
  - Ajuste do método `editar_solicitacao` para implementar a validação de prontuário existente e a lógica de promoção/mesclagem da solicitação pendente do paciente de destino.
  - Gravação correta no histórico de ações.
