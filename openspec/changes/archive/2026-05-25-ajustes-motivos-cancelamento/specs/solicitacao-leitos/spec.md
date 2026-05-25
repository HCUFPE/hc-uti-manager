## MODIFIED Requirements

### Requirement: Gestão da Fila e Reserva pela UTI
O sistema MUST permitir que a equipe da UTI visualize a fila de solicitações e atribua leitos físicos aos pacientes aprovados, bem como cancele reservas informando obrigatoriamente um motivo pré-definido da lista de cancelamento de reserva (tipo 2). Os motivos permitidos para o cancelamento de reserva pela UTI MUST ser:
- Pedido de vaga clínica (emergência)
- Pedido de vaga pela hemodinâmica
- Pedido de vaga pelo COB (emergência)
- Problemas relacionados a equipamentos
- Falta de vaga na enfermaria para paciente de alta
- Cancelamento de alta da UTI

#### Scenario: Reserva de leito
- **WHEN** o usuário da UTI avalia uma solicitação pendente e vincula um número de leito físico
- **THEN** o status da solicitação é atualizado para sinalizar que o leito está reservado
- **THEN** o setor solicitante consegue ver que o paciente tem um leito garantido

#### Scenario: Cancelamento de reserva de leito
- **WHEN** o usuário da UTI precisa desfazer uma reserva
- **THEN** o sistema exige a seleção de um motivo pré-definido da nova lista clínica/operacional para o cancelamento
- **THEN** a reserva é desfeita, a solicitação volta para pendente e o histórico registra a ação com o respectivo motivo

### Requirement: Controle de Permissões na Edição
O sistema MUST restringir a edição e cancelamento das solicitações apenas ao setor que as criou ou a administradores do sistema. Adicionalmente, o sistema MUST bloquear a edição de solicitações que já possuem leito reservado, EXCETO para usuários com papéis específicos (BC, BC-ADMIN, COB, COB-ADMIN, HEM, HEM-ADMIN). Ao cancelar uma vaga (reservada ou não), o sistema MUST exigir que seja informado um motivo de cancelamento, e se houver leito reservado, a reserva também MUST ser cancelada. O sistema também MUST garantir que a edição de dados reflita no banco de estados de leito correspondente e que o alerta de mudança de prioridade só ocorra caso a prioridade mude. Para o cancelamento de solicitação pendente, os motivos permitidos MUST ser:
- Cirurgia suspensa por outros motivos
- Paciente encaminhado para enfermaria de origem após a cirurgia
- Alteração do mapa cirúrgico

#### Scenario: Cancelamento de solicitação pendente
- **WHEN** a cirurgia é suspensa ou a vaga não é mais necessária e o usuário cancela o pedido pendente
- **THEN** o sistema exibe a lista atualizada de motivos pré-definidos, exige a seleção de um deles, remove da fila ativa da UTI e registra no histórico com o motivo correspondente
