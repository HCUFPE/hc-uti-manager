## Requirements

### Requirement: Include Patient Record in Destination Alerts
The alerts generated for defined destination of alta, altered destination, or released/available destination MUST display the patient's medical record number (prontuário) formatted as `(Prontuário <prontuario>)` at the end of the alert message.

#### Scenario: Verify alert message formatting
- **GIVEN** a destination action occurs for a patient with prontuário `"22341010"`
- **WHEN** the alert is generated
- **THEN** the alert message SHALL append `(Prontuário 22341010)` to the end.
