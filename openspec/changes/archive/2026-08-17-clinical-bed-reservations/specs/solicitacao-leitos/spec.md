## ADDED Requirements

### Requirement: Ocultação de Leitos Clínicos para Reservas do Bloco Cirúrgico
Ao carregar a lista de leitos disponíveis para a alocação/reserva de solicitações ativas do Bloco Cirúrgico (BC), o sistema MUST omitir os leitos que estão com a marcação `bloqueado_clinico == True`.

#### Scenario: Filtro de leitos para paciente cirúrgico
- **WHEN** o usuário do sistema solicita a listagem de leitos livres para efetuar a reserva de um paciente cirúrgico
- **THEN** o sistema exclui todos os leitos que possuem `bloqueado_clinico == True` da lista de opções exibidas

### Requirement: Swap de Bloqueio Clínico no Remanejamento
Ao remanejar a reserva de um paciente do Leito X para o Leito Y que estava reservado para Clínico/COB/HEM, o sistema MUST mover a flag de bloqueio clínico para o Leito X de origem que foi desocupado.

#### Scenario: Remanejamento de paciente com troca de bloqueio
- **WHEN** o usuário da UTI muda a reserva de um paciente do Leito X para o Leito Y (onde Y possui `bloqueado_clinico == True`)
- **THEN** o sistema associa o paciente ao Leito Y, limpa a flag `bloqueado_clinico` de Y, e define `bloqueado_clinico = True` no Leito X (leito de origem)
