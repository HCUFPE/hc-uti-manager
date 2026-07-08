## 1. Banco de Dados e Modelos

- [x] 1.1 Criar o arquivo `src/models/historico_ocupacao.py` com a definição do modelo `HistoricoOcupacao`.
- [x] 1.2 Importar e registrar o modelo `HistoricoOcupacao` no metadata da aplicação no `src/main.py`.

## 2. Tarefa em Background de Fechamento Diário

- [x] 2.1 Implementar no `src/main.py` a rotina em background que calcula a taxa real de ocupação da UTI diariamente e a persiste no SQLite.
- [x] 2.2 Iniciar a tarefa de fechamento diário como um `asyncio.create_task` durante o evento de startup do FastAPI (`lifespan`).

## 3. Integração com Provedor de Indicadores

- [x] 3.1 Modificar o método correspondente no `src/providers/implementations/indicadores_provider.py` para ler a ocupação real da semana atual de `historico_ocupacao`.

## 4. Testes e Publicação

- [x] 4.1 Validar a inicialização do banco SQLite localmente e verificar que a nova tabela é criada automaticamente.
- [ ] 4.2 Commit, push e deploy com rebuild na VM.
