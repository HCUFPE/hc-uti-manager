## MODIFIED Requirements

### Requirement: Prevenção de Alertas Duplicados
O sistema MUST garantir que alertas gerados a partir do histórico de ações ou estados de leitos não sejam duplicados quando a rotina de sincronização for executada múltiplas vezes. A comparação de data/hora do alerta com a do histórico SHALL desconsiderar variações de fuso horário e precisão de microssegundos para evitar duplicidade. Adicionalmente, a verificação de data para hoje SHALL normalizar de forma robusta e unificada os formatos de data (`DD-MM-YYYY`, `DD/MM/YYYY` e `YYYY-MM-DD`).

#### Scenario: Sincronização repetida de histórico
- **WHEN** a rotina de geração de alertas é executada repetidamente para os mesmos eventos de histórico com pequenas variações de fuso horário ou microssegundos
- **THEN** o sistema SHALL identificar que o alerta já existe no banco e não criar um novo registro duplicado

#### Scenario: Validação de data em formatos mistos
- **WHEN** a rotina de geração de alertas valida se uma cirurgia é para hoje a partir de dados em formatos `DD-MM-YYYY` (SQLite local) ou `DD/MM/YYYY`
- **THEN** o sistema SHALL converter a data para `YYYY-MM-DD` e realizar a comparação com sucesso
