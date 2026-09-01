## ADDED Requirements

### Requirement: Exibição da Especialidade do Paciente nas Solicitações de Alta
O sistema MUST apresentar a especialidade médica atual do paciente na lista de solicitações de alta do painel do NIR/UTI, posicionada como uma badge visualmente identificável antes da data e hora de criação da solicitação.

#### Scenario: Visualização de especialidade na lista de altas
- **WHEN** o usuário acessa a tela de solicitações de alta
- **THEN** o sistema SHALL renderizar a especialidade do paciente (`alta.especialidade`) em uma badge ao lado esquerdo da data de criação de cada solicitação
