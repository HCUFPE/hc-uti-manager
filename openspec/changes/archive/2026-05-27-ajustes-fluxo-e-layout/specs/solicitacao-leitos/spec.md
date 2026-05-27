## MODIFIED Requirements

### Requirement: Controle de Permissões na Edição
O sistema MUST restringir a edição e cancelamento das solicitações apenas ao setor que as criou ou a administradores do sistema. EXCETO que usuários com papéis de UTI (`UTI`, `UTI-Admin`) MUST ter permissão para cancelar uma solicitação que esteja no status "Pendente", desde que o motivo do cancelamento seja obrigatoriamente "Falta de vaga de UTI".

Adicionalmente, o sistema MUST permitir a edição de solicitações mesmo que já possuam leito reservado, permitindo inclusive a alteração do prontuário do paciente (o que caracteriza uma troca de paciente). Ao cancelar uma vaga (reservada ou não), o sistema MUST exigir que seja informado um motivo de cancelamento, e se houver leito reservado, a reserva também MUST ser cancelada. O sistema também MUST garantir que a edição de dados reflita no banco de estados de leito correspondente e que o alerta de mudança de prioridade só ocorra caso a prioridade mude. 

Para o cancelamento de solicitação pendente pelos setores criadores ou administradores, os motivos permitidos MUST ser:
- Cirurgia suspensa por outros motivos
- Paciente encaminhado para enfermaria de origem após a cirurgia
- Alteração do mapa cirúrgico

Para o cancelamento de solicitação pendente por usuários da UTI (`UTI`, `UTI-Admin`), o motivo permitido MUST ser exclusivamente:
- Falta de vaga de UTI

#### Scenario: Edição de prontuário com troca de paciente
- **WHEN** o usuário seleciona uma solicitação reservada ou pendente para edição e altera o número do prontuário
- **THEN** o sistema SHALL permitir a digitação, consultar os novos dados no AGHU e, ao salvar, processar a troca registrando a nova solicitação e mantendo a reserva do leito físico correspondente
