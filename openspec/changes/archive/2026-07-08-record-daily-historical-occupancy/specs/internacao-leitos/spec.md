## ADDED Requirements

### Requirement: Registro Diário de Ocupação
O sistema MUST realizar o fechamento diário e registrar a taxa de ocupação dos leitos da UTI no banco de dados local de forma automática às 23:59 de cada dia.

#### Scenario: Fechamento diário automático
- **WHEN** o relógio do sistema atinge 23:59 de cada dia
- **THEN** o sistema SHALL calcular a taxa de ocupação real dos leitos (total de ocupados sobre o total de leitos) e salvar o registro com a data correspondente na tabela de histórico de ocupação.

## MODIFIED Requirements

### Requirement: Gráfico de Ocupação Semanal
O sistema MUST obter o percentual de ocupação dos dias anteriores da semana corrente a partir do histórico de ocupação gravado no banco de dados, em vez de simular valores aleatórios. Se não houver registro para um determinado dia no banco de dados, o sistema SHALL retornar como fallback a taxa de ocupação real atualizada do censo.

#### Scenario: Visualização de Ocupação Real e Histórica no Gráfico
- **WHEN** o usuário visualiza o gráfico de ocupação semanal na tela de indicadores
- **THEN** o sistema SHALL carregar o histórico de ocupação diária gravado no banco e exibir os dados reais correspondentes no gráfico para cada dia da semana corrente.
