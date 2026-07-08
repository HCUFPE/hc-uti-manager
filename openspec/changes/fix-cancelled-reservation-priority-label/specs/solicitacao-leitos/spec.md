## MODIFIED Requirements

### Requirement: Cancelamento de Reserva Atualiza Fila
Ao cancelar uma reserva de leito, as prioridades da fila correspondente devem ser recalculadas para evitar duplicidades ou buracos.

#### Scenario: Sincronização automática pós cancelamento de reserva
- **WHEN** o usuário cancela a reserva de um leito através do painel de leitos
- **THEN** a solicitação de leito correspondente SHALL retornar ao status "Pendente" e ter seu destino limpo
- **THEN** o sistema SHALL recalcular as prioridades (`P1`, `P2`, `P3`...) para todas as solicitações pendentes daquela mesma data de cirurgia, ajustando os valores no banco de dados

### Requirement: Rótulo do Botão de Conclusão de Cirurgia
O botão de ação rápida para concluir uma cirurgia a partir do painel de reservados deve usar terminologia imperativa de ação.

#### Scenario: Rótulo do botão de cirurgia para pacotes reservados
- **WHEN** a solicitação de leito está no status "Reservado" e com a cirurgia ainda não concluída
- **THEN** o botão correspondente SHALL exibir o texto de ação "Finalizar Cirurgia"
