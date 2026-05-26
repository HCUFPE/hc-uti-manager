## Context

Atualmente, a solicitação de alta realizada pela equipe da UTI através do modal de Alta no painel principal do frontend (`Home.vue`) contém um campo `<textarea>` para a digitação livre de necessidades especiais. Isso é enviado ao endpoint `POST /api/altas/{leito_id}` no payload como o campo `necessidadesEspeciais` (string) e persistido diretamente no banco SQLite na tabela `solicitacoes_alta`, coluna `necessidades_especiais` (VARCHAR(255)).

Para uniformizar esses dados e simplificar a rotina, o usuário deve selecionar as necessidades a partir de uma lista fixa de opções.

## Goals / Non-Goals

**Goals:**
- Substituir a caixa de texto livre por um conjunto de checkboxes no modal de alta.
- Implementar exclusão mútua entre a opção "Nenhum" e as demais opções no frontend.
- Concatenar as opções selecionadas por vírgula e enviá-las como string para manter total compatibilidade com o backend e a tabela do banco local sem necessitar de migrações estruturais de dados.

**Non-Goals:**
- Alterar o esquema do banco de dados (SQLite) ou criar tabelas associativas para necessidades.
- Permitir edição de necessidades especiais no painel do NIR (onde apenas o destino é indicado/alterado).

## Decisions

### Decisão 1: Serialização Frontend vs Modelagem de Banco Relacional
Decidimos manter a persistência de necessidades especiais como uma string única delimitada por vírgula na coluna existente `necessidades_especiais`.
- **Alternativa A**: Criar uma tabela associativa e mapear cada necessidade como um ID e chaves estrangeiras.
- **Alternativa B (Escolhida)**: Manter a serialização como string delimitada por vírgula e tratar a seleção no frontend.
- **Razão da Escolha**: A alternativa B é totalmente retrocompatível com os registros existentes de texto livre, não exige migração de banco local (Alembic) e atende perfeitamente ao escopo operacional do sistema, mantendo a simplicidade do backend.

### Decisão 2: Comportamento dos Checkboxes no Vue 3
No arquivo `frontend/src/views/Home.vue`, usaremos um array reativo `selectedNecessidades = ref<string[]>([])` associado com `v-model` às checkboxes e dispararemos uma função de tratamento no evento `@change` de cada uma delas para impor as regras de negócio:
- Se "Nenhum" for checado: Limpa todo o array e deixa apenas `["Nenhum"]`.
- Se qualquer outra for checada: Remove `"Nenhum"` do array (se presente).
- Antes de enviar a requisição de alta, se o array estiver vazio, definimos como `["Nenhum"]` e então realizamos um `.join(', ')` para atribuir a `formAlta.value.necessidadesEspeciais`.

## Risks / Trade-offs

- **[Risco]**: Pacientes antigos com textos livres no banco podem não bater exatamente com as opções.
  - **Mitigação**: O frontend apenas renderiza a string do banco de dados no painel do NIR (`Altas.vue`) e na listagem, o que significa que textos antigos continuarão sendo lidos e impressos normalmente sem quebrar a visualização.
