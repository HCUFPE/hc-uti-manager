## ADDED Requirements

### Requirement: Registro de Observações de Passagem de Caso Estruturada
O sistema MUST exigir que os setores solicitantes insiram observações clínicas estruturadas (Passagem de Caso) de transição no momento da finalização de uma cirurgia. O botão de salvamento no frontend e a requisição no backend MUST ser validados conforme as regras de obrigatoriedade.

#### Scenario: Preenchimento correto do formulário de passagem de caso
- **WHEN** o usuário do Bloco Cirúrgico preenche o procedimento realizado, seleciona pelo menos uma via aérea (ex: TOT) e pelo menos um suporte ventilatório (ex: Ventilação mecânica), marca as opções de hemodinâmica, drogas vasoativas, reposição, transfusão, sangramento, diurese, acessos venosos, ferida operatória e informa o profissional responsável
- **THEN** o sistema habilita o botão "Salvar e Finalizar" e a requisição HTTP `POST /api/solicitacoes/{id}/cirurgia-finalizada` é aceita com sucesso

#### Scenario: Bloqueio do botão por falta de dados obrigatórios
- **WHEN** o usuário deixa campos obrigatórios em branco (ex: sem selecionar suporte respiratório ou sem informar o profissional responsável)
- **THEN** o sistema desabilita o botão de confirmação e impede a submissão do formulário no frontend

#### Scenario: Cirurgia não realizada desativa a obrigatoriedade do procedimento
- **WHEN** o usuário marca a opção "Cirurgia não realizada" no formulário
- **THEN** o sistema desativa a obrigatoriedade de preenchimento do campo "Procedimento realizado", mas mantém todos os outros checklists clínicos obrigatórios

### Requirement: Edição da Passagem de Caso pelo Bloco Cirúrgico
O solicitante MUST poder editar os dados preenchidos da passagem de caso, desde que a UTI ainda não tenha completado a confirmação da liberação do encaminhamento.

#### Scenario: Edição permitida antes da liberação
- **WHEN** a UTI ainda não validou e o Bloco clica em "Editar Passagem"
- **THEN** o sistema abre o formulário pré-preenchido e permite submeter as alterações através do método `PUT`

#### Scenario: Edição negada após a liberação da UTI
- **WHEN** a UTI já confirmou a liberação do leito e o Bloco tenta alterar os dados
- **THEN** o backend rejeita a alteração retornando erro `403 Forbidden`

### Requirement: Visualização Posterior pela UTI
A equipe da UTI MUST poder visualizar a passagem de caso estruturada a qualquer momento no card do leito correspondente.

#### Scenario: Consulta rápida à passagem de caso
- **WHEN** o usuário clica no botão "Ver Passagem de Caso" no card do leito (mesmo já liberado)
- **THEN** o sistema exibe o formulário com os dados gravados em modo somente leitura
