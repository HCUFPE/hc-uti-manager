## Context

A rota `GET /api/leitos` retorna informações sensíveis de pacientes (prontuário, nome, idade, diagnóstico, especialidade) e leitos da UTI. Atualmente, a rota está configurada sem verificação de token JWT, permitindo requisições anônimas.

## Goals / Non-Goals

**Goals:**
- Proteger a rota `GET /api/leitos` exigindo token JWT válido (`Depends(auth_handler.auth_wrapper)`).
- Proteger a rota `GET /api/leitos/disponiveis` exigindo token JWT válido (`Depends(auth_handler.auth_wrapper)`).

**Non-Goals:**
- Modificar o fluxo de autenticação do frontend (o Axios do Vue.js já injeta automaticamente o token JWT no cabeçalho `Authorization: Bearer <token>` quando o usuário está logado).

## Decisions

- **Utilização de `auth_handler.auth_wrapper`**:
  - *Decisão*: Aplicar `current_user: dict = Depends(auth_handler.auth_wrapper)` no handler dos endpoints de leitura de leitos.
  - *Razão*: É o padrão já estabelecido no projeto para verificar tokens JWT válidos e decodificar a sessão do usuário.

## Risks / Trade-offs

- **[Risco] Bloqueio de acessos sem login**: Usuários não logados receberão status 401 Unauthorized. Isso é o comportamento desejado para conformidade com a LGPD e a política de segurança da informação do hospital.
