## Why

O Gráfico de Ocupação Semanal na aba de Indicadores atualmente exibe dados simulados (com variações aleatórias em torno da taxa atual) para os dias anteriores da semana. Para fornecer relatórios gerenciais fidedignos, é necessário registrar a taxa de ocupação diária real e exibi-la no gráfico a partir do histórico gravado no banco de dados.

## What Changes

- **Nova Tabela de Histórico:** Criação da tabela `historico_ocupacao` no banco de dados SQLite local contendo `data` e `taxa_ocupacao`.
- **Registro Diário Automático:** Implementação de um job periódico ou rotina de fechamento diário automatizado que calcula a taxa real de ocupação do censo de leitos e a salva no banco de dados.
- **Gráfico Dinâmico Real:** Atualização do cálculo no `indicadores_provider.py` para consultar a tabela de histórico para os dias da semana corrente, eliminando a simulação aleatória e caindo em um fallback padrão (taxa atual) apenas se não houver dados gravados para a data específica.

## Capabilities

### New Capabilities
Nenhuma.

### Modified Capabilities
- `internacao-leitos`: O censo de ocupação do gráfico semanal passará a ser 100% histórico e real, baseado nos registros salvos diariamente no banco de dados.

## Impact

- **Banco de Dados (SQLite):** Criação da tabela `historico_ocupacao` via migração do Alembic ou registro no SQLAlchemy.
- **Backend (Python):** Inclusão de um script ou job de agendamento de tarefas em segundo plano no `main.py` e modificação do método correspondente em `indicadores_provider.py`.
