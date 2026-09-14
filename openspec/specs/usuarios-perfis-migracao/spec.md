# usuarios-perfis-migracao Specification

## Purpose
Especificação de preservação de perfis de acesso, rotinas de carga inicial do AD e regras de autorização estrita baseadas no banco local.

## Requirements
### Requirement: Preservação de Perfis no Reset do Banco
A rotina de limpeza de dados transacionais na VM MUST preservar os perfis de acesso cadastrados localmente no banco, limpando apenas dados operacionais.

#### Scenario: Execução da limpeza preservando perfis
- **WHEN** o desenvolvedor executa o script de limpeza de banco de dados na VM
- **THEN** os dados das tabelas `solicitacoes_leito`, `solicitacoes_alta`, `historico_acoes`, `alertas`, `refresh_tokens` e `leito_estados` SHALL ser apagados
- **THEN** as configurações de perfis na tabela `usuarios_perfis` SHALL ser mantidas inalteradas

### Requirement: Carga de Dados do AD (Backfill)
O sistema MUST prover um script utilitário capaz de sincronizar em lote as informações de Nome Completo, Lotação e E-mail a partir do AD para os perfis que já estão salvos no banco SQLite local da VM.

#### Scenario: Execução da carga de dados retroativa (Backfill)
- **WHEN** o desenvolvedor executa o script de backfill de perfis
- **THEN** o script SHALL conectar-se à VM e consultar todos os registros da tabela `usuarios_perfis`
- **THEN** para cada usuário listado, o script SHALL buscar seus atributos de Nome, Setor e E-mail no Active Directory
- **THEN** o script SHALL gravar os atributos consultados de volta nas colunas `nome_completo`, `lotacao` e `email` da tabela correspondente na VM

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
