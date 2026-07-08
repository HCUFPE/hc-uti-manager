## Why

Atualmente, o remanejamento ("Mudar Leito") de uma solicitação de leito reservada está limitado a transferir o paciente apenas para leitos que estejam completamente disponíveis (sem nenhuma reserva ativa). 

Em situações de alta ocupação, a equipe da UTI precisa de flexibilidade para reorganizar e otimizar a alocação de leitos realizando a troca direta (swap) de reservas de dois pacientes que já possuem leitos reservados.

## What Changes

- **Endpoint de Listagem de Leitos**: Ajustar o endpoint `/api/leitos/disponiveis` para aceitar um parâmetro `incluir_reservados` (boolean). Se `true`, retornará também os leitos que já possuem reserva ativa, marcando-os com `ja_tem_reserva = true` e o prontuário correspondente, para que possam ser exibidos como alvos de troca.
- **Lógica de Remanejamento no Backend**: Modificar o método `remanejar_reserva` em `SolicitacaoLeitoController` para que, ao tentar remanejar uma solicitação para um leito já reservado por outra pessoa:
  - Identifique a solicitação e o paciente que ocupa a reserva no leito destino.
  - Faça a troca (swap) dos dados de reserva entre os dois leitos no banco SQLite.
  - Atualize a propriedade `destino` de ambas as solicitações.
- **Interface Gráfica (Frontend)**:
  - Atualizar os modais de "Mudar Leito" em `Home.vue` e `Solicitacoes.vue` para listar também leitos reservados quando o remanejamento estiver em andamento.
  - Exibir um rótulo indicativo claro nos leitos já reservados (ex: *"Reservado (Prontuário X) - Trocar"*).

## Capabilities

### Modified Capabilities
- `internacao-leitos`: Gestão de alocação de leitos e possibilidade de troca de reservas ativas entre solicitações.

## Impact

- **Backend**:
  - `src/routers/leito.py`: Adicionar parâmetro `incluir_reservados` na rota GET.
  - `src/controllers/leitos_controller.py`: Ajustar filtragem de leitos disponíveis com base no novo parâmetro.
  - `src/controllers/solicitacao_leito_controller.py`: Implementar lógica de troca/swap de reservas no método `remanejar_reserva`.
- **Frontend**:
  - `frontend/src/views/Home.vue` & `frontend/src/views/Solicitacoes.vue`: Ajustar a chamada de leitos disponíveis para passar o parâmetro de inclusão de reservados e exibir visualmente a opção de troca.
