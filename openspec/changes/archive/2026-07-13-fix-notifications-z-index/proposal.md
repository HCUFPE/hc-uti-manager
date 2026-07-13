## Why

Ao abrir o popover de notificações ("sininho"), ele é exibido atrás dos cards de leitos, tornando impossível a leitura das mensagens. Corrigir a ordenação tridimensional (z-index) do componente resolve esse bug visual.

## What Changes

- **Ajuste de z-index do Popover:** Adicionar a classe `z-50` ao container e painel do componente `NotificationsPopover` para garantir que ele flutue por cima de todos os outros elementos da tela (como os cards de leitos).

## Capabilities

### New Capabilities

### Modified Capabilities
- `alertas`: Correção de z-index do painel de notificações.

## Impact

- **Frontend:** `frontend/src/components/NotificationsPopover.vue`
