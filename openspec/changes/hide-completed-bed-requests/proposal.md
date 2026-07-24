## Why

A tela de Solicitações de Vaga exibe as solicitações concluídas de forma aberta na Seção 3. Conforme as solicitações vão sendo concluídas (pacientes admitidos nos leitos), essa seção cresce e causa poluição visual, dificultando o foco nas solicitações ativas e pendentes. Além disso, os operadores gostariam de ver a data e hora em que cada solicitação foi concluída para auditoria e controle visual rápido.

## What Changes

- Frontend: Adicionar funcionalidade de expansão/recolhimento (collapse/expand) na seção de Solicitações Concluídas, deixando-a recolhida por padrão.
- Frontend: Exibir a data e hora de conclusão (pequena) em cada card de solicitação concluída.
- Backend: Incluir o campo `atualizado_em` (data/hora de conclusão) na resposta da rota `/api/solicitacoes` (no `SolicitacaoLeitoController.listar_solicitacoes`).

## Capabilities

### New Capabilities
- `hide-completed-bed-requests`: Adicionar controles de visualização (expand/collapse) para solicitações concluídas e exibir a data/hora de conclusão.

### Modified Capabilities

## Impact

- Modificações no frontend em `frontend/src/views/Solicitacoes.vue`.
- Modificações no backend em `src/controllers/solicitacao_leito_controller.py` para expor a data de atualização (`atualizado_em`).
