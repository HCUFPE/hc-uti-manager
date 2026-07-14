## Why

No cálculo do horário médio de reserva por turno, o backend valida se a solicitação possui `sol.turno == "Manha"`. No entanto, no banco de dados o turno é persistido com a acentuação correta: `"Manhã"`. Isso faz com que o indicador de "Turno Manhã" seja sempre exibido como "N/D" (Não Disponível).

## What Changes

- **Filtro de Turno no Backend (`indicadores_provider.py`):**
  - Ajustar o mapeamento e validações do turno para suportar tanto `"Manhã"` quanto `"Manha"`.

## Capabilities

### Modified Capabilities
- `indicadores`: Correção do cálculo do Turno Manhã.

## Impact

- **Backend:** `src/providers/implementations/indicadores_provider.py`
