## MODIFIED Requirements

### Requirement: Sinalização de Cirurgia Finalizada pelos Solicitantes
O sistema MUST permitir que usuários com os perfis solicitantes (BC, COB, HEM, seus respectivos administradores, ou administradores do sistema) marquem uma solicitação de leito com status "reservada" como "Cirurgia Finalizada", fornecendo opcionalmente informações sobre a passagem de caso.

#### Scenario: Solicitante sinaliza fim da cirurgia
- **WHEN** o usuário de um setor solicitante clica no botão "Cirurgia Finalizada" em sua fila de solicitações reservadas
- **THEN** o sistema exibe o questionário de passagem de caso, atualiza o status de encaminhamento da solicitação para "Cirurgia Finalizada" e registra as observações se fornecidas
