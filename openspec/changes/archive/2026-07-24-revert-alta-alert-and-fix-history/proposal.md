## Why

O usuário deseja manter o comportamento onde novos alertas são gerados com "Alterou o Destino de Alta" e novos históricos são registrados como alteração. Além disso, deseja executar um script de correção retroativa na base de dados de produção para corrigir os registros históricos de alteração de leito passados, sem necessidade de alterar registros passados de alertas.

## What Changes

- Backend: Manter a lógica de diferenciação de alertas e históricos novos.
- Banco de Dados: Criar e executar um script em `scratch/fix_historical_actions.py` na VM dentro do container para corrigir retroativamente os históricos passados.

## Capabilities

### New Capabilities
- `revert-alta-alert-and-fix-history`: Executar a migração retroativa de histórico de destino na UTI.

## Impact

- `scratch/fix_historical_actions.py`
