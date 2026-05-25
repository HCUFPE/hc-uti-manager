## Context

No sistema atual, se houver conflito de reserva (outro paciente ocupar o leito reservado no AGHU) ou se a UTI simplesmente decidir realocar um paciente reservado para outro leito, não existe uma forma direta de redefinir o leito de destino. É necessário cancelar a reserva (voltando a solicitação para Pendente) e reservá-la novamente para o novo leito. Essa abordagem de múltiplos passos gera atrito operacional.

## Goals / Non-Goals

**Goals:**
- Permitir o remanejamento direto de um leito reservado para outro leito disponível.
- Garantir a atomicidade das transações no banco de dados local (SQLite) para evitar duplicações ou reservas órfãs.
- Registrar cada ação de remanejamento no histórico de ações do sistema com auditoria (usuário e leitos envolvidos).

**Non-Goals:**
- Não automatizar a detecção inteligente e remanejamento automático de leitos. A decisão de remanejar cabe inteiramente ao usuário (UTI/Admin).
- Não alterar as regras de admissão e alta do AGHU.

## Decisions

### 1. Novo Endpoint Dedicado vs Extensão do PATCH de Solicitações
* **Opção A**: Permitir a edição do campo `destino` via endpoint de edição geral `PATCH /api/solicitacoes/{sol_id}`.
* **Opção B (Escolhida)**: Criar um endpoint exclusivo `POST /api/solicitacoes/{sol_id}/remanejar-reserva`.
* **Racional**: A alteração do leito envolve a modificação de tabelas distintas (`LeitoEstado` para limpar a reserva do leito antigo e criar no novo, e `SolicitacaoLeito` para atualizar o destino). Um endpoint dedicado simplifica a validação de permissões, a validação de disponibilidade do novo leito e garante a atomicidade da operação.

### 2. Fluxo de Atualização no Banco de Dados
Para garantir a consistência das tabelas, a rotina de remanejamento no backend executará os seguintes passos em transação:
1. Buscar os detalhes da reserva atual na tabela `leito_estados` associada ao `solicitacao_id`.
2. Remover a reserva no leito de origem (`limpar_reserva_por_solicitacao`).
3. Registrar a reserva no leito de destino (`salvar_reserva`).
4. Atualizar o campo `destino` da solicitação na tabela `solicitacoes_leito` para `Leito {novo_leito_id}`.

### 3. Exibição de Erros em Conflitos de Ocupação
Caso o novo leito selecionado já possua outra reserva ou esteja ocupado de fato no AGHU, a transação deve ser recusada e retornar HTTP 400 informando o motivo.

## Risks / Trade-offs

- **[Risco] Reservas Órfãs** → Se o processo falhar na metade, a solicitação pode apontar para um leito enquanto a tabela `LeitoEstado` aponta para outro (ou fica vazia).
  - *Mitigação*: Executar todas as operações de banco sob o mesmo bloco de transação (`async with session.begin():` ou fluxo sequencial garantido no SQLite local).
- **[Risco] Concorrência** → Dois usuários tentarem reservar o mesmo leito simultaneamente durante o remanejamento.
  - *Mitigação*: Validar a disponibilidade do leito alvo imediatamente antes de salvar a nova reserva.
