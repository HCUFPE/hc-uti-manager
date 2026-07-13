## 1. Implementação no Frontend

- [x] 1.1 Adicionar o estado `isTvMode` e a ação `toggleTvMode` no store de UI `frontend/src/stores/ui.ts` persistindo no localStorage.
- [x] 1.2 Ajustar `frontend/src/layouts/DefaultLayout.vue` para ocultar o cabeçalho e menu lateral e remover o padding lateral quando `uiStore.isTvMode` for verdadeiro.
- [x] 1.3 Modificar `frontend/src/views/Home.vue` para adicionar o botão de alternância do Modo TV, ocultar o sumário de leitos do topo e tornar o grid de leitos mais denso quando ativado.
- [x] 1.4 Alterar a lógica do filtro de status em `frontend/src/views/Home.vue` para permitir a seleção de múltiplos status ao mesmo tempo (comportamento de multi-select).

## 2. Validação Local

- [ ] 2.1 Compilar e rodar a aplicação localmente para validar a responsividade e o comportamento das novas funções.
