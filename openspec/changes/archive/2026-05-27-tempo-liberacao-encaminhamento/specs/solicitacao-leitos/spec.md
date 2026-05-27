## ADDED Requirements

### Requirement: Registro de Horário de Fim de Cirurgia e Liberação
A solicitação de leito MUST registrar o momento exato em que a cirurgia correspondente é finalizada e o momento exato em que o encaminhamento é liberado. Ao liberar o encaminhamento, o sistema MUST registrar o tempo decorrido no histórico de auditoria.

#### Scenario: Registro de fim da cirurgia e liberação de encaminhamento
- **WHEN** o solicitante clica em "Cirurgia Finalizada"
- **THEN** o sistema SHALL gravar a data e a hora atual no campo de cirurgia finalizada
- **WHEN** a UTI clica em "Liberar Encaminhamento"
- **THEN** o sistema SHALL gravar a data e a hora atual no campo de encaminhamento liberado, calcular a diferença de tempo e salvar o tempo decorrido na mensagem do histórico
