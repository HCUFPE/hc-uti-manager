## ADDED Requirements

### Requirement: Modo TV para Visualização de Leitos
O sistema MUST oferecer um Modo TV (Monitoramento Dedicado) que oculta a barra lateral, o cabeçalho e os cards de estatísticas resumidas do topo, maximizando a área de exibição e aumentando a densidade do grid de leitos para que caibam na tela sem necessidade de rolagem vertical.

#### Scenario: Ativação do Modo TV
- **WHEN** o usuário clica no botão de alternância do Modo TV
- **THEN** a barra lateral, o cabeçalho principal e os cards de métricas do topo SHALL ser ocultados
- **THEN** o grid de leitos SHALL ser exibido com maior densidade de colunas

### Requirement: Filtro de Status com Seleção Múltipla
O painel de monitoramento de leitos MUST permitir a seleção de múltiplos status ao mesmo tempo, aplicando a união dos leitos correspondentes aos status selecionados.

#### Scenario: Seleção de múltiplos filtros de status
- **WHEN** o usuário seleciona "Disponíveis" e depois "Reservado"
- **THEN** a tela de leitos SHALL exibir simultaneamente todos os leitos com status "Disponível" ou "Reservado"
