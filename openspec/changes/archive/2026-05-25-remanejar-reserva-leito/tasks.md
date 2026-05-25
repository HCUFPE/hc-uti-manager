## 1. Backend Implementation

- [x] 1.1 Implementar a lógica de transação para remanejar a reserva entre leitos na classe `LeitoEstadoProvider` em `src/providers/implementations/leito_estado_provider.py`.
- [x] 1.2 Implementar o método `remanejar_reserva` na classe `SolicitacaoLeitoController` em `src/controllers/solicitacao_leito_controller.py`, validando a disponibilidade do leito alvo.
- [x] 1.3 Criar a rota `POST /api/solicitacoes/{sol_id}/remanejar-reserva` em `src/routers/solicitacoes_leito.py` com proteção por perfil (apenas Administrador e UTI).

## 2. Frontend Implementation

- [x] 2.1 Adicionar o botão "Mudar Leito" nos cards de leito reservado em `frontend/src/components/BedCard.vue` para os perfis autorizados.
- [x] 2.2 Adicionar o botão "Mudar Leito" na fila de solicitações reservadas em `frontend/src/views/Solicitacoes.vue`.
- [x] 2.3 Implementar o modal de escolha de novo leito para remanejamento e os respectivos handlers de chamada à API em `frontend/src/views/Home.vue` e `frontend/src/views/Solicitacoes.vue`.

## 3. Verification

- [x] 3.1 Validar que o remanejamento direto transfere a reserva no censo sem deixar registros órfãos ou duplicados.
- [x] 3.2 Validar que o remanejamento registra a ação contendo leito de origem e destino no histórico de ações.
