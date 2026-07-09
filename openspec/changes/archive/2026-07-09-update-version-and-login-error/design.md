## Context

A tela de login possui uma informação de rodapé desatualizada e oculta as mensagens reais de erro de autenticação do backend devido a uma interceptação indesejada do Axios (que tenta fazer um refresh token em solicitações de login falhas com 401).

## Goals / Non-Goals

**Goals:**
- Atualizar o rodapé com a versão e data correta no frontend.
- Corrigir o interceptor de resposta do Axios no frontend para que requisições falhas de login (`/api/login`) não ativem a rotina de refresh.
- Traduzir a mensagem padrão de erro de autenticação no backend para ser amigável.

**Non-Goals:**
- Criação de telas adicionais ou alteração de fluxos de login em segundo fator.

## Decisions

- **Modificação do Interceptor Axios (`api.ts`):**
  - Ajustar a condição de interceptação do erro `401` para excluir explicitamente requisições enviadas à rota `/api/login`:
    ```javascript
    if (error.response.status === 401 && !originalRequest._retry && !originalRequest.url?.includes('/api/login'))
    ```
  - Com isso, o erro 401 do login será propagado diretamente para o formulário de login no frontend, permitindo que a mensagem do backend seja exibida na tela.

- **Mensagem Amigável no Backend (`auth.py`):**
  - Mudar o valor de `detail` nas exceções de credenciais inválidas para `"Usuário ou senha incorretos"`.

## Risks / Trade-offs

- **Exposição de erros:** Mostrar se o usuário ou senha estão errados.
  - *Mitigação:* A mensagem genérica "Usuário ou senha incorretos" é segura e padrão de mercado, pois não revela se apenas o usuário está correto e a senha errada ou vice-versa.
