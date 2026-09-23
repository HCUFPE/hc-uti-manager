## Context

Atualmente, quando uma pessoa acessa a raiz da aplicação (`/`), o Vue Router inicia a montagem do componente `Home.vue`. Ao mesmo tempo, o guard de rota identifica que o usuário não possui token e força a transição de rota para `/login`. No entanto, como o `onMounted` de `Home.vue` chama `loadLeitos()` de forma assíncrona, a requisição `GET /api/leitos` é disparada sem token e retorna HTTP 401. A instrução do bloco `catch` de `loadLeitos()` dispara um `toast.error('Falha ao carregar leitos. Verifique a conexao.')`, que aparece flutuando sobre a página de login.

Além disso, ao analisar a autenticação em `src/routers/auth.py`, a variável `access_token_expires` atrelava `timedelta(minutes=15)` quando `remember_me` estava marcado como `True`, causando o vencimento prematuro da sessão.

## Goals / Non-Goals

**Goals:**
- Silenciar notificações de erro no frontend quando o status retornado for HTTP 401 ou quando o usuário não estiver autenticado.
- Estender a validade do token JWT de acesso para 7 dias quando o usuário marcar "Lembrar de mim" no login.
- Atualizar a documentação de requisitos e changelog conforme regras de Spec-Driven Development do projeto.
- Executar os deploys em Homologação (`10.34.0.151`) e Produção (`10.34.0.192`).

**Non-Goals:**
- Alterar o mecanismo de Refresh Token do interceptor do Axios.

## Decisions

1. **Filtro de Exceção no `loadLeitos` em `Home.vue`**:
   - Verificar `if (error.response?.status !== 401 && authStore.isAuthenticated)` antes de chamar `toast.error()`.
   - *Motivo*: Impede que redirecionamentos normais de autenticação sujem a UI com alertas de erro de conexão.

2. **Ajuste da regra `remember_me` em `auth.py`**:
   - Mudar `timedelta(minutes=15)` para `timedelta(days=7)` quando `remember_me` for verdadeiro.

## Risks / Trade-offs

- [Risk] Sessões de 7 dias mantêm a credencial ativa por mais tempo no dispositivo do usuário.
  - *Mitigation*: O logout explícito destrói o token e limpa a sessão local.
