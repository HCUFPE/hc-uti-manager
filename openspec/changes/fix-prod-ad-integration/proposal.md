## Why

No ambiente de produção (VM 10.34.0.192), a busca de novos usuários no Active Directory (AD/LDAP Ebserh) falha com a mensagem "usuário não localizado", enquanto no ambiente de homologação funciona corretamente. É necessário investigar a conectividade de rede/portas com o servidor AD (ex: 389/636), verificar as variáveis de ambiente de produção e ajustar o tratamento de exceção/logs no provedor LDAP para diagnosticar e resolver a falha.

## What Changes

- Ajustar e harmonizar as variáveis de ambiente `LDAP_*` na VM de Produção (`/var/app/hc-uti-manager/.env`).
- Adicionar tratamento detalhado de erros e logs de diagnóstico no `LdapAuthProvider` para capturar falhas de timeout, bind ou busca de usuários no servidor AD.
- Testar conectividade de rede (host e porta LDAP) a partir do container de Produção (`hc-uti-backend`).

## Capabilities

### New Capabilities
- `prod-ad-integration-fix`: Diagnóstico e correção da consulta de usuários no Active Directory Ebserh em ambiente de produção.

### Modified Capabilities

## Impact

- `src/providers/implementations/ldap_auth_provider.py`
- Arquivo `.env` na VM de Produção (`10.34.0.192`)
- Rota de cadastro/busca de usuários em `src/routers/admin.py`
