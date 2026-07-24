## Requirements

### Requirement: Refine Login View Labels and Orthography
The login view interface SHALL display correct accentuation and casing for Brazilian Portuguese.

#### Scenario: Verify system description text
- **WHEN** the login page is loaded
- **THEN** the system description SHALL read "Sistema de Gestão de Leitos de Terapia Intensiva"
- **AND** the hospital name SHALL read "do Hospital das Clínicas da UFPE".

#### Scenario: Verify input field labels and placeholders
- **WHEN** the username input is rendered
- **THEN** the label SHALL be "Usuário"
- **AND** the placeholder SHALL be "Seu usuário"
- **AND** any validation error messages related to the username SHALL refer to it as "usuário".

#### Scenario: Verify network login hint text
- **WHEN** the network login hint is rendered at the bottom
- **THEN** it SHALL display: "Utilize login e senha de rede".

### Requirement: Remove Redundant Login Controls
The login page SHALL NOT display controls that are irrelevant to LDAP/Active Directory authentication.

#### Scenario: Check header and forgot password button
- **WHEN** the login page is loaded
- **THEN** the heading "Bem-vindo de Volta" SHALL NOT be displayed
- **AND** the button "Esqueceu a senha?" SHALL NOT be displayed.
