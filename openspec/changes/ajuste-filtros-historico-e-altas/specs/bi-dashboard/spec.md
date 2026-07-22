## ADDED Requirements

### Requirement: Filtro Agrupado por Tipo de Ação no Histórico
O sistema MUST apresentar exatamente 3 opções de filtro por tipo de ação na tela de Histórico:
- **Altas**: consolida ações de alta (`alta`), definição/mudança de destino (`alteracao_destino`, `destino_disponivel`, `destino_pendente`) e cancelamento de alta (`cancelamento`).
- **Solicitações**: consolida criação de solicitação (`nova_solicitacao`), edição (`edicao`) e cancelamento/exclusão de solicitação (`exclusao_solicitacao`).
- **Reservas**: consolida reservas (`reserva`), remanejamento/redefinição de reserva (`remanejamento_reserva`) e cancelamento de reserva (`cancelamento_reserva`).

#### Scenario: Filtragem por Altas no Histórico
- **WHEN** o usuário seleciona o filtro "Altas" na tela de histórico
- **THEN** o sistema exibe apenas os eventos de alta, alteração de destino e cancelamento de alta

#### Scenario: Filtragem por Solicitações no Histórico
- **WHEN** o usuário seleciona o filtro "Solicitações" na tela de histórico
- **THEN** o sistema exibe apenas os eventos de nova solicitação, edição e exclusão de solicitação

#### Scenario: Filtragem por Reservas no Histórico
- **WHEN** o usuário seleciona o filtro "Reservas" na tela de histórico
- **THEN** o sistema exibe apenas os eventos de reserva, remanejamento de reserva e cancelamento de reserva

### Requirement: Nomenclatura de Altas Pendentes no Dashboard
O painel de indicadores MUST exibir o termo "Altas Pendentes (Aguardando Transferência)" para o indicador de altas ativas que aguardam saída da UTI.

#### Scenario: Exibição do indicador de altas pendentes
- **WHEN** o usuário abre a tela de indicadores
- **THEN** o sistema apresenta a linha de volume correspondente com o texto "Altas Pendentes (Aguardando Transferência)"
