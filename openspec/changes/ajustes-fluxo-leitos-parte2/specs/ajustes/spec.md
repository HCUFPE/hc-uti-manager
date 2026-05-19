# Spec: ajustes-fluxo-leitos-parte2

## Backend Specifications

### API Updates

#### 1. `DELETE /api/altas/{alta_id}`
- **Route**: `src/routers/altas.py`
- **Input**:
  - Path: `alta_id: int`
  - Query: `motivo: str` (Required)
- **Logic**:
  - Verify the user has UTI permissions.
  - Call `controller.cancelar_alta(alta_id)`.
  - Record history: `detalhes=f"Alta #{alta_id} cancelada. Motivo: {motivo}"`.

#### 2. `POST /api/solicitacoes/{sol_id}/cancelar-reserva`
- **Route**: `src/routers/solicitacoes_leito.py`
- **Input**:
  - Path: `sol_id: int`
  - Query: `motivo: str` (Already implemented in previous spec)
- **Logic**:
  - Nothing changes in backend, but frontend will send specific Motivo UTI strings.

### Controller Updates

#### 1. `src/controllers/leitos_controller.py`
- **Function**: `listar_leitos`
- **Logic Modification**:
  ```python
  # Se não apareceu no AGHU ainda, verificamos CONFLITO
  prontuario_aghu_neste_leito = leito.get('prontuario_atual')
  if prontuario_aghu_neste_leito and prontuario_reserva:
      # Alguém ocupou o leito e não é quem reservamos
      is_alta = leito.get('alta_solicitada', False)
      leito['conflito_reserva'] = not is_alta
  else:
      leito['conflito_reserva'] = False
  ```

## Frontend Specifications

### Views & Components Updates

#### 1. `Solicitacoes.vue`
- Define a new constant: `const MOTIVOS_CANCELAMENTO_RESERVA = ['Motivo UTI A', 'Motivo UTI B', 'Motivo UTI C']`.
- In the cancellation modal `<select>`, dynamically use `MOTIVOS_CANCELAMENTO_RESERVA` if `isCancelamentoReserva` is true. Otherwise, use `MOTIVOS_CANCELAMENTO`.

#### 2. `BedCard.vue` (Cancel Alta)
- Add a cancellation modal similar to the one in `Solicitacoes.vue`.
- Define constant: `const MOTIVOS_CANCELAMENTO_ALTA = ['Cancelamento de Alta Tipo A', 'Cancelamento de Alta Tipo B', 'Cancelamento de Alta Tipo C']`.
- On clicking "Cancelar Alta":
  - Open modal to select motif.
  - Send the motif as a query parameter via `DELETE /api/altas/{id}?motivo={encoded}`.
