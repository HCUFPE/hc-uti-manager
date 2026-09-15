## 1. Backend Implementation

- [x] 1.1 Adicionar `Depends(auth_handler.auth_wrapper)` ao endpoint `GET /api/leitos` em `src/routers/leito.py`
- [x] 1.2 Adicionar `Depends(auth_handler.auth_wrapper)` ao endpoint `GET /api/leitos/disponiveis` em `src/routers/leito.py`

## 2. Verification & Deploy

- [x] 2.1 Testar que requisições anônimas para `/api/leitos` retornam 401 Unauthorized
- [ ] 2.2 Subir a alteração para a branch `homologacao` e atualizar o container na VM de Homologação
