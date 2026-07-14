## Why

Atualmente, ao filtrar o histórico por "Destino" ou "Alta", o sistema não retorna registros. Isso ocorre porque o frontend envia `"destino"` ou `"alta"`, mas no banco de dados esses eventos são categorizados com sub-tipos mais específicos, como `"alteracao_destino"`, `"destino_disponivel"`, `"destino_pendente"` ou `"conclusao_alta"`.

## What Changes

- **Agrupamento de Filtros no Backend:** Modificar a consulta no `HistoricoProvider.listar` para que:
  - O filtro `"destino"` retorne registros de tipos: `["destino", "alteracao_destino", "destino_disponivel", "destino_pendente"]`.
  - O filtro `"alta"` retorne registros de tipos: `["alta", "conclusao_alta"]`.

## Capabilities

### New Capabilities

### Modified Capabilities
- `alertas`: Filtro correto de histórico de ações.

## Impact

- **Backend:** `src/providers/implementations/historico_provider.py`
