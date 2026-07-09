## Why

1. O texto da versão no rodapé da página de login está desatualizado (data de junho).
2. Quando um usuário insere credenciais incorretas (usuário inexistente ou senha incorreta), a tela exibe o erro incompreensível `Erro: Refresh token not found`. Isso ocorre porque o interceptor Axios do frontend intercepta a resposta `401 Unauthorized` da tentativa de login e tenta fazer o refresh do token em segundo plano de forma errônea, mascarando o erro original de credenciais inválidas.

## What Changes

- **Atualização da Versão:** Alterar o rodapé na tela de login para refletir a data `09/07/2026 às 13:42h`.
- **Correção do Interceptor do Frontend:** Ajustar o interceptor de resposta do Axios (`api.ts`) para ignorar tentativas de reautenticação (`refresh token`) quando a requisição original for a rota de login (`/api/login`).
- **Tradução da Mensagem do Backend:** Atualizar as respostas de falha de autenticação do backend de `Invalid credentials` para `Usuário ou senha incorretos`.

## Capabilities

### New Capabilities

### Modified Capabilities
- `usuario-config`: Melhoria nas mensagens de erro de login e exibição de versão no rodapé.

## Impact

- **Frontend (Vue/Axios):** `frontend/src/views/Login.vue` (texto da versão) e `frontend/src/services/api.ts` (interceptor).
- **Backend (FastAPI):** `src/auth/auth.py` (mensagens de erro do provedor de autenticação) e `src/main.py` (comentário de versão no topo).
