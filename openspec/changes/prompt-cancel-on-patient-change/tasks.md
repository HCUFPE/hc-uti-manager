## 1. Implementação no Backend

- [x] 1.1 Atualizar `src/controllers/solicitacao_leito_controller.py` para receber `cancelar_antiga` e ajustar o status do paciente anterior para `Cancelada` ou `Pendente`, além de seus logs correspondentes.

## 2. Implementação no Frontend

- [x] 2.1 Adicionar modal `showModalConfirmacaoTrocaProntuario` em `frontend/src/views/Solicitacoes.vue`.
- [x] 2.2 Integrar a lógica de interceptação de edição e envio da flag `cancelar_antiga` na função `salvarNova` / `confirmarSalvarEdicao`.

## 3. Validação

- [x] 3.1 Validar se a alteração de prontuário exibe a confirmação e executa corretamente o comportamento selecionado na lista de solicitações.
