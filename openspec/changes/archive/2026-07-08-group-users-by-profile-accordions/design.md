## Context

A visualização de usuários na tela de configurações (`AdminConfig.vue`) precisa ser refinada para agrupar e organizar de forma modular os usuários por setor. Também precisamos carregar os dados reais de 21 novos operadores do NIR para produção.

## Goals / Non-Goals

**Goals:**
- Agrupar usuários do NIR com NIR-Admin, UTI com UTI-Admin, etc.
- Apresentar acordeões expansíveis com a contagem total de usuários.
- Ordenar os usuários alfabeticamente (A-Z) pelo nome dentro de cada acordeão.
- Criar script automatizado para importar os 21 usuários NIR do AD.

## Decisions

### 1. Script de Importação dos Usuários do NIR
Criaremos um script `scratch/backfill_nir_users.py` contendo a lista dos 21 logins confirmados:
1. `alessandra.barros`
2. `ana.crist`
3. `angelica.negromonte`
4. `barbara.ferreira`
5. `caline.ferraz`
6. `careli.brandao`
7. `catia.cavalcante`
8. `christyne.jorge`
9. `araujo.cristiane`
10. `cristiane.falves`
11. `edlene.freitas`
12. `edna.albuquerque`
13. `fabiola.ribeiro`
14. `maira.valle`
15. `manuelle.holanda`
16. `mauricia.silva`
17. `monica.andrade`
18. `paulene.xavier`
19. `paulo.rcsilva`
20. `thayana.dantas`
21. `vera.gomes`

O script executará no ambiente da VM buscando os atributos reais de cada usuário no LDAP/AD e inserindo-os no banco de dados SQLite `/app/data/app.db` com o perfil `"NIR"`.

### 2. Agrupamento Reativo (`AdminConfig.vue`)
Criaremos uma propriedade computada `groupedPerfis` que divide o array `perfis` nos grupos de setor. Dentro da mesma computada, ordenaremos cada grupo alfabeticamente:
```typescript
groups[key].users.sort((a, b) => {
  const nomeA = (a.nome_completo || a.username || "").toLowerCase();
  const nomeB = (b.nome_completo || b.username || "").toLowerCase();
  return nomeA.localeCompare(nomeB);
});
```

### 3. Controle de Expansão/Colapso (Frontend)
Definiremos um `ref` contendo a expansão inicial dos grupos. Por conveniência e facilidade de teste do usuário, iniciaremos com a regulação (NIR) expandido e o restante colapsado:
```typescript
const expandedGroups = ref<Record<string, boolean>>({
  nir: true,
  uti: false,
  bc: false,
  hem: false,
  cob: false,
  admin: false,
  comum: false
});
```
Cada cabeçalho de grupo será renderizado como um acordeão estilizado com chevron interativo.
