# 📜 CHANGELOG — Histórico Oficial de Versões e Entregas

Este documento mantém o histórico público, auditável e imutável de todas as versões e atualizações do **HC-UTI Manager** (Hospital das Clínicas da UFPE / EBSERH / SETISD).

> 🚨 **REGRA DE GOVERNANÇA (OBRIGATÓRIA):**
> Toda e qualquer nova versão ou alteração no código do sistema — **por menor que seja (Minor, Patch, Bugfix, Refatoração de UI ou Ajuste de Segurança)** — DEVE obrigatoriamente registrar uma nova entrada neste arquivo `CHANGELOG.md` e atualizar o timestamp em `src/version.py` e `docs/projeto_inicial/SPEC.md`.

---

## [Unreleased]

### A Fazer / Em Planejamento
- Propostas de melhorias contínuas registradas via OpenSpec (`openspec/changes/`).

---

## [1.7.1] - 2026-09-17

### Corrigido (Fixed) & Ajustado (Adjusted)
- **Supressão de Toast Fantasma no Redirecionamento 401**: Ajustado o tratamento de exceção em `Home.vue` (`loadLeitos`) para ignorar erros HTTP `401 Unauthorized` ou quando o usuário não estiver autenticado. Isso impede que o alerta vermelho "Falha ao carregar leitos. Verifique a conexao." seja exibido indevidamente sobre a tela de login durante o redirecionamento automático de sessão expirada.
- **Duração do Token de Acesso ("Lembrar de Mim")**: Ajustado em `src/routers/auth.py` para que credenciais que marquem a opção "Lembrar de mim" no login emitam token JWT válido por **7 dias** (168 horas), mantendo **24 horas** no login padrão sem a opção marcada.
- **Bump de Versão SSOT**: Versão atualizada para `1.7.1` em `src/version.py` e `frontend/package.json`.

---

## [1.7.0] - 2026-09-15

### Adicionado (Added) & Segurança
- **Security Headers HTTP**: Adição de middleware global `@app.middleware("http")` em `src/main.py` injetando os cabeçalhos `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection`, `Cache-Control: no-store, no-cache` e `Pragma: no-cache` para total alinhamento com o Framework SETISD.
- **Proteção Estrita na Consulta de Leitos**: Exigência de autenticação JWT (`Depends(auth_handler.decode_token)`) nas rotas `GET /api/leitos` e `GET /api/leitos/disponiveis` para bloquear acessos anônimos (retornando `401 Unauthorized`).
- **SSOT de Versão**: Centralização da versão e identidade do sistema no backend (`src/version.py`) consumida dinamicamente pelo Swagger e pela store reativa no frontend (`frontend/src/config/version.ts`).
- **Endpoint de Telemetria (`GET /api/health`)**: Exposição de dados institucionais, versão e status de conexão dos bancos `app_db` (SQLite) e `aghu_postgres` (PostgreSQL).
- **Validação de Usuários no AD**: Remodelação da interface `AdminConfig.vue` com consulta e pré-validação no Active Directory corporativo Ebserh antes de salvar perfis no banco local.

### Removido (Removed)
- Expurgo do comentário legado de versão do topo de `src/main.py`.

---

## [1.6.1] - 2026-09-01

### Adicionado (Added)
- **Alertas Sonoros de Admissão Concluída (NIR)**: Som melódico sintetizado via Web Audio API (escala C-E-G) acionado dinamicamente para o grupo NIR ao confirmar a admissão no AGHU.
- **Especialidade nas Altas**: Exibição da especialidade clínica do paciente na aba de solicitações de alta médica (`Altas.vue`).

---

## [1.6.0] - 2026-08-26

### Adicionado (Added)
- **Passagem de Caso Clínica Obrigatória**: Modal de preenchimento obrigatório de informações anestésico-cirúrgicas no Bloco Cirúrgico e modal de Checkpoint visual na UTI antes de liberar o transporte do paciente.
- **Modo TV**: Interface otimizada em tela cheia com auto-scroll contínuo para exibição em monitores de parede nos plantões de regulação.
- **Controle Global de Som**: Alternância Mute/Unmute no topo da interface.

### Corrigido (Fixed)
- **Trava de Concorrência**: Implementação de `double-checked locking` no banco de dados para evitar registros duplicados em execuções concorrentes de autolimpeza de leitos.

---

## [1.5.0] - 2026-08-17

### Adicionado (Added)
- **Reserva Preventiva (Clínico/COB/HEM)**: Funcionalidade para reservar leitos preventivamente para demandas clínicas urgentes, com autolimpeza via censo do AGHU e transferência automática em caso de swap de leitos.
- **Substituição de Leitos Reservados**: Permite a troca (swap) entre leitos mesmo quando um dos leitos possui reserva física ativa.

---

## [1.4.12] - 2026-08-15

### Adicionado (Added)
- **Métrica de Tempo de Encaminhamento**: Exibição no dashboard do tempo médio entre a liberação do encaminhamento pelo Bloco Cirúrgico e a admissão na UTI.
- **Acesso Ampliado**: Liberação de navegação nas telas de Indicadores e Histórico para todos os perfis autenticados.

---

## [1.4.10] - 2026-08-12

### Melhores (Changed)
- **Auditoria de Alertas**: Registro do usuário específico que visualizou e deu ciência no popover de alertas.

---

## [1.4.9] - 2026-08-10

### Corrigido (Fixed)
- **Alertas do NIR**: Ajustes no fluxo de popover e notificações do Núcleo Interno de Regulação.

---

## [1.4.8] - 2026-08-08

### Melhores (Changed)
- **Tela de Login**: Inclusão de marcas d'água corporativas (HC-UFPE / Ebserh), suporte a acentuação e mensagens de erro amigáveis.

---

## [1.4.7] - 2026-08-05

### Corrigido (Fixed)
- **Histórico de Auditoria**: Ajuste no registro de detalhes de prontuários em alterações de reservas.

---

## [1.4.6] - 2026-08-02

### Adicionado (Added)
- **Reatribuição de Destino pelo NIR**: Permite ao regulador do NIR alterar o leito de enfermaria de destino de altas a qualquer momento antes da saída física.

---

## [1.4.5] - 2026-07-30

### Corrigido (Fixed)
- **Conclusão de Solicitações**: Correção no fluxo de encerramento automático quando o censo do AGHU detecta ocupação.

---

## [1.4.4] - 2026-07-27

### Adicionado (Added)
- **Alerta UTI -> Cirurgia**: Notificação temporária quando uma solicitação da fila é criada para um paciente que já ocupa leito na UTI.

---

## [1.4.3] - 2026-07-24

### Adicionado (Added)
- **Alerta Sonoro do NIR**: Bipe sonoro configurável para pendências de regulação de leitos.

---

## [1.4.2] - 2026-07-20

### Corrigido (Fixed)
- **Filtros do Histórico**: Correção no agrupamento de sub-tipos de ação ao filtrar por altas e destinos de leito.

---

## [1.4.1] - 2026-07-18

### Corrigido (Fixed)
- **Pesquisa no Histórico**: Ajuste na busca por palavra-chave e ordenação cronológica das ações.

---

## [1.4.0] - 2026-07-15

### Adicionado (Added)
- **Validação de Cirurgia Agendada**: Bloqueio de novas solicitações para pacientes sem cirurgia futura agendada no AGHU.
- **Motivos de Cancelamento**: Reajuste nos motivos automatizados de expiração e cancelamento de solicitações.

---

## [1.3.0] - 2026-07-10

### Adicionado (Added)
- **Métrica de Higienização**: Indicador de tempo médio de higienização de leitos a partir dos extratos do AGHU.
- **Prevenção de Duplicidades**: Bloqueio contra solicitações de alta duplicadas para o mesmo prontuário.
- **Novo Motivo de Cancelamento**: Inclusão formal da opção "Paciente já na UTI".

---

## [1.2.0] - 2026-06-28

### Adicionado (Added)
- **Seleção Inteligente de Cirurgias**: Ordenação no banco PostgreSQL para selecionar a cirurgia agendada mais próxima (`obter_cirurgia_aghu.sql`).
- **Edição de Prontuário**: Opção para cancelar ou manter a solicitação antiga pendente ao editar o prontuário.

---

## [1.1.0] - 2026-06-15

### Adicionado (Added)
- **Login Case-Insensitive**: Suporte para ignorar maiúsculas/minúsculas na autenticação LDAP do Active Directory.
- **Sinais Sonoros da UTI**: Bipes sonoros em loop para solicitações de prioridade urgente.

---

## [1.0.2] - 2026-06-05

### Adicionado (Added)
- **Gráficos e KPIs**: Visualização de distribuição por especialidade e razões de cancelamento no dashboard.

---

## [1.0.1] - 2026-06-02

### Melhores (Changed)
- **Fila Dinâmica P1 a P10**: Ajuste no algoritmo de pontuação e priorização manual da fila de leitos.

---

## [1.0.0] - 2026-06-01

### Release Inicial
- Sistema base **HC UTI Manager** entregue e implantado (FastAPI + Vue 3 + AGHU + Podman + Nginx + Systemd).
