# Design: ajustes-fluxo-leitos-parte2

## Component Changes

### Frontend
1. **`Solicitacoes.vue`**:
   - Introduce `MOTIVOS_CANCELAMENTO_RESERVA` array `['Motivo UTI A', 'Motivo UTI B', 'Motivo UTI C']`.
   - Conditionally use `MOTIVOS_CANCELAMENTO_RESERVA` when `isCancelamentoReserva` is true, otherwise use the existing `MOTIVOS_CANCELAMENTO` (which might be for solicitantes).
   
2. **`BedCard.vue` (or component handling "Cancelar Alta")**:
   - Instead of a simple `confirm()`, implement a modal for canceling an Alta.
   - The modal will have a select input populated with `['Cancelamento de Alta Tipo A', 'Cancelamento de Alta Tipo B', 'Cancelamento de Alta Tipo C']`.
   - Dispatch the selected motif via query parameter to `DELETE /api/altas/{alta_id}?motivo=...`.

### Backend
1. **`src/routers/altas.py`**:
   - In `DELETE /{alta_id}`, accept an optional `motivo: str` as a Query parameter.
   - Pass the motif to the `historico.registrar` details string. Example: `detalhes=f"Alta #{alta_id} cancelada. Motivo: {motivo}"`.
   
2. **`src/controllers/leitos_controller.py`**:
   - In `listar_leitos`, locate the condition where `prontuario_reserva` is empty (inside `if lto_id in estados: ... else: ...`).
   - Fix logic:
     ```python
     # Only check for conflict if there actually IS a reservation
     if prontuario_reserva:
         leito['conflito_reserva'] = not is_alta
     else:
         leito['conflito_reserva'] = False
     ```
   - Actually, wait, let's review the current logic of `leitos_controller.py`:
     ```python
     if lto_id in estados:
         est = estados[lto_id]
         prontuario_reserva = str(est.prontuario_proximo or "").strip()
         
         if prontuario_reserva and prontuario_reserva in census_map:
             # handle fulfillment
         else:
             prontuario_aghu_neste_leito = leito.get('prontuario_atual')
             # FIX: only flag conflict if there's a reservation pending
             if prontuario_aghu_neste_leito and prontuario_reserva:
                 is_alta = leito.get('alta_solicitada', False)
                 leito['conflito_reserva'] = not is_alta
             else:
                 leito['conflito_reserva'] = False
     ```
     This prevents raising a conflict flag for a bed that merely has an empty reservation object (e.g. state created for Alta).

3. **`AlertaController` & `AltasController` Notification Integration**:
   - `AltasController` currently does:
     ```python
     await self.historico_provider.registrar(
         operador=operador,
         tipo="alteracao_destino",
         acao="Definiu destino de alta",
         detalhes=f"Leito {alvo.lto_id}: Destino {payload['leitoDestino']}",
         prontuario=str(alvo.prontuario)
     )
     ```
   - `AlertaController` correctly maps `alteracao_destino` to an alert targeting the UTI (`perfil_alvo: None`). 
   - We will just ensure this process is working and requires no major rewrites, fulfilling the user's requirement.

## Flow Changes
- **UTI Reservation Cancellation**: Same flow, updated modal options.
- **UTI Alta Cancellation**: Added modal step to select a motif.
- **NIR Destination Updates**: Generates alerts for UTI natively via existing infrastructure.
- **Leitos Conflict Logic**: The false positive bug is resolved, preventing confusion.
