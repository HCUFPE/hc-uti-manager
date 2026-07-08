## Context

A UTI necessita de flexibilidade para remanejar leitos de pacientes cujas vagas já foram reservadas, permitindo a troca direta de leitos entre dois pacientes que já possuam reservas.

## Decisions

### 1. Parâmetro no Endpoint de Leitos
Adicionar `incluir_reservados: bool = False` no endpoint `/api/leitos/disponiveis` (e no controller correspondente). Isso permite que a consulta retorne leitos vazios ou com alta solicitada mesmo que já possuam reserva. Esses leitos virão com os atributos `ja_tem_reserva = True` e `prontuario_proximo` preenchidos.

### 2. Transação de Troca (Swap) no Backend
Na rota de remanejar (`POST /api/solicitacoes/{sol_id}/remanejar-reserva`):
1. Verificar se o leito destino possui uma reserva de outro paciente.
2. Se possuir, obter a solicitação destino associada.
3. Trocar os dados das colunas (`prontuario_proximo`, `idade_proximo`, `especialidade_proximo`, `solicitacao_id`) de ambos os registros na tabela `leito_estados` associados ao leito de origem e leito de destino.
4. Salvar e persistir a alteração.
5. Atualizar o campo `destino` em ambas as solicitações.

### 3. Interface no Frontend
Em `frontend/src/views/Home.vue` e `frontend/src/views/Solicitacoes.vue`:
- Adicionar o parâmetro `?incluir_reservados=true` na chamada de leitos disponíveis quando a ação for um remanejamento.
- Exibir uma sinalização visual clara (`Reservado (Prontuário X) - Trocar` em tom âmbar/amarelo) para indicar que a seleção daquele leito resultará em uma troca direta de reservas de leitos entre os dois pacientes.
