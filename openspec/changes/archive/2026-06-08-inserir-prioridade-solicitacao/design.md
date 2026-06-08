## Context

No formulário de criação de solicitações de leito no frontend, o usuário pode escolher uma prioridade específica de P1 a P10.
Contudo, o método `criar_solicitacao` no backend não inclui a prioridade informada no dicionário de dados a serem salvos e chama `_sincronizar_prioridades` sem informar o `sol_id_foco` e a `prioridade_desejada`. Isso descarta a prioridade manual de cadastro e ordena o novo paciente puramente com base nas regras cronológicas de desempate.

## Goals / Non-Goals

**Goals:**
- Gravar a prioridade do payload ao criar uma solicitação.
- Repassar essa prioridade como desejada para o algoritmo de sincronização.

**Non-Goals:**
- Alterar as prioridades de outros buckets ou alterar a ordenação padrão por data e turno.

## Decisions

### 1. Ajuste em `criar_solicitacao`
- Vamos extrair `prioridade` do payload recebido em `criar_solicitacao`.
- Adicionar `"prioridade": payload.get("prioridade")` na inserção de dados do banco local.
- Chamar `await self._sincronizar_prioridades(dt, trn, sol_id_foco=sol.id, prioridade_desejada=payload.get("prioridade"))` para sincronizar e preservar a prioridade informada.

## Risks / Trade-offs

- **[Risco]** Prioridade não informada (None ou string vazia).
  - **Mitigação**: O algoritmo de sincronização já lida com prioridade None de forma padrão, enviando a nova solicitação para o final da fila cronológica.
