## Goals / Non-Goals

**Goals:**
- Separar o tipo de evento de histórico para cancelamento de reservas iniciado pelo solicitante (Bloco) versus a própria UTI.
- Exibir essas contagens de forma segmentada no dashboard de indicadores.

## Decisions

### 1. Histórico e Controller (`src/controllers/solicitacao_leito_controller.py`)
- Na função de troca de paciente, identificar se a ação de cancelamento foi por troca de paciente e registrar no histórico com:
  - `tipo = "cancelamento_solicitante"`
  - `acao = "Cancelou reserva de leito (Troca de Paciente)"`
  - Refrasear as mensagens de log no banco para:
    - Paciente A (antigo): `"Solicitação #{sol_id} (Paciente A) voltou para a fila (Pendente). Motivo: Leito {alvo_destino_orig} foi remanejado para o Paciente B (Prontuário {nova_sol.prontuario}) via troca de paciente."`
    - Paciente B (novo): `"Solicitação #{nova_sol.id} (Paciente B) foi reservada para o Leito {alvo_destino_orig}. Motivo: Recebeu a vaga do Paciente A (Prontuário {alvo.prontuario}) via troca de paciente."`

### 1b. Motor de Alertas (`src/controllers/alerta_controller.py`)
- Atualizar a verificação de eventos de histórico de cancelamento. Se `tipo == "cancelamento_solicitante"`:
  - Se a ação contiver `"Troca de Paciente"`:
    - `titulo = "Reserva Remanejada (Troca de Paciente)"`
  - Caso contrário:
    - `titulo = "Reserva Cancelada pelo Solicitante"`
  - Tipo do alerta: `"aviso"`.
  - Destinatário: NIR / UTI.

### 2. Provedor de Indicadores (`src/providers/implementations/indicadores_provider.py`)
- Em `obter_resumo_indicadores`, carregar separadamente:
  - `cancelamentos_res_uti_periodo` = eventos com `tipo == "cancelamento_reserva"`.
  - `cancelamentos_res_sol_periodo` = eventos com `tipo == "cancelamento_solicitante"`.
- Adicionar ao dicionário `volumes` de retorno:
  ```python
  "cancelamento_reservas_uti": len(cancelamentos_res_uti_periodo),
  "cancelamento_reservas_solicitante": len(cancelamentos_res_sol_periodo),
  ```

### 3. Frontend (`frontend/src/views/Indicadores.vue`)
- Modificar o Quadro 2 para exibir:
  - Linha 1: `Reservas Canceladas pela UTI` -> `detalhado.volumes?.cancelamento_reservas_uti ?? 0`
  - Linha 2: `Reservas Canceladas pelo Solicitante` -> `detalhado.volumes?.cancelamento_reservas_solicitante ?? 0`
