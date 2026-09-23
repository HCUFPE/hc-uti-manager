# Documentação de Segredos e Configurações - HC UTI Manager

Este documento descreve o padrão de gestão de segredos e variáveis de ambiente do **HC UTI Manager** em conformidade com as diretrizes do **Framework SETISD**.

---

## 1. Visão Geral

A aplicação utiliza o módulo `src/config.py` com validação no boot (`pydantic-settings`). O sistema valida o arquivo `.env` na inicialização e **impede a subida do servidor** se `ENVIRONMENT=production` contiver segredos fracos ou vazios.

---

## 2. Lista de Variáveis de Ambiente

| Variável | Descrição | Exemplo / Valor Padrão | Obrigatório em Prod? |
|---|---|---|---|
| `ENVIRONMENT` | Ambiente de execução (`development`, `production`) | `production` | **Sim** |
| `SECRET_KEY` / `JWT_SECRET` | Chave de assinatura de tokens JWT | `MuzR983#$kL!z92k0a#...` | **Sim** (Mín. 16 caracteres) |
| `POSTGRES_DSN` | Conexão PostgreSQL com a base AGHU | `postgresql+asyncpg://user:pass@10.34.0.92:5432/dbaghu` | **Sim** |
| `SQLITE_DSN` | Conexão SQLite do banco local | `sqlite+aiosqlite:///./data/app.db` | **Sim** |
| `AD_URL` | Servidores Active Directory EBSERH | `ldap://UFPE-PVW-AD1.ebserhnet.ebserh.gov.br:389` | **Sim** |
| `AD_BIND_USER` | Usuário de leitura do AD | `EBSERHNET\svc_uti` | **Sim** |
| `AD_BIND_PASSWORD` | Senha de serviço do AD | `*****` | **Sim** |

---

## 3. Regras de Boot em Produção

Se `ENVIRONMENT=production`, a inicialização executará as seguintes verificações automáticas:
1. `SECRET_KEY` não pode ser nula, vazia ou ter menos de 16 caracteres.
2. `SECRET_KEY` não pode ser uma das chaves fracas conhecidas (`secret`, `123456`, `admin`, etc.).
3. Se qualquer validação falhar, o servidor emitirá uma mensagem de erro crítica e encerrará o processo imediatamente com código de erro.
