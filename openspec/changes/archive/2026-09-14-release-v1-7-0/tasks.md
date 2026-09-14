# tasks.md — Versão 1.7.0 (Health Check, Versioning SSOT & Autorização Estrita AD)

## 1. Backend: Versioning SSOT e Health Check

- [x] 1.1 Criar o módulo central `src/version.py` com `VERSION = "1.7.0"`, `APP_NAME = "HC-UTI Manager"`, `SYSTEM_TITLE = "Gestão de Leitos UTI"`, `LAST_UPDATE`, `ORGANIZATION` e `DEPARTMENT`
- [x] 1.2 Criar o roteador `src/routers/health.py` com o endpoint `GET /api/health` testando `app_db` local (`SELECT 1`) e `aghu_postgres`
- [x] 1.3 Atualizar `src/main.py` importando `VERSION` e `APP_NAME` de `version.py` e registrando o roteador `health.router`

## 2. Backend: Autorização Estrita e Remoção de Perfil Comum

- [x] 2.1 Modificar `src/routers/auth.py` para validar `UsuarioPerfil` localmente após sucesso no AD e lançar HTTP 403 Forbidden para usuários não cadastrados (mantendo fallback para super admins `admin` e `daniel.turmina`)
- [x] 2.2 Excluir referências de atribuição de perfil `Comum` em `src/routers/auth.py` e `src/routers/admin.py` (removendo `Role.COMUM` da lista de papéis atribuíveis)

## 3. Frontend: Versioning Reativo e Expurgo de Perfil Comum

- [x] 3.1 Atualizar `frontend/src/config/version.ts` como store reativa com `ref` consumindo `GET /api/health` com fallbacks seguros
- [x] 3.2 Atualizar versão para `1.7.0` em `frontend/package.json`
- [x] 3.3 Atualizar `frontend/src/stores/auth.ts` removendo o perfil `Comum` dos perfis atribuíveis (`getAssignableProfiles`) e helpers de perfil

## 4. Frontend: Remodelação da Tela de Gestão de Usuários (AdminConfig.vue)

- [x] 4.1 Renomear o botão principal da tela `frontend/src/views/AdminConfig.vue` para `+ Novo Usuário`
- [x] 4.2 Adicionar o fluxo de busca e validação prévia no Active Directory (`/api/admin/ad-search/{login}`) com botão `🔍 Consultar Login` e acionamento por Enter
- [x] 4.3 Implementar o card visual de confirmação (verde) exibindo Nome Completo, Lotação e E-mail validados pelo AD
- [x] 4.4 Configurar validação no modal para manter o botão "Salvar Usuário" desabilitado para novos cadastros até a confirmação de validação no AD

## 5. Documentação e Especificações

- [x] 5.1 Atualizar `docs/projeto_inicial/02-requisitos.md` com os novos requisitos funcionais de telemetria `/api/health`, SSOT de versão e autorização híbrida estrita
- [x] 5.2 Atualizar `docs/projeto_inicial/04-modelo-dados.md` e `docs/projeto_inicial/05-interfaces.md` documentando o contrato do endpoint `/api/health`
- [x] 5.3 Atualizar `docs/projeto_inicial/SPEC.md` registrando a entrega da versão 1.7.0 no roadmap e changelog de desenvolvimento

## 6. Verificação, Build e Deploy em Homologação

- [x] 6.1 Compilar o frontend com `npm run build` e validar tipagem TypeScript (`vue-tsc`)
- [x] 6.2 Executar suíte de testes de integridade do backend
- [x] 6.3 Executar deploy para o ambiente de homologação (`scratch/deploy_homolog.py`) e verificar integridade da stack
