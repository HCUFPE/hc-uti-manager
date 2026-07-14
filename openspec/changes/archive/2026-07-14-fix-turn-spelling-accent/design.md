## Context

No `IndicadoresProvider.get_indicadores_gerais`, os turnos de cirurgia são verificados.

## Decisions

- **Modificação em `src/providers/implementations/indicadores_provider.py`:**
  Ajustar a verificação de `sol.turno`:
  ```python
  if sol and sol.turno in ["Manhã", "Manha", "Tarde"]:
      ...
      if sol.turno in ["Manhã", "Manha"]:
          minutos_manha.append(minutos_dia)
      else:
          minutos_tarde.append(minutos_dia)
  ```
