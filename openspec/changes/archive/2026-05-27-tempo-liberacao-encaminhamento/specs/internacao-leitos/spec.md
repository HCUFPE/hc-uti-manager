## ADDED Requirements

### Requirement: Temporizador de Espera de Liberação no Card
O card de leito no painel da UTI, quando possuir um paciente com cirurgia finalizada mas sem encaminhamento liberado, MUST apresentar um temporizador indicando o tempo decorrido desde o encerramento da cirurgia.

#### Scenario: Visualização do relógio com tempo de espera
- **WHEN** o usuário visualiza o card de um leito que está no status "Cirurgia Concluída"
- **THEN** o card do leito SHALL exibir um ícone de relógio e um contador dinâmico (ex: "45m", "1h 12m") ao lado do texto de conclusão, representando o tempo de espera do paciente
