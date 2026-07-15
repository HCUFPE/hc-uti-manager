# internacao-leitos Specification

## Purpose
TBD - created by archiving change setup-openspec-docs. Update Purpose after archive.
## Requirements
### Requirement: Gestão de Leitos
O sistema MUST gerenciar o censo de internação, mostrando a disponibilidade e ocupação dos leitos. O sistema MUST considerar como leitos disponíveis para reserva aqueles com status "Livre", "Alta", "Limpeza" ou "Higienização".

#### Scenario: Ocupação de Leito
- **WHEN** um paciente é admitido na unidade e associado ao leito
- **THEN** o sistema atualiza o status do leito para ocupado e exibe no mapa de leitos

#### Scenario: Reserva de Leito em Higienização
- **WHEN** um usuário busca leitos disponíveis para reserva de uma solicitação
- **THEN** os leitos com status "Limpeza" e "Higienização" também são listados como opções válidas

### Requirement: Exigência de Motivo no Cancelamento de Reserva na Visão de Leitos
O sistema MUST exigir que a equipe da UTI (ou Administradores) selecione obrigatoriamente um motivo pré-definido da lista de cancelamento de reserva (tipo 2) ao cancelar uma reserva de leito a partir da visão geral/card de leitos do painel principal, impedindo o cancelamento sem justificativa.

#### Scenario: Cancelamento de reserva com motivo informado
- **WHEN** o usuário clica em "Cancelar Reserva" no card do leito e escolhe um motivo da lista pré-definida
- **THEN** o sistema abre um modal de confirmação, exige a seleção do motivo, envia para o backend, desfaz a reserva localmente e registra o cancelamento com o respectivo motivo no histórico

### Requirement: Motivos de Cancelamento de Alta
O sistema MUST disponibilizar os seguintes motivos pré-definidos para cancelamento de alta na visão geral de leitos: "Piora Clínica" e "Leito de Enfermaria Indisponível".

#### Scenario: Cancelamento de alta
- **WHEN** o usuário clica em "Cancelar Alta" em um leito com alta solicitada e seleciona o motivo correspondente
- **THEN** o sistema atualiza o status do leito para ocupado e registra no histórico o cancelamento com o motivo escolhido

### Requirement: Cancelamento de Alta pelo NIR
O sistema MUST permitir que os usuários do perfil NIR (ou Administradores) cancelem solicitações de alta ativa a partir da fila de solicitações de alta recebidas, fornecendo obrigatoriamente um motivo justificado da lista.

#### Scenario: Cancelamento com sucesso pelo NIR
- **WHEN** o usuário do NIR clica em "Cancelar Solicitação" e escolhe o motivo "Leito de Enfermaria Indisponível"
- **THEN** o sistema cancela a solicitação de alta no banco de dados e registra a ação sob o operador do NIR no histórico de ações

### Requirement: Atualização Visual e Liberação de Encaminhamento pela UTI
O sistema MUST gerenciar o fluxo visual e a autorização de transferência de pacientes com leito de UTI reservado pós-cirúrgico.

#### Scenario: Reserva fica amarela após cirurgia finalizada
- **WHEN** uma reserva vinculada a um leito é sinalizada como "Cirurgia Finalizada"
- **THEN** o card do leito no painel da UTI SHALL apresentar destaque na cor amarela indicando a prontidão do paciente
- **THEN** o botão "Liberar Encaminhamento" SHALL ficar disponível para a equipe da UTI nesse leito

#### Scenario: Animação piscante no card do leito para a UTI
- **WHEN** um usuário logado com o perfil UTI (ou Administrador) visualiza o painel de leitos e o leito possui uma reserva ativa com status "Cirurgia Finalizada"
- **THEN** o card do leito correspondente SHALL apresentar uma animação piscante (pulsando a opacidade/borda de cor amarela continuamente)
- **THEN** se o perfil logado não for UTI (ou Administrador), a animação piscante SHALL estar desabilitada e o leito se manterá com o destaque amarelo estático

#### Scenario: Alerta sonoro de cirurgia finalizada para a UTI
- **WHEN** o Painel de Leitos é atualizado e detecta que uma cirurgia foi recém-finalizada para um leito reservado e o usuário logado pertence ao perfil UTI (ou Administrador)
- **THEN** o sistema SHALL reproduzir um sinal sonoro curto de notificação se o som estiver ativado nas configurações do painel
- **THEN** se o perfil logado não for UTI (ou Administrador), nenhum som SHALL ser executado

#### Scenario: Liberação de encaminhamento pela UTI e reserva verde
- **WHEN** o usuário da UTI clica em "Liberar Encaminhamento" no card do leito
- **THEN** o sistema altera o status do encaminhamento para "Encaminhamento Liberado"
- **THEN** o card do leito no painel da UTI SHALL apresentar destaque na cor verde indicando que a transferência está autorizada
- **THEN** a animação piscante e a reprodução de alertas sonoros para esse leito SHALL ser encerrada

#### Scenario: UTI cancela liberação de encaminhamento
- **WHEN** o usuário da UTI clica em "Cancelar Liberação" no card do leito com status "Encaminhamento Liberado"
- **THEN** o sistema altera o status do encaminhamento para "Cirurgia Finalizada" (não liberado)
- **THEN** o card do leito no painel da UTI SHALL voltar a apresentar destaque na cor amarela piscante (para perfil UTI)

#### Scenario: Controle de som no painel de leitos
- **WHEN** o usuário do painel com perfil UTI (ou Administrador) clica no controle de ativar/desativar som
- **THEN** o sistema SHALL alternar o estado do áudio de notificações e persistir essa escolha no local storage do navegador

### Requirement: Remanejamento de Reserva no Card do Leito
O sistema MUST permitir que a equipe da UTI (ou Administradores) altere o leito físico reservado de um paciente diretamente a partir da visualização de cards de leitos.

#### Scenario: Visualização do botão de remanejamento no card
- **WHEN** o usuário visualiza o card de um leito que possui uma reserva ativa
- **THEN** o botão "Mudar Leito" SHALL estar disponível no card (caso o perfil seja UTI ou Administrador)

#### Scenario: Remanejamento de reserva executado com sucesso
- **WHEN** o usuário clica em "Mudar Leito", seleciona um novo leito disponível e confirma a ação
- **THEN** o sistema atualiza o leito de destino do paciente para o novo leito selecionado e limpa a reserva do leito original

### Requirement: Lista de Múltipla Escolha para Necessidades Especiais de Alta
Ao registrar uma nova solicitação de alta para um leito de UTI, o sistema MUST disponibilizar um rol de seleção múltipla (checkboxes) para a especificação das necessidades especiais do paciente, em substituição ao campo de texto livre. As opções disponíveis no rol MUST ser:
- Isolamento de contato
- Isolamento respiratório
- Em uso de O2
- Necessidade de aspiração
- Necessidade de ventilador no leito
- Nenhum

O sistema MUST gerenciar a exclusão mútua das seleções da seguinte forma:
1. Se o usuário marcar "Nenhum", todas as outras opções selecionadas devem ser desmarcadas automaticamente.
2. Se o usuário marcar qualquer outra opção que não seja "Nenhum", a opção "Nenhum" deve ser desmarcada automaticamente.
3. Se o usuário não marcar nenhuma opção explicitamente, o sistema MUST assumir e persistir o valor "Nenhum".

O sistema MUST persistir a seleção concatenando as opções escolhidas em uma única string separada por vírgula no banco de dados local para manter a compatibilidade com a coluna de texto existente.

#### Scenario: Solicitação de alta com múltiplas necessidades específicas
- **WHEN** o usuário abre o modal de alta, seleciona as opções "Isolamento de contato" e "Em uso de O2" e confirma a solicitação
- **THEN** o sistema desmarca a opção "Nenhum" se estivesse selecionada e envia o payload com a string formatada "Isolamento de contato, Em uso de O2" para persistência no banco

#### Scenario: Solicitação de alta com a opção Nenhum ou sem seleção
- **WHEN** o usuário abre o modal de alta, seleciona a opção "Nenhum" (ou não seleciona nenhuma das opções) e confirma a solicitação
- **THEN** o sistema desmarca as outras opções se estivessem selecionadas e envia o payload com a string formatada "Nenhum" para persistência no banco

### Requirement: Atualização Automática do Censo e Leitos
A tela do Painel de Leitos (Home) do frontend MUST atualizar as informações de leitos e censo automaticamente a cada 2 minutos (120.000 ms) enquanto estiver ativa/montada.

#### Scenario: Atualização automática periódica no painel de leitos
- **WHEN** o usuário estiver com a tela do Painel de Leitos (Home) aberta
- **THEN** o sistema SHALL iniciar um temporizador (timer) que recarrega a lista de leitos a cada 2 minutos
- **THEN** ao desmontar ou trocar de tela, o temporizador SHALL ser cancelado/limpo para evitar vazamentos de memória

### Requirement: Exibição de Nome e Hora da Cirurgia na Reserva de Leito
O card de leito no painel principal, quando possuir uma reserva de próximo paciente ativa, MUST exibir o nome do próximo paciente e o horário programado de início da cirurgia. O horário da cirurgia MUST ser exibido no formato `DD/MM/AAAA - HH:MM`.

#### Scenario: Visualização dos dados adicionais da reserva
- **WHEN** o usuário visualiza o card de um leito que possui uma reserva ativa
- **THEN** o sistema SHALL exibir o nome do próximo paciente entre o número do prontuário e a idade
- **THEN** o sistema SHALL exibir a data e hora da cirurgia no formato "DD/MM/AAAA - HH:MM" no bloco de detalhes da cirurgia

### Requirement: Temporizador de Espera de Liberação no Card
O card de leito no painel da UTI, quando possuir um paciente com cirurgia finalizada mas sem encaminhamento liberado, MUST apresentar um temporizador indicando o tempo decorrido desde o encerramento da cirurgia. Uma vez que o encaminhamento seja liberado, o temporizador e o relógio MUST ser ocultados e o status do card alterado para indicar a liberação.

#### Scenario: Visualização do relógio com tempo de espera
- **WHEN** o usuário visualiza o card de um leito que está no status "Cirurgia Concluída" e o encaminhamento não foi liberado ainda
- **THEN** o card do leito SHALL exibir um ícone de relógio e um contador dinâmico (ex: "45m", "1h 12m") ao lado do texto de conclusão, representando o tempo de espera do paciente

#### Scenario: Ocultamento do relógio após liberação do encaminhamento
- **WHEN** o encaminhamento do paciente com cirurgia concluída é liberado pela UTI
- **THEN** o card do leito SHALL ocultar o temporizador de espera e exibir a etiqueta "Encaminhamento Liberado"

### Requirement: Detecção de Conflito de Reserva
O sistema MUST identificar e marcar como em conflito qualquer leito físico de UTI que possua uma reserva de paciente cadastrada localmente no banco de dados, mas que esteja atualmente ocupado por um paciente diferente no censo do hospital (AGHU), exceto se houver uma solicitação de alta ativa para o ocupante atual.

#### Scenario: Detecção de conflito em leito ocupado sem alta ativa
- **WHEN** o usuário do painel visualiza um leito reservado para o Paciente A, mas o censo do AGHU indica que o leito está ocupado pelo Paciente B (sendo que não há solicitação de alta ativa cadastrada para o Paciente B)
- **THEN** o sistema SHALL marcar o leito como em conflito (`conflito_reserva` = True) e exibir um destaque visual de conflito no card do leito

#### Scenario: Ausência de conflito em leito ocupado com alta ativa
- **WHEN** o usuário do painel visualiza um leito reservado para o Paciente A, o censo indica que está ocupado pelo Paciente B, e existe uma solicitação de alta ativa cadastrada para o Paciente B
- **THEN** o sistema SHALL considerar que o Paciente B está prestes a sair, portanto o leito não está em conflito (`conflito_reserva` = False)

### Requirement: Registro de Prontuário no Histórico de Gestão de Alta (Solicitação, Destino e Conclusão)
O sistema MUST associar o prontuário do paciente nos registros de histórico de ações quando uma nova solicitação de alta for criada, quando uma solicitação de alta for cancelada, quando a alta for concluída, quando o destino de alta for definido/alterado, e quando a disponibilidade do leito de destino for definida/cancelada.

#### Scenario: Gravação do prontuário na solicitação de alta
- **WHEN** o usuário cria uma solicitação de alta para um leito
- **THEN** o sistema identifica o prontuário do ocupante atual daquele leito e grava o registro no histórico de ações contendo o número do prontuário no campo `prontuario`

#### Scenario: Gravação do prontuário no cancelamento de alta
- **WHEN** o usuário cancela uma solicitação de alta
- **THEN** o sistema recupera o prontuário associado àquela alta e grava o registro no histórico de ações contendo o número do prontuário no campo `prontuario`

#### Scenario: Gravação do prontuário na conclusão de alta
- **WHEN** uma solicitação de alta é concluída (ex: via censo do AGHU)
- **THEN** o sistema grava o registro de conclusão de alta no histórico de ações contendo o número do prontuário no campo `prontuario`

#### Scenario: Gravação do prontuário na definição do destino
- **WHEN** o NIR define ou altera o leito de destino de uma alta
- **THEN** o sistema grava o registro no histórico de ações contendo o número do prontuário no campo `prontuario`

#### Scenario: Gravação do prontuário na sinalização de destino disponível
- **WHEN** o NIR sinaliza que o leito de destino está disponível ou indisponível
- **THEN** o sistema grava o registro no histórico de ações contendo o número do prontuário no campo `prontuario`

### Requirement: Prevenção de Cliques Duplos no Envio de Solicitação de Alta
A interface do frontend MUST desabilitar o botão de envio de solicitação de alta no formulário após o primeiro clique e exibir um indicador visual de salvamento ("loading") até que a requisição seja concluída.

#### Scenario: Submissão do modal de alta
- **WHEN** o usuário clica em solicitar alta no formulário
- **THEN** o botão de confirmação fica desabilitado e a requisição é processada uma única vez pelo servidor

