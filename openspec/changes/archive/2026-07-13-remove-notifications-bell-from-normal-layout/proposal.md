## Why

O usuário deseja que o sininho de notificações apareça exclusivamente no Modo TV, removendo a exibição do cabeçalho geral (modo normal) para simplificar a interface de uso cotidiano.

## What Changes

- **Remoção do Popover no Layout Padrão:** Remover o componente `NotificationsPopover` de `DefaultLayout.vue` para que ele não apareça ao lado do menu de perfil no cabeçalho comum.
- **Manutenção no Modo TV:** Manter o componente ativo na tela principal (`Home.vue`) apenas quando o Modo TV estiver ativo.

## Capabilities

### New Capabilities

### Modified Capabilities
- `alertas`: Ocultação do sininho de notificações no layout de navegação comum.

## Impact

- **Frontend:** `frontend/src/layouts/DefaultLayout.vue`
