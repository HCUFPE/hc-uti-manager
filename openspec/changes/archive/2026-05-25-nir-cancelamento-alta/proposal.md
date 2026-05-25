## Why

Atualmente, o NIR não tem autonomia para cancelar solicitações de alta na lista de pendências recebidas, dependendo de que a UTI o faça manualmente. Adicionalmente, quando o NIR precisa recusar/cancelar uma alta por indisponibilidade de leitos, a UTI precisa ser notificada imediatamente por meio de um alerta automático do sistema, e o histórico de ações deve registrar claramente que a ação foi efetuada pelo NIR.

## What Changes

- **Botão de Cancelamento de Alta para o NIR**: Exibição de um botão "Cancelar Solicitação" para usuários com perfil NIR/Admin na tela de solicitações de alta recebidas (`Altas.vue`).
- **Modal de Motivo de Cancelamento**: Abertura de um modal ao clicar no botão para selecionar o motivo (com a opção única inicial: "Leito de Enfermaria Indisponível").
- **Permissão de Endpoint no Backend**: Atualização do endpoint `DELETE /api/altas/{alta_id}` para permitir o acesso a usuários com a role `NIR` ou `NIR_ADMIN`.
- **Alerta Automático para a UTI**: Geração de um alerta específico com título "Cancelamento de Alta pelo NIR" e perfil alvo UTI quando a alta for cancelada pelo NIR.

## Capabilities

### New Capabilities

<!-- Nenhuma nova capacidade é introduzida neste ciclo -->

### Modified Capabilities

- `internacao-leitos`: Inclusão da capacidade de cancelamento de solicitação de alta pelo NIR com motivo obrigatório.
- `alertas`: Geração de alerta para a UTI quando o NIR cancelar uma solicitação de alta.

## Impact

- **Backend**: Rota `DELETE /api/altas/{alta_id}` em `src/routers/altas.py` para receber permissões NIR e query params de motivo. O processador de histórico e alertas em `alerta_controller.py` gerará a notificação para a UTI.
- **Frontend**: Modificação na tela `Altas.vue` para incluir o botão e modal de justificativa para o NIR.
