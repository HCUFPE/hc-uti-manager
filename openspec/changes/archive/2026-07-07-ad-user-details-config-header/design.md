## Context

A aplicação armazena a relação de usuários e perfis locais na tabela `usuarios_perfis` (SQLite), contendo apenas `username` e `perfil`. Atualmente, a identificação dos usuários na tela de administração é feita apenas pelo `username` do AD, e o cabeçalho exibe apenas o ícone de perfil (bonequinho).

Para melhorar a usabilidade, implementaremos o preenchimento automático das informações cadastrais (Nome Completo, Lotação e E-mail) extraídas diretamente do Active Directory (AD) e salvaremos estes dados no banco local para fins de listagem rápida e exibição no cabeçalho.

## Goals / Non-Goals

**Goals:**
- Estender a tabela e modelo `UsuarioPerfil` para armazenar `nome_completo`, `lotacao` e `email`.
- Criar uma rota no backend que busque dados de um `username` no AD usando a conta de serviço configurada.
- Atualizar a interface de gerenciamento de perfis para autocompletar esses campos no blur/busca do username.
- Alterar o rótulo do botão principal para "+ Novo Usuário".
- Exibir o Nome Completo e Setor no cabeçalho (ao lado esquerdo do ícone do usuário).

**Non-Goals:**
- Sincronização bidirecional de dados (a aplicação nunca escreverá no AD).
- Atualização em lote automática de todos os usuários já cadastrados retroativamente (os dados serão preenchidos ou atualizados sob demanda ou quando o próprio usuário fizer login).

## Decisions

### 1. Armazenamento local das informações cadastrais
- **Opção A:** Consultar o AD dinamicamente (N+1 queries) para cada usuário listado na tabela de administração.
- **Opção B (Escolhida):** Adicionar colunas `nome_completo`, `lotacao` e `email` na tabela local `usuarios_perfis` e salvá-los no momento do cadastro.
- **Razoamento:** Evita latência e sobrecarga de rede na consulta do AD para renderizar a lista. Além disso, garante que a aplicação continue exibindo os dados mesmo em cenários de instabilidade na conexão com o AD.

### 2. Criação do endpoint de busca no AD
- **Detalhe:** Adicionar a rota `GET /api/admin/ad-search/{username}` que chama `auth_handler.authenticate_user(username, None)`.
- **Razoamento:** Aproveita o fluxo de busca de atributos já implementado no `ActiveDirectoryAuthProvider` que usa a credencial administrativa (bind) para buscar os atributos de qualquer usuário.

### 3. Exibição de Nome e Setor no cabeçalho
- **Detalhe:** Colocar um bloco de texto alinhado à direita antes do botão de dropdown no componente `ProfileDropdown.vue`.
- **Razoamento:** Usar classes utilitárias do Tailwind (como `hidden sm:block`) para ocultar as informações em telas móveis e manter o visual limpo, destacando o Nome com maior peso e o Setor/Departamento em fonte menor e cor secundária.

## Risks / Trade-offs

- **[Risco]** Instabilidade ou queda do AD impedindo o cadastro de usuários.
  - **Mitigação:** Se o endpoint de busca falhar, o frontend exibirá um aviso amigável e liberará os campos (Nome Completo, Lotação e E-mail) para digitação manual no formulário.
- **[Risco]** Mudança de cargo ou setor do funcionário no AD não refletida no banco local.
  - **Mitigação:** No login do usuário (`src/routers/auth.py`), o sistema atualizará automaticamente os campos `nome_completo`, `lotacao` e `email` na tabela `usuarios_perfis` se o usuário logado já possuir um perfil salvo.
