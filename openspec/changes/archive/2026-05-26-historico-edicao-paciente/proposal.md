## Why

Ao alterar o prontuário (ou seja, o paciente) em uma solicitação de vaga existente, a auditoria histórica é corrompida se o registro antigo simplesmente sofrer um UPDATE destrutivo. Esse comportamento dificulta o rastreamento retrospectivo e a geração de indicadores precisos, pois mascara o cancelamento de uma intenção de internação e a criação de outra. Além disso, é necessário garantir que todas as transições de estado críticas do sistema registrem logs detalhados e consistentes (data/hora, operador e descrição da ação) no histórico.

## What Changes

- **Tratamento de Edição com Troca de Paciente**: Quando uma edição alterar o campo `prontuario` de uma solicitação ativa, o sistema deve tratar isso internamente como:
  - Cancelamento da solicitação original (com motivo "Alteração de Prioridade pós Reserva de Leito").
  - Criação de uma nova solicitação contendo os novos dados do paciente obtidos do AGHU.
- **Manutenção de Vagas Reservadas**: Se a solicitação original possuía um leito reservado, a reserva no leito físico (SQLite) deve permanecer ativa e ser transferida automaticamente para a nova solicitação/paciente, mantendo o status de "Reservado" sem interrupções.
- **Auditoria de Ações e Histórico Consistente**: Verificação e padronização dos registros de histórico (`HistoricoProvider`) em todas as operações cruciais do sistema (criar, editar, reservar, remanejar, liberar e cancelar), garantindo que gravem data/hora exata, operador do sistema (usuário logado) e descrição detalhada da ação.

## Capabilities

### New Capabilities
- Nenhuma

### Modified Capabilities
- `solicitacao-leitos`: Alteração do comportamento de edição de solicitações quando envolve a mudança de prontuário (paciente), garantindo integridade no histórico e manutenção da reserva ativa do leito.

## Impact

- **Backend**:
  - `src/controllers/solicitacao_leito_controller.py`: Modificar o método `editar_solicitacao` para detectar troca de prontuário, criar nova solicitação, cancelar a antiga e reassociar o leito reservado caso exista.
  - Verificação geral de rotas e chamadas para registrar o operador nos logs de histórico de forma consistente.
- **Banco de Dados**:
  - Garantia de que a tabela `historico` possui todas as colunas necessárias para auditoria precisa de indicadores (data/hora, operador e ação).
