## Why

Atualmente, solicitações de leitos não podem ser editadas após o leito já ter sido reservado. Isso causa problemas quando há necessidade de atualizar dados clínicos, de justificativa, ou informações da solicitação original após a reserva, forçando fluxos paralelos de comunicação. Permitir que solicitantes específicos (BC, BC-ADMIN, COB, COB-ADMIN, HEM e HEM-ADMIN) editem a solicitação garante que os dados fiquem sempre atualizados e acurados no sistema.

## What Changes

- Permitir a edição de solicitações de leitos que já possuam leito reservado/vinculado.
- Restringir essa permissão de edição pós-reserva para usuários com os seguintes papéis: BC, BC-ADMIN, COB, COB-ADMIN, HEM e HEM-ADMIN.
- Garantir que o frontend não bloqueie a ação de edição para esses perfis em solicitações reservadas.
- Garantir que o backend valide os papéis do usuário ao processar a atualização de uma solicitação reservada.

## Capabilities

### New Capabilities

*(Nenhuma)*

### Modified Capabilities

- `solicitacao-leitos`: Mudança na regra de permissão de edição, relaxando a restrição de edição para solicitações com leito reservado quando o usuário possuir papéis específicos.

## Impact

- **Frontend**: `Solicitacoes.vue` e componentes relacionados (botões de ação) para permitir o fluxo de edição dependendo dos grupos (AD/JWT) do usuário.
- **Backend**: Endpoint de edição de solicitação (presumivelmente em `routers/solicitacoes.py` ou `controllers/solicitacoes_controller.py`) para validar se o usuário pertence aos grupos autorizados a editar quando a solicitação já tem leito reservado.
