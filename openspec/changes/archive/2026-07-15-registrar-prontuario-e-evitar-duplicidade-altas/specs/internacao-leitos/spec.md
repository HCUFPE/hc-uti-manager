## ADDED Requirements

### Requirement: Registro de Prontuário no Histórico de Gestão de Alta (Solicitação, Destino e Conclusão)
O sistema MUST associar o prontuário do paciente nos registros de histórico de ações quando uma nova solicitação de alta for criada, quando uma solicitação de alta for cancelada, quando a alta for concluída, quando o destino de alta for definido/alterado, e quando a disponibilidade do leito de destino for definida/cancelada.

#### Scenario: Gravação do prontuário na solicitação de alta
- **WHEN** o usuário cria uma solicitação de alta para um leito
- **THEN** o sistema identifica o prontuário do ocupante atual daquele leito e grava o registro no histórico de ações contendo o número do prontuário no campo `prontuario`

#### Scenario: Gravação do prontuário no cancelamento de alta
- **WHEN** o usuário cancela uma solicitação de alta
- **THEN** o sistema recupera o prontuário associado àquela alta e grava o registro no histórico de ações contendo o número do prontuário no campo `prontuario`

#### Scenario: Gravação do prontuário na conclusão de alta
- **WHEN** uma solicitação de alta é concluída (ex: via censo do AGHU)
- **THEN** o sistema grava o registro de conclusão de alta no histórico de ações contendo o número do prontuário no campo `prontuario`

#### Scenario: Gravação do prontuário na definição do destino
- **WHEN** o NIR define ou altera o leito de destino de uma alta
- **THEN** o sistema grava o registro no histórico de ações contendo o número do prontuário no campo `prontuario`

#### Scenario: Gravação do prontuário na sinalização de destino disponível
- **WHEN** o NIR sinaliza que o leito de destino está disponível ou indisponível
- **THEN** o sistema grava o registro no histórico de ações contendo o número do prontuário no campo `prontuario`

### Requirement: Prevenção de Cliques Duplos no Envio de Solicitação de Alta
A interface do frontend MUST desabilitar o botão de envio de solicitação de alta no formulário após o primeiro clique e exibir um indicador visual de salvamento ("loading") até que a requisição seja concluída.

#### Scenario: Submissão do modal de alta
- **WHEN** o usuário clica em solicitar alta no formulário
- **THEN** o botão de confirmação fica desabilitado e a requisição é processada uma única vez pelo servidor
