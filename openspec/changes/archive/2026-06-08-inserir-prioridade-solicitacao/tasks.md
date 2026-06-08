## 1. Implementação no Backend

- [x] 1.1 Atualizar o método `criar_solicitacao` em `src/controllers/solicitacao_leito_controller.py` para extrair e persistir a prioridade informada no payload de criação.
- [x] 1.2 Chamar `_sincronizar_prioridades` passando os parâmetros de foco correspondentes à nova solicitação e à prioridade informada.

## 2. Validação

- [x] 2.1 Criar um script de teste em `scratch/test_prioridade_criacao.py` que valide a gravação e reordenamento correto no ato de criação.
- [x] 2.2 Executar o teste localmente.
