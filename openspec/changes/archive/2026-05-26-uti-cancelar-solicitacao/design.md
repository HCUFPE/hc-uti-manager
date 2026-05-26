## Context

Atualmente, o censo e gerenciamento de solicitações de vagas no censo local são controlados pelas rotas do backend. A permissão para cancelar uma solicitação (status "Pendente", antes de haver qualquer reserva de leito) é restrita apenas ao proprietário/setor solicitante (ou administrador) no endpoint `DELETE /api/solicitacoes/{sol_id}`.

A equipe da UTI deseja poder dispensar ou cancelar solicitações na fila diretamente sob o motivo "Falta de vaga de UTI", permitindo maior controle do fluxo do censo pela UTI.

## Goals / Non-Goals

**Goals:**
- Permitir que usuários com papéis da UTI (`UTI`, `UTI-Admin`) cancelem solicitações com status "Pendente".
- Restringir o motivo de cancelamento da UTI para a opção única: `"Falta de vaga de UTI"`.
- Habilitar o botão "Cancelar Solicitação" na visão de solicitações pendentes para a equipe da UTI.
- Pré-selecionar o motivo de cancelamento se houver apenas uma opção disponível no modal.

**Non-Goals:**
- Permitir que a UTI edite dados clínicos das solicitações pendentes alheias.
- Permitir que outros setores (BC, COB, HEM) usem o motivo de cancelamento "Falta de vaga de UTI".

## Decisions

### Decisão 1: Ajuste na Validação da Rota do Backend
Atualizaremos a verificação de permissão em `src/routers/solicitacoes_leito.py` no método `cancelar_solicitacao`.
- **Alternativa A**: Criar uma nova rota dedicada como `POST /api/solicitacoes/{id}/cancelar-pela-uti`.
- **Alternativa B (Escolhida)**: Incrementar a lógica de permissão da rota `DELETE /api/solicitacoes/{sol_id}` existente para aceitar a UTI caso o status da solicitação seja `"Pendente"` e o motivo passado via query parameter seja `"Falta de vaga de UTI"`.
- **Razão da Escolha**: Mantém a assinatura e a uniformidade do endpoint de exclusão, apenas estendendo a lógica de validação de papéis de forma elegante e centralizada.

### Decisão 2: Comportamento das Opções no Frontend
No arquivo `frontend/src/views/Solicitacoes.vue`:
1. Habilitaremos o botão de cancelamento para usuários da UTI na seção de pendentes:
   `v-if="podeGerenciar(sol) || authStore.isUTI"`
2. Ajustaremos a propriedade computada `motivosAtuais` para retornar `['Falta de vaga de UTI']` quando o usuário for da UTI e não for administrador.
3. No método `abrirModalCancelamento`, se o array resultante `motivosAtuais` tiver tamanho 1, o valor será automaticamente preenchido em `motivoCancelamento.value` para facilitar a usabilidade.

## Risks / Trade-offs

- **[Risco]**: A equipe da UTI tentar usar o botão para cancelar solicitações já reservadas.
  - **Mitigação**: O botão de cancelamento de solicitação na interface fica na seção de solicitações pendentes ("Aguardando Reserva de Leito"). Para solicitações com leito reservado, a UTI deve primeiro cancelar a reserva do leito (o que as devolve ao estado pendente) ou o cancelamento deve passar pelas regras comuns de reserva.
