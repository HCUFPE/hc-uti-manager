## Context

Atualmente, o fluxo de troca de paciente na edição de solicitação (`editar_solicitacao`) cria incondicionalmente um novo registro de solicitação para o paciente de destino, sem verificar se ele já possui um prontuário ativo. Se o paciente de destino já tiver uma solicitação pendente ou reservada na base, isso gera registros duplicados ativos.

## Goals / Non-Goals

**Goals:**
- Validar a existência de solicitações ativas do paciente de destino antes de processar a troca de prontuário na edição.
- Rejeitar a troca se o paciente de destino já possuir uma reserva de leito ativa.
- Mesclar de forma transparente (promover a solicitação pendente existente para reservada) se o paciente de destino possuir uma solicitação pendente, evitando duplicidade e reaproveitando o leito de origem.
- Manter o comportamento padrão de criação de nova solicitação caso o paciente de destino não tenha histórico de solicitações ativas.

**Non-Goals:**
- Alterar o comportamento da rota de criação inicial de solicitação (`criar_solicitacao`), que já valida duplicidade.
- Modificar o fluxo de cancelamento ou alta de leitos.

## Decisions

### Decisão 1: Lógica do Fluxo de Edição (`editar_solicitacao`)
A verificação de duplicidade e a mescla serão centralizadas no método `editar_solicitacao` da classe `SolicitacaoLeitoController`.

Ao detectar a troca de prontuário:
1. Buscar solicitações ativas ("Pendente" ou "Reservado") para o novo prontuário.
2. Se houver uma com status "Reservado", lançar `HTTPException(400, "O paciente de destino já possui uma reserva de leito ativa.")`.
3. Se houver uma com status "Pendente":
   - Atualizar esse registro preexistente: `status = alvo.status` e `destino = alvo.destino`.
   - Transferir a reserva física no banco SQLite (`LeitoEstado`) para o ID desse registro preexistente (se a solicitação de origem `alvo` estava no status "Reservado").
   - Atualizar a solicitação original (`alvo`): `status = "Cancelada"`, `destino = None`.
   - Registrar no histórico: log de cancelamento da solicitação antiga e log de reserva/atualização para a solicitação existente promovida do novo paciente.
4. Se não houver solicitação ativa, segue o fluxo atual de criação de novo registro + cancelamento do antigo.

*Alternativas consideradas*:
- Bloquear a edição incondicionalmente se o paciente destino já tiver qualquer solicitação. (Decisão rejeitada porque a mesclagem inteligente é mais fluida e evita que o usuário tenha que cancelar manualmente a solicitação pendente existente para depois editar a outra).

## Risks / Trade-offs

- **[Risco] Inconsistência ao atualizar estados no banco (SQLite)**: Se a atualização da solicitação falhar após a transferência do leito, o banco pode ficar inconsistente.
  - **Mitigação**: Executar as operações de escrita dentro da mesma sessão de banco de dados e aplicar o `commit` apenas no final do fluxo.
