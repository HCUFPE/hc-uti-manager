## 1. Versão e Backend Modifications

- [ ] 1.1 Atualizar `src/version.py` e `frontend/package.json` para a nova versão `1.7.1`.
- [ ] 1.2 Alterar a expiração do token JWT na rota de login em `src/routers/auth.py` para 7 dias quando `remember_me` for verdadeiro.

## 2. Frontend Modifications

- [ ] 2.1 Adicionar checagem de erro HTTP 401 e estado de autenticação em `frontend/src/views/Home.vue` para suprimir a mensagem de erro de leitos na tela de login.
- [ ] 2.2 Testar a compilação do frontend (`npm run build` na pasta frontend).

## 3. Specification & Documentation Sync

- [ ] 3.1 Atualizar `docs/projeto_inicial/02-requisitos.md` com a nova regra de sessão (Lembrar de mim = 7 dias, Padrão = 24h).
- [ ] 3.2 Atualizar `CHANGELOG.md` com o registro das correções da versão.

## 4. Deploy & Verification

- [ ] 4.1 Fazer commit e push das alterações no Git.
- [ ] 4.2 Realizar o deploy no ambiente de Homologação (`10.34.0.151`).
- [ ] 4.3 Realizar o deploy no ambiente de Produção (`10.34.0.192`).
