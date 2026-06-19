## Context

Atualmente, o sistema gerencia a prioridade das solicitações de leitos de UTI agrupando-as em "buckets" divididos por Data de Cirurgia AND Turno. Isso significa que as filas de prioridades (P1, P2...) rodam de forma independente para cada turno do mesmo dia.
O usuário solicitou unificar essa fila para que todas as cirurgias agendadas para o mesmo dia concorram na mesma fila de prioridades diária (P1 a Pn), independente do turno (Manhã, Tarde ou Noite).

## Goals / Non-Goals

**Goals:**
- Unificar a fila de prioridades para ser agrupada e ordenada exclusivamente pela Data da Cirurgia.
- Adaptar o método de sincronização de prioridades no backend (`_sincronizar_prioridades`) para ignorar o parâmetro de turno.
- Atualizar todas as chamadas do backend que sincronizavam prioridades para o novo formato simplificado.
- Remover o critério de ordenação por Turno no computed de exibição da fila no frontend (`Solicitacoes.vue`).

**Non-Goals:**
- Não removeremos o campo "Turno" do cadastro do paciente ou do banco de dados (ele continua sendo exibido nos cards e armazenado no banco, apenas deixa de atuar no agrupamento e na lógica de ordenação de prioridades).
- Não alteraremos os cálculos de médias e indicadores de dashboards baseados em turnos.

## Decisions

- **Modificação da Assinatura e Lógica de `_sincronizar_prioridades`**:
  O parâmetro `turno` será removido ou tornado opcional no método `_sincronizar_prioridades`. O filtro de busca de registros no banco de dados local será simplificado para:
  `bucket = [s for s in todas if s.data_cirurgia == data_cirurgia and s.status == "Pendente"]`
  Dessa forma, todas as solicitações pendentes para a mesma data serão reordenadas de P1 a Pn sequencialmente.

- **Atualização das Chamadas**:
  Todas as rotas e métodos do `SolicitacaoLeitoController` que chamavam `_sincronizar_prioridades` serão atualizados para não enviar o turno ou enviar o turno como opcional/ignorado.

- **Ordenação no Frontend**:
  No arquivo `Solicitacoes.vue`, no computed `solicitacoesFiltradas`, removeremos a ordenação secundária por Turno. O fluxo de ordenação para desempate de prioridade no mesmo dia passará a ser diretamente:
  `Data da Cirurgia` -> `Prioridade (P1 < P2...)` -> `Horário de Início` -> `Data/Hora da Solicitação (ordem de inclusão)`.

## Risks / Trade-offs

- **[Risco] Reatribuição em Massa**:
  Ao unificar as prioridades por dia, um dia com muitas solicitações (ex: 15 cirurgias) terá todas as prioridades sequenciadas de P1 a P15.
  *Mitigação*: O sistema já suporta prioridades maiores no banco de dados e exibe até P10 no select de cadastro (prioridades maiores serão computadas como P11, P12... na ordenação se necessário).
