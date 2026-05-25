## 1. Regras de Cancelamento

- [x] 1.1 Atualizar `src/routers/solicitacoes_leito.py` (ou controller correspondente) para não bloquear a exclusão (`DELETE /{sol_id}`) caso a solicitação esteja reservada, mas apenas se o usuário pertencer aos perfis autorizados (BC, BC-ADMIN, COB, etc.).
- [x] 1.2 Garantir que ao excluir uma solicitação que está reservada, a reserva física atrelada ao leito seja limpa antes da exclusão (`estado_provider.limpar_reserva_por_solicitacao`).
- [x] 1.3 Atualizar o frontend (`Solicitacoes.vue`) para exibir o botão "Cancelar Solicitação" para usuários autorizados mesmo quando a solicitação está com status Reservado.
- [x] 1.4 Adicionar suporte ao campo "motivo" na rota de cancelamento de reserva (`POST /{sol_id}/cancelar-reserva`) em `src/routers/solicitacoes_leito.py` e exigi-lo no frontend ao clicar em "Cancelar Reserva".

## 2. Leitos e Disponibilidade

- [x] 2.1 Em `src/routers/leito.py` (ou `leito_estado_provider.py`), ajustar a query de `get_disponiveis` (leitos disponíveis para reserva) para incluir também leitos com status `Limpeza` ou `Higienização`.

## 3. Correções na Edição (Sincronização e Histórico)

- [x] 3.1 Na função `editar_solicitacao` do controller de solicitações de leito, injetar a dependência ou usar o `estado_provider` para atualizar os campos do paciente (prontuário, idade, especialidade, etc.) no leito físico associado caso a solicitação possua uma reserva.
- [x] 3.2 Em `src/routers/solicitacoes_leito.py`, no endpoint `PATCH /{sol_id}`, ajustar a checagem que define `tipo_hist = "alteracao_prioridade"` para validar não só se `"prioridade" in payload`, mas se o valor é de fato **diferente** do valor que já constava na solicitação original.
