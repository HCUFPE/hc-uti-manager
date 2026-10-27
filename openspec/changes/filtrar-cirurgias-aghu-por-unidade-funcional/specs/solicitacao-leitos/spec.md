# Spec Delta: solicitacao-leitos

## MODIFIED Requirements

### Requirement: Integração com AGHU no Cadastro de Solicitação
Ao cadastrar uma nova solicitação de vaga/leito, o sistema MUST integrar com o banco de dados do AGHU para recuperar automaticamente os dados demográficos e cirúrgicos do paciente com base no prontuário informado, simplificando o processo de entrada para o usuário. Os campos que MUST ser importados são: Nome do Paciente, Data de Nascimento, Especialidade, Procedimento Principal, Data da Cirurgia e Hora de Início.

**Filtro por Unidade Funcional Cirúrgica**: O sistema MUST filtrar as cirurgias recuperadas do AGHU considerando exclusivamente as unidades funcionais cirúrgicas e intervencionistas autorizadas, de acordo com o setor solicitante ou o tipo da solicitação:
- **Bloco Cirúrgico (BC)**: Unidade Funcional `28` (`BLOCO CIRURGICO`).
- **Centro Obstétrico (COB)**: Unidade Funcional `20` (`CENTRO OBSTETRICO`).
- **Hemodinâmica (HEM)**: Unidades Funcionais `47` (`HEMODINAMICA - PDT`) e `233` (`HEMODINAMICA (AMBULATORIO)`).
- **Consulta Geral (Admin / UTI)**: Conjunto restrito de unidades cirúrgicas válidas (`28`, `20`, `47`, `233`). Procedimentos realizados em outras unidades não autorizadas (como Endoscopia na Unidade `155`) MUST ser sumariamente desconsiderados na busca de cirurgias.

**Priorização de Situação de Agendamento**: A consulta SQL no AGHU MUST priorizar cirurgias que estejam com situação `AGND` (Agendada) em detrimento de procedimentos já finalizados (`RZDA`), ordenando a seguir pela proximidade temporal em relação à data corrente (`CURRENT_DATE`).

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

#### Scenario: Importação de cirurgia agendada no Bloco Cirúrgico ignorando procedimento de outra unidade
- **WHEN** um usuário do Bloco Cirúrgico (BC) consulta no AGHU um paciente que possui um procedimento diagnóstico realizado em outra unidade (ex: Endoscopia na Unidade 155) e uma cirurgia geral programada no Bloco Cirúrgico (Unidade 28)
- **THEN** o sistema SHALL ignorar o procedimento da Unidade 155 e preencher o formulário exclusivamente com os dados da cirurgia agendada no Bloco Cirúrgico (Unidade 28)

#### Scenario: Importação de cirurgia específica do Centro Obstétrico ou Hemodinâmica
- **WHEN** um usuário do Centro Obstétrico (COB) ou Hemodinâmica (HEM) consulta um prontuário no AGHU
- **THEN** o sistema SHALL filtrar e recuperar exclusivamente as cirurgias e procedimentos vinculados às suas respectivas unidades funcionais autorizadas (20 para COB, 47 ou 233 para HEM)
