## ADDED Requirements

### Requirement: Registro de Observações de Passagem de Caso pelo Bloco Cirúrgico
O sistema MUST permitir que os setores solicitantes insiram observações clínicas críticas (Passagem de Caso) de transição no momento da finalização de uma cirurgia. Esse registro MUST ser opcional para garantir a agilidade do processo.

#### Scenario: Registro de passagem de caso ao finalizar cirurgia
- **WHEN** o usuário do Bloco Cirúrgico clica em "Finalizar Cirurgia" e escolhe a opção "Sim" para inserir informações clínicas
- **THEN** o sistema exibe um campo de texto livre e, após o preenchimento e clique em "Salvar", conclui a cirurgia associando o texto à solicitação do paciente no banco de dados

#### Scenario: Conclusão direta de cirurgia sem passagem de caso
- **WHEN** o usuário do Bloco Cirúrgico clica em "Finalizar Cirurgia" e escolhe a opção "Não" no questionário de inserção clínica
- **THEN** o sistema conclui a cirurgia imediatamente, sem abrir campos de texto ou exigir entrada de dados extras

### Requirement: Confirmação e Leitura de Passagem de Caso pela UTI
O sistema MUST exigir que a equipe da UTI leia e confirme ciência sobre as observações de passagem de caso inseridas pelo Bloco Cirúrgico no momento exato em que for autorizar o encaminhamento do paciente para o leito.

#### Scenario: Liberação de encaminhamento com passagem de caso exige confirmação
- **WHEN** o usuário da UTI clica em "Liberar Encaminhamento" para um leito reservado cuja cirurgia foi concluída com passagem de caso preenchida
- **THEN** o sistema abre obrigatoriamente um modal exibindo as observações clínicas informadas e as opções de confirmar ou cancelar
- **THEN** o status do encaminhamento só é alterado para "Encaminhamento Liberado" após o usuário clicar em "Ciente e Liberar"

#### Scenario: Cancelamento da liberação no modal de passagem
- **WHEN** o usuário visualiza o modal com a passagem de caso e clica em "Cancelar"
- **THEN** o modal é fechado, a ação de liberação é abortada e a solicitação permanece com o status original de "Cirurgia Finalizada" (não liberada)
