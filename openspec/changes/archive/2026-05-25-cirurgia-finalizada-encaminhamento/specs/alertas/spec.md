## ADDED Requirements

### Requirement: Alerta de Cirurgia Finalizada para a UTI
O sistema MUST gerar um alerta automático direcionado para o perfil UTI sempre que um solicitante sinalizar a conclusão de uma cirurgia.

#### Scenario: Geração de alerta de cirurgia finalizada
- **WHEN** a rotina de sincronização de alertas detecta que uma cirurgia foi finalizada para um leito reservado
- **THEN** o sistema SHALL gerar um alerta do tipo "aviso" com título "Cirurgia Finalizada" e mensagem contendo o prontuário do paciente pronto para encaminhamento direcionado para a UTI (perfil_alvo = None)

### Requirement: Alerta de Encaminhamento Liberado para o Solicitante
O sistema MUST gerar um alerta automático direcionado para o setor solicitante original (COB, HEM, ou BC) quando a UTI autorizar o encaminhamento do paciente.

#### Scenario: Geração de alerta de encaminhamento autorizado
- **WHEN** a rotina de sincronização de alertas detecta que a UTI liberou o encaminhamento para uma reserva
- **THEN** o sistema SHALL gerar um alerta do tipo "info" direcionado especificamente para o setor solicitante original (perfil_alvo = setor solicitante) informando que o paciente já pode ser transferido

### Requirement: Alerta de Liberação Cancelada para o Solicitante
O sistema MUST gerar um alerta automático direcionado para o setor solicitante original (COB, HEM, ou BC) quando a UTI cancelar a liberação de encaminhamento do paciente.

#### Scenario: Geração de alerta de liberação de encaminhamento cancelada
- **WHEN** a rotina de sincronização de alertas detecta que a UTI cancelou a liberação de encaminhamento para uma reserva
- **THEN** o sistema SHALL gerar um alerta do tipo "critico" direcionado especificamente para o setor solicitante original (perfil_alvo = setor solicitante) informando que a liberação de encaminhamento foi cancelada e o transporte deve ser suspenso
