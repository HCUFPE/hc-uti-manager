## 1. Banco de Dados e Backend

- [x] 1.1 Adicionar as colunas `cirurgia_finalizada_em` e `encaminhamento_liberado_em` no modelo `SolicitacaoLeito` em `src/models/solicitacao_leito.py`
- [x] 1.2 Adicionar comandos de `ALTER TABLE` no lifespan startup em `src/main.py` para criar as colunas de forma automática no SQLite local se estiverem ausentes
- [x] 1.3 Atualizar os métodos `marcar_cirurgia_finalizada`, `liberar_encaminhamento` e `cancelar_liberacao` no arquivo `src/controllers/solicitacao_leito_controller.py` para salvar os respectivos timestamps e retornar a duração da espera
- [x] 1.4 Modificar a rota `POST /api/solicitacoes/{sol_id}/liberar-encaminhamento` em `src/routers/solicitacoes_leito.py` para capturar a duração e registrá-la nos detalhes do histórico de auditoria
- [x] 1.5 Atualizar a listagem de leitos físicos em `src/controllers/leitos_controller.py` para expor o campo `cirurgia_finalizada_em` com o fuso compensado para Brasília (UTC-3)
- [x] 1.6 Implementar o cálculo da média do tempo de espera em minutos no `IndicadoresProvider` em `src/providers/implementations/indicadores_provider.py` e retornar no dicionário de detalhados

## 2. Frontend: Exibição do Temporizador e Novo Indicador

- [x] 2.1 Atualizar a definição do tipo `Patient` em `frontend/src/views/Home.vue` e `frontend/src/components/BedCard.vue` para conter `horaCirurgiaFinalizada?: string`
- [x] 2.2 Mapear a propriedade `cirurgia_finalizada_em` no frontend no arquivo `frontend/src/views/Home.vue`
- [x] 2.3 Implementar temporizador reativo no componente `frontend/src/components/BedCard.vue` que atualiza a cada 1 minuto exibindo o tempo total decorrido ao lado do ícone `ClockIcon`
- [x] 2.4 Adicionar o card do novo indicador "Tempo Médio de Liberação de Encaminhamento" na visualização `frontend/src/views/Indicadores.vue`, formatando o resultado de forma elegante (horas/minutos)
