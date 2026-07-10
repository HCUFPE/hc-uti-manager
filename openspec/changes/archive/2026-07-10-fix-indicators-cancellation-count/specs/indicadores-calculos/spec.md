## ADDED Requirements

### Requirement: Cálculo Preciso de Solicitações Canceladas
O sistema MUST contar corretamente as solicitações canceladas e exibi-las no dashboard de indicadores, mapeando o tipo de evento `"exclusao_solicitacao"` gravado no histórico de ações.

#### Scenario: Contagem de solicitações canceladas
- **WHEN** existem solicitações canceladas registradas como "exclusao_solicitacao" no histórico de ações do período
- **THEN** a contagem de solicitações canceladas no dashboard de indicadores SHALL refletir a quantidade exata dessas ocorrências
