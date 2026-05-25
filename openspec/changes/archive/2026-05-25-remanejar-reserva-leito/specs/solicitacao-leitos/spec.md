## ADDED Requirements

### Requirement: Remanejamento de Reserva de Leito pela UTI
O sistema MUST permitir que a equipe da UTI e administradores alterem diretamente o leito reservado de uma solicitação com status "Reservado" para outro leito disponível.

#### Scenario: Remanejamento de leito de reserva
- **WHEN** o usuário da UTI visualiza uma solicitação com leito reservado e solicita a alteração do leito destino, selecionando um novo leito vago
- **THEN** o sistema remove a reserva do leito original, transfere-a para o novo leito de destino e atualiza as informações de destino da solicitação, mantendo o status "Reservado" e registrando a mudança no histórico
