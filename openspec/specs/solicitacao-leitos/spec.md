# solicitacao-leitos Specification

## Purpose
TBD - created by archiving change setup-openspec-docs. Update Purpose after archive.
## Requirements
### Requirement: Criação de Solicitação de Leito
O sistema MUST permitir que usuários dos setores solicitantes (Bloco Cirúrgico, Centro Obstétrico e Hemodinâmica) criem requisições de leito de UTI. O sistema MUST rejeitar e impedir a criação de uma nova solicitação se já houver uma solicitação ativa ('Pendente' ou 'Reservado') para o mesmo prontuário de paciente.

#### Scenario: Solicitação de vaga bem sucedida
- **WHEN** o usuário de um setor solicitante preenche o prontuário, data da cirurgia e especialidade
- **THEN** o sistema salva a requisição com o status inicial adequado
- **THEN** a solicitação passa a aparecer na fila de avaliação da UTI

#### Scenario: Rejeição de solicitação duplicada para mesmo prontuário ativo
- **WHEN** o usuário tenta cadastrar uma solicitação para um prontuário que já tem status "Pendente" ou "Reservado" no sistema
- **THEN** o sistema bloqueia o cadastro e retorna uma mensagem de erro indicando que já há uma solicitação ativa para aquele prontuário

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

### Requirement: Sinalização de Cirurgia Finalizada pelos Solicitantes
O sistema MUST permitir que usuários com os perfis solicitantes (BC, COB, HEM, seus respectivos administradores, ou administradores do sistema) marquem uma solicitação de leito com status "reservada" como "Cirurgia Finalizada".

#### Scenario: Solicitante sinaliza fim da cirurgia
- **WHEN** o usuário de um setor solicitante clica no botão "Cirurgia Finalizada" em sua fila de solicitações reservadas
- **THEN** o sistema atualiza o status de encaminhamento da solicitação para "Cirurgia Finalizada" e notifica a UTI

### Requirement: Remanejamento de Reserva de Leito pela UTI
O sistema MUST permitir que a equipe da UTI e administradores alterem diretamente o leito reservado de uma solicitação com status "Reservado" para outro leito disponível.

#### Scenario: Remanejamento de leito de reserva
- **WHEN** o usuário da UTI visualiza uma solicitação com leito reservado e solicita a alteração do leito destino, selecionando um novo leito vago
- **THEN** o sistema remove a reserva do leito original, transfere-a para o novo leito de destino e atualiza as informações de destino da solicitação, mantendo o status "Reservado" e registrando a mudança no histórico

### Requirement: Integração com AGHU no Cadastro de Solicitação
Ao cadastrar uma nova solicitação de vaga/leito, o sistema MUST integrar com o banco de dados do AGHU para recuperar automaticamente os dados demográficos e cirúrgicos do paciente com base no prontuário informado, simplificando o processo de entrada para o usuário. Os campos que MUST ser importados são: Nome do Paciente, Data de Nascimento, Especialidade, Procedimento Principal, Data da Cirurgia e Hora de Início.

O sistema MUST mapear o turno automaticamente a partir da hora de início da cirurgia nos seguintes intervalos:
- **Manhã**: das 07:00 às 12:59
- **Tarde**: das 13:00 às 18:59
- **Noite**: das 19:00 às 06:59 (no dia seguinte)

A prioridade inicial do paciente na fila e a ordem de exibição correspondente MUST ser definida de forma crescente com base na data da cirurgia e, em caso de empate na data, pelo turno (Manhã < Tarde < Noite) e, em caso de empate no turno, de forma cronológica pelo horário de início da cirurgia (horários mais cedo recebem prioridades maiores: P1, P2, P3...), exceto se o usuário informar especificamente uma prioridade de cadastro (ex: P3) no formulário, a qual MUST ser respeitada de forma prioritária e gravada imediatamente no banco de dados, aplicando as regras de reordenamento e deslocamento aos outros registros na fila.

No entanto, caso haja uma alteração de prioridade manual pelo usuário (ex: alterando de P2 para P1), o sistema MUST respeitar e manter a prioridade definida manualmente para a solicitação em foco, deslocando as demais solicitações do mesmo bucket (mesma data da cirurgia e turno) de acordo com sua ordem cronológica relativa para garantir uma fila contínua sem duplicatas ou lacunas.

No ambiente de desenvolvimento local (Mock), o sistema MUST retornar dados simulados de cirurgia. Para possibilitar testes locais de transição de datas e indicadores temporais:
1. O prontuário `6` MUST retornar dados de cirurgia agendada para o **dia seguinte** (amanhã).
2. O prontuário `7` MUST retornar dados de cirurgia agendada para **2 dias no futuro** (depois de amanhã).
3. Outros prontuários sem mapeamento estático mockado MUST retornar cirurgia para o dia corrente.

#### Scenario: Cadastro de solicitação com prontuário localizado com sucesso
- **WHEN** o usuário solicitante fornece um prontuário válido e com cirurgia programada ativa no AGHU e clica em cadastrar
- **THEN** o sistema executa a consulta no AGHU, recupera os dados, calcula a idade e o turno correspondente, define a prioridade de acordo com a ordem cronológica do início da cirurgia para aquele dia/turno, e cria a solicitação no status "Pendente"

#### Scenario: Cadastro de solicitação com prontuário inexistente ou cirurgia cancelada
- **WHEN** o usuário fornece um prontuário que não possui cirurgias programadas ou cujas cirurgias estão canceladas (`situacao = 'CANC'`) no AGHU
- **THEN** o sistema blocks o cadastro e retorna um erro informativo indicando que nenhuma cirurgia ativa foi encontrada para o prontuário fornecido

#### Scenario: Ajuste manual de prioridade na fila respeitado
- **WHEN** o usuário edita a prioridade de uma solicitação com id "5" de "P2" para "P1" em um bucket que contém as solicitações "2" (P1) e "5" (P2)
- **THEN** o sistema atualiza a solicitação "5" para "P1" e desloca a solicitação "2" para "P2", mantendo a integridade da fila sem duplicatas ou lacunas

#### Scenario: Cadastro de solicitação com prioridade informada manualmente
- **WHEN** o usuário solicitante fornece um prontuário válido e preenche a prioridade manual como "P3"
- **THEN** o sistema cria a solicitação com prioridade "P3" e reordena os demais pacientes do mesmo bucket de forma correspondente

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

### Requirement: Exibição do Horário da Cirurgia na Fila
O sistema MUST exibir o horário de início da cirurgia na visualização dos cards de solicitação de leito, posicionado especificamente entre a data prevista da cirurgia e o turno do paciente.

#### Scenario: Visualização do horário da cirurgia na fila
- **WHEN** o usuário visualiza a fila de solicitações no frontend
- **THEN** o sistema exibe o horário de início da cirurgia de forma clara no card de detalhes de cada solicitação pendente ou reservada

### Requirement: Atualização Automática da Fila de Solicitações
A tela de Fila de Solicitações do frontend MUST atualizar as informações de solicitações de leitos de UTI automaticamente a cada 2 minutos (120.000 ms) enquanto estiver ativa/montada.

#### Scenario: Atualização automática periódica na fila de solicitações
- **WHEN** o usuário estiver com a tela de Solicitações aberta
- **THEN** o sistema SHALL iniciar um temporizador (timer) que recarrega a lista de solicitações a cada 2 minutos
- **THEN** ao desmontar ou trocar de tela, o temporizador SHALL ser cancelado/limpo para evitar vazamentos de memória

### Requirement: Registro de Horário de Fim de Cirurgia e Liberação
A solicitação de leito MUST registrar o momento exato em que a cirurgia correspondente é finalizada e o momento exato em que o encaminhamento é liberado. Ao liberar o encaminhamento, o sistema MUST registrar o tempo decorrido no histórico de auditoria.

#### Scenario: Registro de fim da cirurgia e liberação de encaminhamento
- **WHEN** o solicitante clica em "Cirurgia Finalizada"
- **THEN** o sistema SHALL gravar a data e a hora atual no campo de cirurgia finalizada
- **WHEN** a UTI clica em "Liberar Encaminhamento"
- **THEN** o sistema SHALL gravar a data e a hora atual no campo de encaminhamento liberado, calcular a diferença de tempo e salvar o tempo decorrido na mensagem do histórico

### Requirement: Escala de Prioridade até P10
O formulário de criação e edição de solicitações de leito MUST permitir que o usuário classifique manualmente a prioridade do paciente em uma escala de P1 (Maior) até P10 (Menor).

#### Scenario: Visualização e seleção da prioridade P10
- **WHEN** o usuário abre o formulário de nova solicitação ou edição
- **THEN** a lista de opções de prioridade SHALL disponibilizar todas as opções de P1 a P10 de forma ordenada, onde P1 representa a maior prioridade e P10 a menor prioridade

