## ADDED Requirements

### Requirement: Remanejamento de Reserva no Card do Leito
O sistema MUST permitir que a equipe da UTI (ou Administradores) altere o leito físico reservado de um paciente diretamente a partir da visualização de cards de leitos.

#### Scenario: Visualização do botão de remanejamento no card
- **WHEN** o usuário visualiza o card de um leito que possui uma reserva ativa
- **THEN** o botão "Mudar Leito" SHALL estar disponível no card (caso o perfil seja UTI ou Administrador)

#### Scenario: Remanejamento de reserva executado com sucesso
- **WHEN** o usuário clica em "Mudar Leito", seleciona um novo leito disponível e confirma a ação
- **THEN** o sistema atualiza o leito de destino do paciente para o novo leito selecionado e limpa a reserva do leito original
