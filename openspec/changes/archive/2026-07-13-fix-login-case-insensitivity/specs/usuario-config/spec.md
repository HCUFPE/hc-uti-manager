## ADDED Requirements

### Requirement: Autenticação Insensível a Maiúsculas/Minúsculas para Perfis
O sistema MUST mapear o perfil do usuário local de forma insensível a maiúsculas/minúsculas (case-insensitive) em relação ao nome de usuário digitado no login do Active Directory.

#### Scenario: Login com variação de caixa
- **WHEN** o usuário realiza login no AD com letras maiúsculas ou misturadas (ex: "Cinthia.souza")
- **THEN** o sistema SHALL normalizar o nome de usuário para minúsculas e recuperar com sucesso o perfil de acesso correto (ex: "BC") do banco de dados local
