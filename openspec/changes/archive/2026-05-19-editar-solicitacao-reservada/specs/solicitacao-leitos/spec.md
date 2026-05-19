## MODIFIED Requirements

### Requirement: Controle de Permissões na Edição
O sistema MUST restringir a edição e cancelamento das solicitações apenas ao setor que as criou ou a administradores do sistema. Adicionalmente, o sistema MUST bloquear a edição de solicitações que já possuem leito reservado, EXCETO para usuários com papéis específicos (BC, BC-ADMIN, COB, COB-ADMIN, HEM, HEM-ADMIN), que mantêm a permissão de edição.

#### Scenario: Cancelamento de solicitação
- **WHEN** a cirurgia é suspensa e a vaga não é mais necessária
- **THEN** o setor solicitante pode cancelar o pedido e removê-lo da fila ativa da UTI

#### Scenario: Edição de solicitação com leito reservado por usuário comum
- **WHEN** um usuário sem papel de gestão ou controle administrativo tenta editar uma solicitação reservada
- **THEN** o sistema bloqueia a ação (interface desabilitada) e a API recusa a requisição

#### Scenario: Edição de solicitação com leito reservado por usuário com perfil especial
- **WHEN** um usuário com as roles BC, BC-ADMIN, COB, COB-ADMIN, HEM ou HEM-ADMIN tenta editar uma solicitação reservada
- **THEN** o sistema permite o acesso ao formulário de edição e processa a atualização com sucesso
