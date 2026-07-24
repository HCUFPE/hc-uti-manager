## ADDED Requirements

### Requirement: Hide completed requests by default with expansion control
The bed requests page (Solicitações de Vaga) SHALL hide completed requests (solicitações com status "Concluída") by default, presenting a collapsible header that shows the count of completed requests and can be toggled by the user to expand or collapse the section.

#### Scenario: Page load with completed requests
- **WHEN** the requests page is loaded and there are completed requests
- **THEN** the completed requests section SHALL be collapsed/hidden by default, showing only the section header with the total count of completed requests.

#### Scenario: Toggle completed requests visibility
- **WHEN** the user clicks the collapsible header or toggle button in the completed requests section
- **THEN** the system SHALL toggle the visibility of the completed requests cards (expanding if collapsed, and collapsing if expanded).

### Requirement: Display conclusion date and time in completed requests
Each completed request card SHALL display the date and time when the request was concluded.

#### Scenario: View completed request card
- **WHEN** the completed requests section is expanded and cards are visible
- **THEN** each card SHALL show a small text label indicating the conclusion date and time (e.g., "Concluído em: DD/MM/AAAA HH:MM").
