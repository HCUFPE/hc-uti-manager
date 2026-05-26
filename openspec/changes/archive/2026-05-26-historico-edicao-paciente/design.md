## Context

Atualmente, o sistema permite que as áreas solicitantes editem solicitações mesmo que já estejam com leitos reservados pela UTI. No entanto, se o usuário alterar o prontuário (isto é, trocar o paciente) em uma edição, o registro antigo sofre um UPDATE destrutivo. Isso corrompe o histórico clínico-administrativo e inviabiliza indicadores de performance (ex: tempo de espera na fila, motivos de cancelamento e fluxo de cirurgias de emergência). 

Para resolver isso, qualquer alteração de prontuário em uma solicitação ativa deve ser tratada como o cancelamento da solicitação antiga (motivo: "Alteração de Prioridade pós Reserva de Leito") e a criação de uma nova solicitação com os dados do novo prontuário obtidos do AGHU. Caso houvesse um leito reservado, a reserva do leito físico deve ser transferida para o novo paciente sem que o leito passe pelo estado disponível, garantindo a continuidade da reserva.

## Goals / Non-Goals

**Goals:**
- Detectar a alteração do prontuário durante a edição de uma solicitação.
- Cancelar logicamente a solicitação antiga com o status "Cancelada" e o motivo de cancelamento "Alteração de Prioridade pós Reserva de Leito".
- Criar a nova solicitação a partir dos dados retornados do AGHU.
- Transferir atomicamente no SQLite (`LeitoEstado`) a reserva de leito da solicitação antiga para a nova, se houver.
- Registrar as ações no histórico (`HistoricoProvider`) contendo data/hora, operador (username) e a descrição da troca.
- Verificar a abrangência e consistência dos logs de histórico em todas as ações de estado críticas do sistema.

**Non-Goals:**
- Impedir a alteração de prontuário durante a edição.
- Alterar as permissões de acesso e segurança das rotas.
- Re-sincronizar dados com o AGHU de solicitações já concluídas.

## Decisions

### Decisão 1: Abstração da Troca de Paciente na Camada Controller
Em vez de tratar a substituição no frontend ou criar um endpoint dedicado, interceptaremos a troca de prontuário diretamente no método `editar_solicitacao` de `SolicitacaoLeitoController`.
- **Alternativa A**: Criar um endpoint `POST /api/solicitacoes/{id}/trocar-paciente`.
- **Alternativa B (Escolhida)**: Interceptar a edição de `prontuario` dentro do `PATCH /api/solicitacoes/{id}` existente.
- **Razão da Escolha**: Mantém a simplicidade da API REST e da interface no frontend (que usa o formulário comum de edição), garantindo que a lógica complexa de banco de dados (SQLite) ocorra de forma transparente no backend.

### Decisão 2: Propagação do Usuário Operador no Fluxo de Edição
Atualizar a assinatura do método `editar_solicitacao` no controller para receber o parâmetro `username` (operador logado do token JWT) repassado pelo router.
- **Razão**: Permitir que a camada de controller registre diretamente no histórico as ações de cancelamento, criação e transferência de reserva com o operador correto, em vez de depender apenas do log genérico de edição do router.

### Lógica de Transferência de Reserva
No SQLite (`LeitoEstado`), a reserva está vinculada ao `solicitacao_id` e traz dados redundantes de prontuário, idade e especialidade. Caso a solicitação antiga (ID $A$) estivesse reservada para o leito $L$, nós:
1. Criamos a nova solicitação (ID $B$) com status "Reservado" e `destino` = `"Leito L"`.
2. Cancelamos a solicitação antiga (ID $A$) com status "Cancelada" e `destino` = `None`.
3. Atualizamos a linha de `LeitoEstado` onde `solicitacao_id == A` para apontar para `solicitacao_id = B` e atualizamos os campos `prontuario_proximo`, `idade_proximo` e `especialidade_proximo` com os dados do novo paciente.
4. Sincronizamos as prioridades nos buckets das datas/turnos antigo e novo.

## Risks / Trade-offs

- **[Risco]**: Inconsistência na fila de prioridades caso o novo paciente caia em uma data/turno diferente da anterior.
  - **Mitigação**: Executar a reordenação (`_sincronizar_prioridades`) em ambos os dias e turnos (origem e destino) após a criação e o cancelamento.
- **[Risco]**: Perda de rastreabilidade se a transferência da reserva falhar no meio.
  - **Mitigação**: Executar as operações de persistência e atualização da reserva dentro do mesmo escopo lógico da transação do banco do SQLite.
