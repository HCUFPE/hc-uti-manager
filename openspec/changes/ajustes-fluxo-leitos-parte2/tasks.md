## 1. Frontend Updates

- [x] 1.1 In `Solicitacoes.vue`, create the `MOTIVOS_CANCELAMENTO_RESERVA` array and conditionally use it in the cancellation modal if `isCancelamentoReserva` is true.
- [x] 1.2 In `BedCard.vue` (or the component handling Alta Cancellation), implement a modal for "Cancelar Alta" with a select input populated by `MOTIVOS_CANCELAMENTO_ALTA`.
- [x] 1.3 In `BedCard.vue`, update the `cancelarAlta` method to send the `motivo` via query parameter to the `DELETE /api/altas/{id}` endpoint.

## 2. Backend Updates

- [x] 2.1 In `src/routers/altas.py`, update `DELETE /{alta_id}` to require a `motivo: str` Query parameter.
- [x] 2.2 In `src/routers/altas.py`, update the history `registrar` call within `cancelar_alta` to append the selected motif.
- [x] 2.3 In `src/controllers/leitos_controller.py`, fix the conflict logic inside `listar_leitos` so it only flags a conflict if `prontuario_reserva` is present.
