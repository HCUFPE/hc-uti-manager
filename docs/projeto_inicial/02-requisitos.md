# Especificação de Requisitos — HC-UTI Manager

Este documento detalha os requisitos funcionais (RF) e requisitos não funcionais (RNF) do sistema **HC-UTI Manager**, garantindo o mapeamento de sua entrega técnica.

---

## 1. Requisitos Funcionais (RF)

| ID | Título | Descrição | Nível de Importância |
| :--- | :--- | :--- | :--- |
| **RF001** | Autenticação Híbrida | Login integrado via LDAP/Active Directory corporativo (Ebserh) com fallback automático para Mock offline em desenvolvimento. | Essencial |
| **RF002** | Integração AGHU | Importação e sincronização em tempo real de pacientes e cirurgias agendadas a partir do banco de dados oficial (PostgreSQL). | Essencial |
| **RF003** | Fila Dinâmica de Vagas | Fila sequencial e automática de solicitações de leito ordenada por prioridade (P1 a P10) e cronologicamente. | Essencial |
| **RF004** | Censo de Leitos (Bed Cards) | Painel visual dinâmico com cards para cada leito da UTI (mostrando ocupante atual, alta solicitada ou próxima reserva). | Essencial |
| **RF005** | Reserva de Leitos | Vinculação de uma solicitação de vaga pendente a um leito físico disponível, atualizando o status para "Reservado". | Essencial |
| **RF006** | Troca de Pacientes (Swap) | Substituição de um paciente na fila por outro, transferindo a reserva física e cancelando a solicitação antiga para evitar duplicidades. | Essencial |
| **RF007** | Regulação de Destinos (NIR) | Gestão de pacientes de alta da UTI, permitindo ao NIR definir e registrar o leito de enfermaria de destino (liberando a vaga na UTI). | Essencial |
| **RF008** | Alertas em Tempo Real | Geração de alertas visuais/sonoros para o painel (altas pendentes, novas solicitações do dia, reservas e cancelamentos do solicitante). | Essencial |
| **RF009** | Histórico de Auditoria | Log cronológico inalterável de todas as ações de usuários (ação, operador, detalhes, prontuário e timestamp). | Essencial |
| **RF010** | KPIs e Indicadores | Dashboard com taxas de ocupação, total de admissões e segmentação de cancelamentos (separando os provocados pela UTI dos causados pelo Bloco). | Desejável |

---

## 2. Requisitos Não Funcionais (RNF)

| ID | Categoria | Descrição |
| :--- | :--- | :--- |
| **RNF001** | Arquitetura | Arquitetura desacoplada em camadas utilizando Injeção de Dependências no FastAPI (Roteador -> Controller -> Provedor). |
| **RNF002** | Banco de Dados Híbrido | Operação simultânea com PostgreSQL (leitura remota do AGHU) e SQLite (gravação rápida de estado local e auditoria). |
| **RNF003** | Concorrência | Proteção de concorrência e condições de corrida no motor de alertas utilizando Lock assíncrono (`asyncio.Lock`). |
| **RNF004** | Segurança de Sessão | Autenticação baseada em Access Token (JWT em memória) e Refresh Token (armazenado em cookie seguro `HttpOnly`). |
| **RNF005** | Resiliência e Infra | Deploy via Podman Compose gerenciado como serviço systemd de inicialização automática na VM. |
| **RNF006** | Manutenibilidade | Rotinas automáticas de backup diário rotativo do banco SQLite e limpeza de logs do journald/Podman. |

---

## 3. Detalhamento SDD (CARE)

Abaixo está o detalhamento estruturado de requisitos operacionais críticos do sistema:

### [CARE-RF006] Troca de Pacientes (Mesclagem Inteligente)
*   **Context (Contexto):** O Bloco Cirúrgico edita uma solicitação e altera o prontuário para um novo paciente.
*   **Action (Ação):** O sistema verifica se o paciente de destino já possui solicitação ativa. Se possuir, cancela a solicitação de origem e mescla o estado (se houver reserva ativa de leito, transfere os dados da reserva física para a solicitação preexistente).
*   **Result (Resultado):** O censo local de leitos e o histórico de auditoria refletem a substituição sem criar registros duplicados ou leitos fantasmas.
*   **Evaluation (Avaliação):** Validação de integridade nos logs gerados no histórico de ações.

### [CARE-RNF003] Proteção de Concorrência de Alertas
*   **Context (Contexto):** Múltiplos componentes do frontend disparam requisições paralelas para `/api/alertas/gerar` no milissegundo de carregamento da tela.
*   **Action (Ação):** Implementar um semáforo de concorrência com `asyncio.Lock()` no ciclo de execução do `AlertaController.gerar_alertas()`.
*   **Result (Resultado):** As requisições rodam de forma estritamente sequencial. A segunda requisição lê o banco após o commit da primeira e identifica que o alerta já existe, impedindo duplicidades.
*   **Evaluation (Avaliação):** Zeramento de alertas com mesmo timestamp de criação e IDs duplicados para o mesmo evento de histórico.