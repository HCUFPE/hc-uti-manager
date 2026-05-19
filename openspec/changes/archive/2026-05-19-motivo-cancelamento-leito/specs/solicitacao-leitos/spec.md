## MODIFIED Requirements

### Requirement: Controle de Permissões na Edição
O sistema MUST restringir a edição e cancelamento das solicitações apenas ao setor que as criou ou a administradores do sistema, e MUST exigir que seja informado um motivo de cancelamento ao excluir a vaga.

#### Scenario: Cancelamento de solicitação
- **WHEN** a cirurgia é suspensa ou a vaga não é mais necessária
- **THEN** o sistema exibe uma lista de motivos pré-definidos (ex: Motivo A, Motivo B, Motivo C) e exige a seleção de um
- **THEN** o setor solicitante cancela o pedido e o sistema remove da fila ativa da UTI
- **THEN** o sistema registra a exclusão e o motivo escolhido no histórico do paciente
