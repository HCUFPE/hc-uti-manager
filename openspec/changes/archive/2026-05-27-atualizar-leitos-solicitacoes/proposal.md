## Why

Atualmente, as telas principais de Leitos (`Home.vue`) e Solicitações (`Solicitacoes.vue`) não possuem um mecanismo de atualização automática (polling). Os dados só são atualizados quando o usuário entra na tela ou quando realiza alguma ação direta que force o recarregamento. 

Com a adição do polling automático de 2 minutos, garantimos que os profissionais (NIR, UTI, COB) vejam as informações mais recentes vindas do censo do AGHU e as novas solicitações inseridas por outros solicitantes sem a necessidade de recarregar a página manualmente.

## What Changes

- Adicionar polling automático temporizado de 2 minutos (120.000 ms) na tela de Painel de Leitos (`Home.vue`).
- Adicionar polling automático temporizado de 2 minutos (120.000 ms) na tela de Solicitações (`Solicitacoes.vue`).
- Garantir que os intervalos (timers) sejam devidamente limpos quando os componentes correspondentes forem desmontados para evitar vazamentos de memória (memory leaks).

## Capabilities

### New Capabilities

<!-- Nenhuma nova capacidade é necessária -->

### Modified Capabilities

- `internacao-leitos`: O painel de visualização de leitos deve atualizar as informações de censo do AGHU automaticamente a cada 2 minutos.
- `solicitacao-leitos`: A tela de solicitações deve atualizar a lista de solicitações pendentes e reservadas automaticamente a cada 2 minutos.

## Impact

- Frontend: Arquivos `frontend/src/views/Home.vue` e `frontend/src/views/Solicitacoes.vue`.
