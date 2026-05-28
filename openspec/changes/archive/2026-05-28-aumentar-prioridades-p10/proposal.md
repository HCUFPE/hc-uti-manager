## Why

Currently, when creating or editing a bed request, users can only choose priorities from `P1` (highest) to `P5` (lowest). To allow finer granularity in priority classification for the UTI, the selection range needs to be expanded up to `P10`.

## What Changes

- **Priority Selection Update (`Solicitacoes.vue`)**:
  - Extend the select dropdown options for priority in the new/edit request modal to include `P6` through `P10`.
  - Mark `P10` as the lowest priority.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- None

## Impact

- `frontend/src/views/Solicitacoes.vue`
