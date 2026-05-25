# internacao-leitos Specification

## Purpose
TBD - created by archiving change setup-openspec-docs. Update Purpose after archive.
## Requirements
### Requirement: Gestão de Leitos
O sistema MUST gerenciar o censo de internação, mostrando a disponibilidade e ocupação dos leitos. O sistema MUST considerar como leitos disponíveis para reserva aqueles com status "Livre", "Alta", "Limpeza" ou "Higienização".

#### Scenario: Ocupação de Leito
- **WHEN** um paciente é admitido na unidade e associado ao leito
- **THEN** o sistema atualiza o status do leito para ocupado e exibe no mapa de leitos

#### Scenario: Reserva de Leito em Higienização
- **WHEN** um usuário busca leitos disponíveis para reserva de uma solicitação
- **THEN** os leitos com status "Limpeza" e "Higienização" também são listados como opções válidas

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

### Requirement: Cancelamento de Alta pelo NIR
O sistema MUST permitir que os usuários do perfil NIR (ou Administradores) cancelem solicitações de alta ativa a partir da fila de solicitações de alta recebidas, fornecendo obrigatoriamente um motivo justificado da lista.

#### Scenario: Cancelamento com sucesso pelo NIR
- **WHEN** o usuário do NIR clica em "Cancelar Solicitação" e escolhe o motivo "Leito de Enfermaria Indisponível"
- **THEN** o sistema cancela a solicitação de alta no banco de dados e registra a ação sob o operador do NIR no histórico de ações

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

### Requirement: Remanejamento de Reserva no Card do Leito
O sistema MUST permitir que a equipe da UTI (ou Administradores) altere o leito físico reservado de um paciente diretamente a partir da visualização de cards de leitos.

#### Scenario: Visualização do botão de remanejamento no card
- **WHEN** o usuário visualiza o card de um leito que possui uma reserva ativa
- **THEN** o botão "Mudar Leito" SHALL estar disponível no card (caso o perfil seja UTI ou Administrador)

#### Scenario: Remanejamento de reserva executado com sucesso
- **WHEN** o usuário clica em "Mudar Leito", seleciona um novo leito disponível e confirma a ação
- **THEN** o sistema atualiza o leito de destino do paciente para o novo leito selecionado e limpa a reserva do leito original

