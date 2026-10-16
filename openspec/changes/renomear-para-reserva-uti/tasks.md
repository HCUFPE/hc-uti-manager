# Tasks: Renomeação do Sistema para "Reserva UTI"

## 1. Identidade no Backend e Contratos de API

- [x] 1.1 Atualizar `src/version.py` definindo `APP_NAME = "Reserva UTI"` e `SYSTEM_TITLE = "Gestão e Reserva de Leitos UTI"` e verificar retorno no endpoint `/api/health`
- [x] 1.2 Atualizar mensagem textual de bloqueio em `src/routers/auth.py` referenciando o Administrador do Reserva UTI

## 2. Textos e Identidade no Frontend

- [x] 2.1 Atualizar `<title>` em `frontend/index.html` para `Reserva UTI (HC-UFPE)` e verificar título da aba
- [x] 2.2 Atualizar tela de login `frontend/src/views/Login.vue` com título textual "Reserva UTI" e subtítulo institucional
- [x] 2.3 Atualizar menu lateral `frontend/src/components/SidebarNav.vue` para exibir "Reserva UTI" no topo
- [x] 2.4 Atualizar fallback em `frontend/src/config/version.ts` para `Reserva UTI` e mensagem em `frontend/src/views/AdminConfig.vue`
- [x] 2.5 Executar build do frontend (`npm run build`) para verificar compilação sem erros

## 3. Documentação e Especificações

- [x] 3.1 Atualizar o `README.md` principal com a nova identidade do sistema
- [x] 3.2 Atualizar cadernos de requisitos e arquitetura em `docs/projeto_inicial/` (`01-visao.md`, `02-requisitos.md`, `03-casos-uso.md`, `04-modelo-dados.md`, `05-interfaces.md`, `06-arquitetura.md`, `07-glossario.md` e `SPEC.md`)
- [x] 3.3 Atualizar o `CHANGELOG.md` registrando a nova versão com o reposicionamento para Reserva UTI
