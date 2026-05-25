## Why

Atualmente, não existe comunicação formal no sistema para notificar a UTI de que um paciente de cirurgia eletiva (solicitada por COB, HEM ou BC) finalizou o procedimento e está pronto para transporte, nem para a UTI notificar o solicitante de que o leito está liberado para recebimento. Esse novo fluxo otimiza a coordenação de transporte de pacientes críticos.

## What Changes

- **Botão "Cirurgia Finalizada"**: Adição de um botão na visualização de solicitações de leitos dos solicitantes (COB, HEM, BC) para marcar a cirurgia como concluída.
- **Mudança de Estado Visual da Reserva (Amarelo)**: Ao finalizar a cirurgia, a cor da reserva no painel da UTI mudará para amarelo, indicando que o paciente está pronto para encaminhamento.
- **Botão "Liberar Encaminhamento"**: Exibição de um botão na tela de leitos da UTI para que a equipe libere a transferência do paciente.
- **Mudança de Estado Visual da Reserva (Verde)**: Após a liberação pela UTI, a cor da reserva mudará para verde, indicando que o transporte foi autorizado.
- **Alertas Bidirecionais**:
  - Alerta para a UTI quando o solicitante finaliza a cirurgia: `"Prontuário {prontuario} pronto para ser encaminhado para UTI (Cirurgia Finalizada)"`.
  - Alerta para o Solicitante correspondente quando a UTI libera o encaminhamento.

## Capabilities

### New Capabilities

*(Nenhuma)*

### Modified Capabilities

- `solicitacao-leitos`: Inclusão do botão de finalização de cirurgia nas solicitações reservadas e novo status visual.
- `internacao-leitos`: Adaptação do censo de leitos/reserva para refletir os estados amarelo (Cirurgia Finalizada) e verde (Encaminhamento Liberado), e adição do botão de liberação pela UTI.
- `alertas`: Geração de novos alertas automáticos para UTI e solicitantes durante o fluxo de encaminhamento.

## Impact

- **Backend**:
  - Ajuste no modelo/tabela de solicitações ou de reservas de leitos para armazenar os novos estados do encaminhamento (ex: `cirurgia_finalizada` e `encaminhamento_liberado`).
  - Criação ou ajuste de endpoints para marcar cirurgia finalizada e liberar encaminhamento.
  - Geração de histórico correspondente para o processamento de alertas automáticos.
- **Frontend**:
  - Modificação em `Solicitacoes.vue` para exibir o botão e atualizar o estado do solicitante.
  - Modificação em `Home.vue` (card do leito) para atualizar cores das reservas e exibir o botão de liberação de encaminhamento para a UTI.
