## 1. Backend Changes

- [x] 1.1 Atualizar a rota `DELETE /api/leitos/{leito_id}/reserva` em [leito.py](file:///c:/Users/daniel.turmina/Documents/HC-UTI-Manager/src/routers/leito.py) para aceitar e exigir o parâmetro `motivo`, concatenando o valor aos detalhes do registro de histórico correspondente.

## 2. Frontend Changes

- [x] 2.1 Atualizar `MOTIVOS_CANCELAMENTO_RESERVA` em [Solicitacoes.vue](file:///c:/Users/daniel.turmina/Documents/HC-UTI-Manager/frontend/src/views/Solicitacoes.vue) com as novas opções clínicas.
- [x] 2.2 Atualizar `MOTIVOS_CANCELAMENTO_ALTA` em [Home.vue](file:///c:/Users/daniel.turmina/Documents/HC-UTI-Manager/frontend/src/views/Home.vue) com as novas opções ("Piora Clínica" e "Leito de Enfermaria Indisponível").
- [x] 2.3 Adicionar `MOTIVOS_CANCELAMENTO_RESERVA` e implementar um modal de confirmação em [Home.vue](file:///c:/Users/daniel.turmina/Documents/HC-UTI-Manager/frontend/src/views/Home.vue) para capturar o motivo da reserva antes de disparar a requisição HTTP.
- [x] 2.4 Atualizar `MOTIVOS_CANCELAMENTO` em [Solicitacoes.vue](file:///c:/Users/daniel.turmina/Documents/HC-UTI-Manager/frontend/src/views/Solicitacoes.vue) com as novas opções de cancelamento pendente.

## 3. Verification

- [x] 3.1 Validar que cancelar uma reserva a partir do card do leito agora abre um modal exigindo a seleção do motivo correspondente.
- [x] 3.2 Validar que o motivo escolhido é registrado com sucesso no histórico de ações do backend.
