## MODIFIED Requirements

### Requirement: Provisionamento de Usuário Apenas com Login
A criação e edição de perfis de usuário deve exigir apenas a indicação do Login de Rede, delegando ao backend a busca e resolução de dados complementares do AD.

#### Scenario: Atribuição de perfil resolve dados do AD no backend
- **WHEN** o administrador envia um formulário contendo apenas o `username` e o `perfil`
- **THEN** o servidor SHALL buscar as informações de Nome Completo, Lotação e E-mail no Active Directory
- **THEN** o servidor SHALL salvar estes dados no registro do banco de dados local antes de efetuar o commit
- **THEN** se a busca no AD falhar, o servidor SHALL manter os campos em branco ou usar dados padrões, sem abortar a requisição

### Requirement: Interface Simplificada de Atribuição
O modal de cadastro e edição de perfis deve ocultar campos adicionais que são geridos de forma automatizada pelo servidor.

#### Scenario: Formulário de perfil simplificado e botão renomeado
- **WHEN** o administrador abre o formulário de atribuição de perfil
- **THEN** as entradas manuais para Nome Completo, Lotação e E-mail SHALL não ser exibidas no modal
- **THEN** o botão de salvamento SHALL exibir o texto "Salvar Usuário"
