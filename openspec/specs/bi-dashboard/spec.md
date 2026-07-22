# bi-dashboard Specification

## Purpose
TBD - created by archiving change setup-openspec-docs. Update Purpose after archive.
## Requirements
### Requirement: Integração com Metabase
O sistema MUST apresentar painéis gerenciais e analíticos usando componentes do Metabase.

#### Scenario: Visualização de Dashboards
- **WHEN** o usuário navega para a seção de relatórios
- **THEN** o sistema carrega o painel de BI correspondente através de integração em iframe/API

### Requirement: Acesso ao Dashboard de Indicadores e Histórico para Perfis Admin
O sistema MUST permitir que todos os usuários com perfil de administrador setorial (`*-Admin`, ou seja, `UTI-Admin`, `NIR-Admin`, `COB-Admin`, `BC-Admin` e `HEM-Admin`) e administradores do sistema (`Administrador` ou `admin`) acessem as rotas de API e as telas de interface correspondentes ao Histórico de Ações e Indicadores.

#### Scenario: Usuário com perfil setorial admin acessa indicadores
- **WHEN** um usuário logado com o perfil `BC-Admin` tenta visualizar o painel de Indicadores
- **THEN** o sistema exibe a interface com gráficos e métricas de desempenho

### Requirement: Filtro de Data na Tela de Indicadores
A tela de Indicadores MUST apresentar campos de seleção de período (data de início e data de fim) permitindo ao usuário refinar e atualizar os indicadores de forma dinâmica.

#### Scenario: Usuário seleciona período de datas
- **WHEN** o usuário define uma data de início e fim no filtro e clica em aplicar
- **THEN** a tela recarrega os dados de indicadores com base no intervalo de datas selecionado

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

