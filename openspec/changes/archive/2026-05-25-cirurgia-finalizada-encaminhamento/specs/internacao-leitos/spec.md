## ADDED Requirements

### Requirement: Atualização Visual e Liberação de Encaminhamento pela UTI
O sistema MUST gerenciar o fluxo visual e a autorização de transferência de pacientes com leito de UTI reservado pós-cirúrgico.

#### Scenario: Reserva fica amarela após cirurgia finalizada
- **WHEN** uma reserva vinculada a um leito é sinalizada como "Cirurgia Finalizada"
- **THEN** o card do leito no painel da UTI SHALL apresentar destaque na cor amarela indicando a prontidão do paciente
- **THEN** o botão "Liberar Encaminhamento" SHALL ficar disponível para a equipe da UTI nesse leito

#### Scenario: Liberação de encaminhamento pela UTI e reserva verde
- **WHEN** o usuário da UTI clica em "Liberar Encaminhamento" no card do leito
- **THEN** o sistema altera o status do encaminhamento para "Encaminhamento Liberado"
- **THEN** o card do leito no painel da UTI SHALL apresentar destaque na cor verde indicando que a transferência está autorizada

#### Scenario: UTI cancela liberação de encaminhamento
- **WHEN** o usuário da UTI clica em "Cancelar Liberação" no card do leito com status "Encaminhamento Liberado"
- **THEN** o sistema altera o status do encaminhamento para "Cirurgia Finalizada" (não liberado)
- **THEN** o card do leito no painel da UTI SHALL voltar a apresentar destaque na cor amarela
