## Context

O Gráfico de Ocupação Semanal é construído sob dados simulados via gerador aleatório. Precisamos estruturar uma tabela de histórico para consolidar as taxas reais ao fim de cada dia e ajustar o painel de Indicadores para carregar e exibir esses dados reais persistidos.

## Goals / Non-Goals

**Goals:**
- Criar a tabela e o modelo SQLAlchemy `HistoricoOcupacao`.
- Implementar um loop assíncrono em background (iniciado no `lifespan` do FastAPI) que calcule e salve a taxa de ocupação real às 23:59 de cada dia.
- Modificar o `indicadores_provider.py` para carregar a ocupação correspondente de cada dia da semana corrente a partir do banco local, preenchendo datas faltantes com a taxa de ocupação instantânea.

**Non-Goals:**
- Migração de dados históricos retroativos fictícios (o histórico real passará a ser acumulado a partir do deploy).

## Decisions

- **Modelo `HistoricoOcupacao`:**
  - Tabela: `historico_ocupacao`
  - Colunas: `data` (Date, chave primária) e `taxa_ocupacao` (Float).
- **Background Loop de Fechamento Diário:**
  - No `lifespan` do `src/main.py`, iniciaremos um loop assíncrono em background (`asyncio.create_task`) que acorda periodicamente (ex: a cada 10 minutos) e verifica se o dia mudou e se o registro do dia anterior/atual às 23:59 foi inserido. Se não foi, calcula e grava no SQLite.
- **Leitura no Indicadores Provider:**
  - Consultar `historico_ocupacao` selecionando os registros onde a data esteja entre a segunda-feira e o domingo da semana atual.

## Risks / Trade-offs

- **Servidor Desligado às 23:59:** Se a máquina virtual for reiniciada ou estiver desligada no exato momento do fechamento, a taxa daquele dia não será gravada.
  - *Mitigação:* A rotina de segundo plano também verificará no startup do servidor se há dias anteriores sem registro na semana atual e os preencherá de forma retroativa usando a última taxa conhecida.
