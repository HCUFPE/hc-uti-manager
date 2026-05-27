## ADDED Requirements

### Requirement: Exibição de Nome e Hora da Cirurgia na Reserva de Leito
O card de leito no painel principal, quando possuir uma reserva de próximo paciente ativa, MUST exibir o nome do próximo paciente e o horário programado de início da cirurgia. O horário da cirurgia MUST ser exibido no formato `DD/MM/AAAA - HH:MM`.

#### Scenario: Visualização dos dados adicionais da reserva
- **WHEN** o usuário visualiza o card de um leito que possui uma reserva ativa
- **THEN** o sistema SHALL exibir o nome do próximo paciente entre o número do prontuário e a idade
- **THEN** o sistema SHALL exibir a data e hora da cirurgia no formato "DD/MM/AAAA - HH:MM" no bloco de detalhes da cirurgia
