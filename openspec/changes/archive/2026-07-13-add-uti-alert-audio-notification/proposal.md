## Why

Para garantir que a equipe da UTI responda rapidamente a novos alertas gerados especificamente para a UTI, é necessário um alerta sonoro recorrente similar ao que já ocorre quando uma cirurgia é finalizada. O alarme deve soar a cada 30 segundos até que o alerta correspondente seja arquivado (marcado como lido).

## What Changes

- **Integração de Alerta Sonoro por Notificação:** Modificar o timer de verificação de áudio em `Home.vue` para consultar a contagem de alertas não lidos da UTI (`/api/alertas/unread-count`).
- **Reprodução Recorrente (30s):** Se houver algum alerta não lido voltado para a UTI (e o perfil do usuário for UTI), disparar os mesmos bipes sonoros repetitivos a cada 30 segundos, até que seja dada ciência do alerta.

## Capabilities

### New Capabilities

### Modified Capabilities
- `alertas`: Alerta sonoro de 30 em 30 segundos para alertas pendentes direcionados para a UTI.

## Impact

- **Frontend:** `frontend/src/views/Home.vue`
