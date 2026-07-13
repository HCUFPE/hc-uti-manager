## Why

O login via Active Directory (AD) aceita credenciais independentemente de letras maiúsculas/minúsculas. No entanto, a tabela local de perfis de usuário (`usuarios_perfis`) armazena os usernames estritamente em minúsculas. Se um usuário digita seu username com variação de caixa (ex: `Cinthia.souza`), o login é validado no AD mas a busca do perfil local falha, fazendo com que ele caia no perfil "Comum" (sem permissões de solicitante).

## What Changes

- **Normalização de Username:** Converter o `username` retornado pelo provedor de autenticação AD para letras minúsculas (`.strip().lower()`) antes de executar consultas no banco local de perfis de usuário em `src/routers/auth.py`.

## Capabilities

### New Capabilities

### Modified Capabilities
- `usuario-config`: Normalização de username para evitar inconsistência de perfil devido à sensibilidade de maiúsculas/minúsculas.

## Impact

- **Backend:** `src/routers/auth.py`
