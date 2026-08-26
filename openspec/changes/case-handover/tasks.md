## 1. Banco de Dados e Modelo

- [x] 1.1 Adicionar a coluna `passagem_caso = Column(String, nullable=True)` ao modelo `SolicitacaoLeito` em `src/models/solicitacao_leito.py`.
- [x] 1.2 Criar e rodar uma migração do Alembic no banco local para incluir a coluna `passagem_caso` na tabela `solicitacoes_leito`.
- [x] 1.3 Adaptar a serialização/deserialização no método `to_dict` do modelo `SolicitacaoLeito` para converter a string JSON gravada de volta para objeto estruturado, se for um JSON válido.

## 2. Implementação no Backend (API e Validações)

- [x] 2.1 Criar Pydantic Schemas detalhados representando o formulário estruturado e todas as suas validações em `src/models/solicitacao_leito.py` ou em arquivo de schemas.
- [x] 2.2 Atualizar o endpoint `POST /api/solicitacoes/{sol_id}/cirurgia-finalizada` para aceitar e validar o novo payload estruturado (Pydantic), serializando-o para string JSON antes de salvar.
- [x] 2.3 Criar o endpoint `PUT /api/solicitacoes/{sol_id}/passagem-caso` no controller e router, aplicando a regra que impede edições após a UTI ter efetuado a validação da liberação.

## 3. Frontend do Solicitante (Formulário e Edição)

- [x] 3.1 Construir a interface visual do formulário estruturado de passagem de caso (Checkboxes, inputs e condicionais como "Cirurgia não realizada") no modal de finalização em `Solicitacoes.vue`.
- [x] 3.2 Implementar a reatividade de validação do frontend para habilitar o botão "Salvar e Finalizar" apenas com todos os critérios obrigatórios satisfeitos.
- [x] 3.3 Adicionar o botão "Editar Passagem" no painel de solicitações e integrá-lo com o modal para atualizar a passagem de caso antes da liberação pela UTI.

## 4. Frontend da UTI (Leitura e Visualização Histórica)

- [x] 4.1 Adaptar o modal de checkpoint de liberação da UTI em `BedCard.vue` para renderizar os dados estruturados da passagem de caso de forma clara e limpa.
- [x] 4.2 Incluir o botão permanente "Ver Passagem de Caso" nos cards de leitos na UTI para permitir a leitura histórica e modo somente leitura a qualquer momento.
- [x] 4.3 Disponibilizar a visualização da passagem de caso histórica a partir da tela de auditoria (Histórico de Ações), com tratamento adequado para registros legados.

## 5. Testes e Validação

- [x] 5.1 Criar testes de integração simulando a submissão correta, submissão inválida, edição e consulta de passagem de caso estruturada.
