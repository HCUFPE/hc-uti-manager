## Why

When a bed referral is released by the UTI team (`encaminhamentoLiberado` is `true`), the elapsed wait time stops and is recorded in the database. However, on the frontend Bed Card UI, the wait timer clock and the yellow "Cirurgia Concluída" badge continue to display and run because the template only checks `cirurgiaFinalizada` to render them. We need to hide the clock/timer and update the badge status to "Encaminhamento Liberado" once the referral is released.

## What Changes

- **Frontend Update (`BedCard.vue`)**:
  - Restrict the display of the wait timer clock and the "Cirurgia Concluída" badge to cases where `cirurgiaFinalizada` is true AND `encaminhamentoLiberado` is false (`cirurgiaFinalizada && !encaminhamentoLiberado`).
  - Introduce a new state badge/indicator "Encaminhamento Liberado" (with emerald theme and dot) when `encaminhamentoLiberado` is true to match the green styling of the card.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- None

## Impact

- `frontend/src/components/BedCard.vue`
