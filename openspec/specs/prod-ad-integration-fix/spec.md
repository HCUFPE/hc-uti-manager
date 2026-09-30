# prod-ad-integration-fix Specification

## Purpose
TBD - created by archiving change fix-prod-ad-integration. Update Purpose after archive.
## Requirements
### Requirement: Consulta e Validação de Usuários no Active Directory em Produção
O backend do sistema MUST realizar a consulta e o binding no Active Directory (AD/LDAP Ebserh) com tratamento resiliente de exceções e logs detalhados de diagnóstico no ambiente de produção.

#### Scenario: Consulta de usuário com sucesso no AD de Produção
- **WHEN** o administrador digita o username de um novo usuário para cadastro em produção
- **THEN** o sistema consulta o AD Ebserh na rede corporativa, obtém os dados do usuário (nome, e-mail, departamento) e retorna para pré-preenchimento do cadastro

#### Scenario: Falha de conexão ou timeout com servidor LDAP no ambiente de Produção
- **WHEN** o servidor LDAP não responde na porta configurada ou o bind falha no ambiente de produção
- **THEN** o sistema registra o log detalhado contendo host, porta e erro exato (ex: ConnectionRefused, Timeout, InvalidCredentials) e retorna uma mensagem clara de erro ao administrador

#### Scenario: Usuário realmente inexistente no AD Ebserh
- **WHEN** a consulta no AD retorna lista vazia de resultados
- **THEN** o sistema informa que o usuário não foi localizado no Active Directory Ebserh

