## 1. Backend: Autocompletar dados do AD ao salvar

- [x] 1.1 Atualizar `POST /api/admin/perfis` em `src/routers/admin.py` para resolver e preencher automaticamente Nome Completo, Lotação e E-mail a partir do AD

## 2. Frontend: Modal Simplificado

- [x] 2.1 Remover os inputs de Nome Completo, Lotação e E-mail do modal de usuário em `frontend/src/views/AdminConfig.vue`
- [x] 2.2 Desativar a consulta pelo evento blur e simplificar o estado de carregamento do AD no frontend
- [x] 2.3 Alterar o rótulo do botão de salvamento no modal para "Salvar Usuário"
