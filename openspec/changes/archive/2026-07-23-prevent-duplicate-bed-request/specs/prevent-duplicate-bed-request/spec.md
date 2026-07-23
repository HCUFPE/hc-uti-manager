## ADDED Requirements

### Requirement: Block solicitation for patients already occupying a bed
The system SHALL prevent the creation or editing of a bed request (solicitação de leito) if the patient's medical record (prontuário) is already occupying a physical bed in the UTI according to the real-time AGHu census.

#### Scenario: Creating a request for a patient who already has a bed
- **WHEN** the operator attempts to create a request for a medical record that is present in the active AGHu census as occupying a bed
- **THEN** the system SHALL reject the request with HTTP Status 400 and detail "O paciente deste prontuário já ocupa o Leito X da UTI! A solicitação não poderá ser criada." where X is the identifier of the occupied bed.

#### Scenario: Editing a request to a patient who already has a bed
- **WHEN** the operator attempts to change a request's medical record to one that is present in the active AGHu census as occupying a bed
- **THEN** the system SHALL reject the modification with HTTP Status 400 and detail "O paciente deste prontuário já ocupa o Leito X da UTI! A solicitação não poderá ser criada." where X is the identifier of the occupied bed.
