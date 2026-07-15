## Why

Atualmente, não é possível aferir com precisão o tempo que os leitos de UTI passam em processo de higienização (limpeza). Esse tempo é um indicador operacional crítico para avaliar a eficiência do fluxo de leitos e identificar gargalos na liberação de vagas, permitindo uma gestão de leitos mais dinâmica e baseada em dados reais.

## What Changes

- Extração e análise do histórico de movimentações de leitos (`agh.ain_extrato_leitos`) no banco de dados do AGHU.
- Criação de uma nova métrica nos Indicadores Operacionais que calcula a média de tempo (em minutos) em que os leitos de UTI permanecem no status "LIMPEZA".
- Inclusão do novo indicador no dashboard do frontend sob a seção de tempos médios de processo.

## Capabilities

### New Capabilities

*(Nenhuma nova capacidade)*

### Modified Capabilities

- `indicadores-calculos`: Adicionar a métrica de tempo médio de higienização dos leitos de UTI à API de indicadores consolidados.

## Impact

- **Backend**: Injeção da nova query SQL no `LeitoAghuProvider`, adição da regra de cálculo no `IndicadoresProvider` e alteração do contrato de resposta do endpoint `/api/indicadores/resumo`.
- **Frontend**: Inclusão de um novo card com o tempo de higienização médio na tela de Indicadores.
