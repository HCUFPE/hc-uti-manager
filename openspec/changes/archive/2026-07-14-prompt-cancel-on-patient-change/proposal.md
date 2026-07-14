## Why

Quando um usuário edita uma solicitação (reservada ou pendente) e troca o prontuário para outro paciente, o sistema automaticamente cancelava a solicitação do paciente anterior. Agora, o Bloco Cirúrgico (solicitante) poderá escolher se prefere cancelar a solicitação antiga ou deixá-la ativa na lista de solicitações pendentes (caso a cirurgia antiga ainda precise ocorrer).

## What Changes

- **Backend (`solicitacao_leito_controller.py`):**
  - Receber o campo `cancelar_antiga` (booleano) no payload do PATCH de edição.
  - Se `cancelar_antiga` for falso, atualizar o status do paciente antigo para `"Pendente"` em vez de `"Cancelada"`.
  - Ajustar logs de histórico de acordo.

- **Frontend (`Solicitacoes.vue`):**
  - Quando o prontuário for modificado na edição de uma solicitação, exibir modal de confirmação.
  - Oferecer as opções: "Cancelar Antiga" (`cancelar_antiga: true`), "Voltar para a Fila" (`cancelar_antiga: false`) ou "Cancelar Alteração".

## Capabilities

### Modified Capabilities
- `solicitacoes`: Confirmação de ação ao alterar o paciente de uma solicitação de vaga.
