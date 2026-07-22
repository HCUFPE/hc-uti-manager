## 1. Pinia Store Updates

- [x] 1.1 Atualizar `frontend/src/stores/ui.ts` para gerenciar o estado global de silenciamento (`isMuted`) e encapsular a lógica de geração e reprodução do bip sonoro (`tocarAlertaSonoro`).

## 2. Layout Global Updates

- [x] 2.1 Adicionar no layout global (`frontend/src/layouts/DefaultLayout.vue`) a checagem periódica (a cada 30 segundos) de alertas não lidos, acionando o som global se o usuário logado pertencer ao perfil NIR ou UTI.
- [x] 2.2 Integrar um botão de mute/unmute visual no header do layout global (`DefaultLayout.vue`) para permitir mutar ou desmutar de qualquer tela de forma persistente no `localStorage`.

## 3. Home View Cleanup

- [x] 3.1 Limpar a lógica de timer local e de áudio redundante do componente `frontend/src/views/Home.vue`.
- [x] 3.2 Atualizar o monitoramento de cirurgias pendentes na `Home.vue` para que invoque o método `uiStore.tocarAlertaSonoro()` caso haja novas cirurgias pendentes de liberação na UTI.
