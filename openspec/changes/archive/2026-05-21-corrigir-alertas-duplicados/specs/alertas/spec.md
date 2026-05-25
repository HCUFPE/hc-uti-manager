## ADDED Requirements

### Requirement: Prevenção de Alertas Duplicados
O sistema MUST garantir que alertas gerados a partir do histórico de ações ou estados de leitos não sejam duplicados quando a rotina de sincronização for executada múltiplas vezes.

#### Scenario: Sincronização repetida de histórico
- **WHEN** a rotina de geração de alertas é executada repetidamente para os mesmos eventos de histórico com pequenas variações de milissegundos
- **THEN** o sistema SHALL identificar que o alerta já existe no banco e não criar um novo registro duplicado

### Requirement: Preservação de Histórico de Alertas Gargalo
O sistema MUST manter persistidos todos os alertas da categoria "Gargalo" (como solicitações de alta, acomodações definidas e eventos históricos da UTI), mesmo que a condição de origem não seja mais ativa ou a janela de 24 horas tenha expirado.

#### Scenario: Sincronização após término de pendência
- **WHEN** uma solicitação de alta é resolvida ou cancelada, ou um evento do histórico passa do limite de 24 horas
- **THEN** o sistema SHALL manter o alerta correspondente na tabela de alertas (sem excluí-lo) para fins de registro histórico
