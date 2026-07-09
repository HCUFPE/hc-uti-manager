## ADDED Requirements

### Requirement: Mensagem Amigável de Falha de Login
O sistema MUST exibir a mensagem "Usuário ou senha incorretos" quando a autenticação de login falhar devido a credenciais inválidas (usuário inexistente ou senha incorreta), propagando o erro real para o formulário.

#### Scenario: Falha de autenticação no login
- **WHEN** o usuário digita credenciais inválidas e clica em Entrar
- **THEN** o sistema SHALL exibir o alerta contendo a mensagem de erro "Usuário ou senha incorretos"
