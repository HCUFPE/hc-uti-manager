## Why

Atualmente, o sistema permite o cadastro de cirurgias com data retroativa no fluxo de solicitações de leito. Além disso, o fluxo de troca de paciente (swap) grava um motivo genérico/fixo de cancelamento no histórico (mesmo para solicitações que estavam apenas pendentes, sem reserva ativa) e não detalha quais prontuários foram substituídos. Por fim, a tela de histórico possui filtros de tipo que não retornam resultados devido a divergências de nomenclatura de tipos entre o frontend e o backend.

## What Changes

- **Trava de Data Retroativa**: Bloqueio de novas solicitações ou swaps se a data da cirurgia for no passado (comparação apenas por dia/mês/ano).
- **Motivo Dinâmico de Cancelamento no Swap**: Diferenciação do motivo registrado no histórico entre `"Alteração de Prioridade pós Solicitação"` (para pendentes) e `"Alteração de Prioridade pós Reserva de Leito"` (para reservadas).
- **Detalhamento no Histórico de Swap**: Exibição de prontuários envolvidos no swap de forma explícita no histórico de ações.
- **Operador da Reserva Automática no Swap**: Registro de novas reservas geradas automaticamente pelo swap com o operador `"Sistema"`.
- **Ajuste de Filtros de Histórico**: Mapeamento e correção dos filtros de tipo de histórico no backend e frontend para que exibam registros reais para solicitações, cancelamentos e reservas.

## Capabilities

### New Capabilities
<!-- Nenhuma nova capability está sendo introduzida -->

### Modified Capabilities
- `solicitacao-leitos`: Ajustes nas regras de criação, edição e cancelamento de solicitações de leito e histórico de ações.

## Impact

- `src/controllers/solicitacao_leito_controller.py`
- `src/providers/implementations/historico_provider.py`
- `frontend/src/views/Historico.vue`
