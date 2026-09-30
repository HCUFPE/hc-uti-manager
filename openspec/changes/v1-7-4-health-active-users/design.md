## Context

Atualmente o endpoint `GET /api/health` retorna informações de status, versão e estado da aplicação. Para permitir que dashboards operacionais no Grafana/Zabbix acompanhem a quantidade de usuários ativos concorrentes no sistema em tempo real, precisamos calcular o total de usuários distintos cujo `expires_at` na tabela `refresh_tokens` seja maior que a data/hora atual.

## Goals / Non-Goals

**Goals:**
- Atualizar a versão do sistema para `1.7.4`.
- Consultar de forma resiliente a quantidade de usuários distintos com token válido no SQLite local em `src/routers/health.py`.
- Expor a propriedade `"active_users"` no JSON do `/api/health`.

**Non-Goals:**
- Alterar o modelo da tabela `refresh_tokens`.
- Alterar o tempo de expiração dos tokens.

## Decisions

- **Decisão 1:** Executar a consulta `SELECT COUNT(DISTINCT user_id) FROM refresh_tokens WHERE expires_at > datetime('now')` de forma segura via sessão assíncrona SQLAlchemy/aiosqlite no endpoint de healthcheck.
- **Decisão 2:** Embutir o bloco em `try/except` que define `active_users = 0` em caso de erro, garantindo que o monitoramento de saúde nunca falhe por causa de uma consulta de métrica.

## Risks / Trade-offs

- **[Risco]** Sobrecarga no endpoint de healthcheck por chamadas muito frequentes do Grafana → **Mitigação:** A query no SQLite é extremamente leve e faz uma contagem simples indexada por data.
