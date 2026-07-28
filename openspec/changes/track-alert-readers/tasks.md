## 1. Database and Model Changes

- [x] 1.1 Atualizar `src/models/alerta.py` com as novas colunas `lido_em` e `lido_por` e ajustar `to_dict()`.
- [x] 1.2 Gerar migration Alembic para criar as novas colunas na tabela `alertas`.

## 2. Backend Logic Changes

- [x] 2.1 Atualizar o router `src/routers/alertas.py` para injetar o `current_user` e passar o operador nas rotas de leitura.
- [x] 2.2 Atualizar `AlertaController.atualizar_status_leitura` e `marcar_todos_como_lidos` em `src/controllers/alerta_controller.py` para salvar `lido_em` e `lido_por`.

## 3. Frontend Changes

- [x] 3.1 Atualizar `frontend/src/views/Alertas.vue` para exibir o emissor, data/hora de leitura e usuário.
- [x] 3.2 Atualizar `frontend/src/components/NotificationsPopover.vue` para exibir a mesma string de informação de leitura.

## 4. Version and Deployment

- [x] 4.1 Incrementar versão do app para "1.4.10".
