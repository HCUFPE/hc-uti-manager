## Context

The system has a conflict detection mechanism in `src/controllers/leitos_controller.py` that flags beds with a `conflito_reserva` alert when a bed is occupied by a different patient in the hospital census than the patient who has a local reservation in the database.

However, in `mock_beds`, the `UTI-03` bed had hardcoded fields for both an occupied patient (`123456`) and a next patient (`987654`) directly in the mock data returned from the censo. Since this mock next patient wasn't stored in the SQLite database, it went to the `else` block of the controller's merge loop where `conflito_reserva` is hardcoded to `False`, bypassing the conflict detection logic entirely.

We need to:
1. Verify the conflict detection system works by checking the controller's handling of database-backed reservations.
2. Remove the mock next patient fields from `UTI-03` to prevent this invalid/confusing mock state.

## Goals / Non-Goals

**Goals:**
- Verify and document that the database-backed conflict detection logic is functioning correctly.
- Clean up `mock_beds` in `src/controllers/leitos_controller.py` to remove `prontuario_proximo` and other next-patient mock fields from the occupied bed `UTI-03`.

**Non-Goals:**
- Rewrite the core reservation conflict detection logic.
- Perform any database schema changes.

## Decisions

### 1. Verification of Conflict Detection Logic
We will verify the code in `src/controllers/leitos_controller.py` by inspecting the logic where `lto_id in estados` is `True`. 
- If a reservation exists for a bed (stored in `estados`), and the bed is occupied (`prontuario_atual` is not `None` in the censo), and the occupant's prontuario does not match the reservation, `conflito_reserva` is set to `not is_alta` (so it detects a conflict if there is no pending alta).
- If the patient occupies the bed and the reservation matches, the reservation is automatically cleared and resolved as `Concluída`.
This logic is sound and functions correctly for real data.

### 2. Remove Hardcoded Next Patient from `UTI-03` Mock
We will edit the `mock_beds` array in `src/controllers/leitos_controller.py` to remove:
- `"prontuario_proximo": "987654"`
- `"nome_proximo": "PACIENTE CHEGANDO"`
- `"hora_cirurgia_proximo": "10:30"`
From `UTI-03`.

## Risks / Trade-offs

- None identified.
