## 1. Implementar Polling no Painel de Leitos

- [x] 1.1 Importar `onUnmounted` do Vue no arquivo `frontend/src/views/Home.vue`
- [x] 1.2 Configurar o `setInterval` no `onMounted` para chamar `loadLeitos()` a cada 2 minutos (120.000 ms)
- [x] 1.3 Limpar o temporizador usando `onUnmounted` para prevenir memory leaks

## 2. Implementar Polling na Fila de Solicitações

- [x] 2.1 Importar `onUnmounted` do Vue no arquivo `frontend/src/views/Solicitacoes.vue`
- [x] 2.2 Configurar o `setInterval` no `onMounted` para chamar `carregarSolicitacoes()` a cada 2 minutos (120.000 ms)
- [x] 2.3 Limpar o temporizador usando `onUnmounted` para prevenir memory leaks
