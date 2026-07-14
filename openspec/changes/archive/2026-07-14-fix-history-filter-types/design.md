## Context

Tanto o tipo de ação "Alta" quanto "Destino" possuem sub-tipos no banco de dados local que precisam ser retornados ao aplicar o filtro correspondente.

## Goals / Non-Goals

**Goals:**
- Mapear filtros principais para sub-tipos internos de ações.

## Decisions

- **Modificação em `src/providers/implementations/historico_provider.py`:**
  Ajustar a verificação de `tipo` para:
  ```python
  if tipo:
      if tipo == "destino":
          stmt = stmt.where(HistoricoAcao.tipo.in_(["destino", "alteracao_destino", "destino_disponivel", "destino_pendente"]))
      elif tipo == "alta":
          stmt = stmt.where(HistoricoAcao.tipo.in_(["alta", "conclusao_alta"]))
      else:
          stmt = stmt.where(HistoricoAcao.tipo == tipo)
  ```
