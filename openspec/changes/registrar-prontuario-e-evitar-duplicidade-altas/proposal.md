## Why

Identificamos duas falhas na gestão de solicitações de alta:
1. **Solicitações Duplicadas (Race Condition)**: Clicar rapidamente no botão de solicitar alta envia requisições em paralelo ao backend. Como as validações concorrentes rodam antes do `commit` no banco SQLite, ambas passam e geram registros duplicados para o mesmo leito.
2. **Histórico Sem Rastreabilidade de Prontuário**: Os registros do histórico de ações de "solicitação de alta" e "cancelamento de alta" não salvavam o prontuário do paciente associado. Isso impede a filtragem correta do histórico de ações daquele prontuário.

## What Changes

- **Prevenção de Cliques Duplos (Frontend)**: Desabilitar o botão de submissão do formulário de alta e exibir estado de carregamento durante o envio do pedido no frontend.
- **Rastreabilidade de Prontuário no Histórico (Backend)**: Capturar e gravar o número de prontuário correspondente no campo `prontuario` do histórico de ações (`historico_acoes`) nas ações de solicitar alta e cancelar alta.

## Capabilities

### New Capabilities

*(Nenhuma nova capacidade)*

### Modified Capabilities

- `internacao-leitos`: Melhorar a robustez do fluxo de solicitação e cancelamento de alta e garantir o registro do prontuário no histórico.

## Impact

- **Frontend**: Modificação no modal de solicitação de alta em `Solicitacoes.vue` para desabilitar o botão de salvar durante a requisição.
- **Backend**: Atualização nos controllers e routers de leitos e altas para incluir o prontuário no histórico de ações de solicitação e cancelamento de alta.
