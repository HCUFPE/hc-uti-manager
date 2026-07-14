## Why

Para preencher a lacuna da coluna esquerda e enriquecer os indicadores do sistema, adicionaremos uma tabela exibindo os "Principais Motivos de Cancelamento". Adicionalmente, melhoraremos o gráfico de pizza de "Distribuição por Especialidade" para exibir uma legenda detalhada com o número exato de leitos ocupados por especialidade, sem necessidade de passar o mouse.

## What Changes

- **Backend (`indicadores_provider.py`):**
  - Analisar as strings de cancelamento do período para extrair os motivos.
  - Retornar o dicionário `motivos_cancelamento` agrupado na resposta de indicadores.

- **Frontend (`Indicadores.vue`):**
  - Adicionar o card de tabela "Principais Motivos de Cancelamento" na coluna esquerda, abaixo das Métricas por Demandante.
  - Ajustar o card de pizza para ter uma legenda customizada do lado do gráfico exibindo a cor da fatia, nome da especialidade e a quantidade de leitos.

## Capabilities

### Modified Capabilities
- `indicadores`: Tabela de motivos de cancelamento e melhorias no gráfico de pizza.
