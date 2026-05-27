## ADDED Requirements

### Requirement: Detecção de Conflito de Reserva
O sistema MUST identificar e marcar como em conflito qualquer leito físico de UTI que possua uma reserva de paciente cadastrada localmente no banco de dados, mas que esteja atualmente ocupado por um paciente diferente no censo do hospital (AGHU), exceto se houver uma solicitação de alta ativa para o ocupante atual.

#### Scenario: Detecção de conflito em leito ocupado sem alta ativa
- **WHEN** o usuário do painel visualiza um leito reservado para o Paciente A, mas o censo do AGHU indica que o leito está ocupado pelo Paciente B (sendo que não há solicitação de alta ativa cadastrada para o Paciente B)
- **THEN** o sistema SHALL marcar o leito como em conflito (`conflito_reserva` = True) e exibir um destaque visual de conflito no card do leito

#### Scenario: Ausência de conflito em leito ocupado com alta ativa
- **WHEN** o usuário do painel visualiza um leito reservado para o Paciente A, o censo indica que está ocupado pelo Paciente B, e existe uma solicitação de alta ativa cadastrada para o Paciente B
- **THEN** o sistema SHALL considerar que o Paciente B está prestes a sair, portanto o leito não está em conflito (`conflito_reserva` = False)
