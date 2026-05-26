## MODIFIED Requirements

### Requirement: Controle de Permissões na Edição
O sistema MUST restringir a edição e cancelamento das solicitações apenas ao setor que as criou ou a administradores do sistema. EXCETO que usuários com papéis de UTI (`UTI`, `UTI-Admin`) MUST ter permissão para cancelar uma solicitação que esteja no status "Pendente", desde que o motivo do cancelamento seja obrigatoriamente "Falta de vaga de UTI".

Adicionalmente, o sistema MUST bloquear a edição de solicitações que já possuem leito reservado, EXCETO para usuários com papéis específicos (BC, BC-ADMIN, COB, COB-ADMIN, HEM, HEM-ADMIN). Ao cancelar uma vaga (reservada ou não), o sistema MUST exigir que seja informado um motivo de cancelamento, e se houver leito reservado, a reserva também MUST ser cancelada. O sistema também MUST garantir que a edição de dados reflita no banco de estados de leito correspondente e que o alerta de mudança de prioridade só ocorra caso a prioridade mude. 

Para o cancelamento de solicitação pendente pelos setores criadores ou administradores, os motivos permitidos MUST ser:
- Cirurgia suspensa por outros motivos
- Paciente encaminhado para enfermaria de origem após a cirurgia
- Alteração do mapa cirúrgico

Para o cancelamento de solicitação pendente por usuários da UTI (`UTI`, `UTI-Admin`), o motivo permitido MUST ser exclusivamente:
- Falta de vaga de UTI

#### Scenario: Cancelamento de solicitação pendente pelo próprio criador
- **WHEN** a cirurgia é suspensa ou a vaga não é mais necessária e o usuário do setor criador cancela o pedido pendente
- **THEN** o sistema exibe a lista dos motivos pré-definidos (como "Alteração do mapa cirúrgico"), exige a seleção de um deles, remove da fila ativa da UTI e registra no histórico com o motivo correspondente

#### Scenario: Cancelamento de solicitação pendente pela UTI por falta de vagas
- **WHEN** o usuário do perfil UTI decide cancelar uma solicitação que está na fila (status "Pendente") devido à indisponibilidade de leitos
- **THEN** o sistema exibe uma confirmação exigindo o motivo fixo "Falta de vaga de UTI", cancela a solicitação e registra o cancelamento com o respectivo motivo e o operador da UTI no histórico
