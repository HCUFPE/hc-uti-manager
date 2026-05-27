## Why

Quando um paciente tem sua cirurgia concluída pelo Bloco Cirúrgico, Hemodinâmica ou Centro Obstétrico, ele aguarda a liberação de encaminhamento pela equipe da UTI. Atualmente, o sistema não rastreia o tempo gasto nessa fila de espera, dificultando a análise de gargalos de transferência pós-operatória. Medir este tempo (do fim da cirurgia até a liberação de encaminhamento) e exibi-lo em tempo real (timer) e de forma consolidada (indicadores) é crucial para monitorar a eficiência operacional da UTI e da gestão de vagas.

## What Changes

- Modificar a tabela SQLite `solicitacoes_leito` para incluir duas novas colunas de controle de tempo: `cirurgia_finalizada_em` e `encaminhamento_liberado_em`.
- Backend:
  - Quando a cirurgia for finalizada, salvar o timestamp atual em `cirurgia_finalizada_em`.
  - Quando o encaminhamento for liberado pela UTI, salvar o timestamp em `encaminhamento_liberado_em`, calcular o tempo de liberação transcorrido em minutos e salvá-lo de forma textual no histórico de auditoria (ex: `[Tempo de Liberação: XX minutos]`).
  - Quando o encaminhamento for cancelado/revogado pela UTI, zerar o campo `encaminhamento_liberado_em`.
  - Atualizar o retorno de leitos (`listar_leitos`) para incluir o campo `cirurgia_finalizada_em` no objeto do próximo paciente.
  - Atualizar o endpoint de indicadores `/api/indicadores/resumo` para calcular a média desse tempo de espera (em minutos) para o período filtrado.
- Frontend:
  - No Painel de Leitos (`Home.vue` / `BedCard.vue`), quando houver reserva no status "Cirurgia Concluída", exibir um relógio (ícone `ClockIcon`) com um contador que atualiza a cada minuto mostrando o tempo decorrido (ex: `45m`, `1h 12m`) desde `cirurgia_finalizada_em`.
  - Na tela de Indicadores (`Indicadores.vue`), incluir um novo card na seção de tempos médios mostrando o "Tempo Médio de Liberação de Encaminhamento" da UTI formatado em horas e minutos.

## Capabilities

### New Capabilities

<!-- Nenhuma nova capacidade -->

### Modified Capabilities

- `solicitacao-leitos`: A solicitação de leito deve registrar e logar o tempo decorrido entre a conclusão cirúrgica e a liberação de encaminhamento pela UTI.
- `internacao-leitos`: O card de leito reservado com cirurgia concluída deve exibir visualmente um temporizador em execução.
- `indicadores-calculos`: O sistema deve calcular o tempo médio de liberação de encaminhamento para o painel de indicadores operacionais.

## Impact

- Banco de dados: Esquema `SolicitacaoLeito` (novos campos) e migração em `main.py` para garantir que as colunas existam.
- Backend: `src/controllers/solicitacao_leito_controller.py`, `src/controllers/leitos_controller.py`, `src/providers/implementations/indicadores_provider.py`.
- Frontend: `frontend/src/components/BedCard.vue`, `frontend/src/views/Indicadores.vue`, `frontend/src/views/Home.vue`.
