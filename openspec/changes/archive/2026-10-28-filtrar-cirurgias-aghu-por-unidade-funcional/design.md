# Design: Filtrar Cirurgias do AGHU por Unidade Funcional Cirúrgica

## Context

Atualmente, o arquivo SQL [`obter_cirurgia_aghu.sql`](file:///c:/Users/daniel.turmina/Documents/HC-uti-manager/src/providers/sql/solicitacao/obter_cirurgia_aghu.sql) consulta a tabela `agh.mbc_cirurgias` filtrando apenas por `pac.prontuario = :prontuario` e `cir.situacao <> 'CANC'`. No AGHU do HC-UFPE/Ebserh:
- O módulo MBC (Bloco Cirúrgico) engloba também unidades ambulatoriais e salas de procedimentos diagnósticos, como Endoscopia (`unf_seq = 155`).
- As unidades cirúrgicas e intervencionistas que originam demanda real de leitos de UTI no hospital são:
  - **Unidade 28**: `BLOCO CIRURGICO` (Sigla: `BC`)
  - **Unidade 20**: `CENTRO OBSTETRICO` (Sigla: `COB`)
  - **Unidades 47 e 233**: `HEMODINAMICA - PDT` e `HEMODINAMICA (AMBULATORIO)` (Sigla: `HEM`)

Quando um paciente realiza um exame simples em outra unidade no mesmo dia (ex: Duodenoscopia na Unidade 155), a query SQL calcula distância temporal `0` e o seleciona, ofuscando cirurgias de grande porte agendadas no Bloco Cirúrgico (Unidade 28) para dias subsequentes.

## Goals / Non-Goals

**Goals:**
- Filtrar cirurgias no AGHU restringindo obrigatoriamente `cir.unf_seq` às unidades permitidas (`28`, `20`, `47`, `233`).
- Aplicar filtro dinâmico baseado no perfil do solicitante logado ou no parâmetro `tipo` selecionado na tela (`Cirurgico` -> `28`, `Obstetrico` -> `20`, `HEM` -> `47, 233`, fallback seguro -> `[28, 20, 47, 233]`).
- Priorizar registros com situação `AGND` (Agendada) no `ORDER BY`, de modo que procedimentos já concluídos (`RZDA`) não sobreponham cirurgias programadas.
- Atualizar a rota `GET /api/solicitacoes/consultar-aghu/{prontuario}` e o frontend (`Solicitacoes.vue`) para propagar o `tipo` da solicitação.

**Non-Goals:**
- Não alterar a tabela de solicitações local do SQLite nem os dados já salvos no censo.
- Não alterar a integração de admissão/censo de leitos (que já lê leitos físicos da UTI).

## Decisions

### Decisão 1: Cláusula SQL e Mapeamento de Unidades Funcionais
- Na query SQL, adicionar a condição:
  ```sql
  AND cir.unf_seq = ANY(:unf_seqs)
  ```
- O parâmetro `:unf_seqs` receberá uma lista de inteiros com os identificadores das unidades autorizadas.
- O controller determinará `unf_seqs` segundo a regra:
  - Se `tipo == 'Cirurgico'` ou perfil for `BC` / `BC-Admin` → `[28]`
  - Se `tipo == 'Obstetrico'` ou perfil for `COB` / `COB-Admin` → `[20]`
  - Se `tipo == 'HEM'` ou perfil for `HEM` / `HEM-Admin` → `[47, 233]`
  - Em qualquer outro caso (ex: Administrador / UTI sem tipo explícito ou Clinico) → `[28, 20, 47, 233]`

### Decisão 2: Priorização de Cirurgias Agendadas (`situacao = 'AGND'`)
- No `ORDER BY` da consulta SQL:
  ```sql
  ORDER BY 
    CASE WHEN cir.situacao = 'AGND' THEN 0 ELSE 1 END,
    CASE WHEN cir.dthr_inicio_cirg >= CURRENT_DATE THEN 0 ELSE 1 END,
    CASE WHEN cir.dthr_inicio_cirg >= CURRENT_DATE 
         THEN (cir.dthr_inicio_cirg - CURRENT_DATE) 
         ELSE (CURRENT_DATE - cir.dthr_inicio_cirg) 
    END ASC
  LIMIT 1;
  ```
- *Vantagem*: Se o paciente tiver uma cirurgia agendada para daqui a alguns dias e um procedimento já realizado no mesmo dia, o sistema priorizará a cirurgia agendada (`AGND`), que é o objeto da reserva de vaga na UTI.

### Decisão 3: Propagação no Endpoint e no Frontend
- O endpoint `consultar_aghu(prontuario: str, tipo: Optional[str] = Query(None))` receberá o parâmetro opcional e injetará o perfil do `current_user`.
- O frontend em `Solicitacoes.vue` chamará:
  ```typescript
  const url = formNova.value.tipo 
    ? `/api/solicitacoes/consultar-aghu/${pront}?tipo=${encodeURIComponent(formNova.value.tipo)}`
    : `/api/solicitacoes/consultar-aghu/${pront}`;
  const { data } = await api.get(url);
  ```

## Risks / Trade-offs

- **[Risco de cirurgias em unidades não cadastradas]** → Caso o hospital abra um novo centro cirúrgico com outro `unf_seq`.
  - *Mitigação*: As unidades autorizadas ficam centralizadas no controller e podem ser facilmente parametrizadas ou expandidas via configuração.
