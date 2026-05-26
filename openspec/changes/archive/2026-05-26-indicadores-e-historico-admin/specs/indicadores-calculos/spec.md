## ADDED Requirements

### Requirement: Filtro de Período nos Indicadores
O sistema MUST aceitar parâmetros opcionais de data de início (`data_inicio` ou `start_date`) e data de fim (`data_fim` ou `end_date`) nas requisições do endpoint de indicadores para filtrar os eventos e dados a serem calculados no período fornecido.

#### Scenario: Filtragem por período bem sucedida
- **WHEN** o usuário passa datas de início e fim na URL do endpoint de indicadores
- **THEN** o sistema filtra as solicitações e ações ocorridas entre essas datas e calcula os indicadores correspondentes

### Requirement: Cálculo de Novas Internações Semanais na UTI
O sistema MUST calcular o número médio semanal de novas internações na UTI no período filtrado. Esse cálculo deve ser subdividido em: geral, por demandante (BC, HEM, COB e CLI) e por especialidade. CLI representa pacientes clínicos, que são identificados quando a solicitação não possui setor cirúrgico definido.

#### Scenario: Cálculo de internações semanais
- **WHEN** o sistema processa as solicitações com leito ocupado (admitidos) e o histórico de ações no período filtrado
- **THEN** o sistema calcula a média de novas internações agrupadas por semana, geral, por demandante e por especialidade

### Requirement: Cálculo do Tempo Médio de Ocupação de Leitos de UTI
O sistema MUST calcular o tempo médio de ocupação de um leito de UTI no período filtrado. Esse cálculo deve ser subdividido em: geral, por demandante (BC, HEM, COB e CLI) e por especialidade. O tempo de ocupação é computado a partir do momento da admissão (conclusão) até a efetiva saída/liberação de alta.

#### Scenario: Cálculo do tempo de ocupação
- **WHEN** o sistema calcula o tempo decorrido entre a entrada na UTI (evento `conclusao`) e a saída (evento `conclusao_alta` ou liberação de leito) para cada internação concluída no período filtrado
- **THEN** o sistema retorna a média geral, por demandante e por especialidade em horas ou dias

### Requirement: Cálculo de Taxas de Atendimento e Cancelamento
O sistema MUST calcular a taxa de atendimento (solicitações atendidas/concluídas divididas pelo total de solicitações) e a taxa de cancelamento (solicitações canceladas divididas pelo total de solicitações) ocorridas no período.

#### Scenario: Cálculo de taxas de atendimento e cancelamento
- **WHEN** o sistema totaliza as solicitações criadas ou modificadas no período filtrado
- **THEN** o sistema calcula a proporção de solicitações com status Concluído (atendidas) e Cancelado (canceladas) em relação ao total de solicitações criadas

### Requirement: Cálculo do Tempo Médio de Solicitação até Ocupação
O sistema MUST calcular o tempo médio decorrido desde a criação da solicitação de vaga de UTI até o momento em que o paciente efetivamente ocupou o leito (evento `conclusao`), para as solicitações atendidas no período.

#### Scenario: Cálculo do tempo médio de solicitação até ocupação
- **WHEN** o sistema calcula a diferença entre o carimbo de data/hora de criação da solicitação e o evento `conclusao` do histórico
- **THEN** o sistema retorna a média desse tempo em horas para o período selecionado

### Requirement: Cálculo do Horário Médio de Reserva por Turno
O sistema MUST calcular o horário médio em que a UTI faz a reserva de leitos para os pacientes do turno, dividido entre os turnos Manhã e Tarde, com base nos registros do histórico de ações de reserva.

#### Scenario: Cálculo do horário médio de reserva
- **WHEN** o sistema extrai a hora do dia dos eventos de reserva (`reserva`) no histórico associados a cirurgias do turno Manhã e Tarde
- **THEN** o sistema retorna o horário médio formatado (HH:MM) para cada turno

### Requirement: Cálculo do Tempo Médio de Recepção do Paciente pós Fim Cirúrgico
O sistema MUST calcular o tempo médio entre o horário em que o paciente do Bloco Cirúrgico (BC) estava pronto para envio à UTI (evento de fim cirúrgico / pronto para envio) e o horário de admissão/entrada física na UTI (evento `conclusao`), para solicitações concluídas no período.

#### Scenario: Cálculo do tempo de recepção pós cirúrgico
- **WHEN** o sistema recupera a diferença de tempo entre o evento de sinalização de cirurgia finalizada e a ocupação do leito na UTI
- **THEN** o sistema retorna o tempo médio de recepção pós-cirúrgica em minutos

### Requirement: Cálculo do Tempo Médio de Acomodação de Alta
O sistema MUST calcular o tempo médio decorrido desde que a UTI solicitou a alta do paciente (evento de criação da solicitação de alta) até o momento em que o NIR informou o leito de acomodação pós-UTI (destino informado).

#### Scenario: Cálculo do tempo de acomodação de alta
- **WHEN** o sistema calcula o tempo entre a solicitação de alta e a definição de destino pós-UTI pelo NIR
- **THEN** o sistema retorna a média em horas para o período selecionado

### Requirement: Cálculo do Tempo Médio de Liberação do Leito de Acomodação pós-UTI
O sistema MUST calcular o tempo médio decorrido desde que o NIR informou o leito de acomodação pós-UTI até o momento em que o NIR liberou efetivamente o leito (conclusão/liberação de alta).

#### Scenario: Cálculo do tempo de liberação pós-UTI
- **WHEN** o sistema calcula o tempo entre a definição do destino pós-UTI e a liberação efetiva do leito pós-UTI pelo NIR
- **THEN** o sistema retorna o tempo médio em horas

### Requirement: Cálculo dos Indicadores de Volume e Percentuais Relativos
O sistema MUST calcular métricas volumétricas absolutas e percentuais relativos: quantidade total de solicitações feitas, quantidade de solicitações reservadas, quantidade de solicitações reservadas e concluídas, quantidade de cancelamento de solicitações, quantidade de cancelamento de reservas, quantidade de altas solicitadas e percentuais em relação à quantidade de solicitações feitas e reservas concluídas.

#### Scenario: Cálculo de volumes e percentuais
- **WHEN** o sistema consolida todas as contagens de estados e eventos no período filtrado
- **THEN** o sistema retorna os totais absolutos e as relações percentuais especificadas
