## Context

No arquivo `indicadores_provider.py`, a contagem de solicitações canceladas e reservas canceladas depende da consulta ao histórico de ações (`historico_acoes`) filtrando pela coluna `tipo`. Atualmente o filtro usa o tipo `"cancelamento"`, mas as ações do sistema gravam como `"exclusao_solicitacao"` e `"cancelamento_reserva"`.

## Goals / Non-Goals

**Goals:**
- Ajustar os filtros de contagem de cancelamentos em `src/providers/implementations/indicadores_provider.py` para mapear `"exclusao_solicitacao"` e `"cancelamento_reserva"`.
- Garantir que as taxas e os totais de cancelamentos exibam os valores reais (exemplo: hoje deve mostrar `2` cancelamentos).

**Non-Goals:**
- Alterar o esquema do banco de dados ou a forma como os logs do histórico são gravados.

## Decisions

- **Modificação em `indicadores_provider.py`:**
  - Atualizar a linha 251:
    ```python
    tem_canc = any(self._parse_sol_id(ev.detalhes) == s.id for ev in historico_todos if ev.tipo in ["cancelamento", "exclusao_solicitacao"])
    ```
  - Atualizar a linha 377 (cancelamento de solicitação):
    ```python
    cancelamentos_sol_periodo = [ev for ev in historico_todos if ev.tipo in ["cancelamento", "exclusao_solicitacao"] and in_period(ev.criado_em) and "reserva" not in ev.acao.lower()]
    ```
  - Atualizar a linha 378 (cancelamento de reserva):
    ```python
    cancelamentos_res_periodo = [ev for ev in historico_todos if ev.tipo == "cancelamento_reserva" and in_period(ev.criado_em)]
    ```

## Risks / Trade-offs

- Nenhum risco visual ou funcional detectado. A modificação apenas alinha a leitura do histórico com o que o banco de dados de fato grava.
