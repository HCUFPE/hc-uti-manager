# design.md — Versão 1.7.0 (Health Check, Versioning SSOT & Autorização Estrita AD)

## Context

O HC-UTI Manager é uma aplicação para governança e gestão de leitos de UTI no Hospital das Clínicas da UFPE (HC-UFPE / EBSERH). O sistema opera em arquitetura híbrida: FastAPI no backend, Vue 3 no frontend e integração de autenticação com o Active Directory institucional via LDAP.

Historicamente, três inconsistências arquiteturais se acumularam no projeto:
1. **Descentralização de versão:** O número de versão e metadados de identidade estavam espalhados e desincronizados entre `src/main.py` ("1.5.0"), `frontend/src/config/version.ts` ("1.6.1") e `frontend/package.json` ("1.6.1").
2. **Ausência de endpoint de telemetria e health check:** Não existia uma rota oficial `/api/health` para sondas de monitoramento (Kubernetes, Uptime Kuma, Zabbix) e para fornecer dados de versão em tempo de execução para clientes frontend e ferramentas de observabilidade.
3. **Brecha de autorização no login corporativo:** Ao autenticar com sucesso no Active Directory, caso o usuário não estivesse registrado na tabela local de perfis (`usuarios_perfis`), o backend atribuía silenciosamente o perfil "Comum", concedendo entrada ao sistema para qualquer colaborador do hospital. Além disso, a tela `AdminConfig.vue` permitia a adição de usuários com campos textuais soltos sem pré-validação no AD corporativo.

## Goals / Non-Goals

**Goals:**
- Centralizar o versionamento e identidade em `src/version.py` como Single Source of Truth (SSOT).
- Disponibilizar `GET /api/health` testando conexões de banco de dados (`app_db` SQLite local e `aghu_postgres` remoto) e retornando HTTP 200 (healthy) ou HTTP 503 (unhealthy).
- Fazer o frontend consumir `/api/health` dinamicamente na inicialização via store reativa Vue 3, mantendo fallbacks estáticos em caso de indisponibilidade da rede.
- Proteger a aplicação com autorização estrita: bloquear com HTTP 403 Forbidden qualquer autenticação válida no AD que não possua registro prévio em `usuarios_perfis` (com exceção de super administradores configurados).
- Expurgo total do perfil "Comum" legado em todas as camadas (backend, stores, componentes).
- Remodelar o modal de usuários em `AdminConfig.vue` para exigir busca e validação antecipada no AD corporativo (`/api/admin/ad-search/{login}`), exibindo banner informativo antes de habilitar o botão de salvamento.

**Non-Goals:**
- Alterar o protocolo de autenticação LDAP/AD existente (`auth_handler.py`).
- Modificar esquemas de tabelas ou migrações do banco SQLite (as colunas `nome_completo`, `lotacao` e `email` já existem em `usuarios_perfis`).
- Implementar gerenciamento granular de permissões por funcionalidade (mantém-se o modelo de perfis baseado em RBAC).

## Decisions

### 1. Single Source of Truth em `src/version.py`
- **Decisão:** Criar `src/version.py` contendo constantes globais (`VERSION = "1.7.0"`, `APP_NAME`, `SYSTEM_TITLE`, `LAST_UPDATE`, `ORGANIZATION`, `DEPARTMENT`).
- **Alternativa considerada:** Ler `package.json` ou usar variáveis de ambiente. Rejeitado porque a aplicação roda empacotada no backend Python/FastAPI e variáveis de ambiente não garantem atualização rastreável no controle de versão.

### 2. Monitoramento Ativo em `/api/health` com `SELECT 1`
- **Decisão:** O endpoint `/api/health` executa `SELECT 1` usando `async_session_maker` em `request.app.state.app_db` (banco essencial local) e checa `request.app.state.aghu_db` (banco secundário AGHU).
- **Tratamento de status:** Se `app_db` falhar, retorna HTTP 503 Service Unavailable e `"status": "unhealthy"`. Se `aghu_db` não estiver configurado ou estiver desabilitado, registra `"aghu_postgres": "disabled_or_not_configured"` sem derrubar a saúde essencial do app local, a menos que uma falha catastrófica ocorra.

### 3. Autorização Local Estrita (Bloqueio 403 para Não Autorizados)
- **Decisão:** No fluxo de login em `src/routers/auth.py`, após a validação bem-sucedida de credenciais pelo Active Directory:
  - Se `user["username"]` estiver na lista `SUPER_ADMINS` (`["admin", "daniel.turmina"]`), atribui perfil "Administrador".
  - Se existir registro em `UsuarioPerfil`, atribui `perfil_obj.perfil`. Se possuir flag `ativo == False`, bloqueia com 403.
  - Caso contrário (sem registro local), lança `HTTPException(status_code=403, detail="O usuário '...' é válido no Active Directory, mas não possui autorização de acesso neste sistema. Solicite o cadastro ao Administrador da UTI.")`.
- **Alternativa considerada:** Auto-provisionamento de perfil visitante/leitura. Rejeitado por determinação estrita de segurança institucional e governança de dados sensíveis de pacientes na UTI.

### 4. Remoção do Perfil "Comum"
- **Decisão:** Remover todas as ocorrências de "Comum" do enum de perfis atribuíveis (`authStore.getAssignableProfiles()`, `Role.COMUM` em `admin.py`), direcionando qualquer usuário para papéis específicos de setor (UTI, NIR, BC, COB, HEM e respectivos administradores) ou Administrador geral.

### 5. Pré-validação de Usuários no Frontend (`AdminConfig.vue`)
- **Decisão:** O modal de novo usuário exige consulta ativa no AD antes de salvar:
  - Botão principal da tela: `+ Novo Usuário`.
  - Input de login acompanhado de botão `🔍 Consultar AD` (e trigger no Enter).
  - Consulta ao endpoint existente `GET /api/admin/ad-search/{login}`.
  - Ao localizar, autopreenche `nome_completo`, `lotacao` e `email`, exibindo banner visual verde de confirmação.
  - Botão "Salvar Usuário" desabilitado se não houver validação prévia confirmada no AD (para novos usuários).

## Risks / Trade-offs

- **[Risco] Bloqueio inadvertido de colaboradores legítimos no login:** Usuários que antes acessavam com perfil "Comum" não conseguirão logar após a atualização.
  - *Mitigação:* Mensagem clara de erro 403 orientando a procurar o Administrador da UTI para cadastro prévio. Os super administradores (`admin`, `daniel.turmina`) estão protegidos por fallback de segurança.
- **[Risco] Latência na consulta `/api/health` durante alta carga:**
  - *Mitigação:* A consulta utiliza `SELECT 1` assíncrono leve e rápido, com timeout padrão do pool de conexões.
- **[Risco] Falha temporária no Active Directory ao tentar cadastrar novos usuários:**
  - *Mitigação:* O frontend captura erros de rede ou 404/500 do AD e exibe toast claro (`Usuário não localizado no Active Directory`), impedindo persistência de dados inconsistentes.

## Migration Plan

1. **Deploy da versão 1.7.0 no backend:** Criar `src/version.py`, criar `src/routers/health.py`, plugar em `src/main.py`, atualizar regras de login em `src/routers/auth.py` e `src/routers/admin.py`.
2. **Atualização do frontend:** Atualizar `frontend/src/config/version.ts`, `frontend/src/stores/auth.ts`, `frontend/src/views/AdminConfig.vue` e `frontend/package.json`.
3. **Build e Teste:** Executar `npm run build` no frontend para gerar os estáticos em `src/static/dist` e validar a inicialização da API.
4. **Sincronização de Especificações:** Atualizar `docs/projeto_inicial/02-requisitos.md`, `04-modelo-dados.md`, `05-interfaces.md` e `SPEC.md`.
