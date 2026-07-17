## Why

Na tela de Indicadores, a tabela de motivos de cancelamento exibe cada swap de paciente como uma linha separada, pois a mensagem de motivo contêm os números de prontuário envolvidos (ex: "Alteração de Prioridade pós Solicitação (Prontuário X foi substituído pelo Prontuário Y)"). Isso impede o agrupamento e a contagem consolidada dos motivos.

## What Changes

- Ajustar a extração e contagem de motivos de cancelamento no backend de indicadores para limpar as informações adicionais de prontuários (como o padrão `(Prontuário X foi substituído por Y)`), agrupando-os corretamente sob os motivos limpos.

## Capabilities

### New Capabilities
<!-- Nenhuma nova capability -->

### Modified Capabilities
- `indicadores-calculos`: Regras de agregação dos dados de indicadores.

## Impact
- `src/providers/implementations/indicadores_provider.py`
