## 1. Backend Implementation

- [x] 1.1 Em `src/routers/solicitacoes_leito.py`, atualizar a verificação de permissão no método `cancelar_solicitacao` para permitir que usuários da UTI cancelem solicitações pendentes quando o motivo fornecido for "Falta de vaga de UTI".

## 2. Frontend Implementation

- [x] 2.1 Em `frontend/src/views/Solicitacoes.vue`, habilitar a visibilidade do botão "Cancelar Solicitação" na fila de pendentes para perfis UTI (`v-if="podeGerenciar(sol) || authStore.isUTI"`).
- [x] 2.2 Em `frontend/src/views/Solicitacoes.vue`, ajustar a propriedade computada `motivosAtuais` para retornar o motivo fixo "Falta de vaga de UTI" para a UTI (e misturar para admins).
- [x] 2.3 Em `frontend/src/views/Solicitacoes.vue`, ajustar o método `abrirModalCancelamento` para pré-selecionar o motivo de cancelamento se a lista contiver apenas um item.

## 3. Verification

- [x] 3.1 Escrever teste automatizado para validar que a UTI consegue cancelar solicitações pendentes com o motivo específico e é bloqueada em outros cenários.
- [x] 3.2 Executar a build de produção do frontend (`npm run build`) para verificar a integridade da aplicação.
