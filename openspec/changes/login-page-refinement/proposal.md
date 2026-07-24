## Why

Ajustar e refinar a página de login para melhorar a ortografia, acentuação e remover elementos desnecessários (como "Esqueceu a senha?", já que a autenticação é via LDAP/AD institucional, e o título duplicado "Bem-vindo de Volta").

## What Changes

- Frontend: Remover o título "Bem-vindo de Volta" em `frontend/src/views/Login.vue`.
- Frontend: Corrigir "Gestao" para "Gestão" e "Clinicas" para "Clínicas".
- Frontend: Corrigir "Usuario" para "Usuário" (no label, placeholder e validações Zod).
- Frontend: Remover o botão "Esqueceu a senha?".
- Frontend: Ajustar o texto informativo inferior para "Utilize login e senha de rede" (apenas a primeira palavra em maiúsculo).

## Capabilities

### New Capabilities

### Modified Capabilities
- `login-page-refinement`: Ajustes ortográficos e remoção de botões desnecessários na tela de login.

## Impact

- `frontend/src/views/Login.vue`
