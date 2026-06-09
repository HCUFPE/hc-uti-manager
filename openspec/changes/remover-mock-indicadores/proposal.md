## Why

Atualmente, o provedor de indicadores gerais (`IndicadoresProvider`) possui um valor de fallback mockado (`45.2` minutos) para o tempo médio de liberação de encaminhamento quando não há dados no banco e a variável de ambiente `ENV` está configurada como `"development"`. Isso confunde o usuário que limpa o banco de dados e ainda visualiza dados calculados na tela.

## What Changes

- Remoção do fallback mockado (`45.2`) para o indicador de tempo médio de liberação de encaminhamento em `IndicadoresProvider`.
- Exibição de `0.0` quando não houver dados no banco para cálculo de média de tempo.

## Capabilities

### New Capabilities

<!-- Nenhuma nova capability está sendo introduzida -->

### Modified Capabilities

- `indicadores-calculos`: Os indicadores e gráficos do painel de controle devem exibir o valor real calculado, retornando 0.0 em caso de banco de dados limpo ou ausência de dados, sem injetar valores fictícios.

## Impact

- Afeta `get_indicadores_gerais` em `src/providers/implementations/indicadores_provider.py`.
