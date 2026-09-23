## ADDED Requirements

### Requirement: Tabela Unificada de Auditoria Imutável
O sistema MUST manter um registro de auditoria imutável na tabela `audit_logs` para todas as ações relevantes categorizadas em `SEGURANCA`, `NEGOCIO_CLINICO` ou `CONFIGURACAO`. O registro MUST armazenar timestamp, acao, usuario_id, detalhes e os objetos JSON `estado_anterior` e `estado_novo`.

#### Scenario: Registro de auditoria em alta médica
- **WHEN** um usuário realiza a alta de um paciente ou leito
- **THEN** o sistema grava um novo registro em `audit_logs` com categoria `NEGOCIO_CLINICO`, capturando o estado do leito antes e depois da operação.

#### Scenario: Registro de auditoria de autenticação e gestão de usuários
- **WHEN** ocorre um evento de autenticação, atribuição ou exclusão de perfil de usuário em AdminConfig.vue
- **THEN** o sistema grava um registro de auditoria com categoria `SEGURANCA` capturando o estado do usuário antes e depois da operação.

#### Scenario: Registro automático de operações médicas e clínicas
- **WHEN** qualquer operador realiza uma ação clínica (reserva, solicitação de alta, cancelamento, swap ou passagem de caso)
- **THEN** o sistema intercepta via `HistoricoProvider.registrar()` e salva uma entrada em `audit_logs` sob a categoria `NEGOCIO_CLINICO`.

## ADDED Requirements

### Requirement: Central de Configurações e Validação de Segredos no Boot
O sistema MUST validar todas as variáveis de ambiente necessárias no arquivo `src/config.py` durante o boot do servidor. Se o ambiente estiver configurado como `production`, o sistema MUST rejeitar chaves secretas fracas ou variáveis obrigatórias ausentes e encerrar a inicialização com erro explicativo.

#### Scenario: Boot em produção com chave fraca
- **WHEN** a aplicação é iniciada em ambiente `production` com `SECRET_KEY` igual a `secret` ou `123456`
- **THEN** a aplicação encerra a execução impedindo a sobem do servidor e emitindo log de erro crítico de segurança.

#### Scenario: Boot em ambiente válido
- **WHEN** a aplicação é iniciada com todas as variáveis obrigatórias e segredos seguros
- **THEN** a validação de configurações passa com sucesso e o servidor inicializa.
