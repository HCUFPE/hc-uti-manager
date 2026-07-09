## 1. Ajustes no Frontend

- [x] 1.1 Atualizar o texto da versão no rodapé do arquivo `frontend/src/views/Login.vue` para a data de hoje.
- [x] 1.2 Modificar o interceptor do Axios em `frontend/src/services/api.ts` para evitar a tentativa de refresh token quando a requisição original falha na rota `/api/login`.

## 2. Ajustes no Backend

- [x] 2.1 Atualizar as mensagens de erro de login no `src/auth/auth.py` para `"Usuário ou senha incorretos"`.
- [x] 2.2 Atualizar o comentário de versão no topo do arquivo `src/main.py`.

## 3. Testes e Publicação

- [x] 3.1 Testar a autenticação com credenciais inválidas localmente e verificar se o erro real é impresso na tela.
- [ ] 3.2 Commit, push e deploy com rebuild na VM.
