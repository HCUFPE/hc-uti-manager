## Why

O setor UTI espelha o painel de monitoramento de leitos em uma TV, porém é necessário usar a barra de rolagem para ver todos os leitos devido ao espaço vertical consumido pelo cabeçalho principal e os cards de estatísticas. Além disso, o filtro de leitos atual é restritivo por permitir selecionar apenas um status por vez (ex: só "Disponível" ou só "Reservado").

## What Changes

- **Modo TV (Monitoramento Dedicado):** Adição de um botão de alternância para o "Modo TV". Quando ativado, este modo oculta o cabeçalho global, a barra de navegação e a seção de métricas resumo, utilizando todo o espaço disponível da viewport com um grid mais compacto/denso.
- **Filtro com Seleção Múltipla:** Alterar a lógica do filtro de status na página inicial para permitir a seleção de múltiplos status ao mesmo tempo, mantendo o layout atual de botões de filtro. Clicar em "Todos" limpará a seleção, exibindo tudo de uma vez.

## Capabilities

### New Capabilities

### Modified Capabilities
- `internacao-leitos`: Suporte a Modo TV compacto para exibição completa em telas e filtros de status com seleção múltipla.

## Impact

- **Frontend:** `frontend/src/views/Home.vue`
