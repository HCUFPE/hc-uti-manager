## ADDED Requirements

### Requirement: Alerta Sonoro de Recorrência para Alertas da UTI
Sempre que houver algum alerta não lido/não confirmado pendente para a UTI, o sistema deve reproduzir o alerta sonoro a cada 30 segundos, desde que o usuário esteja logado com o perfil UTI e o som não esteja silenciado.

#### Scenario: Alerta pendente na UTI
- **GIVEN** o usuário está com perfil UTI e o som ativado
- **WHEN** chega um novo alerta para a UTI (não lido)
- **THEN** o sistema SHALL tocar o bipe sonoro de alerta a cada 30 segundos
- **AND** parar de tocar o bipe sonoro assim que a ciência for dada (alerta marcado como lido)
