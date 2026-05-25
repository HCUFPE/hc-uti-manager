## ADDED Requirements

### Requirement: Cancelamento de Alta pelo NIR
O sistema MUST permitir que os usuários do perfil NIR (ou Administradores) cancelem solicitações de alta ativa a partir da fila de solicitações de alta recebidas, fornecendo obrigatoriamente um motivo justificado da lista.

#### Scenario: Cancelamento com sucesso pelo NIR
- **WHEN** o usuário do NIR clica em "Cancelar Solicitação" e escolhe o motivo "Leito de Enfermaria Indisponível"
- **THEN** o sistema cancela a solicitação de alta no banco de dados e registra a ação sob o operador do NIR no histórico de ações
