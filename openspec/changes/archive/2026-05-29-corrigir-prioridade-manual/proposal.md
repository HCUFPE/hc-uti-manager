## Why

Atualmente, quando há múltiplas solicitações de leito no mesmo dia e turno (mesmo bucket) e o usuário altera manualmente a prioridade de uma solicitação (ex: mudando um paciente de P2 para P1), o sistema salva a alteração, mas a prioridade é imediatamente sobrescrita para o valor original (P2) pelo algoritmo de sincronização automática de prioridades. Isso ocorre porque o algoritmo reordena as solicitações estritamente pela hora da cirurgia e data de criação, desconsiderando a prioridade que o usuário definiu manualmente.

## What Changes

- Refatoração da função `_sincronizar_prioridades` no controlador de solicitações de leito para respeitar a prioridade definida manualmente pelo usuário para uma solicitação específica (`sol_id_foco`).
- Ajuste no algoritmo de sincronização para que, quando uma prioridade manual for definida, a solicitação em foco seja posicionada no local desejado e as outras solicitações no mesmo bucket sejam deslocadas mantendo a ordenação cronológica relativa entre elas.
- Garantia de que a sequência de prioridades permaneça sem lacunas (P1, P2, P3...) após o ajuste manual.

## Capabilities

### New Capabilities

<!-- Nenhuma nova capability está sendo introduzida -->

### Modified Capabilities

- `solicitacao-leitos`: A sincronização de prioridades no bucket de solicitações de leito passará a priorizar a ordenação manual quando fornecido um id de foco com uma prioridade desejada, ajustando os outros elementos sem sobrescrever a intenção do usuário.

## Impact

- Afeta `SolicitacaoLeitoController` (`src/controllers/solicitacao_leito_controller.py`), especificamente o método `_sincronizar_prioridades` e suas chamadas em edição, exclusão e alteração de status de solicitação.
- Melhora a experiência de uso do painel de regulação de leitos (Bloco Cirúrgico), permitindo que a prioridade seja reordenada manualmente na fila do mesmo dia e turno.
