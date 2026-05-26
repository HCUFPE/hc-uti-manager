## 1. Backend: Injeção de Dependências e Auditoria do Censo

- [x] 1.1 Injetar `historico_provider` no construtor do `LeitosController` em `src/dependencies.py`
- [x] 1.2 Atualizar `LeitosController` para receber `historico_provider` em `src/controllers/leitos_controller.py`
- [x] 1.3 Implementar log do evento `conclusao` (admissão) na sincronização inteligente em `LeitosController.listar_leitos`
- [x] 1.4 Implementar detecção e log do evento `conclusao_alta` (saída física/discharge) na sincronização inteligente em `LeitosController.listar_leitos`

## 2. Backend: Controle de Acesso para Administradores Setoriais

- [x] 2.1 Atualizar dependências de autenticação nos roteadores de Histórico (`src/routers/historico.py`) e Indicadores (`src/routers/indicadores.py`) para permitir perfis que terminam com `-Admin` (utilizando `check_role`)

## 3. Backend: Cálculos de Indicadores e Filtros por Período

- [x] 3.1 Atualizar `IndicadoresController.obter_resumo` para aceitar `data_inicio` e `data_fim` opcionais e repassar ao `IndicadoresProvider`
- [x] 3.2 Atualizar `IndicadoresProvider.get_indicadores_gerais` para aceitar `data_inicio` e `data_fim` e filtrar por período
- [x] 3.3 Implementar cálculo do número médio semanal de novas internações (geral, demandantes, especialidades)
- [x] 3.4 Implementar cálculo do tempo médio de ocupação de leitos (geral, demandantes, especialidades)
- [x] 3.5 Implementar cálculo das taxas de atendimento e cancelamento de solicitações
- [x] 3.6 Implementar cálculo do tempo médio de solicitação até ocupação física
- [x] 3.7 Implementar cálculo do horário médio de reserva de leito por turno (manhã e tarde)
- [x] 3.8 Implementar cálculo do tempo médio de recepção pós fim cirúrgico para pacientes do BC
- [x] 3.9 Implementar cálculo do tempo médio de acomodação de alta (solicitação UTI até definição NIR)
- [x] 3.10 Implementar cálculo do tempo médio de liberação de leito de acomodação pós-UTI (definição NIR até liberação/alta censo)
- [x] 3.11 Implementar contagem de volumes absolutos e cálculo de percentuais relativos

## 4. Frontend: Menus de Navegação e Filtros de Indicadores

- [x] 4.1/4.1 Atualizar visibilidade dos links de Histórico e Indicadores no `SidebarNav.vue` para incluir usuários `isAnyAdmin`
- [x] 4.2 Adicionar campos de filtro por período (data inicial e final) na tela `Indicadores.vue`
- [x] 4.3 Integrar os novos indicadores de tempos médios e taxas no painel de cartões de KPI
- [x] 4.4 Atualizar gráficos e tabelas de volume para exibir as novas métricas e percentuais relativos de fluxo

## 5. Validação e Testes

- [x] 5.1 Criar script de teste em `scripts/test_indicadores_fluxo.py` para validar todos os cálculos e logs
- [x] 5.2 Executar testes locais e garantir que o build do frontend (`npm run build`) funciona com sucesso
