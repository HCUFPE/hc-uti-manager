# solicitacao-leitos Specification

## Purpose
TBD - created by archiving change setup-openspec-docs. Update Purpose after archive.
## Requirements
### Requirement: Criação de Solicitação de Leito
O sistema MUST permitir que usuários dos setores solicitantes (Bloco Cirúrgico, Centro Obstétrico e Hemodinâmica) criem requisições de leito de UTI.

#### Scenario: Solicitação de vaga bem sucedida
- **WHEN** o usuário de um setor solicitante preenche o prontuário, data da cirurgia e especialidade
- **THEN** o sistema salva a requisição com o status inicial adequado
- **THEN** a solicitação passa a aparecer na fila de avaliação da UTI

### Requirement: Gestão da Fila e Reserva pela UTI
O sistema MUST permitir que a equipe da UTI visualize a fila de solicitações e atribua leitos físicos aos pacientes aprovados, bem como cancele reservas informando obrigatoriamente um motivo.

#### Scenario: Reserva de leito
- **WHEN** o usuário da UTI avalia uma solicitação pendente e vincula um número de leito físico
- **THEN** o status da solicitação é atualizado para sinalizar que o leito está reservado
- **THEN** o setor solicitante consegue ver que o paciente tem um leito garantido

#### Scenario: Cancelamento de reserva de leito
- **WHEN** o usuário da UTI precisa desfazer uma reserva
- **THEN** o sistema exige a seleção de um motivo pré-definido para o cancelamento
- **THEN** a reserva é desfeita, a solicitação volta para pendente e o histórico registra a ação

### Requirement: Controle de Permissões na Edição
O sistema MUST restringir a edição e cancelamento das solicitações apenas ao setor que as criou ou a administradores do sistema. Adicionalmente, o sistema MUST bloquear a edição de solicitações que já possuem leito reservado, EXCETO para usuários com papéis específicos (BC, BC-ADMIN, COB, COB-ADMIN, HEM, HEM-ADMIN). Ao cancelar uma vaga (reservada ou não), o sistema MUST exigir que seja informado um motivo de cancelamento, e se houver leito reservado, a reserva também MUST ser cancelada. O sistema também MUST garantir que a edição de dados reflita no banco de estados de leito correspondente e que o alerta de mudança de prioridade só ocorra caso a prioridade mude.

#### Scenario: Cancelamento de solicitação pendente
- **WHEN** a cirurgia é suspensa ou a vaga não é mais necessária
- **THEN** o sistema exibe uma lista de motivos pré-definidos e exige a seleção de um
- **THEN** o setor solicitante cancela o pedido e o sistema remove da fila ativa da UTI
- **THEN** o sistema registra a exclusão e o motivo escolhido no histórico do paciente

#### Scenario: Cancelamento de solicitação reservada por usuário especial
- **WHEN** um usuário com permissão gestora tenta cancelar uma solicitação já reservada
- **THEN** o sistema limpa a reserva do leito físico e cancela a solicitação em seguida
- **THEN** o motivo de cancelamento é registrado no histórico do paciente

#### Scenario: Edição de solicitação com leito reservado por usuário com perfil especial
- **WHEN** um usuário com as roles gestoras edita uma solicitação reservada
- **THEN** o sistema permite o acesso ao formulário de edição e processa a atualização
- **THEN** os novos dados (idade, prontuário, especialidade) são replicados no leito físico associado
- **THEN** o histórico registra apenas as ações correspondentes sem falsos positivos de "mudança de prioridade"

