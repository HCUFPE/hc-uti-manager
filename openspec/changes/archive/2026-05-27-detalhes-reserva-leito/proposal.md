## Why

Atualmente, na visão geral de leitos, os cards dos leitos com reserva ativa ("Próximo Paciente") exibem apenas o prontuário, a idade, a especialidade, a data da cirurgia e o turno. Adicionar o nome do paciente e o horário previsto da cirurgia (no formato `DD/MM/AAAA - HH:MM`) facilita a identificação rápida e o acompanhamento logístico pelas equipes da UTI e do NIR diretamente na tela principal, sem necessidade de navegar até a fila de solicitações.

## What Changes

- Modificar o controller do backend (`LeitosController.listar_leitos`) para extrair os campos `nome_proximo` (nome do paciente reservado) e `hora_cirurgia_proximo` (horário da cirurgia) da solicitação vinculada ao leito.
- Atualizar a interface do card de leitos (`BedCard.vue` e `Home.vue`) para mapear e exibir os campos adicionais:
  - Exibir o nome do próximo paciente em tamanho pequeno entre o prontuário e a idade.
  - Exibir o horário da cirurgia concatenado com a data no formato `DD/MM/AAAA - HH:MM` no pequeno bloco de cirurgia.

## Capabilities

### New Capabilities

<!-- Nenhuma nova capacidade -->

### Modified Capabilities

- `internacao-leitos`: A visualização de reservas de leitos físicos deve expor o nome do paciente e a data/hora completa da cirurgia programada.

## Impact

- Backend: `src/controllers/leitos_controller.py`
- Frontend: `frontend/src/views/Home.vue`, `frontend/src/components/BedCard.vue`
