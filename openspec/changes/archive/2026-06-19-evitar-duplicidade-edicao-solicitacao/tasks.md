## 1. Implementação no Backend

- [x] 1.1 Atualizar `editar_solicitacao` em `src/controllers/solicitacao_leito_controller.py` para buscar solicitações ativas do paciente de destino ao alterar o prontuário.
- [x] 1.2 Implementar bloqueio se o paciente de destino já possuir uma reserva de leito ativa ("Reservado").
- [x] 1.3 Implementar a lógica de mesclagem promovendo a solicitação pendente do paciente de destino para "Reservado" (caso a de origem estivesse reservada), herdando o leito.
- [x] 1.4 Implementar a transferência de reserva física no banco SQLite (`LeitoEstado`) e cancelamento da solicitação original do paciente de origem.
- [x] 1.5 Gravar as ações correspondentes no histórico de auditoria (Logs).

## 2. Validação e Testes

- [x] 2.1 Criar script de teste em `scratch/` para validar a mesclagem inteligente de solicitação pendente existente.
- [x] 2.2 Criar script de teste em `scratch/` para validar a rejeição de troca se o novo paciente já possuir reserva de leito ativa.
- [x] 2.3 Executar todos os testes automatizados locais para certificar de que as regras funcionam conforme especificado.
