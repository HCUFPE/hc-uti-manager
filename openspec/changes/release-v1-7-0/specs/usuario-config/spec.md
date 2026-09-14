# usuario-config Delta Specification

## MODIFIED Requirements

### Requirement: Preenchimento Automático de Dados do AD no Cadastro
O sistema MUST expor um endpoint no backend que busque os dados do usuário no Active Directory (AD) pelo `username` e o formulário de inclusão na tela de administração MUST exigir a validação prévia deste usuário no Active Directory antes de permitir o salvamento. Os dados validados (Nome Completo, Lotação e E-mail) MUST ser exibidos em um painel/card de confirmação visual e preencher automaticamente os campos correspondentes do cadastro.

#### Scenario: Pesquisa e validação de usuário do AD com sucesso
- **WHEN** o administrador digita o login institucional no campo de usuário e aciona o botão "🔍 Consultar Login" ou pressiona Enter
- **THEN** o frontend SHALL invocar o endpoint `/api/admin/ad-search/{login}`
- **THEN** o formulário SHALL exibir um card visual com destaque positivo (verde) informando a validação do usuário com seu Nome Completo, Lotação e E-mail
- **THEN** o botão de submissão ("Salvar Usuário") SHALL ser habilitado para persistência

#### Scenario: Usuário do AD não localizado no diretório
- **WHEN** o administrador pesquisa por um login inexistente ou inválido no Active Directory
- **THEN** o sistema SHALL exibir uma notificação de erro (toast) informando que o usuário não foi localizado no Active Directory
- **THEN** o card de confirmação de validação não SHALL ser exibido
- **THEN** o botão "Salvar Usuário" SHALL permanecer desabilitado para novos cadastros

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
