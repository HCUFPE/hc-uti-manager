## Why

A tela de indicadores (BI Dashboard) está exibindo incorretamente a contagem de solicitações canceladas e taxas de cancelamento como 0. Isso ocorre porque o backend (`indicadores_provider.py`) tenta filtrar no histórico eventos de tipo `"cancelamento"` e `"cancelamento"`, porém o histórico de ações do sistema grava esses eventos usando os tipos `"exclusao_solicitacao"` e `"cancelamento_reserva"`, respectivamente.

## What Changes

- **Correção dos Filtros de Tipo de Evento:** Ajustar as linhas do provedor de indicadores (`indicadores_provider.py`) que buscam pelo histórico de ações para usar `"exclusao_solicitacao"` e `"cancelamento_reserva"`.
- **Exibição Correta:** Restabelecer a contagem correta (exibindo o número real de cancelados, como o 2 no caso de hoje) na interface.

## Capabilities

### New Capabilities

### Modified Capabilities
- `indicadores-calculos`: Ajuste nos tipos de eventos considerados para contagem de solicitações e reservas canceladas.

## Impact

- **Backend:** `src/providers/implementations/indicadores_provider.py`
