# solicitacao-leitos Specification

## Purpose
TBD - created by archiving change setup-openspec-docs. Update Purpose after archive.
## Requirements
### Requirement: Criação de Solicitação de Leito
O sistema MUST permitir que usuários dos setores solicitantes (Bloco Cirúrgico, Centro Obstétrico e Hemodinâmica) criem requisições de leito de UTI.

#### Scenario: Solicitação de vaga bem sucedida
- **WHEN** o usuário de um setor solicitante preenche o prontuário, data da cirurgia e especialidade
- **THEN** o sistema salva a requisição com o status inicial adequado
- **THEN** a solicitação passa a aparecer na fila de avaliação da UTI

### Requirement: Gestão da Fila e Reserva pela UTI
O sistema MUST permitir que a equipe da UTI visualize a fila de solicitações e atribua leitos físicos aos pacientes aprovados.

#### Scenario: Reserva de leito
- **WHEN** o usuário da UTI avalia uma solicitação pendente e vincula um número de leito físico
- **THEN** o status da solicitação é atualizado para sinalizar que o leito está reservado
- **THEN** o setor solicitante consegue ver que o paciente tem um leito garantido

### Requirement: Controle de Permissões na Edição
O sistema MUST restringir a edição e cancelamento das solicitações apenas ao setor que as criou ou a administradores do sistema. Adicionalmente, o sistema MUST bloquear a edição de solicitações que já possuem leito reservado, EXCETO para usuários com papéis específicos (BC, BC-ADMIN, COB, COB-ADMIN, HEM, HEM-ADMIN). Ao cancelar uma vaga, o sistema MUST exigir que seja informado um motivo de cancelamento.

#### Scenario: Cancelamento de solicitação
- **WHEN** a cirurgia é suspensa ou a vaga não é mais necessária
- **THEN** o sistema exibe uma lista de motivos pré-definidos e exige a seleção de um
- **THEN** o setor solicitante cancela o pedido e o sistema remove da fila ativa da UTI
- **THEN** o sistema registra a exclusão e o motivo escolhido no histórico do paciente

#### Scenario: Edição de solicitação com leito reservado por usuário comum
- **WHEN** um usuário sem papel de gestão ou controle administrativo tenta editar uma solicitação reservada
- **THEN** o sistema bloqueia a ação (interface desabilitada) e a API recusa a requisição

#### Scenario: Edição de solicitação com leito reservado por usuário com perfil especial
- **WHEN** um usuário com as roles BC, BC-ADMIN, COB, COB-ADMIN, HEM ou HEM-ADMIN tenta editar uma solicitação reservada
- **THEN** o sistema permite o acesso ao formulário de edição e processa a atualização com sucesso

