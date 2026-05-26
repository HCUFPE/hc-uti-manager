## Why

Atualmente, ao solicitar alta de um paciente do leito de UTI, a equipe descreve as necessidades especiais em um campo de texto livre (textarea). Isso gera descrições inconsistentes e dificulta a triagem e o planejamento do transporte ou isolamento no setor de destino pelo NIR. Padronizar as necessidades especiais em uma lista de múltipla escolha com opções predefinidas elimina a ambiguidade e melhora a eficiência do fluxo de alta.

## What Changes

- **Interface de Solicitação de Alta**: Substituir o campo de texto livre (textarea) por uma lista de seleção múltipla (checkboxes) com as seguintes opções:
  - Nenhum
  - Isolamento de contato
  - Isolamento respiratório
  - Em uso de O2
  - Necessidade de aspiração
  - Necessidade de ventilador no leito
- **Regras de Seleção Dinâmica**:
  - Se "Nenhum" for selecionado, desmarcar automaticamente qualquer outra opção.
  - Se qualquer outra opção for selecionada, desmarcar automaticamente a opção "Nenhum".
  - Se nenhuma opção for selecionada explicitamente, tratar/salvar como "Nenhum".
- **Armazenamento e Exibição**: As necessidades selecionadas devem ser enviadas e salvas como uma string formatada (ex: delimitada por vírgulas) no banco de dados local para manter a compatibilidade com a coluna existente, permitindo visualização unificada no painel do NIR (Altas).

## Capabilities

### New Capabilities
- Nenhuma

### Modified Capabilities
- `internacao-leitos`: Atualização do requisito de solicitação de alta para exigir a seleção de necessidades a partir de uma lista padronizada de múltipla escolha em vez de entrada de texto livre.

## Impact

- **Frontend**:
  - `frontend/src/views/Home.vue`: Modificar o modal de solicitação de alta para renderizar o rol de checkboxes para as necessidades especiais, implementando a lógica de exclusão mútua da opção "Nenhum" e a concatenação dos valores antes de enviar à API.
- **Backend**:
  - `src/controllers/altas_controller.py` e rotas: Garantir que o valor recebido seja devidamente persistido no banco local.
