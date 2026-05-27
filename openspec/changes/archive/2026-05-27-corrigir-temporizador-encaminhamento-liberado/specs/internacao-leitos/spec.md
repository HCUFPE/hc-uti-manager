## MODIFIED Requirements

### Requirement: Temporizador de Espera de Liberação no Card
O card de leito no painel da UTI, quando possuir um paciente com cirurgia finalizada mas sem encaminhamento liberado, MUST apresentar um temporizador indicando o tempo decorrido desde o encerramento da cirurgia. Uma vez que o encaminhamento seja liberado, o temporizador e o relógio MUST ser ocultados e o status do card alterado para indicar a liberação.

#### Scenario: Visualização do relógio com tempo de espera
- **WHEN** o usuário visualiza o card de um leito que está no status "Cirurgia Concluída" e o encaminhamento não foi liberado ainda
- **THEN** o card do leito SHALL exibir um ícone de relógio e um contador dinâmico (ex: "45m", "1h 12m") ao lado do texto de conclusão, representando o tempo de espera do paciente

#### Scenario: Ocultamento do relógio após liberação do encaminhamento
- **WHEN** o encaminhamento do paciente com cirurgia concluída é liberado pela UTI
- **THEN** o card do leito SHALL ocultar o temporizador de espera e exibir a etiqueta "Encaminhamento Liberado"
