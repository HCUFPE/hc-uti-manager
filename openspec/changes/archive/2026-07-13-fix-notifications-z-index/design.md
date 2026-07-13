## Context

O popover de notificações está sobreposto por elementos com maior z-index (como os cards de leitos na página inicial).

## Goals / Non-Goals

**Goals:**
- Adicionar `z-50` no painel flutuante do popover em `NotificationsPopover.vue`.
- Adicionar `z-40` ou `z-50` no container principal do componente para forçar o empilhamento 3D correto.

## Decisions

- **Modificação em `frontend/src/components/NotificationsPopover.vue`:**
  Adicionar `z-50` na div container (`class="relative z-50"`) e no painel flutuante (`class="absolute right-0 mt-3 w-80 ... z-50"`).
