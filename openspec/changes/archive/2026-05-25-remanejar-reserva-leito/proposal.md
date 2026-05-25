## Why

Permite que a UTI altere diretamente o leito reservado de um paciente sem precisar cancelar a reserva existente e criar uma nova do zero. Isso agiliza a resolução de conflitos de reserva (por exemplo, quando o leito planejado é ocupado no AGHU por outro paciente) e melhora a coordenação da ocupação de leitos.

## What Changes

- **Alteração direta de leito**: Possibilidade de redefinir o leito de destino para uma solicitação de vaga que já possui status "Reservado".
- **Interface de remanejamento**: Inclusão do botão "Mudar Leito" (ou "Reordenar/Remanejar Vaga") tanto na visão de cards de leito (`BedCard.vue`) quanto na fila de solicitações reservadas (`Solicitacoes.vue`).
- **Modal de transferência**: Exibição de um modal com leitos disponíveis para selecionar o novo destino do paciente.
- **Histórico**: Registro da transferência de leitos no histórico de ações contendo o leito de origem e o leito de destino.

## Capabilities

### New Capabilities
- Nenhuma.

### Modified Capabilities
- `solicitacao-leitos`: Permite redefinir o leito de destino associado a uma solicitação já reservada.
- `internacao-leitos`: Permite movimentar o estado de reserva (`prontuario_proximo`, `idade_proximo`, `especialidade_proximo`, `solicitacao_id`) de um leito de origem para um leito de destino no banco de dados local.

## Impact

- **Backend**:
  - `src/routers/solicitacoes_leito.py`: Nova rota `POST /api/solicitacoes/{sol_id}/remanejar-reserva`.
  - `src/controllers/solicitacao_leito_controller.py`: Novo método `remanejar_reserva`.
  - `src/providers/implementations/leito_estado_provider.py`: Novo método para transferir reservas entre leitos.
- **Frontend**:
  - `frontend/src/components/BedCard.vue`: Botão "Mudar Leito" para UTI/Admin.
  - `frontend/src/views/Solicitacoes.vue`: Botão "Mudar Leito" para UTI/Admin nas solicitações reservadas.
  - `frontend/src/views/Home.vue`: Mapeamento do evento e chamada de API.
