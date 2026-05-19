## 1. Backend

- [x] 1.1 Atualizar `src/controllers/solicitacao_controller.py` (ou roteador de solicitação) para flexibilizar a regra de edição de solicitação reservada, permitindo a atualização caso o usuário pertença aos grupos `BC`, `BC-ADMIN`, `COB`, `COB-ADMIN`, `HEM` ou `HEM-ADMIN`.
- [x] 1.2 Adicionar testes unitários/funcionais (se o projeto suportar) ou revisar o endpoint localmente para confirmar que o 403 Forbidden é retornado apenas para usuários não autorizados que tentam editar uma solicitação reservada.

## 2. Frontend

- [x] 2.1 Modificar o componente `frontend/src/views/Solicitacoes.vue` (ou componente filho como `SolicitacaoCard.vue` / Tabela) para alterar a propriedade `disabled` do botão Editar, utilizando o `authStore` para verificar se o usuário pertence a um dos grupos autorizados caso a solicitação possua um leito reservado.
- [x] 2.2 Verificar o modal de edição para garantir que o formulário não é bloqueado incorretamente por alguma outra checagem de estado quando o usuário possui as *roles* corretas.
