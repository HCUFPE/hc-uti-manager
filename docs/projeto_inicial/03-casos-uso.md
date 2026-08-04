# Modelagem de Casos de Uso — HC-UTI Manager

Este documento descreve os fluxos operacionais e os limites de ação de cada ator no sistema **HC-UTI Manager**.

---

## 1. Diagrama de Casos de Uso

```mermaid
flowchart LR
    %% Atores
    BC((Bloco Cirúrgico))
    UTI((Equipe da UTI))
    NIR((Regulação NIR))
    ADM((Gestor / Admin))
    
    subgraph "Painel HC-UTI Manager"
        UC1([UC001 - Criar Solicitação de Vaga])
        UC2([UC002 - Reservar Leito na UTI])
        UC3([UC003 - Realizar Troca de Paciente / Swap])
        UC4([UC004 - Solicitar Alta de Paciente])
        UC5([UC005 - Definir Leito de Destino])
        UC6([UC006 - Visualizar e Reconhecer Alertas])
        UC7([UC007 - Acompanhar KPIs e Indicadores])
    end
    
    %% Relacionamentos
    BC --- UC1
    BC --- UC2
    BC --- UC3
    BC --- UC6
    
    UTI --- UC2
    UTI --- UC4
    UTI --- UC6
    
    NIR --- UC5
    NIR --- UC6
    
    ADM --- UC7
```

---

## 2. Especificação dos Casos de Uso

### UC001 — Criar Solicitação de Vaga
*   **Ator Principal:** Bloco Cirúrgico (BC).
*   **Fluxo Principal:** 
    1. O usuário digita o número do prontuário do paciente cirúrgico.
    2. O sistema faz uma consulta em tempo real no banco do AGHU (Postgres) para verificar se há cirurgia agendada para hoje ou dias futuros.
    3. O sistema importa os dados (nome, idade, especialidade, procedimento, turno e horário).
    4. O usuário define o tipo de vaga, a prioridade inicial (P1 a P10) e clica em salvar.
    5. A solicitação entra na fila como **Pendente**.

### UC002 — Reservar Leito na UTI
*   **Atores:** Bloco Cirúrgico (BC) ou Equipe da UTI.
*   **Fluxo Principal:**
    1. O usuário visualiza o painel de leitos (Bed Cards) e identifica um leito vago (Disponível).
    2. O usuário seleciona uma solicitação de vaga ativa na fila e clica em **Reservar**.
    3. O sistema atualiza o status da solicitação para **Reservado**, preenche o destino (ex: *Leito 0502G*) e atualiza a reserva no banco SQLite (LeitoEstado).

### UC003 — Realizar Troca de Paciente (Swap)
*   **Ator Principal:** Bloco Cirúrgico (BC).
*   **Fluxo Principal:**
    1. O usuário edita uma solicitação existente e altera o prontuário para um novo paciente (substituição).
    2. O sistema valida se o novo paciente já possui solicitação ativa ou se ocupa leito físico na UTI.
    3. Caso o novo paciente já possua solicitação pendente no banco, o sistema executa a **Mesclagem Inteligente** (cancela a solicitação editada e transfere a reserva física/vaga para a solicitação existente do novo paciente).
    4. O sistema gera os logs adequados na auditoria e atualiza a fila de prioridades.

### UC004 — Solicitar Alta de Paciente
*   **Ator Principal:** Equipe da UTI.
*   **Fluxo Principal:**
    1. O médico ou enfermeiro da UTI entra no card do leito ocupado e clica em **Solicitar Alta**.
    2. O usuário preenche as necessidades especiais (oxigênio, isolamento, etc.) e confirma.
    3. O leito físico muda o status para **Alta** e envia uma notificação/alerta ao NIR.

### UC005 — Definir Leito de Destino
*   **Ator Principal:** Regulação NIR.
*   **Fluxo Principal:**
    1. O NIR visualiza no painel de Altas os leitos aguardando vaga de transferência.
    2. O usuário entra no leito e registra qual enfermaria de destino receberá o paciente.
    3. Ao confirmar a transferência, o leito da UTI é liberado física e sistemicamente (entra no status de *Higienização*).

### UC006 — Visualizar e Reconhecer Alertas
*   **Atores:** UTI, NIR ou Bloco Cirúrgico.
*   **Fluxo Principal:**
    1. O usuário visualiza alertas não lidos específicos para o seu perfil no painel.
    2. Ao tomar conhecimento do alerta, o usuário clica em **Ciente** para arquivar a notificação, registrando quem leu e o timestamp.

---

## 3. Detalhamento SDD (CARE)

### [CARE-UC003] Realizar Troca de Paciente (Swap)
*   **Context:** Uma solicitação `#A` está ativa no banco. O usuário decide editá-la e alterar o prontuário para um paciente `#B`.
*   **Action:** O backend verifica se `#B` já tem solicitação ativa. Se sim, reatribui a reserva de leito (SQLite `leito_estados` e `solicitacoes_leito.destino`) para `#B`, cancela a solicitação `#A` com a justificativa de mesclagem e gera logs detalhados de auditoria.
*   **Result:** A substituição é refletida de forma transparente no painel e na fila, evitando duplicar o paciente `#B` no painel.
*   **Evaluation:** Verificação via testes de integração simulando a rota de edição de prontuários com e sem reserva prévia.

### [CARE-UC006] Tratamento Concorrente de Alertas
*   **Context:** Diversos componentes do frontend disparam requisições paralelas para gerar alertas ao mesmo tempo durante o boot da aplicação.
*   **Action:** Envolver o motor de sincronização no `AlertaController.gerar_alertas()` usando um `asyncio.Lock()` global.
*   **Result:** Execução estritamente serial das requisições. A segunda requisição aguarda a primeira gravar no banco, prevenindo a inserção de registros duplicados para o mesmo evento de histórico.
*   **Evaluation:** Ausência de alertas com mesmo timestamp e dados idênticos para o mesmo log de histórico na base local da VM.
