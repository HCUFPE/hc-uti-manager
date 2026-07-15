## Context

Os leitos de UTI passam por um processo de higienização ("limpeza") após a desocupação. O histórico dessas movimentações é gravado de forma automática no banco do AGHU (tabela `agh.ain_extrato_leitos`). Atualmente, o sistema exibe apenas o estado instantâneo (Censo), mas não calcula o tempo médio histórico em que esses leitos permanecem em higienização.

## Goals / Non-Goals

**Goals:**
- Criar a query SQL para ler o histórico de extrato de leitos da UTI (`unf_seq = 115`) e calcular as durações em que estiveram em status `LIMPEZA`.
- Expor a métrica no endpoint `/api/indicadores/resumo`.
- Adicionar o card visual correspondente no painel de Indicadores do frontend.

**Non-Goals:**
- Monitoramento ou gravação local dessas transições (tudo será calculado sob demanda a partir do histórico do AGHU).
- Cálculo de tempo de higienização de setores fora da UTI.

## Decisions

### 1. Consulta ao AGHU (Uso da tabela `ain_extrato_leitos`)
- **Decisão**: Utilizaremos a função de janela `LEAD` para parear cada mudança para status `LIMPEZA` com a mudança imediatamente posterior daquele mesmo leito.
- **Alternativa**: Fazer múltiplas queries ou varrer os dados via Python na memória. Rejeitado pelo impacto de performance. O uso do `LEAD` no Postgres é extremamente eficiente.

### 2. Mock de dados em ambiente de desenvolvimento
- **Decisão**: Caso a variável `MOCK_BEDS` esteja ativada no ambiente de desenvolvimento, o backend retornará um tempo médio estático (ex: 45 minutos) para evitar erros de conexão na máquina local.

## Risks / Trade-offs

- **[Risco]**: A query pode se tornar lenta com o crescimento do histórico de extratos.
- **[Mitigação]**: Filtraremos os registros de extratos no banco com base no período (`data_inicio` e `data_fim`) informado, limitando o volume de leitura.
