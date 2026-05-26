## Why

Este documento propõe alterações no sistema de gerenciamento de UTI para:
1. Permitir que todos os usuários com perfil de administrador setorial (`*-Admin`, como `BC-Admin`, `COB-Admin`, `HEM-Admin`, `NIR-Admin` e `UTI-Admin`) tenham acesso às telas de Histórico de Ações e Indicadores, permitindo melhor acompanhamento de auditoria e métricas gerenciais sem necessitar do perfil de Administrador Geral.
2. Garantir que todas as ações críticas dos usuários (incluindo conclusão de admissões na UTI e saídas de alta registradas via censo/leitos) sejam corretamente registradas na tabela de histórico de ações (`historico_acoes`).
3. Introduzir um conjunto robusto de novos indicadores operacionais e clínicos para monitorar o fluxo da UTI, tempo de permanência, tempo de espera por leito, taxas de atendimento e cancelamento de solicitações, entre outros, com a capacidade de filtrar dinamicamente por período de datas na interface do usuário.

## What Changes

- **Acesso ao Menu**: Liberação do acesso às rotas e menus de `"Histórico"` e `"Indicadores"` para usuários com perfis cujo nome termina em `-Admin` (ex: `BC-Admin`, `COB-Admin`, `HEM-Admin`, `NIR-Admin`, `UTI-Admin`), além do perfil `"Administrador"` (ou `"admin"`).
- **Auditoria de Histórico Completa**:
  - Registro de evento de histórico `conclusao` quando um paciente ocupa fisicamente o leito reservado (durante a sincronização do censo/leitos).
  - Registro de evento de histórico `conclusao_alta` quando um paciente com alta ativa deixa o leito de UTI.
- **Novos Indicadores**:
  - Número médio semanal de novas internações na UTI (geral, por demandante: BC, HEM, COB, CLI, e por especialidade).
  - Tempo médio de ocupação de um leito de UTI (geral, por demandante: BC, HEM, COB, CLI, e por especialidade).
  - Taxa de atendimento de solicitações de vaga de UTI.
  - Taxa de cancelamento de solicitações de vaga de UTI.
  - Tempo médio de solicitação de vaga de UTI (tempo entre a data/hora da solicitação e o momento da ocupação física).
  - Horário médio de reserva de leito para os pacientes do turno (manhã e tarde).
  - Tempo médio de recepção do paciente após fim cirúrgico (tempo entre a prontidão cirúrgica e a entrada física na UTI).
  - Tempo médio de acomodação de alta (tempo entre o pedido de alta pela UTI e a indicação de leito pós-UTI pelo NIR).
  - Tempo médio de liberação do leito de acomodação pós-UTI (tempo entre a indicação do leito pós-UTI e a efetiva liberação/conclusão da alta).
  - Métricas de volume: solicitações totais, reservadas, concluídas, cancelamentos de solicitações, cancelamentos de reservas, altas e percentuais de relação.
- **Filtro de Período**: Adição de campos de data de início (`data_inicio`) e data de fim (`data_fim`) na tela de indicadores, que serão transmitidos aos novos endpoints do backend para recalculá-los dinamicamente.

## Capabilities

### New Capabilities
- `indicadores-calculos`: Cálculo de novos indicadores clínicos e operacionais na UTI com filtros por período.

### Modified Capabilities
- `bi-dashboard`: Inclusão de novos indicadores e liberação do acesso para perfis do tipo `*-Admin`.
- `solicitacao-leitos`: Garantia de auditoria completa no histórico de ações (logar conclusão de solicitações e alta no censo).

## Impact

- **Backend**:
  - `src/routers/historico.py` e `src/routers/indicadores.py`: Atualização do controle de acesso para perfis `*-Admin`.
  - `src/dependencies.py`: Atualização das funções de validação de papéis se houver validação centralizada.
  - `src/controllers/leitos_controller.py`: Registro dos logs de histórico `conclusao` (admissão) e `conclusao_alta` (conclusão de alta no censo).
  - `src/controllers/indicadores_controller.py`: Implementação dos novos cálculos, incluindo parâmetros de data de início e fim.
  - `src/providers/implementations/indicadores_provider.py` (ou correspondente): Desenvolvimento das consultas e lógica para computar os novos indicadores de tempos médios e taxas a partir do histórico de ações.
- **Frontend**:
  - `frontend/src/views/Indicadores.vue`: Novo painel de métricas com filtros de período, novos gráficos, cards de tempo médio e taxas de cancelamento/atendimento.
  - `frontend/src/components/Sidebar.vue` (ou local correspondente): Ajustar visibilidade dos itens de menu "Histórico" e "Indicadores" para perfis `*-Admin`.
