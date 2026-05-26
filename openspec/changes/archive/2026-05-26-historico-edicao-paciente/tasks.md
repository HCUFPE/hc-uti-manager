## 1. Backend Changes (Controller & Router)

- [x] 1.1 Atualizar a assinatura do método `editar_solicitacao` em `src/controllers/solicitacao_leito_controller.py` para aceitar o parâmetro `username` (operador logado).
- [x] 1.2 Implementar no método `editar_solicitacao` a detecção de troca de prontuário: consultar AGHU para o novo prontuário, criar nova solicitação, cancelar a antiga (status "Cancelada" e motivo "Alteração de Prioridade pós Reserva de Leito") e transferir atomicamente no SQLite (`LeitoEstado`) a reserva física do leito se a vaga original já estivesse reservada.
- [x] 1.3 Implementar o registro detalhado das ações no histórico (`HistoricoProvider`) diretamente no controller quando for detectada a troca de paciente (registrando cancelamento, nova criação e transferência de reserva com o operador e detalhes descritivos corretos).
- [x] 1.4 Atualizar a rota `PATCH /api/solicitacoes/{sol_id}` em `src/routers/solicitacoes_leito.py` para extrair o `username` do token decodificado do usuário logado e repassá-lo para o controller.

## 2. Verification and Auditing

- [x] 2.1 Criar um script de teste automatizado para validar o fluxo de troca de paciente na edição (cancellation, criação, portabilidade de leito e histórico).
- [x] 2.2 Verificar e auditar todos os outros logs de ações do sistema para garantir que capturam corretamente a data/hora, operador e ação descritiva.
