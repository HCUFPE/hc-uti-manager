# Arquitetura e Segurança — HC-UTI Manager

Este documento define a infraestrutura tecnológica do **HC-UTI Manager**, descrevendo a stack técnica, o modelo de segurança e as diretrizes de desenvolvimento (guardrails).

---

## 1. Stack Técnica e Arquitetura de Implantação

O sistema adota uma arquitetura em microsserviços simples e isolada por containers rootless, conforme descrito a seguir:

*   **Frontend:** Vue.js 3, Single Page Application (SPA), estilizado em Vanilla CSS estruturado. O build estático final (HTML/JS/CSS) é compilado e servido de forma otimizada.
*   **Backend:** Python 3.10+, FastAPI (framework assíncrono), SQLAlchemy (ORM assíncrono com `aiosqlite` e `asyncpg`) e Alembic para gerenciamento de migrações estruturais do banco de dados.
*   **Bancos de Dados:**
    *   *SQLite (`app.db`):* Banco de dados local persistente de alta velocidade para dados de fila, reservas de leito, alertas e auditoria.
    *   *PostgreSQL (AGHU):* Banco de dados legad/hospitalar externo consultado via conexão segura somente-leitura.
*   **Servidor Web e Proxy:** Nginx configurado com certificados SSL autoassinados/corporativos, redirecionando tráfego HTTP (porta 80) para HTTPS (porta 443) e atuando como proxy reverso para o backend FastAPI.
*   **Infraestrutura de Servidor (VM):** OS Linux Debian/Ubuntu rodando Podman e Podman-Compose em nível de usuário administrador (rootless). A orquestração do container é monitorada pelo systemd do host.

---

## 2. Autenticação e Autorização (Controle de Acessos - RBAC)

O sistema implementa autenticação integrada e controle de permissões baseada no perfil do usuário:

*   **Provedor de Identidade:** Active Directory via protocolo LDAP.
*   **Estratégia de Sessão (Tokens Híbridos):**
    *   *Access Token:* JWT de curta duração (ex: 15 minutos) armazenado em memória no frontend.
    *   *Refresh Token:* Armazenado localmente em banco de dados SQLite e enviado ao cliente através de um cookie seguro `HttpOnly`, `Secure` e `SameSite=Strict` para renovação transparente de sessão.
*   **Perfis de Acesso (RBAC):**
    *   *Administrador:* Acesso total às configurações do sistema, visualização de KPIs históricos e auditoria de ações.
    *   *Equipe da UTI (Médico/Enfermeiro):* Permissão de ler censo, solicitar alta de paciente de leito e reservar vagas.
    *   *Bloco Cirúrgico (BC / Solicitantes):* Permissão de criar solicitações de vagas, reordenar a prioridade da fila (P1 a P10) e realizar trocas de prontuário (Swap).
    *   *Regulação NIR:* Permissão exclusiva para visualizar altas da UTI e definir o destino final de enfermaria do paciente.

---

## 3. Conformidade LGPD e Rastreabilidade

*   **Log de Auditoria Inalterável:** A tabela `historico_acoes` registra toda e qualquer inserção, edição ou exclusão de solicitações e reservas de leito, indicando o operador responsável, o prontuário do paciente, o timestamp exato e o detalhe do valor alterado.
*   **Exclusão Lógica e Histórico:** O sistema não realiza a exclusão direta de logs de histórico de ações (tabela append-only). O cancelamento de solicitações inativa o registro lógico de fila, mas preserva o dado para conformidade regulatória.
*   **Tratamento Concorrente Seguro:** Processamento atômico garantido por locks concorrentes assíncronos no motor de alertas, impedindo que requisições paralelas gerem duplicidades de dados sensíveis de pacientes.

---

## 4. Guardrails de Desenvolvimento (Anti-Patterns)

Para manter a integridade do código e a robustez sistêmica, qualquer modificação na base de código deve respeitar os seguintes limites:

### Escopo Positivo (Boas Práticas obrigatórias)
*   **Segurança de Segredos:** Todas as chaves JWT, credenciais LDAP, DSNs de bancos de dados PostgreSQL e caminhos SQLite devem ser lidos obrigatoriamente de variáveis de ambiente (`.env`).
*   **Tratamento Assíncrono:** Todas as rotas de banco de dados e provedores externos de rede (LDAP e AGHU) devem ser declaradas como assíncronas (`async/await`) para evitar bloqueio da thread principal do FastAPI.
*   **Migrações estruturais:** Alterações no banco de dados SQLite local devem ser versionadas utilizando arquivos de migração gerados pelo Alembic (`alembic revision --autogenerate`).

### Escopo Negativo (Práticas Proibidas)
*   **Proibido Escrita no AGHU:** A conexão com o banco do AGHU é estritamente de consulta (`SELECT`). É proibida qualquer operação de escrita (`INSERT`/`UPDATE`) no banco PostgreSQL hospitalar.
*   **Proibido Segredos Hardcoded:** Nunca salvar senhas de testes ou chaves simétricas de criptografia diretamente no repositório Git.
*   **Proibido Concorrência sem Lock nos Alertas:** Qualquer rota ou motor que manipule a criação de alertas ou status concorrentes do censo físico de leitos deve utilizar o `asyncio.Lock()` do respectivo controller.