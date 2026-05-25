## Why

Atualmente, ao registrar uma nova solicitação de vaga/leito, os setores solicitantes precisam preencher manualmente diversas informações clínicas e demográficas do paciente (nome, data de nascimento, especialidade, procedimento, data e hora da cirurgia). Este preenchimento manual é moroso e suscetível a erros de digitação. Ao integrar com o banco de dados do AGHU, o preenchimento dessas informações será automatizado informando apenas o prontuário do paciente, melhorando a produtividade das equipes e a consistência dos dados.

## What Changes

- **Preenchimento automático via AGHU**: Ao informar o prontuário do paciente na criação de uma solicitação de leito, o sistema buscará os dados diretamente do banco de dados do AGHU (PostgreSQL ou Oracle, conforme ambiente) usando a query fornecida.
- **Formulário de criação simplificado**: A interface de criação de solicitação de leito exigirá apenas o preenchimento do campo `prontuario` e, opcionalmente, `prioridade`. As demais informações (nome, data de nascimento, especialidade, procedimento principal, data e hora da cirurgia) serão importadas automaticamente do AGHU.
- **Validação de prontuário existente**: Caso o prontuário informado não seja encontrado em nenhuma cirurgia ativa/não cancelada do AGHU, o sistema retornará um erro amigável ao usuário.

## Capabilities

### New Capabilities
- Nenhuma.

### Modified Capabilities
- `solicitacao-leitos`: Permite auto-preencher os dados demográficos e cirúrgicos do paciente no registro de solicitações através de integração com o banco do AGHU.

## Impact

- **Backend**:
  - `src/controllers/solicitacao_leito_controller.py`: Modificar o método `criar_solicitacao` para consultar o banco do AGHU (via provider) antes de cadastrar a solicitação, auto-preenchendo os dados demográficos e cirúrgicos.
  - `src/providers/`: Criação ou ajuste de um provider (ex: `AghuProvider` ou similar) para executar a query no banco do AGHU utilizando a conexão assíncrona já configurada.
- **Frontend**:
  - `frontend/src/views/Solicitacoes.vue`: Ajustar o modal de nova solicitação para solicitar apenas `prontuario` e `prioridade`, preenchendo automaticamente as outras informações ou informando se o prontuário foi localizado com sucesso.
