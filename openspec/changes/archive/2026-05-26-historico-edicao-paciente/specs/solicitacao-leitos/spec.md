## ADDED Requirements

### Requirement: Troca de Paciente na Edição de Solicitação
Quando o usuário edita uma solicitação e altera o prontuário do paciente (caracterizando uma troca de paciente), o sistema MUST tratar essa ação internamente como o cancelamento da solicitação antiga e a criação de uma nova solicitação. O sistema MUST:
1. Cancelar a solicitação original, definindo o status como "Cancelada", atribuindo o motivo "Alteração de Prioridade pós Reserva de Leito", e registrando o cancelamento no histórico com data/hora e operador logado.
2. Criar uma nova solicitação com o novo prontuário informado, cujos dados demográficos e cirúrgicos serão recuperados do AGHU.
3. Se a solicitação original possuía leito reservado, a reserva do leito físico MUST permanecer ativa e ser transferida automaticamente para a nova solicitação criada, de modo que o leito físico passe a conter a reserva do novo paciente de forma ininterrupta.

#### Scenario: Edição com troca de paciente em vaga reservada
- **WHEN** o usuário edita uma solicitação que está reservada para o leito "UTI-01" alterando o prontuário do paciente
- **THEN** o sistema cancela a solicitação original, cria uma nova solicitação com os dados do novo prontuário, transfere a reserva do leito "UTI-01" para a nova solicitação, e gera os registros correspondentes no histórico

### Requirement: Registro Consistente de Auditoria no Histórico
O sistema MUST registrar um histórico de auditoria para toda ação que altere o estado de solicitações de leito ou reservas de leito físico. Cada entrada de histórico MUST conter:
1. Data e hora exata da ação.
2. O identificador/nome do operador (usuário logado) que executou a ação.
3. Descrição textual detalhada da ação executada (incluindo prontuários e leitos envolvidos).

#### Scenario: Gravação de log de auditoria ao realizar ações
- **WHEN** um usuário logado realiza qualquer operação de mudança de estado (criação, edição, reserva, remanejamento, liberação de encaminhamento ou cancelamento)
- **THEN** o sistema grava um registro de histórico contendo a data/hora atual, o nome do usuário operador e os detalhes descritivos da ação
