## MODIFIED Requirements

### Requirement: Atualização Visual e Liberação de Encaminhamento pela UTI
O sistema MUST gerenciar o fluxo visual e a autorização de transferência de pacientes com leito de UTI reservado pós-cirúrgico.

#### Scenario: Reserva fica amarela após cirurgia finalizada
- **WHEN** uma reserva vinculada a um leito é sinalizada como "Cirurgia Finalizada"
- **THEN** o card do leito no painel da UTI SHALL apresentar destaque na cor amarela indicando a prontidão do paciente
- **THEN** o botão "Liberar Encaminhamento" SHALL ficar disponível para a equipe da UTI nesse leito

#### Scenario: Animação piscante no card do leito para a UTI
- **WHEN** um usuário logado com o perfil UTI (ou Administrador) visualiza o painel de leitos e o leito possui uma reserva ativa com status "Cirurgia Finalizada"
- **THEN** o card do leito correspondente SHALL apresentar uma animação piscante (pulsando a opacidade/borda de cor amarela continuamente)
- **THEN** se o perfil logado não for UTI (ou Administrador), a animação piscante SHALL estar desabilitada e o leito se manterá com o destaque amarelo estático

#### Scenario: Alerta sonoro de cirurgia finalizada para a UTI
- **WHEN** o Painel de Leitos é atualizado e detecta que uma cirurgia foi recém-finalizada para um leito reservado e o usuário logado pertence ao perfil UTI (ou Administrador)
- **THEN** o sistema SHALL reproduzir um sinal sonoro curto de notificação se o som estiver ativado nas configurações do painel
- **THEN** se o perfil logado não for UTI (ou Administrador), nenhum som SHALL ser executado

#### Scenario: Liberação de encaminhamento pela UTI e reserva verde
- **WHEN** o usuário da UTI clica em "Liberar Encaminhamento" no card do leito
- **THEN** o sistema altera o status do encaminhamento para "Encaminhamento Liberado"
- **THEN** o card do leito no painel da UTI SHALL apresentar destaque na cor verde indicando que a transferência está autorizada
- **THEN** a animação piscante e a reprodução de alertas sonoros para esse leito SHALL ser encerrada

#### Scenario: UTI cancela liberação de encaminhamento
- **WHEN** o usuário da UTI clica em "Cancelar Liberação" no card do leito com status "Encaminhamento Liberado"
- **THEN** o sistema altera o status do encaminhamento para "Cirurgia Finalizada" (não liberado)
- **THEN** o card do leito no painel da UTI SHALL voltar a apresentar destaque na cor amarela piscante (para perfil UTI)

#### Scenario: Controle de som no painel de leitos
- **WHEN** o usuário do painel com perfil UTI (ou Administrador) clica no controle de ativar/desativar som
- **THEN** o sistema SHALL alternar o estado do áudio de notificações e persistir essa escolha no local storage do navegador
