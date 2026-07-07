## ADDED Requirements

### Requirement: Preenchimento Automático de Dados do AD no Cadastro
O sistema MUST expor um endpoint no backend que busque os dados do usuário no Active Directory (AD) pelo `username` e preencher automaticamente os campos de cadastro no frontend ao cadastrar um novo usuário na tela de administração. Os dados preenchidos MUST ser: Nome Completo (atributo `displayName` ou `cn`), Lotação (atributo `department`) e E-mail (atributo `mail` ou `userPrincipalName`).

#### Scenario: Pesquisa de usuário do AD com sucesso
- **WHEN** o administrador digita um `username` no formulário de inclusão de usuário e aciona a pesquisa ou sai do campo (blur)
- **THEN** o frontend SHALL buscar os dados no endpoint de consulta do AD
- **THEN** os campos de Nome Completo, Lotação e E-mail SHALL ser preenchidos automaticamente com os valores retornados

#### Scenario: Usuário do AD não localizado
- **WHEN** o administrador insere um `username` que não existe no diretório do AD
- **THEN** o sistema SHALL exibir uma mensagem de erro (toast) informando que o usuário não foi localizado e permitir o preenchimento manual dos dados

### Requirement: Rótulo do Botão de Cadastro
O botão responsável por iniciar a inclusão de usuários e abrir o respectivo formulário na tela de configuração do administrador MUST exibir o texto "+ Novo Usuário".

#### Scenario: Visualização do botão na tela de administração
- **WHEN** o administrador acessa a tela de configurações da aplicação
- **THEN** o botão principal de criação de perfil/usuário SHALL estar visível com o texto "+ Novo Usuário"

### Requirement: Detalhes do Usuário no Cabeçalho
O cabeçalho superior direito da aplicação MUST exibir o Nome Completo e o Setor (Lotação) do usuário autenticado posicionados imediatamente antes (à esquerda) do ícone do perfil (bonequinho/avatar). O Setor (Lotação) deve ser exibido em fonte menor e cor secundária em relação ao Nome Completo.

#### Scenario: Exibição das informações do usuário logado
- **WHEN** qualquer usuário autenticado visualiza a barra superior da aplicação
- **THEN** o sistema SHALL renderizar o Nome Completo e a Lotação (obtidos da sessão do usuário) à esquerda do ícone do avatar
- **THEN** a lotação SHALL ser exibida em tamanho menor (ex: text-xs) e na cor cinza/secundária (ex: text-slate-500)
