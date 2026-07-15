## 1. Backend (Regras de Negócio e Histórico)

- [x] 1.1 Implementar a restrição de data de cirurgia retroativa em `criar_solicitacao` e `editar_solicitacao` (troca de prontuário) de `SolicitacaoLeitoController`.
- [x] 1.2 Atualizar o fluxo de swap em `editar_solicitacao` para definir de forma dinâmica o motivo do cancelamento (`Alteração de Prioridade pós Solicitação` vs `Alteração de Prioridade pós Reserva de Leito`) baseado no status anterior.
- [x] 1.3 Incluir nos logs do histórico de swap o detalhamento indicando que o prontuário de origem foi substituído pelo de destino no formato `(Prontuário X foi substituído pelo Prontuário Y)`.
- [x] 1.4 Garantir que o log de reserva automática gerado no swap use operador `"Sistema"`.
- [x] 1.5 Corrigir o mapeamento de tipos de histórico em `HistoricoProvider.listar` para buscar tipos agregados corretos em `"solicitacao"` e `"cancelamento"`.

## 2. Frontend (Histórico e Filtros)

- [x] 2.1 Ajustar a tela do histórico (`frontend/src/views/Historico.vue`) para exibir opções coerentes de filtro no select e testar o funcionamento integrado.
- [x] 2.2 Validar e testar a build de produção local com `npm run build`.
