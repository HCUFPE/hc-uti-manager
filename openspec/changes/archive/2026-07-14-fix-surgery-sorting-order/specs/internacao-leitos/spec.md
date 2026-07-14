## ADDED Requirements

### Requirement: Priorização de Cirurgia Mais Próxima de Hoje
O sistema MUST associar ao leito reservado a cirurgia agendada ativa do paciente que seja mais próxima à data atual (priorizando cirurgias de hoje/futuras), caso o paciente possua mais de um agendamento ativo.

#### Scenario: Paciente com múltiplos agendamentos
- **GIVEN** o paciente tem uma cirurgia agendada para hoje
- **AND** outra cirurgia agendada para a próxima semana
- **WHEN** o sistema busca a cirurgia agendada do paciente para registrar a reserva de leito
- **THEN** a cirurgia agendada para hoje SHALL ser retornada e associada ao leito
