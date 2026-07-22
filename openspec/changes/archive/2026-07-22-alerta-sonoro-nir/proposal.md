## Why

Atualmente, o alerta sonoro na tela principal (Home) é exclusivo para usuários com perfil de UTI, disparando quando há cirurgias pendentes ou alertas não lidos. O Núcleo Interno de Regulação (NIR) também necessita de um sinalizador sonoro imediato ao receber notificações de alta que dependem de sua ação, para agilizar a tomada de providências (ciência de altas e atribuição de destinos).

## What Changes

- Habilitar o alerta sonoro na tela principal (`Home.vue`) para usuários do perfil **NIR**.
- O alerta sonoro para o NIR SHALL tocar a cada 30 segundos (mesma frequência da UTI) se houver pelo menos um alerta não lido no contador de notificações do NIR (`unreadAlertsCount > 0`).
- O alerta sonoro para o NIR SHALL cessar assim que o operador do NIR visualizar/dar ciência de todos os alertas (contador de alertas não lidos for a zero).

## Capabilities

### New Capabilities

N/A

### Modified Capabilities

- `alertas`: introdução do sinalizador sonoro de pendências no frontend para o perfil do NIR.

## Impact

- `frontend/src/views/Home.vue`: atualização da lógica do método `verificarETocarSom` para incluir a validação do perfil do NIR e seus alertas pendentes.
