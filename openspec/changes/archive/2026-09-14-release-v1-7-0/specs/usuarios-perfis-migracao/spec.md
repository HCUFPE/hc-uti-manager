# usuarios-perfis-migracao Delta Specification

## ADDED Requirements

### Requirement: Autorização Híbrida Estrita no Login
O sistema MUST verificar se o colaborador autenticado no Active Directory corporativo possui registro prévio e ativo na tabela local de perfis de acesso (`usuarios_perfis`). Caso o colaborador não esteja cadastrado na tabela de perfis (e não seja um super administrador institucional configurado), o sistema MUST rejeitar a requisição de login com código HTTP 403 Forbidden.

#### Scenario: Login de usuário do AD cadastrado no sistema
- **WHEN** um colaborador insere credenciais corporativas válidas no formulário de login
- **THEN** o sistema autentica as credenciais com o Active Directory
- **THEN** o sistema SHALL localizar o perfil ativo do colaborador no banco de dados local
- **THEN** o sistema SHALL emitir os tokens JWT contendo o perfil de acesso cadastrado e conceder entrada

#### Scenario: Bloqueio de colaborador do AD não autorizado no sistema
- **WHEN** um colaborador insere credenciais corporativas válidas no formulário de login, mas não possui cadastro prévio no banco local de perfis
- **THEN** o sistema SHALL recusar a emissão de token com status HTTP 403 Forbidden
- **THEN** a resposta SHALL detalhar explicitamente que o usuário é válido no Active Directory mas não possui autorização de acesso ao HC-UTI Manager

## REMOVED Requirements

### Requirement: Perfil Legado Comum
**Reason**: Expurgo do perfil "Comum" para adequação ao princípio do menor privilégio e governança estrita de acesso hospitalar (RBAC). O sistema não permite perfis genéricos sem atribuição clara de setor.
**Migration**: Usuários devem ser explicitamente cadastrados por administradores em papéis de setor específicos (UTI, NIR, BC, COB, HEM, Administrador) ou seus respectivos papéis de administração de setor.
