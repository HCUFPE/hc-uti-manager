## 1. Backend

- [x] 1.1 Criar a query SQL `src/providers/sql/leito/tempo_higienizacao.sql` para obter os tempos de higienização do leito no AGHU (filtrando `unf_seq = 115`).
- [x] 1.2 Implementar o método `obter_historico_higienizacao` em `LeitoAghuProvider` para executar a query SQL no Postgres do AGHU.
- [x] 1.3 Adicionar o cálculo e média de tempo de higienização em `IndicadoresProvider`, incluindo suporte a mock com `MOCK_BEDS=true`.
- [x] 1.4 Atualizar a resposta do endpoint `/api/indicadores/resumo` para retornar `tempo_higienizacao_minutos`.

## 2. Frontend

- [x] 2.1 Modificar o layout em `frontend/src/views/Indicadores.vue` para aumentar as colunas e incluir o novo card "Tempo de Higienização".
- [x] 2.2 Integrar o campo `tempo_higienizacao_minutos` no card exibindo o valor computado.
- [x] 2.3 Executar `npm run build` localmente para validar a compilação do frontend.
