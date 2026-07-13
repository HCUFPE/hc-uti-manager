## Context

Melhorar usabilidade da página de alertas e do painel flutuante de notificações.

## Goals / Non-Goals

**Goals:**
- Adicionar o botão "Voltar ao Painel" com ícone de seta em `frontend/src/views/Alertas.vue`.
- Adicionar botão "Ciente" ao lado do horário em `frontend/src/components/NotificationsPopover.vue` chamando a API PUT de status de leitura.

## Decisions

- **Modificação em `Alertas.vue`:**
  - Importar `ArrowLeftIcon` de `@heroicons/vue/24/outline`.
  - Inserir `<router-link to="/">` com estilo apropriado no cabeçalho flex.
- **Modificação em `NotificationsPopover.vue`:**
  - Adicionar o método `markAsRead(id)` que faz a chamada PUT ao backend `/api/alertas/{id}/lido` e remove o alerta da lista local e atualiza o total count.
  - Inserir botão "Ciente" condicionado ao status `unread` na lista do template.
