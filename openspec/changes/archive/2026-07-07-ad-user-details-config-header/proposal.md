## Why

Exibir dados detalhados do usuário (Nome Completo, Lotação, E-mail) vindos do Active Directory na tela de configurações e no cabeçalho superior direito da aplicação. Isso melhora a identificação do usuário logado e facilita o cadastro de novos usuários na tela de administração através do preenchimento automático dos dados após a inserção do username.

## What Changes

- **Preenchimento Automático do AD**: Ao cadastrar/atribuir perfil para um novo usuário na tela de administração, o administrador insere o `username` do AD, e o sistema consulta os dados do AD (via backend) para preencher automaticamente:
  - **Nome Completo** (do atributo `displayName` ou `cn`)
  - **Lotação** (do atributo `department`)
  - **E-mail** (do atributo `mail` ou `userPrincipalName`)
- **Ajuste de Rótulo (Label)**: Renomear o botão de cadastro de usuários na tela de administração para "+ Novo Usuário".
- **Identidade Visual no Cabeçalho**: Exibir no canto superior direito do cabeçalho o Nome Completo do usuário logado e o Setor (lotação) em fonte menor, posicionados imediatamente antes (à esquerda) do ícone do perfil (bonequinho).

## Capabilities

### New Capabilities
- `usuario-config`: Controle de dados de perfil detalhados de usuários (Nome, Lotação e E-mail) vindos do Active Directory e exibição contextual no cabeçalho e na tela de configurações.

### Modified Capabilities
<!-- None -->

## Impact

- **Backend (`src/routers/admin.py` ou `src/routers/users.py`)**: Criar um endpoint (ex: `GET /api/admin/users/ad/{username}`) que permita ao administrador buscar as informações básicas do usuário no AD (Nome, Lotação, E-mail) antes de salvar o perfil.
- **Frontend (`frontend/src/views/AdminConfig.vue`)**: Alterar o botão para "+ Novo Usuário", adicionar os campos (Nome Completo, Lotação, E-mail) na visualização e implementar o gatilho (trigger) de busca ao digitar o username para preencher o formulário automaticamente.
- **Frontend (`frontend/src/components/ProfileDropdown.vue`)**: Alterar o layout no cabeçalho para exibir o Nome Completo e Setor/Departamento antes do avatar (bonequinho).
