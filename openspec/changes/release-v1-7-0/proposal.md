# proposal.md

## Why

Atualmente no HC-UTI Manager, o versionamento do sistema está fragmentado e descentralizado em três pontos distintos (`src/main.py` fixado em 1.5.0, `frontend/src/config/version.ts` em 1.6.1 e `frontend/package.json` em 1.6.1), sem um endpoint de monitoramento de saúde (`/api/health`) para consumo unificado de métricas, versões e estado de bancos de dados.

Além disso, a governança de acesso possui uma vulnerabilidade de autorização: qualquer usuário com credenciais válidas no Active Directory corporativo (EBSERH) consegue logar no sistema recebendo automaticamente o perfil "Comum", mesmo sem ter sido expressamente autorizado ou cadastrado previamente por um administrador. No frontend (`AdminConfig.vue`), o botão de inclusão ainda está rotulado como "Atribuir Perfil", permitindo digitação livre de logins sem pré-validação no AD corporativo.

A versão 1.7.0 padroniza a arquitetura do HC-UTI Manager com o FrameworkSETISD: estabelece Fonte Única da Verdade (SSOT) para versão (`src/version.py`), implementa o endpoint `/api/health`, introduz autorização local estrita (bloqueio 403 para usuários não cadastrados), elimina o perfil "Comum" legado e remodela a experiência de inclusão de usuários com validação antecipada no AD corporativo.

## What Changes

- **Fonte Única da Verdade (SSOT) para Versão e Identidade:** Criação de `src/version.py` definindo `VERSION = "1.7.0"`, `APP_NAME`, `SYSTEM_TITLE`, `LAST_UPDATE`, `ORGANIZATION` e `DEPARTMENT`. Atualização de `src/main.py` para consumir esses metadados.
- **Endpoint Padronizado de Saúde e Monitoramento (`/api/health`):** Criação de `src/routers/health.py` expondo `GET /api/health` para verificação de conectividade com os bancos de dados (`app_db` local e `aghu_postgres`), versão, metadados institucionais e timestamp UTC. Retorna HTTP 200 (healthy) ou HTTP 503 (unhealthy).
- **Consumo Reativo de Versão no Frontend:** Atualização de `frontend/src/config/version.ts` como store reativa baseada em `ref` que consulta `/api/health` na inicialização, mantendo fallback resiliente. Atualização de `frontend/package.json` para `1.7.0`.
- **Autorização Local Estrita (Autenticação Híbrida Segura) (**BREAKING**):** Modificação de `src/routers/auth.py` para bloquear logins (HTTP 403 Forbidden) de usuários que possuam credenciais válidas no Active Directory mas não estejam cadastrados na tabela local `usuarios_perfis` (com exceção dos super administradores definidos, como `admin` e `daniel.turmina`).
- **Remoção do Perfil "Comum" Legado (**BREAKING**):** Eliminação do perfil "Comum" nas atribuições (`auth.py`, `admin.py`, store `auth.ts`, `AdminConfig.vue`), garantindo que apenas perfis operacionais específicos (Administrador, UTI, UTI-Admin, NIR, NIR-Admin, COB, COB-Admin, BC, BC-Admin, HEM, HEM-Admin) existam no sistema.
- **Remodelação da Gestão de Usuários no Frontend (`AdminConfig.vue`):**
  - Alteração do botão de ação principal para "+ Novo Usuário".
  - Modal renomeado para "Novo Usuário (Validação no AD)" em criação.
  - Adição do fluxo de pré-validação com botão "🔍 Consultar AD" (ou Enter no input) consumindo `/api/admin/ad-search/{login}`.
  - Exibição de card verde confirmando nome completo, lotação e e-mail retornados pelo AD.
  - Bloqueio do botão "Salvar Usuário" enquanto o usuário não for validado no Active Directory em novos cadastros.

## Capabilities

### New Capabilities
- `health-check-versioning`: Endpoint `/api/health` e arquitetura Single Source of Truth para versionamento e telemetria de integridade de bancos e serviços.

### Modified Capabilities
- `usuario-config`: Fluxo de cadastro no modal de usuários com validação prévia obrigatória no AD corporativo, exibição de card de confirmação de atributos e bloqueio de criação não validada.
- `usuarios-perfis-migracao`: Restrição de controle de acesso (RBAC) com bloqueio 403 para credenciais AD não cadastradas no banco local e expurgo do perfil legado "Comum".

## Impact

- **Backend:**
  - Novo arquivo `src/version.py`.
  - Novo roteador `src/routers/health.py` registrado em `src/main.py`.
  - `src/routers/auth.py`: Bloqueio estrito 403 no login e remoção do fallback "Comum".
  - `src/routers/admin.py`: Remoção do `Role.COMUM` da lista de perfis atribuíveis.
- **Frontend:**
  - `frontend/src/config/version.ts`: Transformado em store reativa que faz fetch de `/api/health`.
  - `frontend/package.json`: Versão atualizada para 1.7.0.
  - `frontend/src/stores/auth.ts`: Limpeza de `Comum` nas listas de perfis atribuíveis e computadas.
  - `frontend/src/views/AdminConfig.vue`: Interface remodelada com validação no AD corporativo.
- **Documentação do Projeto:**
  - `docs/projeto_inicial/02-requisitos.md`: Registro dos requisitos de SSOT de versão, monitoramento `/api/health` e autorização estrita.
  - `docs/projeto_inicial/04-modelo-dados.md` e `05-interfaces.md`: Documentação do endpoint `/api/health` e payload padronizado.
  - `SPEC.md`: Atualização das metas e registro da versão 1.7.0.
