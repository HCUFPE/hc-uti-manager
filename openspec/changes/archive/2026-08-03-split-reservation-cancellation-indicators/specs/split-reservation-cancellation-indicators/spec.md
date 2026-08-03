## ADDED Requirements

### Requirement: Differentiate Reservation Cancellation Types
The backend MUST identify who initiated a reservation cancellation and classify it as either cancelled by the ICU (`cancelamento_reserva`) or by the requester (`cancelamento_solicitante`).

#### Scenario: Verify requester swap is classified under requester cancellation
- **GIVEN** a request with status `"Reservado"` owned by specialty `"CIRURGIA VASCULAR"`
- **WHEN** the Bloco Cirúrgico swaps the patient
- **THEN** the historical log created for the cancellation of the original reservation MUST have `tipo = "cancelamento_solicitante"`
- **AND** the action text MUST state `"Reserva Cancelada pelo Solicitante (Troca de Paciente)"`.

### Requirement: Differentiate Alert Title on Swap vs Cancellation
When a reservation is modified by the requester, the system MUST generate `"Reserva Remanejada (Troca de Paciente)"` if the reservation was transferred, or `"Reserva Cancelada pelo Solicitante"` if the vacancy was lost.

#### Scenario: Verify alert title on patient swap
- **GIVEN** a historical event with `tipo = "cancelamento_solicitante"` and action containing `"Troca de Paciente"`
- **WHEN** the system generates notifications
- **THEN** the generated alert MUST have `titulo = "Reserva Remanejada (Troca de Paciente)"`.

#### Scenario: Verify alert title on direct cancellation by requester
- **GIVEN** a historical event with `tipo = "cancelamento_solicitante"` representing a direct cancellation of the request
- **WHEN** the system generates notifications
- **THEN** the generated alert MUST have `titulo = "Reserva Cancelada pelo Solicitante"`.

### Requirement: Format Swap History Logs Elegantly
The history logs generated during a patient swap MUST describe the transition clearly for both patients.

#### Scenario: Verify history messages on swap
- **GIVEN** a swap of Patient A to Patient B for a reserved leito
- **WHEN** the swap is completed
- **THEN** the log for Patient A MUST state that their reservation was returned to pending because the leito was remanejador to Patient B
- **AND** the log for Patient B MUST state that they received the reservation from Patient A.

### Requirement: Expose Segregated Metrics in Dashboard
The dashboard indicators screen MUST show separate metrics for cancellations done by the ICU and by the requester.

#### Scenario: Display two separate rows in Summary of Actions
- **WHEN** a user opens the Indicadores page
- **THEN** the table "Resumo de Ações da UTI e Altas (Trabalho)" SHALL contain a row `"Reservas Canceladas pela UTI"`
- **AND** it SHALL contain a separate row `"Reservas Canceladas pelo Solicitante (Troca de Paciente / Suspensão)"`.
