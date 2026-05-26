## MODIFIED Requirements

### Requirement: Registro Consistente de Auditoria no Histórico
O sistema MUST registrar um histórico de auditoria para toda ação que altere o estado de solicitações de leito ou reservas de leito físico. Cada entrada de histórico MUST conter:
1. Data e hora exata da ação.
2. O identificador/nome do operador (usuário logado) que executou a ação.
3. Descrição textual detalhada da ação executada (incluindo prontuários e leitos envolvidos).

Adicionalmente, o sistema MUST registrar no histórico de ações:
- Um evento com tipo `"conclusao"` quando um paciente ocupa fisicamente o leito reservado (sincronizado através do censo).
- Um evento com tipo `"conclusao_alta"` quando um paciente com alta ativa deixa fisicamente o leito de UTI.

#### Scenario: Gravação de log de auditoria ao realizar ações
- **WHEN** um usuário logado realiza qualquer operação de mudança de estado (criação, edição, reserva, remanejamento, liberação de encaminhamento ou cancelamento)
- **THEN** o sistema grava um registro de histórico contendo a data/hora atual, o nome do usuário operador e os detalhes descritivos da ação

#### Scenario: Gravação de log de ocupação física de leito
- **WHEN** o sistema detecta (durante listagem/sincronização de leitos) que o paciente reservado ocupou o leito correspondente e atualiza a solicitação para "Concluída"
- **THEN** o sistema registra no histórico de ações um evento do tipo `"conclusao"` descrevendo a admissão do paciente

#### Scenario: Gravação de log de saída física de alta de leito
- **WHEN** o sistema detecta (durante listagem/sincronização de leitos) que um leito com alta ativa foi liberado (o prontuário atual no censo difere da alta)
- **THEN** o sistema atualiza o status da alta para "concluida" e grava no histórico um evento de tipo `"conclusao_alta"`
