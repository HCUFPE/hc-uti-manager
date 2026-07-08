## Context

O bug de prioridade duplicada ocorre porque a rota de cancelamento de reserva pelo painel de leitos (`DELETE /api/leitos/{leito_id}/reserva`) chama o método `LeitosController.cancelar_reserva`, que reverte o status da solicitação associada para `"Pendente"`, mas não chama o método de reordenação de fila `_sincronizar_prioridades`. Isso faz com que duas solicitações mantenham o valor `"P1"` gravado no banco de dados.

Adicionalmente, precisamos corrigir o texto do botão de ação no frontend de `"Cirurgia Finalizada"` para `"Finalizar Cirurgia"` a fim de indicar a ação a ser executada.

## Goals / Non-Goals

**Goals:**
- Garantir que o cancelamento de uma reserva pela tela de leitos execute o recálculo automático de prioridades para a mesma data.
- Alterar o texto exibido no botão do frontend.

**Non-Goals:**
- Alterar os algoritmos de ordenação por data, especialidade ou hora.

## Decisions

### 1. Invocação dinâmica de `SolicitacaoLeitoController._sincronizar_prioridades`
Para manter o princípio DRY (Don't Repeat Yourself) e reutilizar o algoritmo de priorização complexo, instanciaparemos o `SolicitacaoLeitoController` temporariamente no método `cancelar_reserva` do `LeitosController` e invocaremos a reordenação:
```python
from controllers.solicitacao_leito_controller import SolicitacaoLeitoController
sol_controller = SolicitacaoLeitoController(
    leito_provider=solicitacao_provider,
    estado_provider=self.estado_provider
)
await sol_controller._sincronizar_prioridades(
    solicitacao.data_cirurgia,
    sol_id_foco=sol_id,
    prioridade_desejada=solicitacao.prioridade
)
```

### 2. Modificação da expressão condicional no frontend
Substituir a label estática no template de `frontend/src/views/Solicitacoes.vue`:
- De: `sol.cirurgia_finalizada ? 'Cirurgia Concluída' : 'Cirurgia Finalizada'`
- Para: `sol.cirurgia_finalizada ? 'Cirurgia Concluída' : 'Finalizar Cirurgia'`

## Risks / Trade-offs

- **[Trade-off] Importação circular em Python**: Para mitigar qualquer risco de importação circular entre os dois controllers, realizaremos o `import` de `SolicitacaoLeitoController` localmente dentro do método `cancelar_reserva`.
