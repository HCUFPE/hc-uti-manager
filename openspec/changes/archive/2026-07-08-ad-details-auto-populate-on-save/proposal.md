## Why

Para simplificar a experiência do administrador ao gerenciar usuários, o modal de cadastro deve exigir apenas a inserção do Login da Rede (username) e o Perfil de Acesso. Os campos de Nome Completo, Lotação e E-mail devem ser populados automaticamente pelo backend consultando o Active Directory (AD) no momento de salvar o perfil, em vez de depender de inputs ou buscas do lado do cliente durante a digitação.

Também ajustaremos o botão de confirmação dentro do modal de "Salvar Perfil" para "Salvar Usuário", tornando a ação mais clara para o operador do sistema.

## What Changes

- **Sincronização Automática no Backend**: Atualizar a rota `POST /api/admin/perfis` para realizar a pesquisa no AD e preencher as informações de Nome, Lotação e E-mail do usuário antes de persistir o registro no banco de dados local.
- **Remoção de Inputs Manuais no Frontend**: Remover as caixas de texto de Nome Completo, Lotação e E-mail do modal de usuários no componente `frontend/src/views/AdminConfig.vue`, deixando apenas os inputs de login e perfil.
- **Renomear Botão do Modal**: Alterar o texto de submissão do modal para "Salvar Usuário".

## Capabilities

### Modified Capabilities
- `usuario-config`: Otimização do fluxo de provisionamento de usuários e eliminação de caixas de entrada desnecessárias no formulário de atribuição de privilégios.

## Impact

- **Backend**:
  - `src/routers/admin.py`: Modificar o endpoint de salvamento para buscar os dados no AD se ausentes.
- **Frontend**:
  - `frontend/src/views/AdminConfig.vue`: Limpar o modal, remover a busca local de blur e renomear o botão.
