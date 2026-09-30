## Why

Atualizar a versão do sistema para 1.7.4 e expor a métrica de usuários ativos (`active_users`) no endpoint de saúde `/api/health`. Essa métrica realiza a contagem de usuários distintos com sessões ativas (tokens válidos em `refresh_tokens`) para que dashboards de monitoramento como o Grafana / Zabbix possam acompanhar a quantidade de acessos concorrentes em tempo real.

## What Changes

- Atualização de versão do sistema para `1.7.4` em `src/version.py`, `frontend/src/config/version.ts` e `CHANGELOG.md`.
- Adição da contagem assíncrona de usuários ativos distintos (`SELECT COUNT(DISTINCT user_id) FROM refresh_tokens WHERE expires_at > datetime('now')`) no handler do endpoint `/api/health` em `src/routers/health.py`.
- Exposição do campo `"active_users": active_users` no payload JSON de resposta da API de healthcheck.

## Capabilities

### New Capabilities
- `health-active-users-metric`: Métrica de contagem de usuários ativos no endpoint de healthcheck para monitoramento via Grafana/Zabbix.

### Modified Capabilities

## Impact

- `src/routers/health.py`
- `src/version.py`
- `frontend/src/config/version.ts`
- `CHANGELOG.md`
- Monitoramento externo via Grafana / Zabbix
