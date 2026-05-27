## ADDED Requirements

### Requirement: Atualização Automática da Fila de Solicitações
A tela de Fila de Solicitações do frontend MUST atualizar as informações de solicitações de leitos de UTI automaticamente a cada 2 minutos (120.000 ms) enquanto estiver ativa/montada.

#### Scenario: Atualização automática periódica na fila de solicitações
- **WHEN** o usuário estiver com a tela de Solicitações aberta
- **THEN** o sistema SHALL iniciar um temporizador (timer) que recarrega a lista de solicitações a cada 2 minutos
- **THEN** ao desmontar ou trocar de tela, o temporizador SHALL ser cancelado/limpo para evitar vazamentos de memória
