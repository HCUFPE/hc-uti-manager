## ADDED Requirements

### Requirement: Métrica de Tempo Médio de Liberação de Encaminhamento
O painel de indicadores MUST exibir o tempo médio decorrido entre a conclusão cirúrgica e a liberação de encaminhamento feita pela UTI para as solicitações no período filtrado.

#### Scenario: Visualização do indicador de tempo médio de liberação
- **WHEN** o usuário acessa a tela de Indicadores Operacionais
- **THEN** o sistema SHALL exibir um novo card com o "Tempo Médio de Liberação de Encaminhamento" da UTI formatado em horas e minutos (ou apenas minutos se for inferior a 1 hora)
