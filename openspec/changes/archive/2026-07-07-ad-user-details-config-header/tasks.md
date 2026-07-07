## 1. Banco de Dados e Backend

- [x] 1.1 Adicionar as colunas `nome_completo`, `lotacao` e `email` no modelo `UsuarioPerfil` em `src/models/usuario_perfil.py` e atualizar seu método `to_dict`
- [x] 1.2 Gerar e aplicar a migração do banco usando Alembic (`alembic revision --autogenerate` e `alembic upgrade head`)
- [x] 1.3 Implementar a rota `GET /api/admin/ad-search/{username}` em `src/routers/admin.py` para pesquisar o usuário no AD (com fallback para dados simulados no provedor Mock)
- [x] 1.4 Atualizar a rota `POST /api/admin/perfis` em `src/routers/admin.py` para receber e salvar os novos campos de Nome, Lotação e E-mail no banco local
- [x] 1.5 Atualizar a rota de login e refresh token em `src/routers/auth.py` para sincronizar os dados do AD do próprio usuário se ele já tiver um perfil local salvo

## 2. Cabeçalho de Perfil (Header)

- [x] 2.1 Atualizar `ProfileDropdown.vue` para ler os atributos `displayName` e `department` do store de autenticação
- [x] 2.2 Inserir no template a exibição de Nome Completo e Setor (lotação) alinhados à esquerda do ícone do usuário (com classes responsivas para telas pequenas)

## 3. Tela de Gerenciamento de Usuários (AdminConfig)

- [x] 3.1 Alterar a label do botão de cadastro de "Novo Perfil" para "+ Novo Usuário" no arquivo `AdminConfig.vue`
- [x] 3.2 Atualizar a tabela de listagem de perfis em `AdminConfig.vue` para conter colunas de Usuário (Nome e Login), Lotação, E-mail e Perfil
- [x] 3.3 Implementar a função `buscarUsuarioAD` no frontend que consulta o novo endpoint do backend e preenche os campos do formulário automaticamente no blur do `username`
- [x] 3.4 Incluir no modal de cadastro os inputs correspondentes a Nome Completo, Lotação e E-mail para visualização e eventual ajuste manual
