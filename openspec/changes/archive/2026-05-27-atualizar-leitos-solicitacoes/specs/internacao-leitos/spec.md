## ADDED Requirements

### Requirement: Atualização Automática do Censo e Leitos
A tela do Painel de Leitos (Home) do frontend MUST atualizar as informações de leitos e censo automaticamente a cada 2 minutos (120.000 ms) enquanto estiver ativa/montada.

#### Scenario: Atualização automática periódica no painel de leitos
- **WHEN** o usuário estiver com a tela do Painel de Leitos (Home) aberta
- **THEN** o sistema SHALL iniciar um temporizador (timer) que recarrega a lista de leitos a cada 2 minutos
- **THEN** ao desmontar ou trocar de tela, o temporizador SHALL ser cancelado/limpo para evitar vazamentos de memória
