## Why

During testing, mock data was added to the development bed list in `mock_beds` for `UTI-03` showing an occupied bed (`123456`) with a "next patient" reservation (`987654`) directly in the mock census. In a real scenario, reservations come from the local database, not the hospital census. Because this next patient was hardcoded in the mock census rather than database state, it bypassed the standard database-backed conflict detection logic (which correctly marks a conflict when a reservation exists on a bed occupied by a different patient). We need to verify that conflict detection works and remove this incorrect mock data.

## What Changes

- **Verificação**: Analisar e demonstrar o funcionamento do sistema de detecção de conflitos para leitos com reservas reais vindas do banco de dados.
- **Remoção de Mock**: Remover os campos `"prontuario_proximo": "987654"`, `"nome_proximo": "PACIENTE CHEGANDO"`, e `"hora_cirurgia_proximo": "10:30"` do leito `"UTI-03"` em `mock_beds` no arquivo `src/controllers/leitos_controller.py`.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- None

## Impact

- `src/controllers/leitos_controller.py` (mock beds configuration)
