## Why

Atualmente, quando o Bloco Cirúrgico realiza uma troca de paciente para uma vaga reservada, o sistema registra a ação no histórico como `cancelamento_reserva`. Isso faz com que esse evento seja contabilizado de forma incorreta nas métricas do dashboard sob o rótulo "Reservas Canceladas pela UTI", inflando artificialmente as ações de desfeita de reserva atribuídas à UTI.

Precisamos distinguir reservas desfeitas de fato pela UTI daquelas que foram canceladas/remanejadas pelo solicitante ou Bloco (por exemplo, via troca de paciente).

## What Changes

- Backend: Criar um novo tipo de ação de histórico (`tipo="cancelamento_solicitante"`) para quando a reserva de leito for desfeita pelo solicitante (por exemplo, em trocas de paciente).
- Backend: Atualizar a lógica do controller de solicitações de leito para registrar `tipo="cancelamento_solicitante"` quando a troca de paciente for efetuada pelo Bloco Cirúrgico, gerando mensagens de histórico muito mais legíveis para os dois pacientes (o que perdeu a vaga e o que a herdou).
- Backend: Atualizar o motor de alertas para gerar a notificação **"Reserva Remanejada (Troca de Paciente)"** quando a vaga for transferida de um paciente para outro, e a notificação **"Reserva Cancelada pelo Solicitante"** quando o leito for de fato liberado para a fila geral.
- Backend: Atualizar o provedor de indicadores para somar e retornar dois campos distintos de cancelamento de reservas: `cancelamento_reservas_uti` e `cancelamento_reservas_solicitante`.
- Frontend: Atualizar o quadro de resumo de ações (Trabalho) na tela de Indicadores para exibir as duas linhas separadas correspondentes.

## Capabilities

### New Capabilities

### Modified Capabilities
- `split-reservation-cancellation-indicators`: Exibição segregada de cancelamento de reservas entre UTI e Solicitante no dashboard de indicadores.

## Impact

- `src/controllers/solicitacao_leito_controller.py`
- `src/providers/implementations/indicadores_provider.py`
- `frontend/src/views/Indicadores.vue`
