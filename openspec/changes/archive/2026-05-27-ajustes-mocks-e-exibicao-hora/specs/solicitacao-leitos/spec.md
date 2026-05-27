## MODIFIED Requirements

### Requirement: Integração com AGHU no Cadastro de Solicitação
Ao cadastrar uma nova solicitação de vaga/leito, o sistema MUST integrar com o banco de dados do AGHU para recuperar automaticamente os dados demográficos e cirúrgicos do paciente com base no prontuário informado, simplificando o processo de entrada para o usuário. Os campos que MUST ser importados são: Nome do Paciente, Data de Nascimento, Especialidade, Procedimento Principal, Data da Cirurgia e Hora de Início.

O sistema MUST mapear o turno automaticamente a partir da hora de início da cirurgia nos seguintes intervalos:
- **Manhã**: das 07:00 às 12:59
- **Tarde**: das 13:00 às 18:59
- **Noite**: das 19:00 às 06:59 (no dia seguinte)

A prioridade inicial do paciente na fila e a ordem de exibição correspondente MUST ser definida de forma crescente com base na data da cirurgia e, em caso de empate na data, pelo turno (Manhã < Tarde < Noite) e, em caso de empate no turno, de forma cronológica pelo horário de início da cirurgia (horários mais cedo recebem prioridades maiores: P1, P2, P3...).

No ambiente de desenvolvimento local (Mock), o sistema MUST retornar dados simulados de cirurgia. Para possibilitar testes locais de transição de datas e indicadores temporais:
1. O prontuário `6` MUST retornar dados de cirurgia agendada para o **dia seguinte** (amanhã).
2. O prontuário `7` MUST retornar dados de cirurgia agendada para **2 dias no futuro** (depois de amanhã).
3. Outros prontuários sem mapeamento estático mockado MUST retornar cirurgia para o dia corrente.

#### Scenario: Cadastro de solicitação com prontuário localizado com sucesso
- **WHEN** o usuário solicitante fornece um prontuário válido e com cirurgia programada ativa no AGHU e clica em cadastrar
- **THEN** o sistema executa a consulta no AGHU, recupera os dados, calcula a idade e o turno correspondente, define a prioridade de acordo com a ordem cronológica do início da cirurgia para aquele dia/turno, e cria a solicitação no status "Pendente"

#### Scenario: Cadastro de solicitação com prontuário inexistente ou cirurgia cancelada
- **WHEN** o usuário fornece um prontuário que não possui cirurgias programadas ou cujas cirurgias estão canceladas (`situacao = 'CANC'`) no AGHU
- **THEN** o sistema bloqueia o cadastro e retorna um erro informativo indicando que nenhuma cirurgia ativa foi encontrada para o prontuário fornecido

## ADDED Requirements

### Requirement: Exibição do Horário da Cirurgia na Fila
O sistema MUST exibir o horário de início da cirurgia na visualização dos cards de solicitação de leito, posicionado especificamente entre a data prevista da cirurgia e o turno do paciente.

#### Scenario: Visualização do horário da cirurgia na fila
- **WHEN** o usuário visualiza a fila de solicitações no frontend
- **THEN** o sistema exibe o horário de início da cirurgia de forma clara no card de detalhes de cada solicitação pendente ou reservada
