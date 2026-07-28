## Why

Atualmente, o sistema apenas marca se um alerta foi lido (`lido = True`), mas não registra o momento (`lido_em`) nem quem realizou a ação (`lido_por`). Para fins de auditoria e controle, é importante registrar o usuário que deu ciência ao alerta e exibir essa informação no frontend.

## What Changes

- Backend: Adicionar colunas `lido_em` e `lido_por` no modelo `Alerta`.
- Backend: Criar uma migration Alembic para adicionar essas colunas à tabela `alertas`.
- Backend: Modificar as rotas de marcar como lido para receber o token do usuário e salvar `lido_por` e `lido_em` (com o fuso horário correto).
- Frontend: Atualizar as views de visualização de alertas para exibir a informação de quem e quando visualizou o alerta.
- Versão: Incrementar a versão da aplicação para `1.4.10`.

## Capabilities

### New Capabilities

### Modified Capabilities
- `track-alert-readers`: Registro do usuário e horário de leitura de alertas no banco e exibição no frontend.

## Impact

- `src/models/alerta.py`
- `src/routers/alertas.py`
- `src/controllers/alerta_controller.py`
- `frontend/src/views/Alertas.vue`
- `frontend/src/components/NotificationsPopover.vue`
