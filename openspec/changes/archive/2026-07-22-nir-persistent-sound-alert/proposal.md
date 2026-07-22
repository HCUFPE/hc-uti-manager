## Why

Atualmente, o alerta sonoro periódico para o NIR é disparado apenas quando o usuário está na tela inicial (`Home.vue`). Se o usuário navegar para qualquer outra tela (como a lista de alertas, configurações ou painéis), o som não é reproduzido, fazendo com que alertas críticos passem despercebidos. É necessário que o som toque independentemente da tela ativa no sistema até que o usuário tome ciência dos alertas pendentes.

## What Changes

- Migrar a lógica de verificação e reprodução do alerta sonoro da tela inicial (`Home.vue`) para o layout global (`DefaultLayout.vue`), garantindo que o monitoramento ocorra em qualquer tela que use o layout padrão.
- Manter o comportamento de persistência do som: enquanto houver pelo menos um alerta não lido no contador de notificações (`unreadAlertsCount > 0`), o som deve ser tocado a cada 30 segundos (ou imediatamente ao receber uma nova notificação em background).
- Remover a dependência de estar exclusivamente na `Home.vue` para a reprodução de áudio de alertas do NIR e da UTI.
- Disponibilizar um controle global de áudio (silenciar/ativar) no layout (por exemplo, integrado ao header ou no menu lateral) de forma que o usuário possa mutar/desmutar o som de qualquer tela, sincronizado com o estado local (`localStorage`).

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `alertas`: O alerta sonoro para o NIR e UTI passa a rodar em escopo global (em todo o DefaultLayout) em vez de ficar restrito apenas à tela inicial (`Home.vue`).

## Impact

- `frontend/src/views/Home.vue`: Remoção da lógica de áudio repetitiva e do timer local para alertas sonoros.
- `frontend/src/layouts/DefaultLayout.vue`: Integração da lógica global do timer de som, reprodução de áudio Web Audio API, e controle de mudo (`localStorage` compartilhado).
