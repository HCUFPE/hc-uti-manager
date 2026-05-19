## Why

Identificamos a necessidade de ajustar fluxos e corrigir inconsistências na gestão de solicitações e leitos para refletir melhor a realidade operacional. Gestores (solicitantes com papéis administrativos) precisam ter autonomia para cancelar solicitações já reservadas, e a UTI precisa documentar os motivos ao cancelar reservas. Além disso, precisamos garantir a disponibilidade de reserva para leitos em higienização/limpeza, corrigir a sincronização de dados alterados e evitar alertas falsos de mudança de prioridade.

## What Changes

- **Cancelamento por Solicitantes Gestores**: Perfis `BC`, `BC-ADMIN`, `COB`, `COB-ADMIN`, `HEM` e `HEM-ADMIN` poderão cancelar solicitações, inclusive as que já possuem reserva (cancelando a reserva em cascata). Será exigida a seleção de um motivo.
- **Cancelamento de Reserva pela UTI**: A ação de cancelar uma reserva (voltar para pendente) pela equipe da UTI exigirá a seleção de um motivo.
- **Reserva de Leitos em Limpeza**: Leitos com status "higienização" ou "limpeza" passarão a ser listados como elegíveis para receber uma reserva, permitindo alocação antecipada.
- **Sincronização de Edição**: Quando uma solicitação reservada for editada, as alterações (prontuário, idade, turno, especialidade) serão propagadas para o estado do leito correspondente para refletir corretamente na tela de Leitos.
- **Correção do Alerta de Prioridade**: O alerta de "mudança de prioridade" no histórico/log só será disparado quando o campo prioridade for efetivamente modificado.

## Capabilities

### New Capabilities
*(Nenhuma)*

### Modified Capabilities
- `solicitacao-leitos`: Novas regras de permissão para cancelamento, exigência de motivos e ajuste de disparos de histórico e sincronização de dados.
- `internacao-leitos`: Relaxamento da regra de disponibilidade de leitos, permitindo reservas para leitos em status de higienização ou limpeza.

## Impact

- **Frontend**: 
  - Ajuste na regra de exibição do botão "Cancelar Solicitação" para permitir a ação mesmo se o status for "Reservado" para perfis autorizados.
  - Implementação/verificação do campo de motivo ao cancelar reserva.
- **Backend**:
  - `controllers/solicitacao_leito_controller.py`: lógica de exclusão em cascata (solicitação + reserva) e sincronização de dados com `estado_provider`.
  - `routers/solicitacoes_leito.py`: ajuste na verificação para não barrar o cancelamento de solicitações reservadas e conserto do acionamento de alerta de edição.
  - `routers/leito.py` ou provider equivalente: ajustar os filtros que determinam quais leitos estão disponíveis para reserva.
