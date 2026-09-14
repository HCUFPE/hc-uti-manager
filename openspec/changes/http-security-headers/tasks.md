## 1. Backend Implementation

- [x] 1.1 Importar `Request` de `fastapi` no topo do arquivo `src/main.py`
- [x] 1.2 Adicionar o middleware HTTP `@app.middleware("http")` para injetar os Security Headers (`X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Cache-Control`, `Pragma`) em `src/main.py`

## 2. Verification & Validation

- [x] 2.1 Testar execução do backend FastAPI localmente e validar o retorno dos cabeçalhos HTTP na resposta
- [ ] 2.2 Subir as alterações para a branch `homologacao` e validar o deploy na VM de Homologação
