## ADDED Requirements

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
