## Context

O componente `NotificationsPopover.vue` está implementado no frontend mas atualmente não é importado ou exibido em nenhum lugar do sistema (está oculto). O usuário solicitou que, ao ativar o "Modo TV", o "sininho" de notificações/alertas seja exibido.

## Goals / Non-Goals

**Goals:**
- Integrar o componente `NotificationsPopover` no painel principal (`Home.vue`) apenas quando o Modo TV estiver ativo, posicionado na barra de controles do topo.
- Adicionar o `NotificationsPopover` ao cabeçalho principal do sistema (`DefaultLayout.vue`) na visualização padrão (opcional/desejável para consistência).
- Validar se o popover funciona corretamente sem erros e busca as notificações da API `/api/alertas`.

## Decisions

- **Posicionamento no Modo TV (`Home.vue`):**
  Inserir `<NotificationsPopover v-if="uiStore.isTvMode" />` na linha de botões de controle (`Som Mudo/Ativo`, `Sair da TV`, etc.).
- **Posicionamento no Layout Padrão (`DefaultLayout.vue`):**
  Inserir `<NotificationsPopover />` no cabeçalho ao lado esquerdo do `ProfileDropdown`.
