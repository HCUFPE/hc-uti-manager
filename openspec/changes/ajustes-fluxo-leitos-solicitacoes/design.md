## Context

Há cinco requisitos mistos envolvendo correções e melhorias no fluxo de solicitações e leitos: cancelamento de solicitações reservadas por solicitantes gestores, obrigatoriedade de motivo para cancelamento de reservas, disponibilidade de leitos em limpeza, atualização do estado do leito ao editar uma solicitação e conserto de alertas de prioridade.

## Goals / Non-Goals

**Goals:**
- Permitir que as mesmas roles autorizadas a editar solicitações reservadas (BC, BC-ADMIN, COB, COB-ADMIN, HEM, HEM-ADMIN) possam cancelá-las.
- Exigir motivo no cancelamento de reserva no backend e frontend.
- Modificar o endpoint de leitos disponíveis para incluir os status "higienização" ou "limpeza".
- Na edição de solicitação (`PATCH`), atualizar o estado no SQLite (`leitos`) caso a solicitação possua um leito associado.
- Comparar a prioridade nova com a antiga antes de gravar no histórico.

**Non-Goals:**
- Refatorar a estrutura do histórico ou das tabelas de leitos e solicitações.

## Decisions

- **Cancelamento de Solicitação Reservada**: Em `routers/solicitacoes_leito.py` (e no controller), permitiremos o delete/cancelamento se o `status` for `Reservado` e a role estiver na *allowlist*. Ao invés de lançar erro, o controller fará a limpeza da reserva (`limpar_reserva_por_solicitacao`) seguida pela deleção.
- **Sincronização na Edição**: Em `editar_solicitacao` no controller, se `alvo.status == 'Reservado'`, recuperaremos o leito através de `estado_provider` e atualizaremos a `idade`, `prontuario` e `especialidade` no leito físico para garantir que a tela de "Leitos" reflita os novos dados.
- **Leitos Disponíveis**: A rota ou provider que busca leitos disponíveis (`get_disponiveis`) hoje checa status (Livre, Alta). Adicionaremos "Limpeza" e "Higienização" à cláusula de filtro.
- **Alerta de Prioridade**: No router `patch("/{sol_id}")`, a variável de `tipo_hist` só será `alteracao_prioridade` se `payload.get("prioridade")` estiver presente e for diferente de `solicitacao.prioridade`.

## Risks / Trade-offs

- **[Risk]** Sincronização falhar se o leito associado mudar concorrentemente.
  - *Mitigação*: Atualização direta via `solicitacao_id` no banco de estados (`leitos`).
- **[Risk]** Aumento da complexidade do endpoint de edição.
  - *Mitigação*: Manter a regra delegada ao provedor de leitos físicos, reaproveitando funções de UPDATE que já existem ou criando uma específica para sincronismo.
