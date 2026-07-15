## MODIFIED Requirements

### Requirement: Integração com AGHU no Cadastro de Solicitação
Ao cadastrar uma nova solicitação de vaga/leito, o sistema MUST integrar com o banco de dados do AGHU para recuperar automaticamente os dados demográficos e cirúrgicos do paciente com base no prontuário informado, simplificando o processo de entrada para o usuário. Os campos que MUST ser importados são: Nome do Paciente, Data de Nascimento, Especialidade, Procedimento Principal, Data da Cirurgia e Hora de Início.

O sistema MUST mapear o turno automaticamente a partir da hora de início da cirurgia nos seguintes intervalos:
- **Manhã**: das 07:00 às 12:59
- **Tarde**: das 13:00 às 18:59
- **Noite**: das 19:00 às 06:59 (no dia seguinte)

A prioridade inicial do paciente na fila e a ordem de exibição correspondente MUST ser definida de forma crescente com base na data da cirurgia. Em caso de empate na data, a ordem cronológica pelo horário de início da cirurgia (horários mais cedo recebem prioridades maiores: P1, P2, P3...) e a data/hora de criação do registro no banco local (registros mais antigos criados primeiro recebem prioridade maior) MUST determinar a sequência inicial, exceto se o usuário informar especificamente uma prioridade de cadastro (ex: P3) no formulário, a qual MUST ser respeitada de forma prioritária e gravada imediatamente no banco de dados, aplicando as regras de reordenamento e deslocamento aos outros registros na fila do mesmo dia.

No entanto, caso haja uma alteração de prioridade manual pelo usuário (ex: alterando de P2 para P1), o sistema MUST respeitar e manter a prioridade definida manualmente para a solicitação em foco, deslocando as demais solicitações do mesmo bucket (mesma data da cirurgia) de acordo com sua ordem cronológica relativa para garantir uma fila contínua sem duplicatas ou lacunas.

**Restrição de Data Retroativa**: O sistema MUST rejeitar o cadastro ou edição de solicitação caso a data da cirurgia seja anterior à data da criação/edição (comparação realizada apenas em dia, mês e ano). Em caso de violação, o sistema MUST bloquear o cadastro e retornar a mensagem de erro específica: `"Paciente não possui cirurgia agendada no AGHU"`.

No ambiente de desenvolvimento local (Mock), o sistema MUST retornar dados simulados de cirurgia. Para possibilitar testes locais de transição de datas e indicadores temporais:
1. O prontuário `6` MUST retornar dados de cirurgia agendada para o **dia seguinte** (amanhã).
2. O prontuário `7` MUST retornar dados de cirurgia agendada para **2 dias no futuro** (depois de amanhã).
3. Outros prontuários sem mapeamento estático mockado MUST retornar cirurgia para o dia corrente.

#### Scenario: Cadastro de solicitação com prontuário localizado com sucesso
- **WHEN** o usuário solicitante fornece um prontuário válido e com cirurgia programada ativa no AGHU (com data igual ou posterior a hoje) e clica em cadastrar
- **THEN** o sistema executa a consulta no AGHU, recupera os dados, calcula a idade e o turno correspondente, define a prioridade de acordo com a ordem cronológica do início da cirurgia e de inclusão para aquele dia, e cria a solicitação no status "Pendente"

#### Scenario: Cadastro de solicitação com prontuário inexistente ou cirurgia cancelada
- **WHEN** o usuário fornece um prontuário que não possui cirurgias programadas ou cujas cirurgias estão canceladas (`situacao = 'CANC'`) no AGHU
- **THEN** o sistema blocks o cadastro e retorna um erro informativo indicando que nenhuma cirurgia ativa foi encontrada para o prontuário fornecido

#### Scenario: Rejeição de cadastro de cirurgia no passado
- **WHEN** o usuário fornece um prontuário com cirurgia programada em data anterior à data de hoje (dia, mês e ano)
- **THEN** o sistema bloqueia o cadastro e retorna a mensagem de erro específica: "Paciente não possui cirurgia agendada no AGHU"

#### Scenario: Ajuste manual de prioridade na fila respeitado
- **WHEN** o usuário edita a prioridade de uma solicitação com id "5" de "P2" para "P1" em um bucket que contém as solicitações "2" (P1) e "5" (P2)
- **THEN** o sistema atualiza a solicitação "5" para "P1" e desloca a solicitação "2" para "P2", mantendo a integridade da fila sem duplicatas ou lacunas para aquele dia

#### Scenario: Cadastro de solicitação com prioridade informada manualmente
- **WHEN** o usuário solicitante fornece um prontuário válido e preenche a prioridade manual como "P3"
- **THEN** o sistema cria a solicitação com prioridade "P3" e reordena os demais pacientes do mesmo dia de forma correspondente

### Requirement: Troca de Paciente na Edição de Solicitação
Quando o usuário edita uma solicitação e altera o prontuário do paciente (caracterizando uma troca de paciente), o sistema MUST tratar essa ação internamente verificando se o novo prontuário já possui uma solicitação ativa ("Pendente" ou "Reservado").

Se o novo prontuário já possuir uma solicitação ativa com status "Reservado", o sistema MUST rejeitar a alteração e retornar uma mensagem de erro específica informando que o paciente de destino já possui uma reserva ativa.

Se o novo prontuário já possuir uma solicitação ativa com status "Pendente":
1. O sistema MUST promover a solicitação "Pendente" existente do novo paciente para o status "Reservado", associando-a ao leito de destino da solicitação de origem.
2. O sistema MUST transferir a reserva física do leito no banco de dados para a solicitação existente do novo paciente.
3. O sistema MUST cancelar a solicitação de origem (do paciente antigo), alterando seu status para "Cancelada" e gravando o log correspondente no histórico.

Se o novo prontuário NÃO possuir nenhuma solicitação ativa:
1. O sistema MUST cancelar a solicitação de origem, definindo seu status como "Cancelada".
2. **Definição de Motivo Dinâmico**: Ao cancelar a solicitação de origem, o motivo de cancelamento atribuído no histórico MUST depender do status em que ela estava antes da edição:
   - Se estava `Pendente`: o motivo será `"Alteração de Prioridade pós Solicitação"`.
   - Se estava `Reservado`: o motivo será `"Alteração de Prioridade pós Reserva de Leito"`.
3. **Detalhamento de Substituição**: O histórico da solicitação antiga excluída e da nova solicitação criada MUST detalhar de forma clara a substituição dos pacientes no campo detalhes, utilizando o formato `"(Prontuário X foi substituído pelo Prontuário Y)"`.
4. O sistema MUST criar uma nova solicitação com o novo prontuário informado, cujos dados demográficos e cirúrgicos serão recuperados do AGHU.
5. Se a solicitação original possuía leito reservado, a reserva do leito físico MUST permanecer ativa e ser transferida automaticamente para a nova solicitação criada, de modo que o leito físico passe a conter a reserva do novo paciente de forma ininterrupta.
6. **Operador da Reserva Automática**: A nova reserva do leito físico criada automaticamente para o novo paciente durante a troca MUST ser registrada no histórico sob o operador `"Sistema"`.

#### Scenario: Edição com troca de paciente para novo paciente sem solicitação ativa
- **WHEN** o usuário edita uma solicitação reservada para o leito "UTI-01" alterando o prontuário do paciente X para o paciente Y sem solicitação ativa
- **THEN** o sistema cancela a solicitação original atribuindo o motivo "Alteração de Prioridade pós Reserva de Leito", detalha no log que o prontuário X foi substituído pelo prontuário Y, cria uma nova solicitação com os dados do novo prontuário Y, transfere a reserva do leito "UTI-01" sob o operador "Sistema", e gera os registros no histórico

#### Scenario: Edição com troca de paciente para novo paciente que já possui solicitação pendente
- **WHEN** o usuário edita uma solicitação reservada para o leito "UTI-01" alterando o prontuário para o de um paciente que já possui uma solicitação "Pendente" ativa
- **THEN** o sistema cancela a solicitação original, promove a solicitação pendente preexistente do novo paciente para "Reservado" no leito "UTI-01", transfere a reserva física do leito, e gera os registros de histórico correspondentes

#### Scenario: Rejeição de troca de paciente para paciente já reservado
- **WHEN** o usuário tenta editar uma solicitação alterando o prontuário para o de um paciente que já possui status "Reservado" no sistema
- **THEN** o sistema bloqueia a alteração e retorna um erro informativo: "O paciente de destino já possui uma reserva de leito ativa."

### Requirement: Registro Consistente de Auditoria no Histórico
O sistema MUST registrar um histórico de auditoria para toda ação que altere o estado de solicitações de leito ou reservas de leito físico. Cada entrada de histórico MUST conter:
1. Data e hora exata da ação.
2. O identificador/nome do operador (usuário logado) que executou a ação.
3. Descrição textual detalhada da ação executada (incluindo prontuários e leitos envolvidos).

Adicionalmente, o sistema MUST registrar no histórico de ações:
- Um evento com tipo `"conclusao"` quando um paciente ocupa fisicamente o leito reservado (sincronizado através do censo).
- Um evento com tipo `"conclusao_alta"` quando um paciente com alta ativa deixa fisicamente o leito de UTI.

**Mapeamento de Filtros no Backend**: Ao consultar ou filtrar o histórico pelo parâmetro `tipo`, o sistema MUST mapear as buscas de forma a abranger os tipos reais gravados no banco:
- Se `tipo` for `"solicitacao"`, a busca MUST incluir os tipos: `["solicitacao", "nova_solicitacao", "conclusao"]`.
- Se `tipo` for `"cancelamento"`, a busca MUST incluir os tipos: `["cancelamento", "exclusao_solicitacao", "cancelamento_reserva"]`.

#### Scenario: Gravação de log de auditoria ao realizar ações
- **WHEN** um usuário logado realiza qualquer operação de mudança de estado (criação, edição, reserva, remanejamento, liberação de encaminhamento ou cancelamento)
- **THEN** o sistema grava um registro de histórico contendo a data/hora atual, o nome do usuário operador e os detalhes descritivos da ação

#### Scenario: Filtro por solicitação retorna registros corretos
- **WHEN** o usuário seleciona o filtro "Solicitação" na tela de histórico
- **THEN** o backend executa a busca mapeando para os registros de tipo "solicitacao", "nova_solicitacao" e "conclusao" e retorna o resultado para o frontend

#### Scenario: Filtro por cancelamento retorna registros corretos
- **WHEN** o usuário seleciona o filtro "Cancelamento" na tela de histórico
- **THEN** o backend executa a busca mapeando para os registros de tipo "cancelamento", "exclusao_solicitacao" e "cancelamento_reserva" e retorna o resultado para o frontend
