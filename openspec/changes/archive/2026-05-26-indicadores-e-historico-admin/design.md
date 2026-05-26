## Context

A coordenação da UTI e os administradores setoriais necessitam de maior visibilidade sobre o fluxo operacional da UTI (admissão, permanência, alta e transferência) para reduzir gargalos. O sistema atualmente calcula indicadores muito básicos e restringe o acesso ao Histórico de Ações e aos Indicadores apenas ao perfil de Administrador Geral. Além disso, a sincronização de admissão e alta com o censo (AGHU) não está registrando auditoria no histórico local.

Esta mudança visa estender o acesso a esses painéis a todos os administradores setoriais (`*-Admin`), garantir a integridade do histórico registrando admissões e altas, e implementar novos indicadores clínicos e operacionais precisos, com suporte a filtros de período de datas.

## Goals / Non-Goals

**Goals:**
- Estender a visibilidade das telas de Histórico e Indicadores aos perfis `BC-Admin`, `COB-Admin`, `HEM-Admin`, `NIR-Admin` e `UTI-Admin`.
- Logar automaticamente eventos de auditoria `"conclusao"` (admissão física) e `"conclusao_alta"` (alta física) durante a sincronização inteligente de leitos com o censo do hospital.
- Implementar 9 novos tempos médios, taxas e volumes de fluxo detalhados na API de indicadores, permitindo filtragem por intervalo de datas.
- Atualizar a interface de Indicadores no frontend com filtros de período, cartões de desempenho (kpis) e gráficos detalhados.

**Non-Goals:**
- Alterar as tabelas físicas do banco de dados (o histórico e a tabela de solicitações atual são suficientes para reconstruir os eventos).
- Desenvolver integração de BI externa (o processamento será feito diretamente no backend FastAPI para maior agilidade).

## Decisions

### 1. Injeção de Provedores no LeitosController
- **Decisão**: Passar o `historico_provider` no construtor de `LeitosController` (via `dependencies.py`).
- **Alternativa**: Obter a conexão e executar SQL bruto diretamente no controlador. Descartada por violar as regras de camadas (SQL -> Resource -> Provider -> Controller -> Router).

### 2. Registro no Histórico via Sincronização do Censo (listar_leitos)
- **Decisão**: Identificar no censo se o prontuário que estava reservado em um leito passou a ocupar fisicamente um leito na UTI (qualquer leito). Quando isso ocorrer, registrar evento `"conclusao"`. Da mesma forma, identificar se um leito com alta pendente ou definida passou a estar desocupado ou ocupado por outro prontuário. Quando isso ocorrer, registrar evento `"conclusao_alta"`.
- **Alternativa**: Exigir que a UTI confirme manualmente a admissão e a alta. Descartada pois geraria atrito para a equipe de enfermagem, que já atualiza o sistema do hospital (AGHU).

### 3. Processamento de Tempos Médios em Python no Backend
- **Decisão**: Consultar os eventos de histórico (`HistoricoAcao`) e solicitações (`SolicitacaoLeito` / `SolicitacaoAlta`) no período e realizar o pareamento e cálculo de médias em memória via algoritmos Python no `IndicadoresProvider`.
- **Alternativa**: Executar consultas SQL complexas com joins e subconsultas agregadas. Descartada porque o banco de dados local usa SQLite e fazer pareamento de datas e tempos médios em SQL de forma flexível é extremamente propenso a erros de compatibilidade. O processamento em Python em memória é performático para a escala da aplicação e altamente testável.

### 4. Controle de Acesso no Frontend e Backend
- **Decisão**:
  - No backend: permitir perfis `Administrador` e qualquer perfil que termine com `-Admin` no endpoint de histórico e indicadores.
  - No frontend: liberar visibilidade dos links no `SidebarNav.vue` e permitir acesso às telas correspondentes usando a propriedade computada `isAnyAdmin` já existente no Pinia `auth` store.
- **Alternativa**: Criar um novo papel "Visualizador" ou criar tabelas de permissões finas no banco. Descartada para manter a simplicidade do RBAC atual.

## Risks / Trade-offs

- **[Risco] Inconsistências de fuso horário** -> As datas no banco de dados SQLite são salvas em UTC/GMT, mas apresentadas com ajuste de -3h (Brasília) no frontend. Para os cálculos de tempos médios, faremos as subtrações diretamente com objetos `datetime` ingênuos (ou cientes de fuso se ambos tiverem) e retornaremos o valor em horas ou minutos para evitar distorções de fuso horário.
- **[Risco] Sincronizações repetidas gravando múltiplos logs** -> Se o censo for listado várias vezes por minuto, precisamos garantir que o log de `conclusao` ou `conclusao_alta` seja gravado apenas uma vez.
  - **Mitigação**: O log só é gerado se o status da solicitação de leito ainda não for `"Concluída"` (para admissão) ou se a solicitação de alta ainda for `"pendente"` ou `"definida"` (para altas). Uma vez processado, o status muda para `"Concluída"` ou `"concluida"`, impedindo novos registros em chamadas subsequentes.
