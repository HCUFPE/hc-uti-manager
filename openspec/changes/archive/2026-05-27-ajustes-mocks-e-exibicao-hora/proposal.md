## Why

Atualmente, o ambiente de desenvolvimento local gera dados mockados de cirurgia apenas para o dia de "hoje", impossibilitando o teste de fluxos operacionais e cálculo de indicadores envolvendo cirurgias futuras (amanhã e depois). Além disso, a tela de listagem de solicitações não exibe a hora exata de início da cirurgia, omitindo uma informação relevante para a equipe assistencial.

## What Changes

- **Novos Pacientes Mockados (Amanhã e +2 dias):**
  - Prontuário `6`: Cirurgia agendada para o dia seguinte (amanhã).
  - Prontuário `7`: Cirurgia agendada para 2 dias no futuro (depois de amanhã).
- **Exibição da Hora da Cirurgia no Frontend:**
  - Adição da coluna/campo "Horário" (ou "Hora da Cirurgia") na grade de detalhes de solicitações na tela de gerenciamento de solicitações de leito (`Solicitacoes.vue`), entre a data prevista e o turno mapeado.

## Capabilities

### Modified Capabilities
- `solicitacao-leitos`: A listagem de solicitações passa a exibir também o horário de início da cirurgia.

## Impact

- **Backend:** `src/controllers/solicitacao_leito_controller.py` (atualização do mock generator).
- **Frontend:** `frontend/src/views/Solicitacoes.vue` (modificação do layout dos cards de solicitações para inclusão da hora).
