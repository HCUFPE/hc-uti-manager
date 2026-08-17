## ADDED Requirements

### Requirement: Cálculo do Tempo Médio de Encaminhamento até Admissão
O sistema MUST calcular o tempo médio (em minutos) decorrido desde a liberação do encaminhamento pela UTI (momento em que o encaminhamento foi liberado, registrando o evento `encaminhamento_liberado`) até a admissão física definitiva do paciente no leito da UTI (momento em que a solicitação é concluída e registra o evento `conclusao`), para os pacientes do Bloco Cirúrgico (BC) que completaram o fluxo no período filtrado. Esse indicador representa o tempo de transporte e transferência do paciente.

#### Scenario: Cálculo do tempo médio de encaminhamento até admissão com sucesso
- **WHEN** o sistema calcula a diferença entre o carimbo de data/hora do evento de admissão (`conclusao`) e o evento de liberação de encaminhamento (`encaminhamento_liberado`) no histórico de solicitações concluídas no período
- **THEN** o sistema retorna a média aritmética desse tempo em minutos

### Requirement: Exibição do Tempo de Encaminhamento até Admissão no Dashboard
O painel de indicadores do frontend MUST exibir a métrica de tempo médio de encaminhamento até admissão de forma clara, posicionado lado a lado com as outras métricas de fluxo operacional de leitos de UTI.

#### Scenario: Visualização do indicador de tempo de encaminhamento até admissão
- **WHEN** o usuário acessa a tela de Indicadores
- **THEN** o sistema SHALL renderizar um card específico contendo o "Tempo Médio de Encaminhamento até Admissão" formatado em minutos
