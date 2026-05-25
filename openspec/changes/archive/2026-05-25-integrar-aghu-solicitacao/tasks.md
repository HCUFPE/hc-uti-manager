## 1. Database and Models (Backend)

- [x] 1.1 Atualizar o modelo `SolicitacaoLeito` em `src/models/solicitacao_leito.py` adicionando os campos `nome`, `procedimento` e `hora_cirurgia`.
- [x] 1.2 Criar um script de ajuste para adicionar as colunas `nome`, `procedimento` e `hora_cirurgia` na tabela `solicitacoes_leito` do banco SQLite atual para preservar os dados existentes.

## 2. AGHU Query and Provider (Backend)

- [x] 2.1 Criar a pasta `src/providers/sql/solicitacao` e adicionar o arquivo `obter_cirurgia_aghu.sql` contendo a query SQL fornecida para consulta ao AGHU.
- [x] 2.2 Implementar a classe `AghuCirurgiaProvider` em `src/providers/implementations/aghu_cirurgia_provider.py` para carregar a query SQL e executá-la no banco do AGHU (PostgreSQL).
- [x] 2.3 Atualizar o arquivo `src/dependencies.py` para instanciar e injetar o `AghuCirurgiaProvider` nas dependências necessárias.

## 3. Controller and Endpoints (Backend)

- [x] 3.1 Adicionar a rota `GET /api/solicitacoes/consultar-aghu/{prontuario}` em `src/routers/solicitacoes_leito.py`.
- [x] 3.2 Implementar a lógica de consulta ao AGHU em `SolicitacaoLeitoController`, calculando a idade a partir da data de nascimento, mapeando o turno a partir da hora de início e definindo o tipo do leito.
- [x] 3.3 Atualizar a lógica de `_sincronizar_prioridades` no controller para ordenar de forma cronológica pelo horário de início (`hora_cirurgia`) e recalcular as prioridades (P1, P2, P3...) dinamicamente.
- [x] 3.4 Atualizar o método `criar_solicitacao` do controller para validar os dados demográficos e cirúrgicos resgatados do AGHU antes de criar o registro no banco local.

## 4. Frontend Integration

- [x] 4.1 Modificar a ordenação em `frontend/src/views/Solicitacoes.vue` (`solicitacoesFiltradas`) para usar o campo `hora_cirurgia` no desempate da ordenação visual no mesmo dia e turno.
- [x] 4.2 Modificar o modal de nova solicitação em `frontend/src/views/Solicitacoes.vue` simplificando a interface para exibir inicialmente apenas os campos de Prontuário e Prioridade.
- [x] 4.3 Adicionar gatilho/chamada de API no frontend para buscar os dados no preenchimento do prontuário, mostrando uma seção de visualização somente leitura dos dados demográficos e cirúrgicos encontrados.
- [x] 4.4 Atualizar o comportamento do botão salvar para enviar apenas a solicitação preenchida via auto-população, incluindo o tratamento de erros amigável para prontuários não localizados.

## 5. Verification

- [x] 5.1 Criar um script de teste e validar se o preenchimento automático a partir de prontuários conhecidos funciona de forma consistente no banco local e histórico.
