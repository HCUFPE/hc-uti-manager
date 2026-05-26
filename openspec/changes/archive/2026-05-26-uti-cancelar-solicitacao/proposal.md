## Why

Atualmente, a equipe da UTI (ou administradores) não pode cancelar diretamente uma solicitação de vaga pendente (antes de haver uma reserva). Se a UTI souber de antemão que a solicitação não poderá ser atendida por falta de leitos de UTI livres, ela precisa solicitar que o próprio setor criador cancele a vaga. Isso gera atrito e lentidão no gerenciamento da fila. Permitir que a UTI execute esse cancelamento com um motivo específico ("Falta de vaga de UTI") resolve esse gargalo.

## What Changes

- **Permissão de Cancelamento no Backend**: Atualizar a rota de cancelamento de solicitação para permitir que usuários com papéis da UTI (`UTI`, `UTI-Admin`) excluam/cancelem uma solicitação pendente, desde que o motivo seja obrigatoriamente `"Falta de vaga de UTI"`.
- **Interface Visual (Fila de Solicitações)**: Disponibilizar o botão de cancelamento de solicitação na fila de pendentes para usuários da UTI e administradores.
- **Modal de Confirmação com Motivo Único**: Ao clicar em cancelar, exibir um modal de confirmação onde o motivo pré-definido e imutável/selecionado seja "Falta de vaga de UTI".

## Capabilities

### New Capabilities
- Nenhuma

### Modified Capabilities
- `solicitacao-leitos`: Alteração do requisito de controle de permissões na edição e cancelamento para permitir que a UTI cancele solicitações pendentes sob a justificativa única de "Falta de vaga de UTI".

## Impact

- **Frontend**:
  - `frontend/src/views/Home.vue`: Habilitar a exibição do botão "Cancelar" nos itens da fila de solicitações pendentes para perfis UTI/Administrador. Ao clicar, disparar o fluxo de cancelamento com o motivo fixado como `"Falta de vaga de UTI"`.
- **Backend**:
  - `src/routers/solicitacoes_leito.py`: Ajustar a validação de autorização para permitir o cancelamento por usuários UTI se o status for pendente e o motivo for `"Falta de vaga de UTI"`.
