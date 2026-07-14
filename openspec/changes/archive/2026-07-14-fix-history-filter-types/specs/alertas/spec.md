## ADDED Requirements

### Requirement: Filtro de Alta no Histórico
O filtro de tipo "Alta" no Histórico de Ações MUST retornar todas as ações relacionadas a altas solicitadas (`alta`) e altas concluídas (`conclusao_alta`).

#### Scenario: Filtrando por Alta
- **WHEN** o usuário seleciona o filtro "Alta" no histórico de ações
- **THEN** o sistema SHALL retornar registros de tipos `alta` e `conclusao_alta`

### Requirement: Filtro de Destino no Histórico
O filtro de tipo "Destino" no Histórico de Ações MUST retornar todas as ações relacionadas a definições de destino (`alteracao_destino`), destinação disponível (`destino_disponivel`) ou liberação pendente/cancelada (`destino_pendente`).

#### Scenario: Filtrando por Destino
- **WHEN** o usuário seleciona o filtro "Destino" no histórico de ações
- **THEN** o sistema SHALL retornar registros de tipos `alteracao_destino`, `destino_disponivel` e `destino_pendente`
