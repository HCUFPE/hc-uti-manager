## ADDED Requirements

### Requirement: Lista de Múltipla Escolha para Necessidades Especiais de Alta
Ao registrar uma nova solicitação de alta para um leito de UTI, o sistema MUST disponibilizar um rol de seleção múltipla (checkboxes) para a especificação das necessidades especiais do paciente, em substituição ao campo de texto livre. As opções disponíveis no rol MUST ser:
- Isolamento de contato
- Isolamento respiratório
- Em uso de O2
- Necessidade de aspiração
- Necessidade de ventilador no leito
- Nenhum

O sistema MUST gerenciar a exclusão mútua das seleções da seguinte forma:
1. Se o usuário marcar "Nenhum", todas as outras opções selecionadas devem ser desmarcadas automaticamente.
2. Se o usuário marcar qualquer outra opção que não seja "Nenhum", a opção "Nenhum" deve ser desmarcada automaticamente.
3. Se o usuário não marcar nenhuma opção explicitamente, o sistema MUST assumir e persistir o valor "Nenhum".

O sistema MUST persistir a seleção concatenando as opções escolhidas em uma única string separada por vírgula no banco de dados local para manter a compatibilidade com a coluna de texto existente.

#### Scenario: Solicitação de alta com múltiplas necessidades específicas
- **WHEN** o usuário abre o modal de alta, seleciona as opções "Isolamento de contato" e "Em uso de O2" e confirma a solicitação
- **THEN** o sistema desmarca a opção "Nenhum" se estivesse selecionada e envia o payload com a string formatada "Isolamento de contato, Em uso de O2" para persistência no banco

#### Scenario: Solicitação de alta com a opção Nenhum ou sem seleção
- **WHEN** o usuário abre o modal de alta, seleciona a opção "Nenhum" (ou não seleciona nenhuma das opções) e confirma a solicitação
- **THEN** o sistema desmarca as outras opções se estivessem selecionadas e envia o payload com a string formatada "Nenhum" para persistência no banco
