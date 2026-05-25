## 1. Backend Changes

- [x] 1.1 Remover a exclusão automática de alertas no método `_sincronizar_alertas` em [alerta_controller.py](file:///c:/Users/daniel.turmina/Documents/HC-UTI-Manager/src/controllers/alerta_controller.py) para garantir que nenhum alerta seja removido do banco.

## 2. Frontend Changes

- [x] 2.1 Atualizar `alertConfig` em [Alertas.vue](file:///c:/Users/daniel.turmina/Documents/HC-UTI-Manager/frontend/src/views/Alertas.vue) para que todos os tipos de alerta (`critico`, `aviso`, `info`) usem a mesma aparência visual (azul com ícone de informação).
- [x] 2.2 Simplificar a configuração visual em [NotificationsPopover.vue](file:///c:/Users/daniel.turmina/Documents/HC-UTI-Manager/frontend/src/components/NotificationsPopover.vue) unificando todos os tipos sob a mesma aparência (azul e ícone de sino).

## 3. Verification

- [x] 3.1 Testar a listagem de alertas no frontend e verificar se todos têm a mesma cor e ícone.
- [x] 3.2 Validar que novas gerações de alertas não causam remoção dos alertas antigos do banco de dados.
