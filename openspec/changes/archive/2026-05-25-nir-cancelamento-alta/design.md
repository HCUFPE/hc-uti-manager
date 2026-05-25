## Context

Atualmente, o NIR não consegue cancelar solicitações de alta na lista. Ao mesmo tempo, quando ocorre um cancelamento por parte do NIR (ex: por indisponibilidade de leitos), a UTI precisa ser avisada imediatamente através de um alerta visual no painel.

## Goals / Non-Goals

**Goals:**
- Adicionar permissão ao NIR para o endpoint `DELETE /api/altas/{alta_id}` no backend.
- Discriminar no histórico de ações se o cancelamento foi feito pelo NIR ou pela UTI.
- Gerar alerta direcionado à UTI quando o cancelamento for feito pelo NIR.
- Adicionar interface no frontend (`Altas.vue`) com o botão "Cancelar Solicitação" e modal de motivo obrigatório ("Leito de Enfermaria Indisponível").

**Non-Goals:**
- Modificar o fluxo de cancelamento de solicitações feito a partir dos leitos ocupados no dashboard principal.

## Decisions

- **Permissões de Rota**: Estender a checagem de roles da rota `DELETE /api/altas/{alta_id}` em `src/routers/altas.py` para: `[Role.ADMIN, Role.UTI, Role.UTI_ADMIN, Role.NIR, Role.NIR_ADMIN]`.
- **Log Diferenciado e Alerta para UTI**:
  - No backend (`altas.py`), obter o perfil do usuário logado. Se for NIR/ADMIN, registrar detalhes como `Alta #{alta_id} cancelada pelo NIR. Motivo: {motivo}`.
  - Em `src/controllers/alerta_controller.py`, na verificação de `tipo == "cancelamento"`, checar se a descrição contém `"pelo NIR"`. Se positivo, gerar o alerta direcionado para a UTI (definindo `perfil_alvo = None`) com o título `"Cancelamento de Alta pelo NIR"`.
- **Modal Unificado em Altas.vue**: Criar um modal no frontend (`Altas.vue`) chamado `showModalCancelAlta` que é aberto quando o NIR clica no botão "Cancelar Solicitação". Esse modal terá um select simples contendo o motivo `'Leito de Enfermaria Indisponível'`.

## Risks / Trade-offs

- **Detecção baseada em Texto**:
  - *Risco*: A detecção de quem cancelou a alta se apoiar na presença da string `"pelo NIR"` nos detalhes do histórico.
  - *Mitigação*: Esse padrão é gerado diretamente pela rota controlada no backend, garantindo que o texto seja formatado de forma previsível e imutável.
