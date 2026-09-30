## Context

No ambiente de homologação (VM 10.34.0.151), a integração com o Active Directory (AD) da Ebserh funciona normalmente. No entanto, na VM de produção (10.34.0.192), ao tentar pesquisar um novo usuário no AD, a aplicação retorna "usuário não localizado". Isso pode ser motivado por:
1. Diferenças nas variáveis de ambiente `LDAP_*` entre homologação e produção no `.env`.
2. Restrição de firewall/portas (389 / 636) entre o container de produção e o controlador de domínio AD.
3. Falta de detalhamento de logs de erro em `LdapAuthProvider` para distinguir se houve falha de conexão (Timeout/Refused) ou se a consulta retornou resultado vazio.

## Goals / Non-Goals

**Goals:**
- Identificar e harmonizar a configuração `LDAP_*` no `.env` da VM de Produção (`10.34.0.192`).
- Adicionar tratamento de exceções com logs enriquecidos em `LdapAuthProvider`.
- Testar a conectividade de porta (ex: `nc -zv` ou `python socket`) a partir da VM e container de produção.
- Garantir que a busca de novos usuários no AD passe a funcionar em produção da mesma forma que em homologação.

**Non-Goals:**
- Alterar o modelo de dados de usuários ou perfis no banco de dados.
- Alterar o fluxo de login de usuários já existentes.

## Decisions

- **Decisão 1:** Adicionar logs explícitos de `DEBUG` e `ERROR` no `src/providers/implementations/ldap_auth_provider.py` registrando servidor, porta, base DN e causa exata de exceções de conexão ou bind.
- **Decisão 2:** Inspecionar o arquivo `.env` do servidor de produção (`10.34.0.192`) via SSH e compará-lo com o `.env` de homologação (`10.34.0.151`).

## Risks / Trade-offs

- **[Risco]** As credenciais de bind LDAP no `.env` de Produção estarem incorretas ou expiradas → **Mitigação:** Verificar as credenciais de serviço do AD em produção e atualizar no `.env`.
- **[Risco]** A porta do servidor AD estar bloqueada no firewall para a sub-rede da VM de Produção → **Mitigação:** Executar teste de conectividade de socket a partir da VM de produção.
