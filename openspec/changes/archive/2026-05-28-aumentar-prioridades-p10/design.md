## Context

The UI in `Solicitacoes.vue` provides a dropdown to select patient priority when creating/editing requests. The values are hardcoded in the HTML:
```html
<select v-model="formNova.prioridade" ...>
  <option value="">Nenhuma (Padrão)</option>
  <option value="P1">P1 (Maior)</option>
  <option value="P2">P2</option>
  <option value="P3">P3</option>
  <option value="P4">P4</option>
  <option value="P5">P5 (Menor)</option>
</select>
```

We will extend this select block to go up to `P10` and label `P10` as "(Menor)".

## Goals / Non-Goals

**Goals:**
- Update the priority selection dropdown in `Solicitacoes.vue` to list `P1` through `P10`.

**Non-Goals:**
- Database changes (the backend already supports any string for priority).

## Decisions

### 1. Update options in `Solicitacoes.vue`
We will replace the static options with:
```html
<select v-model="formNova.prioridade" ...>
  <option value="">Nenhuma (Padrão)</option>
  <option value="P1">P1 (Maior)</option>
  <option value="P2">P2</option>
  <option value="P3">P3</option>
  <option value="P4">P4</option>
  <option value="P5">P5</option>
  <option value="P6">P6</option>
  <option value="P7">P7</option>
  <option value="P8">P8</option>
  <option value="P9">P9</option>
  <option value="P10">P10 (Menor)</option>
</select>
```

## Risks / Trade-offs

- None identified.
