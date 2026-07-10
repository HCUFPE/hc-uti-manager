## Context

O dropdown de perfil do cabeçalho superior (`ProfileDropdown.vue`) é renderizado sem a classe `top-full` (que o posicionaria perfeitamente abaixo de seu elemento pai). Devido a isso, ele acaba flutuando de forma errática (sobrepondo o botão) e, com a classe `overflow-hidden`, a borda superior do dropdown corta a imagem/avatar circular do usuário.

## Goals / Non-Goals

**Goals:**
- Posicionar o dropdown exatamente abaixo da barra do cabeçalho.
- Resolver a quebra/corte na imagem circular do avatar.

**Non-Goals:**
- Mudar o conteúdo do dropdown ou a lógica de logout.

## Decisions

- **Modificação em `ProfileDropdown.vue`:**
  - Adicionar a classe `top-full` no elemento absolute do dropdown (`class="absolute right-0 top-full ..."`).
  - O uso de `top-full` instrui o CSS a colocar a div a partir de `100%` da altura do elemento pai, prevenindo sobreposição com o botão e o cabeçalho.

## Risks / Trade-offs

- Nossos testes não indicam nenhum risco visual colateral, pois o elemento pai já possui a classe `relative`.
