## Why

No Modo TV, toda a interface estrutural (cabeçalho e barra lateral) é ocultada para maximizar a área de visualização do grid de leitos. Porém, isso impede que os operadores visualizem alertas ou notificações importantes geradas pelo sistema. Habilitar o componente de notificações ("sininho") no Modo TV resolve essa limitação operacional.

## What Changes

- **Integração do Popover de Notificações no Modo TV:** Exibir o componente `NotificationsPopover` ao lado dos botões de controle na página inicial (`Home.vue`) apenas quando o Modo TV estiver ativo.
- **Correção/Melhoria do Popover:** Garantir o funcionamento consistente do componente `NotificationsPopover` (que atualmente está implementado mas ocultado por não ser utilizado).

## Capabilities

### New Capabilities

### Modified Capabilities
- `alertas`: Integração visual de alertas e notificações com o Modo TV.

## Impact

- **Frontend:** `frontend/src/views/Home.vue` e `frontend/src/components/NotificationsPopover.vue`
