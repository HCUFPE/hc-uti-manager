## 1. Implementação no Backend

- [x] 1.1 Incluir validação contra duplicidade de prontuários ativos (Pendente/Reservado) no método `criar_solicitacao` de `src/controllers/solicitacao_leito_controller.py`.
- [x] 1.2 Corrigir o filtro de exclusão em `_sincronizar_prioridades` de `src/controllers/solicitacao_leito_controller.py` para não omitir solicitações focadas sem prioridade desejada.

## 2. Validação

- [x] 2.1 Criar um script de teste em `scratch/test_duplicidade_e_zerados.py` para testar os dois cenários: bloqueio de prontuário duplicado e nova solicitação sem prioridade manual sendo incluída corretamente na fila.
- [x] 2.2 Executar o teste localmente.
