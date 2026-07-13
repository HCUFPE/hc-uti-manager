## ADDED Requirements

### Requirement: Botão de Retorno na Página de Alertas
A página de todos os alertas MUST exibir um botão "Voltar ao Painel" destacado para permitir que o usuário retorne à página inicial sem depender do histórico do navegador.

#### Scenario: Visualização do botão de retorno
- **WHEN** o usuário acessa a página `/alertas`
- **THEN** o botão "Voltar ao Painel" SHALL estar visível no topo da página

### Requirement: Confirmação de Ciência no Popover de Notificações
O popover de notificações de leitos MUST permitir que o usuário marque um alerta individual como lido/ciente diretamente na lista suspensa do sininho.

#### Scenario: Clicar em "Ciente" no popover
- **WHEN** o usuário visualiza as notificações no popover e clica em "Ciente"
- **THEN** o alerta correspondente SHALL ser marcado como lido no backend e removido da visualização pendente do popover
