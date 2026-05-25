## ADDED Requirements

### Requirement: Alerta de Cancelamento de Alta pelo NIR
O sistema MUST gerar uma notificação/alerta direcionado para a equipe da UTI toda vez que o perfil NIR (ou Administradores sob esse contexto) cancelar uma solicitação de alta de paciente.

#### Scenario: Geração de alerta para a UTI
- **WHEN** a rotina de sincronização de alertas detecta no histórico de ações que uma alta foi cancelada pelo NIR
- **THEN** o sistema SHALL criar um novo alerta com o título "Cancelamento de Alta pelo NIR", com o perfil alvo definido como nulo (visível para UTI) e contendo o motivo correspondente
