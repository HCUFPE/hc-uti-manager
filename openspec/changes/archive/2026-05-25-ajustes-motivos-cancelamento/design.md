## Context

As listas de motivos de cancelamento no frontend precisam ser atualizadas. Além disso, o fluxo de cancelamento de reserva a partir da visão de leitos (`Home.vue`) dispara um `DELETE /api/leitos/{leito_id}/reserva` de forma direta e sem exigir justificativa, omitindo esse dado no log de histórico.

## Goals / Non-Goals

**Goals:**
- Atualizar a lista de motivos de cancelamento de reserva (tipo 2) em `Solicitacoes.vue` e `Home.vue`.
- Atualizar a lista de motivos de cancelamento de alta (tipo 3) em `Home.vue`.
- Forçar a seleção de motivo no frontend (`Home.vue`) e recebimento obrigatório no backend (`leito.py`) para o cancelamento de reserva de leito.

**Non-Goals:**
- Mudar o fluxo de cancelamento de solicitações comuns de vaga (tipo 1).
- Criar novos endpoints (vamos apenas atualizar a assinatura e lógica de `DELETE /api/leitos/{leito_id}/reserva`).

## Decisions

- **Exigência de Justificativa no Endpoint de Leito**: Modificar a assinatura da rota `cancelar_reserva` em `src/routers/leito.py` adicionando o parâmetro de query `motivo: str = Query(..., description="Motivo do cancelamento da reserva")` para forçar o envio a nível de API.
- **Modal de Confirmação em Home.vue**: Criar um novo modal no dashboard `Home.vue` chamado `showModalCancelReserva` contendo o dropdown preenchido com a constante `MOTIVOS_CANCELAMENTO_RESERVA`. O clique em "Cancelar Reserva" no `BedCard` passará a abrir esse modal em vez de disparar a requisição HTTP diretamente.

## Risks / Trade-offs

- **Compatibilidade Retroativa de Rota**:
  - *Risco*: Tornar o parâmetro `motivo` obrigatório no backend pode quebrar integrações antigas caso houvesse outros clientes consumindo esse endpoint.
  - *Mitigação*: Este é um sistema monolítico onde o único consumidor de `DELETE /api/leitos/{leito_id}/reserva` é o próprio frontend Vue. O ajuste no frontend é feito simultaneamente, mitigando o risco.
