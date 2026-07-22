## ADDED Requirements

### Requirement: Alerta Sonoro para o NIR
O sistema MUST emitir um alerta sonoro periódico na tela inicial para operadores do NIR quando houver notificações pendentes de ciência.

#### Scenario: Novo alerta chega ao NIR e toca o bipe
- **WHEN** o usuário com perfil NIR possui 1 ou mais alertas não lidos (`unreadAlertsCount > 0`)
- **THEN** o sistema SHALL reproduzir a sequência de bipes a cada 30 segundos

#### Scenario: Operador do NIR dá ciência e o som cessa
- **WHEN** o operador do NIR marca todos os alertas como lidos (`unreadAlertsCount` vai a 0)
- **THEN** o sistema SHALL parar de emitir o alerta sonoro
