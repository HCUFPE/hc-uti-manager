## Why

O usuário identificou que a nomenclatura de "Altas Pendentes (Aguardando Destino)" no dashboard deve ser alterada para "Altas Pendentes (Aguardando Transferência)" para melhor alinhar com a realidade operacional do hospital. Além disso, a lista de filtros de tipo no histórico de ações necessita de agrupamento de múltiplos eventos técnicos em 3 conceitos principais de negócio (Altas, Solicitações e Reservas), facilitando a auditoria de ações pelos operadores.

## What Changes

- Alterar o texto de "Altas Pendentes (Aguardando Destino)" para "Altas Pendentes (Aguardando Transferência)" na exibição do painel de indicadores.
- Reestruturar o filtro por tipo na página de histórico para consolidar os eventos técnicos do banco de dados em apenas 3 filtros de interface:
  - **Altas**: consolida ações de alta (`alta`), definição/mudança de destino (`alteracao_destino`, `destino_disponivel`, `destino_pendente`) e cancelamento de alta (`cancelamento`).
  - **Solicitações**: consolida criação de solicitação (`nova_solicitacao`), edição (`edicao`) e cancelamento/exclusão de solicitação (`exclusao_solicitacao`).
  - **Reservas**: consolida reservas (`reserva`), remanejamento/redefinição de reserva (`remanejamento_reserva`) e cancelamento de reserva (`cancelamento_reserva`).

## Capabilities

### New Capabilities

N/A

### Modified Capabilities

- `bi-dashboard`: agrupamento de filtros de histórico e ajuste de nomenclatura em indicadores e status de altas.

## Impact

- `frontend/src/views/Indicadores.vue`: alteração de texto e legendas no painel de volumes.
- `frontend/src/views/Historico.vue`: alteração na lista de opções de filtro por tipo de ação de histórico e lógica de agrupamento/filtro no frontend, caso os dados cheguem crus do backend.
