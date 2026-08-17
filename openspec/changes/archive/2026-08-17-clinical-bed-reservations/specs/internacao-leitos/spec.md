## ADDED Requirements

### Requirement: Bloqueio Genérico de Leitos para Clínico/COB/HEM
O sistema MUST permitir que a equipe da UTI e administradores marquem leitos desocupados como reservados para Clínico/COB/HEM. Esse estado deve persistir localmente no SQLite e ser exposto na API.

#### Scenario: Ativação de bloqueio de leito com sucesso
- **WHEN** o usuário com perfil UTI solicita o bloqueio genérico de um leito desocupado
- **THEN** o sistema define a flag `bloqueado_clinico` como True, grava o log de histórico e muda a resposta do painel de leitos

### Requirement: Cancelar Reserva de Leito Clínico
O sistema MUST permitir que a equipe da UTI cancele manualmente a reserva clínica genérica, retornando o leito ao status de desocupado comum.

#### Scenario: Cancelamento de reserva com sucesso
- **WHEN** o usuário com perfil UTI solicita o cancelamento da reserva de um leito Clínico
- **THEN** o sistema define a flag `bloqueado_clinico` como False, grava o log de histórico de cancelamento (`cancelamento_reserva`) e torna o leito disponível para reservas gerais

### Requirement: Auto-limpeza de Bloqueio Clínico na Admissão Física
Se um leito com bloqueio ativo for ocupado no AGHU por qualquer prontuário (entrada de paciente), o sistema MUST limpar a flag de bloqueio de forma automática.

#### Scenario: Paciente entra em leito bloqueado
- **WHEN** a rotina de sincronização do censo detecta que um leito com `bloqueado_clinico == True` passou a estar ocupado no AGHU
- **THEN** o sistema limpa a flag `bloqueado_clinico` (passando a False) e atualiza o estado local do leito
