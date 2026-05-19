## Why

Para melhorar a gestão hospitalar e entender os gargalos no fluxo de internação, é necessário saber o motivo exato pelo qual uma solicitação de leito de UTI é cancelada (ex: cirurgia suspensa, paciente instável, óbito, etc). Atualmente, a exclusão/cancelamento ocorre sem registrar o contexto.

## What Changes

- Inclusão da obrigatoriedade de informar um motivo ao cancelar uma solicitação de leito.
- Criação de uma lista pré-definida de motivos de cancelamento no frontend.
- (Inicialmente, a lista conterá as opções A, B e C para fins de implementação base, podendo ser estendida facilmente depois).
- Registro do motivo no banco de dados e/ou no log de histórico da solicitação.

## Capabilities

### New Capabilities
- N/A

### Modified Capabilities
- `solicitacao-leitos`: Modificação do cenário de cancelamento de solicitação, exigindo que o usuário informe o motivo escolhido na interface.

## Impact

- **Frontend**: O modal/botão de cancelamento passará a exibir um dropdown com os motivos pré-definidos (A, B e C) antes de confirmar a exclusão.
- **Backend (`src/routers/solicitacoes_leito.py`)**: A rota `DELETE /{sol_id}` ou similar precisará receber no corpo da requisição ou nos parâmetros o motivo do cancelamento, registrando no provedor de histórico e salvando na entidade, se aplicável.
