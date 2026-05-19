# Proposal: ajustes-fluxo-leitos-parte2

## Problem Statement

1. **Specific Cancel Reasons for UTI**: Currently, when the UTI cancels a bed reservation, they might see the same cancellation motifs as the *solicitantes*. The UTI needs specific motives (e.g., "Motivo UTI A", "Motivo UTI B", "Motivo UTI C").
2. **NIR Destination Change Alerts**: When the NIR changes a patient's destination after an "Alta" request has been made, the UTI must be alerted. While the backend might be generating history events, we need to ensure the UTI is properly notified.
3. **Specific Cancel Reasons for Alta**: When the UTI cancels an "Alta" request, a specific reason must be selected ("Cancelamento de Alta Tipo A", "Cancelamento de Alta Tipo B", "Cancelamento de Alta Tipo C").
4. **False Conflict Alert Bug**: The system incorrectly displays a "CONFLITO DETECTADO" error for beds that have no reservations but are currently occupied.

## Proposed Solution

1. **UTI Reservation Cancel Motives**: 
   - Update the frontend (`Solicitacoes.vue`) to conditionally display specific motifs ("Motivo UTI A", "Motivo UTI B", "Motivo UTI C") when the user is canceling a reservation (which is an action restricted to UTI/Admins).
   
2. **NIR Destination Alert**: 
   - Ensure the backend properly registers `alteracao_destino` in the history when the destination is changed (`PATCH/PUT` in `altas_controller.py`).
   - The `AlertaController` already maps `alteracao_destino` to `perfil_alvo: None` (which targets the UTI). We will verify and ensure the message is clear and the frontend polls/displays this alert.
   
3. **Alta Cancellation Motives**: 
   - Update `altas.py` `DELETE /{alta_id}` to receive a `motivo` query parameter.
   - Update `altas_controller.py` to record the motif in the history event.
   - Update the frontend (`BedCard.vue` or where the "Cancelar Alta" button resides) to display a modal with the motifs "Cancelamento de Alta Tipo A", "Cancelamento de Alta Tipo B", "Cancelamento de Alta Tipo C" before dispatching the cancellation.
   
4. **Fix Conflict Logic in `leitos_controller.py`**:
   - In `listar_leitos`, the logic currently checks if the bed is occupied and assumes a conflict even if `prontuario_reserva` is empty.
   - We will fix the conditional `if prontuario_aghu_neste_leito:` to only set `conflito_reserva = not is_alta` if there is actually a reservation (`if prontuario_reserva:`).
