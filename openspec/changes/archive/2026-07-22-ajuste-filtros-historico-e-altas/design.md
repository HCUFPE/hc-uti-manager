## Context

O usuário solicitou melhorias na usabilidade do dashboard e na auditoria do histórico de ações:
1. Ajuste de nomenclatura: Alterar "Altas Pendentes (Aguardando Destino)" para "Altas Pendentes (Aguardando Transferência)".
2. Consolidação dos filtros de histórico: Atualmente, os logs são filtrados por tipos técnicos bem granulares (solicitacao, reserva, destino, cancelamento, alta). Isso será consolidado em 3 macro-categorias de negócio no frontend e no backend: Altas, Solicitações e Reservas.

## Goals / Non-Goals

**Goals:**
* Exibir "Altas Pendentes (Aguardando Transferência)" na tabela de resumo de ações de alta no dashboard.
* Reduzir os filtros de tipo de histórico para exatamente 3 opções: Altas, Solicitações e Reservas.
* Agrupar no backend todas as sub-ações correspondentes a cada uma destas 3 categorias para que a listagem de histórico retorne as ações corretas.

**Non-Goals:**
* Alterar o armazenamento físico das ações no banco de dados (os tipos persistidos no banco continuarão sendo os tipos originais específicos).

## Decisions

### 1. Novo agrupamento de tipos de histórico no Backend (`HistoricoProvider`)
Modificaremos a query de histórico para mapear os 3 filtros principais aos seus respectivos sub-tipos:
* **alta**: `alta`, `conclusao_alta`, `destino`, `alteracao_destino`, `destino_disponivel`, `destino_pendente`, `cancelamento`.
* **solicitacao**: `solicitacao`, `nova_solicitacao`, `conclusao`, `edicao`, `alteracao_prioridade`, `cirurgia_finalizada`, `encaminhamento_liberado`, `encaminhamento_cancelado`, `exclusao_solicitacao`.
* **reserva**: `reserva`, `remanejamento_reserva`, `cancelamento_reserva`.

### 2. Filtros de Interface no Frontend (`Historico.vue`)
* A lista `filtroTipos` será simplificada para conter apenas:
  ```typescript
  const filtroTipos = [
    { value: 'alta', label: 'Altas' },
    { value: 'solicitacao', label: 'Solicitações' },
    { value: 'reserva', label: 'Reservas' },
  ];
  ```

### 3. Ajuste de Texto no Frontend (`Indicadores.vue`)
* Atualizar a célula da tabela para exibir "Altas Pendentes (Aguardando Transferência)".

## Risks / Trade-offs

* **[Risk]** Algum tipo de ação não mapeado ficar de fora de um dos três filtros principais.
  * **Mitigation**: Mapeamos de forma exaustiva todas as ações atualmente existentes e mantivemos o fallback `stmt.where(HistoricoAcao.tipo == tipo)` para qualquer outro tipo não mapeado.
