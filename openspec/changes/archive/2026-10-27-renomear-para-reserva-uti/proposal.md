# Proposal: Renomeação do Sistema para "Reserva UTI"

## Why

O sistema atualmente identificado visualmente como **UTI Manager** (ou "HC-UTI Manager") está adotando formalmente o nome **Reserva UTI** no Hospital das Clínicas da UFPE (HC-UFPE/Ebserh).

Essa mudança reflete com exatidão o propósito prático da solução: organizar e sincronizar a reserva de leitos de UTI entre o Bloco Cirúrgico e a UTI. A alteração é estritamente de apresentação e identidade (telas, aba do navegador, menus, versão e documentação), sem qualquer impacto em infraestrutura, banco de dados ou permissões de usuários.

## What Changes

- **Frontend (UI & Textos Visuais)**:
  - Atualização do título da página em `frontend/index.html` de `UTI Manager (HC-UFPE)` para `Reserva UTI (HC-UFPE)`.
  - Atualização do título de texto na tela de Login (`frontend/src/views/Login.vue`) de `UTI Manager` para `Reserva UTI`.
  - Atualização do título de texto no topo do menu lateral (`frontend/src/components/SidebarNav.vue`) de `UTI Manager` para `Reserva UTI`.
  - Atualização do fallback da store reativa `frontend/src/config/version.ts` para `APP_NAME = ref('Reserva UTI')`.
  - Mensagem de diálogo de remoção em `frontend/src/views/AdminConfig.vue`.
  - Avaliação do uso da arte `Logo Reserva UTI.png` no formulário de login.
- **Backend & APIs**:
  - Atualização da Fonte Única da Verdade (`src/version.py`): `APP_NAME = "Reserva UTI"`.
  - Swagger UI (`/docs`) e endpoint `/api/health` passam a exibir "Reserva UTI".
  - Mensagem de texto de retorno de erro no login em `src/routers/auth.py` ("Solicite o cadastro ao Administrador do Reserva UTI").
- **Documentação do Projeto**:
  - Atualização de títulos e referências no `README.md` e cadernos de especificação em `docs/projeto_inicial/`.
  - Registro da atualização no `CHANGELOG.md`.

## Capabilities

### Modified Capabilities
- `health-check-versioning`: O requisito de metadados institucionais e identidade na Fonte Única da Verdade (`src/version.py` e `/api/health`) passa a fornecer `app_name: "Reserva UTI"`.

## Impact

- **Código Frontend**: `frontend/index.html`, `frontend/src/views/Login.vue`, `frontend/src/components/SidebarNav.vue`, `frontend/src/config/version.ts`.
- **Código Backend**: `src/version.py`, `src/routers/auth.py`.
- **Infraestrutura**: NENHUMA alteração em containers, serviços systemd ou arquivos `.env`.
- **Banco de Dados e Perfis**: NENHUMA alteração em tabelas, permissões ou perfis de usuários.
