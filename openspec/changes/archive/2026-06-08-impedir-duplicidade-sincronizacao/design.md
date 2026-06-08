## Context

1. O sistema aceita a inserção de múltiplos registros para o mesmo prontuário enquanto a solicitação está pendente ou reservada, o que é conceitualmente incorreto.
2. O algoritmo em `_sincronizar_prioridades` exclui temporariamente do processamento a solicitação focada (`sol_id_foco`), mas se `prioridade_desejada` for nula (quando inserido sem prioridade), o foco não é adicionado de volta à lista, deixando o novo registro zerado/nulo na fila de prioridades.

## Goals / Non-Goals

**Goals:**
- Validar e bloquear inserções duplicadas de prontuários com solicitações pendentes/reservadas.
- Corrigir a sincronização de prioridades para não excluir a solicitação em foco quando esta for cadastrada sem prioridade manual pré-definida.

## Decisions

### 1. Validação de Duplicidade
- Em `criar_solicitacao`, antes de chamar o AGHU ou criar o registro, consultar as solicitações locais via `leito_provider.get_todas()`.
- Se existir uma solicitação com o mesmo prontuário e com status em `["Pendente", "Reservado"]`, levantar uma `HTTPException(400)`.

### 2. Correção na exclusão temporária do foco
- Em `_sincronizar_prioridades`, alterar a verificação para excluir o foco de `restantes` apenas se `prioridade_desejada` for informada:
  ```python
  if sol_id_foco is not None and s.id == sol_id_foco and prioridade_desejada:
      continue
  ```

## Risks / Trade-offs

- **[Trade-off]** Custo de consulta adicional na criação.
  - **Mitigação**: O volume de solicitações ativas é muito baixo (normalmente < 100 registros), então a busca na memória via `get_todas()` é extremamente rápida e irrelevante para a performance.
