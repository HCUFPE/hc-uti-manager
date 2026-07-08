## Why

Quando uma reserva é cancelada pelo painel de leitos (UTI/Admin), a solicitação retorna ao estado de "Pendente". Contudo, as prioridades da fila não são recalculadas nesta rota (ao contrário do cancelamento feito pela tela de solicitações), fazendo com que a fila fique com duas solicitações com prioridade "P1" simultaneamente. É necessário forçar o recálculo automático de prioridades das solicitações ativas para a mesma data.

Além disso, a rotulagem do botão na listagem de solicitações reservadas exibe "Cirurgia Finalizada" para uma cirurgia que ainda não foi concluída. Ajustaremos o botão para exibir o texto imperativo "Finalizar Cirurgia", condizente com a ação a ser disparada.

## What Changes

- **Sincronização de Prioridades no Cancelamento**: Atualizar o método `cancelar_reserva` em `src/controllers/leitos_controller.py` para instanciar temporariamente o controlador `SolicitacaoLeitoController` e acionar o recálculo automático de prioridades da fila para a data da cirurgia correspondente à solicitação.
- **Ajuste Textual no Botão**: Atualizar o botão de cirurgia no arquivo `frontend/src/views/Solicitacoes.vue` para exibir "Finalizar Cirurgia" quando a cirurgia não estiver concluída.

## Capabilities

### Modified Capabilities
- `solicitacao-leitos`: Melhoria no gerenciamento do ciclo de vida de solicitações e reservas, garantindo a consistência das prioridades na fila após liberação de leitos.

## Impact

- **Backend**:
  - `src/controllers/leitos_controller.py`: Chamar o recálculo de prioridades ao reverter o status de uma vaga reservada para pendente.
- **Frontend**:
  - `frontend/src/views/Solicitacoes.vue`: Ajustar a label no template do botão.
