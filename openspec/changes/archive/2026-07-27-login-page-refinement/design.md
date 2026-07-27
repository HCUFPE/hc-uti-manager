## Goals / Non-Goals

**Goals:**
- Ajustar rótulos, placeholders e textos explicativos de `frontend/src/views/Login.vue` com acentuação e caixa adequadas.
- Remover o cabeçalho `<h1>Bem-vindo de Volta</h1>`.
- Remover o botão `Esqueceu a senha?` para alinhar com o login unificado do AD.

## Decisions

### Modificação em `Login.vue`

1. **Remoção de Título:** Apagar a linha `31` que contém o `h1`.
2. **Correção de Acentuação:**
   - Trocar "Gestao" por "Gestão" na linha `16`.
   - Trocar "Clinicas" por "Clínicas" na linha `17`.
   - Trocar "Usuario" por "Usuário" no label (linha `40`) e no placeholder (linha `46`).
   - Ajustar as strings de erro de validação Zod nas linhas `168` e `169` para incluir "usuário" e "não".
3. **Remoção de Controle Redundante:** Apagar a tag `<button type="button">Esqueceu a senha?</button>` das linhas `86` a `88`.
4. **Caixa de Texto:** Modificar a linha `117` de "Utilize Login e Senha de Rede" para "Utilize login e senha de rede".
