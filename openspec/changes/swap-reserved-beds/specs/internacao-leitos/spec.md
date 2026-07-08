## MODIFIED Requirements

### Requirement: Troca de Leitos Reservados (Swap)
O sistema deve permitir a troca direta de reservas entre dois pacientes.

#### Scenario: Trocar vaga reservada entre dois pacientes
- **WHEN** o operador com perfil UTI ou Administrador abrir o modal de remanejamento ("Mudar Leito") de um paciente já reservado
- **THEN** o sistema SHALL listar também os leitos que possuem reservas ativas
- **WHEN** o operador selecionar um leito já reservado para outro paciente e confirmar a mudança
- **THEN** o sistema SHALL trocar as informações de reserva dos dois leitos no banco de dados local
- **THEN** o destino de ambas as solicitações SHALL ser atualizado com o respectivo novo leito
