## Context

A fila de solicitações de leitos de UTI (mesma data de cirurgia e turno) é ordenada por prioridade (P1, P2, P3...).
O método `_sincronizar_prioridades` é chamado para garantir que a fila não tenha lacunas ou prioridades duplicadas após inclusões, edições ou exclusões.
No entanto, a implementação atual desconsidera os argumentos `sol_id_foco` e `prioridade_desejada`, ordenando toda a fila puramente de forma cronológica (horário de cirurgia e criação). Isso faz com que tentativas de alterar manualmente a prioridade de um paciente sejam desfeitas na sincronização imediata.

## Goals / Non-Goals

**Goals:**
- Ajustar `_sincronizar_prioridades` para respeitar a prioridade manual quando informada por `sol_id_foco` e `prioridade_desejada`.
- Garantir que as outras solicitações no mesmo bucket sejam deslocadas mantendo sua ordem cronológica relativa.
- Manter a integridade da fila (sem lacunas e sem duplicatas, ex: P1, P2, P3...).

**Non-Goals:**
- Alterar as prioridades de outros buckets (outras datas/turnos).
- Mudar regras gerais de permissão de alteração de prioridades.

## Decisions

### 1. Algoritmo de Inserção com Foco de Prioridade
- **Abordagem**: 
  1. Filtrar a solicitação em foco (`sol_id_foco`) do bucket.
  2. Ordenar as solicitações restantes cronologicamente por `hora_cirurgia` e `criado_em`.
  3. Converter a `prioridade_desejada` (ex: `"P1"`) em um índice baseado em 0 (ex: `0`).
  4. Limitar/garantir que esse índice esteja dentro dos limites da lista (`0` a `len(restantes)`).
  5. Inserir a solicitação em foco no índice desejado da lista ordenada.
  6. Reatribuir sequencialmente as prioridades (`P1`, `P2`, ...) de acordo com a nova ordem da lista e persistir no banco apenas os registros que mudaram.
- **Alternativa Considerada**: Ordenar as solicitações pelo valor numérico da sua prioridade atual. Contudo, como a fila pode conter inconsistências temporárias antes da sincronização, a ordenação cronológica relativa das solicitações restantes é mais robusta e previsível.

## Risks / Trade-offs

- **[Risco]** Índice fora dos limites se a prioridade desejada for maior que o tamanho da fila (ex: fila tem 2 itens e o usuário tenta definir P5).
  - **Mitigação**: O algoritmo fará um clamp do índice usando `min(indice_desejado, len(restantes))` para garantir que fique na última posição disponível caso exceda.
