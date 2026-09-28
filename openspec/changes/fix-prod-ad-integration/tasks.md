## 1. Diagnóstico e Ajustes de Conectividade em Produção

- [x] 1.1 Conectar via SSH à VM de Produção (`10.34.0.192`) e comparar as variáveis `AD_*` de `/var/app/hc-uti-manager/.env` com as de Homologação.
- [x] 1.2 Testar a conectividade de rede com o servidor LDAP a partir do container `hc-uti-backend` em produção.

## 2. Melhorias de Resiliência e Tracing no Backend

- [x] 2.1 Adicionar logs de erro detalhados (host, porta, tipo de exceção) no provedor LDAP (`src/auth/auth.py` e `src/routers/admin.py`).
- [x] 2.2 Preservar e harmonizar os parâmetros específicos do ambiente de Produção sem sobrescrever chaves exclusivas.

## 3. Implantação e Validação

- [x] 3.1 Fazer o restart do serviço no ambiente de Produção.
- [ ] 3.2 Testar a busca e adição de um novo usuário do AD pela interface web de Produção.
