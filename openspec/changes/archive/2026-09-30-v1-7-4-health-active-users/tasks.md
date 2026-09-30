## 1. Atualização de Versão para 1.7.4

- [x] 1.1 Atualizar a versão para `1.7.4` em `src/version.py`, `frontend/src/config/version.ts` e `CHANGELOG.md`.

## 2. Implementação da Métrica de Usuários Ativos

- [x] 2.1 Adicionar a consulta de contagem de usuários ativos em `src/routers/health.py`.
- [x] 2.2 Incluir a propriedade `"active_users"` no payload de resposta JSON de `/api/health`.

## 3. Recompilação e Validação

- [x] 3.1 Recompilar o frontend (`npm run build`).
- [x] 3.2 Testar a rota `GET /api/health` e verificar se retorna `"active_users"` e a versão `1.7.4`.
