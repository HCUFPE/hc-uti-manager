## 1. Backend: Parâmetro e Lógica de Troca (Swap)

- [x] 1.1 Adicionar o parâmetro `incluir_reservados` na rota `/api/leitos/disponiveis` e no `LeitosController`
- [x] 1.2 Implementar a lógica de troca (swap) no método `remanejar_reserva` do `SolicitacaoLeitoController` caso o leito de destino já possua reserva ativa

## 2. Frontend: Visualização e Seleção no Remanejamento

- [x] 2.1 Atualizar o modal de remanejamento em `frontend/src/views/Home.vue` para incluir leitos reservados e exibir a sinalização de Troca
- [x] 2.2 Atualizar o modal de remanejamento em `frontend/src/views/Solicitacoes.vue` para incluir leitos reservados e exibir a sinalização de Troca
