## Context

Para atender à necessidade de bloquear leitos preventivamente para os setores Clínico/COB/HEM de forma genérica, este design propõe a adição de uma coluna booleana `bloqueado_clinico` na tabela `leito_estados` do banco local SQLite e os controles necessários para gerenciar esse estado.

## Goals / Non-Goals

**Goals:**
- Permitir o bloqueio genérico de leitos via painel.
- Ocultar leitos bloqueados na listagem de vagas elegíveis para cirurgias gerais (BC).
- Executar o "swap" de bloqueio na alteração de leito (remanejamento).
- Realizar o auto-desbloqueio quando o censo detectar ocupação.
- Atualizar a versão do sistema global para `1.5.0`.

**Non-Goals:**
- Criar fluxos de priorização para os leitos de clínica (bloqueio puramente binário/visual).

## Decisions

### 1. Modelo de Dados (SQLite)
A tabela `leito_estados` persistirá a flag booleana `bloqueado_clinico`.
*   Uma nova migração do Alembic será criada em `alembic/versions/` para adicionar a coluna com `default=False`.
*   O modelo SQLAlchemy `LeitoEstado` em `src/models/leito_estado.py` receberá:
    `bloqueado_clinico = Column(Boolean, default=False)`

### 2. Endpoints e Lógica de Swap
- **`POST /api/leitos/{lto_id}/bloquear-clinico`**
- **`POST /api/leitos/{lto_id}/cancelar-reserva-clinica`**
- Na controller `solicitacao_leito_controller.py`, o método `remanejar_reserva` será alterado para interceptar se o leito destino possui `bloqueado_clinico == True`. Caso afirmativo:
  1. O leito de destino perde a flag.
  2. O leito de origem (que ficou vago) ganha a flag `bloqueado_clinico = True`.

### 3. Histórico de Auditoria (Logs)
Sempre que a reserva clínica for modificada, os seguintes logs devem ser registrados em `HistoricoAcao` (persistidos em SQLite), mantendo total consistência com as tabelas existentes:

- **Bloqueio Clínico Manual (Reserva Clínica):** 
  - `tipo`: `"reserva"`
  - `acao`: `"Reservou leito para Clínico/COB/HEM"`
  - `detalhes`: `"Leito {lto_id} reservado preventivamente para Clínico/COB/HEM."`
  - `prontuario`: `None` (ou string `"Clínico"`)
- **Cancelamento Manual de Reserva Clínica:**
  - `tipo`: `"cancelamento_reserva"`
  - `acao`: `"Cancelou reserva de leito (Clínico/COB/HEM)"`
  - `detalhes`: `"Reserva do leito {lto_id} para Clínico/COB/HEM cancelada manualmente pelo operador."`
  - `prontuario`: `None` (ou string `"Clínico"`)
- **Swap de Reserva no Remanejamento (UTI move o Paciente A para o leito bloqueado Y):**
  - O sistema registrará os seguintes logs de tipo `remanejamento_reserva` na rota do router:
    - **Para o Paciente A (Prontuário `pront_paciente`):**
      - `tipo`: `"remanejamento_reserva"`
      - `acao`: `"Remanejou reserva (Troca)"`
      - `detalhes`: `"Reserva trocada com Clínico/COB/HEM: transferida do Leito {leito_origem} para o Leito {leito_destino}."`
      - `prontuario`: `{pront_paciente}`
    - **Para o Leito X que herda o bloqueio (Prontuário nulo/Clínico):**
      - `tipo`: `"remanejamento_reserva"`
      - `acao`: `"Remanejou reserva (Troca)"`
      - `detalhes`: `"Reserva do Clínico/COB/HEM trocada com Prontuário {pront_paciente}: transferida do Leito {leito_destino} para o Leito {leito_origem}."`
      - `prontuario`: `None`
- **Auto-limpeza pelo Censo (Admissão física):**
  - `tipo`: `"cancelamento_reserva"`
  - `acao`: `"Cancelou reserva de leito (Clínico/COB/HEM) - Auto-limpeza via censo"`
  - `detalhes`: `"Reserva preventiva do leito {lto_id} limpa automaticamente devido à ocupação física do leito pelo prontuário {prontuario}."`
  - `prontuario`: `None`

### 4. Impacto nos Alertas
- **Bloqueio Clínico em si:** Não gera alertas ativos (piscadas ou sons) no painel. O motor de alertas (`AlertaController`) exige um perfil solicitante associado (`perfil_vaga`) para disparar avisos de reservas ou cancelamentos. Como a reserva clínica não tem solicitação correspondente, `perfil_vaga` é `None` e o disparo de alertas é ignorado de forma natural.
- **Transição de Alertas do Paciente no Swap:**
  - Ao executar o Swap de Remanejamento, a reserva do paciente (e a referência de `solicitacao_id` no banco local) é transferida para o novo leito físico.
  - O motor de alertas do backend e o frontend herdam e movem automaticamente os alertas associados àquele paciente (ex: alerta de "cirurgia finalizada") para o novo leito físico.

### 5. Proteção de Indicadores do BI (Evitar Poluição de Métricas)
Para garantir que as ações da reserva clínica genérica (que não possuem prontuário de paciente real) não distorçam as estatísticas de volume de reservas e taxa de cancelamentos no BI Dashboard, os seguintes ajustes MUST ser feitos em [indicadores_provider.py](file:///c:/Users/daniel.turmina/Documents/HC-uti-manager/src/providers/implementations/indicadores_provider.py):
- Ajustar a seleção de `reservas_efetuadas_periodo` para filtrar `ev.prontuario` (garantindo que só eventos com prontuário de paciente real sejam computados).
- Ajustar a seleção de `cancelamentos_res_uti_periodo` para filtrar `ev.prontuario` (desconsiderando cancelamentos de reservas genéricas do Clínico/COB/HEM).

---

## 🧪 Plano de Testes (Versão 1.5.0)

Para homologar a versão `1.5.0`, deverão ser criados os seguintes casos de teste automatizados em Python:

### 1. Testes de Integração Backend (FastAPI / pytest)

*   **`test_bloqueio_desbloqueio_clinico`:**
    *   *Ação:* Disparar chamadas HTTP para os novos endpoints de bloqueio e cancelamento.
    *   *Validação:* Verificar se a coluna `bloqueado_clinico` muda de estado no banco e se uma ação de histórico correspondente é criada.
*   **`test_filtragem_leitos_disponiveis`:**
    *   *Ação:* Bloquear o leito "UTI-01" (`bloqueado_clinico = True`) e solicitar a listagem de leitos disponíveis para uma reserva cirúrgica comum.
    *   *Validação:* Garantir que "UTI-01" não consta na lista de leitos retornados como livres.
*   **`test_swap_bloqueio_remanejamento`:**
    *   *Ação:* Criar paciente reservado no leito "UTI-02". Bloquear o leito "UTI-03" para clínica. Chamar a rota de remanejamento para mover o paciente de "UTI-02" para "UTI-03".
    *   *Validação:* Garantir que:
        - O paciente agora está associado ao leito "UTI-03" (e "UTI-03" teve `bloqueado_clinico` desativado).
        - O leito "UTI-02" (origem) passou a ter `bloqueado_clinico = True`.
*   **`test_censo_limpeza_automatica_bloqueio`:**
    *   *Ação:* Definir `bloqueado_clinico = True` no leito "UTI-04". Simular a leitura do censo do AGHU onde "UTI-04" consta como "Ocupado".
    *   *Validação:* Verificar se o processo do Censo limpa a flag `bloqueado_clinico` para `False`.

### 2. Testes de Interface (Manual/Frontend)
*   **Visualização:** Checar se o BedCard exibe o aviso "Reservado p/ Clínico/COB/HEM" de forma legível e com bom contraste.
*   **Troca de Tela:** Garantir que o botão "Mudar Leito" no card de reserva do paciente consiga exibir os leitos bloqueados para clínica como opção de transferência (uma vez que a troca de leitos permite o swap).
