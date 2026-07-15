## Context

O sistema gerencia as solicitações de leito para a UTI a partir de cirurgias agendadas no AGHU. Algumas inconsistências foram identificadas:
1. Data de cirurgia no passado sendo permitida no cadastro e edição/swap de pacientes.
2. Mensagem de cancelamento de swap estática ("Alteração de Prioridade pós Reserva de Leito") mesmo para solicitações que não possuíam reserva ativa (estavam Pendentes).
3. Falta de rastreabilidade de quais prontuários foram substituídos na ação de swap.
4. O operador das reservas geradas automaticamente pelo swap fica registrado como o solicitante (ex: do Bloco Cirúrgico), quando na verdade é uma ação automática do sistema.
5. Inconsistência de filtros de tipo no histórico no frontend (`Historico.vue`) em relação ao backend.

## Goals / Non-Goals

**Goals:**
- Validar e bloquear qualquer criação ou edição/swap com data de cirurgia anterior à data atual (comparando apenas dia, mês e ano).
- Atribuir o motivo correto de cancelamento no swap com base no status anterior (Pendente ou Reservado).
- Rastrear prontuários substituídos no log do histórico.
- Atribuir o operador `"Sistema"` no histórico de reserva automática gerada pelo swap.
- Harmonizar os filtros de tipo de histórico no frontend e backend.

**Non-Goals:**
- Mudar a lógica de prioridades ou fluxos de reserva manual.
- Modificar o banco do AGHU de produção.

## Decisions

### 1. Bloqueio de Cirurgia no Passado
- **Decisão**: Adicionar validação de data no método `criar_solicitacao` e `editar_solicitacao` (troca de prontuário) de `SolicitacaoLeitoController`. A validação converterá a string `data_cirurgia` para `date` e comparará com `date.today()`.
- **Mensagem**: Em caso de data retroativa, disparar `HTTPException(400, detail="Paciente não possui cirurgia agendada no AGHU")`.
- **Raciocínio**: Mantém a consistência no backend.

### 2. Motivo Dinâmico e Detalhes do Swap no Histórico
- **Decisão**: Em `editar_solicitacao` (fluxo de swap):
  - Verificar se `alvo.status == "Reservado"`. Em caso positivo, registrar o cancelamento com o motivo `"Alteração de Prioridade pós Reserva de Leito"`. Caso contrário (status `"Pendente"`), registrar como `"Alteração de Prioridade pós Solicitação"`.
  - Adicionar aos `detalhes` do log de exclusão e criação a frase: `"(Prontuário X foi substituído pelo Prontuário Y)"`.

### 3. Operador da Reserva Automática
- **Decisão**: Alterar a chamada de `historico.registrar` correspondente à reserva automática gerada no swap para usar explicitamente `operador="Sistema"`.

### 4. Harmonização de Filtros no Histórico
- **Decisão**:
  - No backend (`HistoricoProvider.listar`), se `tipo == "solicitacao"`, mapear na consulta para `["solicitacao", "nova_solicitacao", "conclusao"]`. Se `tipo == "cancelamento"`, mapear para `["cancelamento", "exclusao_solicitacao", "cancelamento_reserva"]`.
  - No frontend (`Historico.vue`), limpar a lista de opções do select e mapear os valores corretamente para as chamadas da API.

## Risks / Trade-offs

- **[Risco]**: A data do servidor ou do AGHU pode estar em fusos horários diferentes.
- **[Mitigação]**: Usar `datetime.now(timezone_local).date()` ou similar baseando-se na data local do sistema para evitar problemas de fuso horário.
