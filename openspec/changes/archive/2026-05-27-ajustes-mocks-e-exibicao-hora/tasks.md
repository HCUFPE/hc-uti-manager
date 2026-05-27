## 1. Backend Modifications

- [x] 1.1 Add mock entries for prontuário 6 (tomorrow) and 7 (in 2 days) in `SolicitacaoLeitoController.consultar_dados_aghu`

## 2. Frontend Modifications

- [x] 2.1 Add surgery hour details in "Aguardando Reserva de Leito" grid inside `Solicitacoes.vue`
- [x] 2.2 Add surgery hour details in "Solicitações com Vagas Reservadas" grid inside `Solicitacoes.vue`

## 3. Verification

- [x] 3.1 Verify frontend compilation with `npm run build`
- [x] 3.2 Add a new solicitation using prontuário 6 and verify it schedules for tomorrow, and prontuário 7 for after tomorrow
