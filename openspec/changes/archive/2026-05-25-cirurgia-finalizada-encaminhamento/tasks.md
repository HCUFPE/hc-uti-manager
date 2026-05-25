## 1. Backend Implementation

- [x] 1.1 Atualizar o modelo de banco de dados `SolicitacaoLeito` em `src/models/solicitacao_leito.py` para incluir as colunas `cirurgia_finalizada` e `encaminhamento_liberado`, e criar a migração necessária com Alembic.
- [x] 1.2 Implementar o endpoint `POST /api/solicitacoes/{sol_id}/cirurgia-finalizada` na rota de solicitações que valida perfil de solicitantes, atualiza o banco e registra o log de histórico.
- [x] 1.3 Implementar o endpoint `POST /api/solicitacoes/{sol_id}/liberar-encaminhamento` na rota de solicitações que valida perfil UTI/Admin, atualiza o banco e registra o log de histórico.
- [x] 1.4 Implementar o endpoint `POST /api/solicitacoes/{sol_id}/cancelar-liberacao` na rota de solicitações que valida perfil UTI/Admin, atualiza o banco (define `encaminhamento_liberado=False`) e registra o log de histórico.
- [x] 1.5 Modificar o `listar_leitos` em `src/controllers/leitos_controller.py` para incluir no retorno as chaves `cirurgia_finalizada` e `encaminhamento_liberado` a partir da solicitação original associada.
- [x] 1.6 Atualizar o sincronizador de alertas em `src/controllers/alerta_controller.py` para detectar eventos de histórico de cirurgia finalizada (alerta para UTI), encaminhamento liberado (alerta para o solicitante) e liberação cancelada (alerta para o solicitante).

## 2. Frontend Implementation

- [x] 2.1 Adicionar botão "Cirurgia Finalizada" e badges informativas na fila de solicitações reservadas em `frontend/src/views/Solicitacoes.vue`.
- [x] 2.2 Atualizar as propriedades reativas do componente `BedCard.vue` e estilizar a coloração amarela e verde nos cards de leitos reservados baseada nos novos status.
- [x] 2.3 Adicionar os botões "Liberar Encaminhamento" e "Cancelar Liberação" para a UTI no `BedCard.vue` e mapear os eventos no componente pai `Home.vue` para chamar os endpoints correspondentes.

## 3. Verification

- [x] 3.1 Validar que o solicitante consegue finalizar a cirurgia de uma solicitação reservada, a reserva fica amarela para a UTI, e um alerta é criado.
- [x] 3.2 Validar que a UTI consegue liberar o encaminhamento, a reserva fica verde, e o solicitante correspondente recebe o alerta de liberação.
