## 1. Implementação no Backend

- [x] 1.1 Refatorar o método `_sincronizar_prioridades` em `src/controllers/solicitacao_leito_controller.py` para receber os parâmetros `sol_id_foco` e `prioridade_desejada` e aplicá-los na ordenação da fila.
- [x] 1.2 Garantir que o deslocamento das outras solicitações mantenha a ordem cronológica relativa (hora da cirurgia e tempo de criação).

## 2. Teste e Validação

- [x] 2.1 Criar um script de teste para validar o cenário de ajuste manual de prioridade.
- [x] 2.2 Executar o script de teste localmente e garantir que a prioridade manual se mantenha e os outros registros sejam deslocados corretamente.
