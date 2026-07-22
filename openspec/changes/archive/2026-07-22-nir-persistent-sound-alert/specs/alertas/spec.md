## MODIFIED Requirements

### Requirement: Alerta Sonoro para o NIR
O sistema MUST emitir um alerta sonoro periódico, independentemente da tela ativa em que o usuário esteja, para operadores do NIR quando houver notificações pendentes de ciência.

#### Scenario: Novo alerta chega ao NIR e toca o bipe
- **WHEN** o usuário com perfil NIR possui 1 ou mais alertas não lidos (`unreadAlertsCount > 0`) em qualquer tela sob o layout padrão (`DefaultLayout.vue`)
- **THEN** o sistema SHALL reproduzir a sequência de bipes a cada 30 segundos

#### Scenario: Operador do NIR dá ciência e o som cessa
- **WHEN** o operador do NIR marca todos os alertas como lidos (`unreadAlertsCount` vai a 0)
- **THEN** o sistema SHALL parar de emitir o alerta sonoro

#### Scenario: Silenciar o alerta sonoro globalmente
- **WHEN** o usuário opta por desativar (mutar) os alertas sonoros através da interface
- **THEN** o sistema SHALL armazenar a preferência no armazenamento local (`localStorage`) e cessar imediatamente qualquer reprodução sonora de alerta em qualquer tela do sistema
