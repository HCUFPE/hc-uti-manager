## MODIFIED Requirements

### Requirement: Criação de Solicitação de Leito
O sistema MUST permitir que usuários dos setores solicitantes (Bloco Cirúrgico, Centro Obstétrico e Hemodinâmica) criem requisições de leito de UTI. O sistema MUST rejeitar e impedir a criação de uma nova solicitação se já houver uma solicitação ativa ('Pendente' ou 'Reservado') para o mesmo prontuário de paciente.

#### Scenario: Solicitação de vaga bem sucedida
- **WHEN** o usuário de um setor solicitante preenche o prontuário, data da cirurgia e especialidade
- **THEN** o sistema salva a requisição com o status inicial adequado
- **THEN** a solicitação passa a aparecer na fila de avaliação da UTI

#### Scenario: Rejeição de solicitação duplicada para mesmo prontuário ativo
- **WHEN** o usuário tenta cadastrar uma solicitação para um prontuário que já tem status "Pendente" ou "Reservado" no sistema
- **THEN** o sistema bloqueia o cadastro e retorna a mensagem de erro específica: "Solicitação para este prontuário já inserida."
