# track-alert-readers Specification

## Purpose
TBD - created by archiving change track-alert-readers. Update Purpose after archive.
## Requirements
### Requirement: Record User Read Receipt for Alerts
When a user marks an alert as read, the system MUST record the current timestamp and the username of the active user.

#### Scenario: Verify backend records reader details
- **GIVEN** a logged-in user `"manuelle.holanda"`
- **WHEN** they call the API to mark alert `1` as read
- **THEN** the alert record SHALL set `lido = True`
- **AND** the `lido_por` field SHALL be set to `"manuelle.holanda"`
- **AND** the `lido_em` field SHALL be set to the current UTC time.

### Requirement: Display Reader Details in UI
The user interface for alerts MUST display the timestamp of creation and, if read, the timestamp and username of the reader.

#### Scenario: Display read receipt on alerts page
- **WHEN** an alert is rendered on the alerts view
- **THEN** it SHALL display the creation time formatted as `"Emitido em: <dataHora>"`
- **AND** if marked as read, it SHALL display the reading time and username formatted as `"Lido em: <lido_em> (<lido_por>)"`.

