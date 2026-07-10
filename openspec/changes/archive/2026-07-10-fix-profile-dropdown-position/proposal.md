## Why

O menu dropdown de perfil (`ProfileDropdown.vue`) no cabeçalho está sobrepondo o botão superior e sofrendo um corte (clipping) em sua parte superior (quebrando a exibição do avatar circular do usuário). Isso ocorre pela falta de uma classe de posicionamento vertical explícita (como `top-full`) combinada com a propriedade `overflow-hidden` do container do dropdown.

## What Changes

- **Ajuste de Posicionamento:** Adicionar a classe `top-full` no container absoluto do dropdown de perfil em `ProfileDropdown.vue` para que ele renderize abaixo do botão.
- **Visualização Correta do Avatar:** Com a posição correta, o avatar e o texto não serão mais cortados na borda superior do dropdown.

## Capabilities

### New Capabilities

### Modified Capabilities
- `usuario-config`: Detalhes do Usuário no Cabeçalho e exibição correta do menu de perfil.

## Impact

- **Frontend:** `frontend/src/components/ProfileDropdown.vue`
