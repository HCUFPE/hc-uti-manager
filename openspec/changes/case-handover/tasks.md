## 1. Banco de Dados e Modelo

- [ ] 1.1 Adicionar a coluna `passagem_caso = Column(String, nullable=True)` ao modelo `SolicitacaoLeito` em `src/models/solicitacao_leito.py`.
- [ ] 1.2 Criar e rodar uma migração do Alembic no banco local para incluir a coluna `passagem_caso` na tabela `solicitacoes_leito`.

## 2. Implementação no Backend (API)

- [ ] 2.1 Ajustar a rota de finalizar cirurgia em `src/routers/solicitacoes_leito.py` para aceitar um payload opcional com `passagem_caso`.
- [ ] 2.2 Atualizar o controller correspondente em `src/controllers/solicitacao_leito_controller.py` para gravar a string no banco ao finalizar a cirurgia.
- [ ] 2.3 Ajustar a rota de listagem de leitos (`listar_leitos` em `src/controllers/leitos_controller.py` ou `src/providers/implementations/leito_estado_provider.py`) para recuperar e expor a passagem de caso no payload JSON do card de leito reservado.

## 3. Frontend do Solicitante (Conclusão de Cirurgia)

- [ ] 3.1 Adicionar a pergunta opcional ("Gostaria de preencher passagem de caso?") no botão "Finalizar Cirurgia" em `Home.vue`.
- [ ] 3.2 Implementar a caixa de texto (`textarea`) expansível no modal do frontend para preenchimento.
- [ ] 3.3 Integrar o salvamento do campo `passagem_caso` no corpo da requisição enviada ao backend.

## 4. Frontend da UTI (Checkpoint na Liberação)

- [ ] 4.1 Modificar o comportamento do botão "Liberar Encaminhamento" em `BedCard.vue`.
- [ ] 4.2 Exibir o modal de checkpoint com as informações clínicas da Passagem de Caso se ela estiver preenchida.
- [ ] 4.3 Implementar a ação "Ciente e Liberar" para confirmar e efetuar a liberação, e a ação "Cancelar" para abortar e fechar o modal.

- [ ] 5.1 Criar um script de teste de integração para simular o fluxo completo da API de passagem de caso.
- [ ] 5.2 Testar manualmente o fluxo completo no navegador.

## 6. Sincronização de Documentação e Requisitos

- [ ] 6.1 Atualizar os requisitos em `docs/projeto_inicial/02-requisitos.md` com a funcionalidade de Passagem de Caso.
- [ ] 6.2 Atualizar os fluxos e casos de uso em `docs/projeto_inicial/03-casos-uso.md`.
- [ ] 6.3 Sincronizar o modelo de dados físico/lógico em `docs/projeto_inicial/04-modelo-dados.md` e payloads de tela em `docs/data-model.md`.
- [ ] 6.4 Atualizar os contratos e endpoints de API em `docs/projeto_inicial/05-interfaces.md`.
