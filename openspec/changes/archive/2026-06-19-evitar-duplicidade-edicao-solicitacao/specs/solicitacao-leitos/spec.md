## MODIFIED Requirements

### Requirement: Troca de Paciente na Edição de Solicitação
Quando o usuário edita uma solicitação e altera o prontuário do paciente (caracterizando uma troca de paciente), o sistema MUST tratar essa ação internamente verificando se o novo prontuário já possui uma solicitação ativa ("Pendente" ou "Reservado").

Se o novo prontuário já possuir uma solicitação ativa com status "Reservado", o sistema MUST rejeitar a alteração e retornar uma mensagem de erro específica informando que o paciente de destino já possui uma reserva ativa.

Se o novo prontuário já possuir uma solicitação ativa com status "Pendente":
1. O sistema MUST promover a solicitação "Pendente" existente do novo paciente para o status "Reservado", associando-a ao leito de destino da solicitação de origem.
2. O sistema MUST transferir a reserva física do leito no banco de dados para a solicitação existente do novo paciente.
3. O sistema MUST cancelar a solicitação de origem (do paciente antigo), alterando seu status para "Cancelada" e gravando o log correspondente no histórico.

Se o novo prontuário NÃO possuir nenhuma solicitação ativa:
1. O sistema MUST cancelar a solicitação de origem, definindo seu status como "Cancelada", atribuindo o motivo "Alteração de Prioridade pós Reserva de Leito", e registrando o cancelamento no histórico com data/hora e operador logado.
2. O sistema MUST criar uma nova solicitação com o novo prontuário informado, cujos dados demográficos e cirúrgicos serão recuperados do AGHU.
3. Se a solicitação original possuía leito reservado, a reserva do leito físico MUST permanecer ativa e ser transferida automaticamente para a nova solicitação criada, de modo que o leito físico passe a conter a reserva do novo paciente de forma ininterrupta.

#### Scenario: Edição com troca de paciente para novo paciente sem solicitação ativa
- **WHEN** o usuário edita uma solicitação reservada para o leito "UTI-01" alterando o prontuário do paciente para um prontuário sem solicitação ativa
- **THEN** o sistema cancela a solicitação original, cria uma nova solicitação com os dados do novo prontuário, transfere a reserva do leito "UTI-01" para a nova solicitação, e gera os registros no histórico

#### Scenario: Edição com troca de paciente para novo paciente que já possui solicitação pendente
- **WHEN** o usuário edita uma solicitação reservada para o leito "UTI-01" alterando o prontuário para o de um paciente que já possui uma solicitação "Pendente" ativa
- **THEN** o sistema cancela a solicitação original, promove a solicitação pendente preexistente do novo paciente para "Reservado" no leito "UTI-01", transfere a reserva física do leito, e gera os registros de histórico correspondentes

#### Scenario: Rejeição de troca de paciente para paciente já reservado
- **WHEN** o usuário tenta editar uma solicitação alterando o prontuário para o de um paciente que já possui status "Reservado" no sistema
- **THEN** o sistema bloqueia a alteração e retorna um erro informativo: "O paciente de destino já possui uma reserva de leito ativa."
