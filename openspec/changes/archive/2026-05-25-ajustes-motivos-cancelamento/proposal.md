## Why

As listas de motivos de cancelamento de reserva de leito e de cancelamento de alta estão desatualizadas em relação às necessidades clínicas. Adicionalmente, quando o perfil da UTI cancela uma reserva de leito a partir do card de leito no painel principal, a ação é executada sem solicitar ou registrar o motivo correspondente, o que prejudica a auditoria e o histórico do fluxo de leitos.

## What Changes

- **Novos Motivos para Cancelamento de Reserva (Tipo 2)**: Substituição dos motivos genéricos no frontend por opções clínicas e operacionais específicas.
- **Novos Motivos para Cancelamento de Alta (Tipo 3)**: Atualização dos motivos de cancelamento de alta no painel de leitos.
- **Exigência de Motivo no Cancelamento de Reserva no Card**: Criação de modal de confirmação no frontend e atualização do endpoint `DELETE /api/leitos/{leito_id}/reserva` no backend para receber e registrar obrigatoriamente o motivo.

## Capabilities

### New Capabilities

<!-- Nenhuma nova capacidade é introduzida neste ciclo -->

### Modified Capabilities

- `solicitacao-leitos`: Atualização dos motivos de cancelamento de reserva de leito.
- `internacao-leitos`: Exigência de motivo ao cancelar reserva de leito a partir do painel geral de leitos e atualização dos motivos de cancelamento de alta.

## Impact

- **Backend**: Rota em `src/routers/leito.py` passará a aceitar e exigir o parâmetro de query `motivo`, gravando a informação nos detalhes do histórico.
- **Frontend**: Componentes `frontend/src/views/Home.vue` e `frontend/src/views/Solicitacoes.vue` terão suas constantes de motivos atualizadas. `Home.vue` passará a abrir um modal de seleção de motivos antes de chamar a API para cancelar a reserva.
