## ADDED Requirements

### Requirement: Registro de Observações de Passagem de Caso pelo Bloco Cirúrgico
O sistema MUST exigir que os setores solicitantes insiram observações clínicas de transição (Passagem de Caso) no momento da finalização de uma cirurgia. Esse registro MUST ser obrigatório para garantir a passagem de informações de segurança.

#### Scenario: Registro de passagem de caso ao finalizar cirurgia
- **WHEN** o usuário do Bloco Cirúrgico clica em "Finalizar Cirurgia"
- **THEN** o sistema exibe o modal de passagem de caso obrigatório e mantém o botão de finalização desabilitado até que observações clínicas sejam digitadas
- **THEN** após o preenchimento e clique em "Salvar e Finalizar", o sistema conclui a cirurgia associando o texto à solicitação do paciente no banco de dados

### Requirement: Confirmação e Leitura de Passagem de Caso pela UTI
O sistema MUST exigir que a equipe da UTI leia e confirme ciência sobre as observações de passagem de caso no momento exato em que for autorizar o encaminhamento do paciente para o leito.

#### Scenario: Liberação de encaminhamento com passagem de caso exige confirmação
- **WHEN** o usuário da UTI clica em "Liberar Encaminhamento" para um leito reservado cuja cirurgia foi concluída
- **THEN** o sistema abre obrigatoriamente um modal exibindo as observações clínicas informadas e as opções de confirmar ou cancelar
- **THEN** o status do encaminhamento só é alterado para "Encaminhamento Liberado" após o usuário clicar em "Ciente e Liberar"

#### Scenario: Cancelamento da liberação no modal de passagem
- **WHEN** o usuário visualiza o modal com a passagem de caso e clica em "Cancelar"
- **THEN** o modal é fechado, a ação de liberação é abortada e a solicitação permanece com o status original de "Cirurgia Finalizada" (não liberada)
