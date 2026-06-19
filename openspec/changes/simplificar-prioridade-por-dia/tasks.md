## 1. Implementação no Backend

- [x] 1.1 Modificar o método `_sincronizar_prioridades` em `src/controllers/solicitacao_leito_controller.py` para remover a segmentação por `turno` e filtrar apenas por `data_cirurgia`
- [x] 1.2 Atualizar as chamadas a `_sincronizar_prioridades` em `criar_solicitacao` para remover o parâmetro `turno`
- [x] 1.3 Atualizar as chamadas a `_sincronizar_prioridades` em `atualizar_status` para remover o parâmetro `turno`
- [x] 1.4 Atualizar as chamadas a `_sincronizar_prioridades` em `editar_solicitacao` para remover o parâmetro `turno`
- [x] 1.5 Atualizar as chamadas a `_sincronizar_prioridades` em `cancelar_solicitacao` para remover o parâmetro `turno`
- [x] 1.6 Atualizar as chamadas a `_sincronizar_prioridades` em `reservar_leito` para remover o parâmetro `turno`
- [x] 1.7 Atualizar as chamadas a `_sincronizar_prioridades` em `cancelar_reserva` para remover o parâmetro `turno`

## 2. Implementação no Frontend

- [x] 2.1 Atualizar o computed `solicitacoesFiltradas` em `frontend/src/views/Solicitacoes.vue` para remover a ordenação por turno, mantendo os demais critérios de ordenação

## 3. Validação e Implantação

- [x] 3.1 Executar testes automatizados locais para certificar de que a lógica de ordenação e deslocamento funciona sem erros
- [ ] 3.2 Submeter as alterações, fazer push para o repositório remoto e implantar na máquina virtual (VM) de produção
