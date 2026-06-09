## Why

Atualmente, no provedor de indicadores (`IndicadoresProvider`), o cálculo da taxa de ocupação não considera os leitos mockados configurados via `MOCK_BEDS=true` em desenvolvimento, fazendo com que a taxa apareça zerada no painel mesmo com os dados mockados ativos. Adicionalmente, o projeto apresenta vulnerabilidades de segurança listadas no repositório GitHub (como no Rollup, Axios, PostCSS, etc.) que precisam ser verificadas e tratadas.

## What Changes

- Modificação do provedor de indicadores (`IndicadoresProvider`) para carregar a lista de leitos a partir do mock se `MOCK_BEDS=true`.
- Correção da lógica de contagem de leitos ocupados no indicador para ser insensível a maiúsculas/minúsculas (`status.upper() == 'OCUPADO'`).
- Atualização de pacotes npm vulneráveis no frontend (Rollup, PostCSS, Axios, etc.) via `npm audit fix`.

## Capabilities

### New Capabilities

<!-- Nenhuma nova capability está sendo introduzida -->

### Modified Capabilities

- `indicadores-calculos`: A métrica de taxa de ocupação exibida no painel de indicadores deve condizer com os leitos mockados configurados em desenvolvimento, assegurando consistência nas informações apresentadas na interface.

## Impact

- Afeta `get_indicadores_gerais` em `src/providers/implementations/indicadores_provider.py`.
- Afeta `frontend/package.json` e `frontend/package-lock.json`.
