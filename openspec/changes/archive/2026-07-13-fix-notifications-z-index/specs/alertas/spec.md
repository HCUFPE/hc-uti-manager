## ADDED Requirements

### Requirement: Ordenação 3D (z-index) do Popover de Notificações
O popover de notificações MUST flutuar acima de qualquer outro elemento na tela, incluindo os cards de leitos.

#### Scenario: Interação com o Popover
- **GIVEN** o usuário abre o popover de notificações
- **THEN** o painel contendo a listagem de alertas SHALL ser renderizado por cima de todos os cards de leitos na página principal
