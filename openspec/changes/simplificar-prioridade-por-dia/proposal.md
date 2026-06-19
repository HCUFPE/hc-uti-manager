## Why

Atualmente, o cálculo e a reordenação das prioridades das solicitações de leito de UTI são segmentados por data da cirurgia E por turno (Manhã, Tarde, Noite). Esta segmentação por turnos adiciona complexidade desnecessária à fila de prioridades, por isso o objetivo é simplificar a lógica para gerenciar e reordenar a prioridade de forma única por dia.

## What Changes

- **Simplificação da Fila**: Remoção da separação e agrupamento por turnos (Manhã/Tarde/Noite) no cálculo e sincronização das prioridades.
- **Prioridade Diária Única**: As solicitações de um mesmo dia serão priorizadas em uma única fila sequencial diária (ex: de P1 a Pn).
- **Ordenação Inicial Cronológica**: No momento do cadastro do paciente para um determinado dia, a prioridade padrão inicial será atribuída seguindo o horário previsto da cirurgia (ou a ordem de inclusão/criação se houver empate no horário da cirurgia), respeitando qualquer prioridade informada explicitamente no cadastro.
- **Manutenção de Reordenações Manuais**: Alterações manuais de prioridade feitas pelo usuário (ex: arrastar/mudar de P2 para P1) serão mantidas, e as demais solicitações do mesmo dia serão deslocadas para garantir uma fila contínua e sem duplicatas/buracos.

## Capabilities

### New Capabilities

*(Nenhuma nova funcionalidade será criada)*

### Modified Capabilities

- `solicitacao-leitos`: A prioridade inicial e as regras de reordenamento das solicitações de leitos de UTI serão agrupadas e calculadas exclusivamente por dia, sem segmentação por turnos.

## Impact

- **Backend**:
  - `SolicitacaoLeitoController._sincronizar_prioridades`: Ajuste do método para buscar e reordenar as solicitações filtrando apenas por `data_cirurgia` e removendo o argumento/filtro de `turno`.
  - Todas as chamadas ao método `_sincronizar_prioridades` (nas rotas de criar, atualizar, deletar e mudar leito) serão simplificadas para não passar ou ignorar o parâmetro de turno.
- **Frontend**:
  - `Solicitacoes.vue`: Ajuste na ordenação multinível do computed `solicitacoesFiltradas` para remover o nível de ordenação por Turno, passando a ordenar apenas por Data da Cirurgia, Prioridade, Horário da Cirurgia e Data da Solicitação.
