## ADDED Requirements

### Requirement: Revert alert title differentiation for altered alta destination
The alerts generated for `alteracao_destino` SHALL always use the title "Destino de Alta Definido" regardless of whether the history action is "Definiu destino de alta" or "Alterou destino de alta".

#### Scenario: Generate alert for defined destination
- **WHEN** the system generates alerts for type `alteracao_destino` with action "Definiu destino de alta"
- **THEN** the alert title SHALL be "Destino de Alta Definido".

#### Scenario: Generate alert for altered destination
- **WHEN** the system generates alerts for type `alteracao_destino` with action "Alterou destino de alta"
- **THEN** the alert title SHALL be "Destino de Alta Definido".

### Requirement: Script to correct historical database logs
The system SHALL have a utility script to retroactively find and correct duplicate `alteracao_destino` history logs in the database.

#### Scenario: Run correction script on historical database
- **WHEN** the correction utility script is executed
- **THEN** for each patient, only the first chronological `alteracao_destino` action SHALL remain "Definiu destino de alta" (or unaltered), and all subsequent chronologically ordered `alteracao_destino` actions for that patient SHALL be updated to "Alterou destino de alta".
