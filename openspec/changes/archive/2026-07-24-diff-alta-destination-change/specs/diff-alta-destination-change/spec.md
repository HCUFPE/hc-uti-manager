## ADDED Requirements

### Requirement: Distinguish between defining and modifying an alta destination in the history
When the NIR defines a destination bed for the first time, the history action SHALL be recorded as "Definiu destino de alta". If a destination bed was already defined and NIR changes it, the history action SHALL be recorded as "Alterou destino de alta".

#### Scenario: NIR defines destination for the first time
- **WHEN** NIR sets the destination bed and the previous destination was empty or null
- **THEN** the system SHALL record a history action of "Definiu destino de alta".

#### Scenario: NIR modifies already defined destination
- **WHEN** NIR sets a new destination bed and there was already a previous destination bed defined
- **THEN** the system SHALL record a history action of "Alterou destino de alta".

### Requirement: Differentiate alert title when destination is modified
When generating alerts from the history, if the history action indicates an alteration of the destination, the alert title sent to the ICU (UTI) SHALL be "Alterou o Destino de Alta" instead of "Destino de Alta Definido".

#### Scenario: Generate alert for modified destination
- **WHEN** the system generates alerts and finds a history event with action "Alterou destino de alta"
- **THEN** the generated alert title SHALL be "Alterou o Destino de Alta".
