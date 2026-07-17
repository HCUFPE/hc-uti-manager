## MODIFIED Requirements

### Requirement: Cálculo dos Indicadores de Volume e Percentuais Relativos
O sistema MUST calcular métricas volumétricas absolutas e percentuais relativos: quantidade total de solicitações feitas, quantidade de solicitações reservadas, quantidade de solicitações reservadas e concluídas, quantidade de cancelamento de solicitações, quantidade de cancelamento de reservas, quantidade de altas solicitadas e percentuais em relação à quantidade de solicitações feitas e reservas concluídas.

**Agrupamento de Motivos de Cancelamento**: Ao extrair e contabilizar os motivos de cancelamento das solicitações no período para exibição na tabela de indicadores, o sistema MUST limpar qualquer detalhe de substituição de prontuários (como o padrão `" (Prontuário X foi substituído pelo Prontuário Y)"`) do texto do motivo. Isso garante que os motivos sejam agregados de forma consistente sob termos padronizados (ex: `"Alteração de Prioridade pós Solicitação"` e `"Alteração de Prioridade pós Reserva de Leito"`).

#### Scenario: Cálculo de volumes e percentuais
- **WHEN** o sistema consolida todas as contagens de estados e eventos no período filtrado
- **THEN** o sistema retorna os totais absolutos e as relações percentuais especificadas

#### Scenario: Agrupamento consolidado de motivos de cancelamento com swap de paciente
- **WHEN** o histórico de ações contém cancelamentos com detalhes contendo substituição de prontuário, como "Alteração de Prioridade pós Solicitação (Prontuário 22348742 foi substituído pelo Prontuário 22349963)"
- **THEN** o sistema remove a informação de substituição e contabiliza o motivo sob a chave consolidada "Alteração de Prioridade pós Solicitação"
