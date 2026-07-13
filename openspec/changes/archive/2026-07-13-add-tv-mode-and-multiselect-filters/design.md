## Context

O painel de monitoramento de leitos precisa de duas melhorias importantes:
1. **Modo TV:** Ocultação de elementos grandes de navegação/resumo (Header, SidebarNav e Overview Cards) e adensamento do grid para caber todos os leitos na viewport da TV.
2. **Seleção Múltipla nos Filtros:** Permitir selecionar mais de um status ao mesmo tempo para filtragem avançada (ex: exibir "Disponíveis" e "Reservados" simultaneamente).

## Goals / Non-Goals

**Goals:**
- Implementar o "Modo TV" com alternador por botão (ícone de TV).
- Ocultar cabeçalho, barra lateral e overview cards no Modo TV.
- Aumentar a densidade do grid de leitos (ex: `grid-cols-6` ou `grid-cols-8`) no Modo TV.
- Permitir seleção múltipla de filtros sem alterar a disposição visual existente dos botões.
- Sincronizar o estado do Modo TV usando o Pinia (`uiStore`) e persistir no `localStorage`.

**Non-Goals:**
- Criar novas telas ou alterar rotas.
- Modificar o banco de dados.

## Decisions

- **1. Loja Pinia (`frontend/src/stores/ui.ts`):**
  - Adicionar o estado reativo `isTvMode` e a ação `toggleTvMode` persistida no `localStorage`.

- **2. Layout Principal (`frontend/src/layouts/DefaultLayout.vue`):**
  - Importar `uiStore` e ocultar condicionalmente `SidebarNav` e `header` com `v-if="!uiStore.isTvMode"`.
  - Ajustar o padding e background da tag `<main>` e o padding do container interno quando `isTvMode` for verdadeiro.

- **3. Filtro e Modo TV em `frontend/src/views/Home.vue`:**
  - Adicionar o botão do Modo TV com um ícone apropriado (ex: `ComputerDesktopIcon` ou similar).
  - Ocultar a seção superior de métricas (`Resumo dos Leitos`) usando `v-if="!uiStore.isTvMode"`.
  - Tornar o grid adaptativo baseado no `uiStore.isTvMode`:
    - Normal: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4`
    - TV: `grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-2`
  - Mudar `statusFilter` de string para array reativo `statusFilters = ref<StatusFilter[]>([]);`.
  - Se `statusFilters` estiver vazio, equivale a exibir todos.
  - Ajustar a classe ativa e a ação `@click` nos botões de filtro para adicionar/remover status do array de filtros ativos.

## Risks / Trade-offs

- **Risco:** O Modo TV ocultar controles necessários para gerenciar leitos.
- **Mitigação:** Os cards individuais de leitos continuarão com todas as suas ações operacionais acessíveis (alta, cancelamento, etc.). Apenas os menus estruturais de navegação global são ocultados.
