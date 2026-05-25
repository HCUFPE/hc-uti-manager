## ADDED Requirements

### Requirement: Exigência de Motivo no Cancelamento de Reserva na Visão de Leitos
O sistema MUST exigir que a equipe da UTI (ou Administradores) selecione obrigatoriamente um motivo pré-definido da lista de cancelamento de reserva (tipo 2) ao cancelar uma reserva de leito a partir da visão geral/card de leitos do painel principal, impedindo o cancelamento sem justificativa.

#### Scenario: Cancelamento de reserva com motivo informado
- **WHEN** o usuário clica em "Cancelar Reserva" no card do leito e escolhe um motivo da lista pré-definida
- **THEN** o sistema abre um modal de confirmação, exige a seleção do motivo, envia para o backend, desfaz a reserva localmente e registra o cancelamento com o respectivo motivo no histórico

### Requirement: Motivos de Cancelamento de Alta
O sistema MUST disponibilizar os seguintes motivos pré-definidos para cancelamento de alta na visão geral de leitos: "Piora Clínica" e "Leito de Enfermaria Indisponível".

#### Scenario: Cancelamento de alta
- **WHEN** o usuário clica em "Cancelar Alta" em um leito com alta solicitada e seleciona o motivo correspondente
- **THEN** o sistema atualiza o status do leito para ocupado e registra no histórico o cancelamento com o motivo escolhido
