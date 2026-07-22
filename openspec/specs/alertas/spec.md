# alertas Specification

## Purpose
TBD - created by archiving change corrigir-alertas-duplicados. Update Purpose after archive.
## Requirements
### Requirement: Prevenção de Alertas Duplicados
O sistema MUST garantir que alertas gerados a partir do histórico de ações ou estados de leitos não sejam duplicados quando a rotina de sincronização for executada múltiplas vezes. A comparação de data/hora do alerta com a do histórico SHALL desconsiderar variações de fuso horário e precisão de microssegundos para evitar duplicidade. Adicionalmente, a verificação de data para hoje SHALL normalizar de forma robusta e unificada os formatos de data (`DD-MM-YYYY`, `DD/MM/YYYY` e `YYYY-MM-DD`).

#### Scenario: Sincronização repetida de histórico
- **WHEN** a rotina de geração de alertas é executada repetidamente para os mesmos eventos de histórico com pequenas variações de fuso horário ou microssegundos
- **THEN** o sistema SHALL identificar que o alerta já existe no banco e não criar um novo registro duplicado

#### Scenario: Validação de data em formatos mistos
- **WHEN** a rotina de geração de alertas valida se uma cirurgia é para hoje a partir de dados em formatos `DD-MM-YYYY` (SQLite local) ou `DD/MM/YYYY`
- **THEN** o sistema SHALL converter a data para `YYYY-MM-DD` e realizar a comparação com sucesso

### Requirement: Preservação de Histórico de Alertas Gargalo
O sistema MUST manter persistidos todos os alertas gerados no sistema (incluindo as categorias "Gargalo", "Infeccioso", "Permanencia", "Limpeza" ou qualquer outra), mesmo que a condição de origem não seja mais ativa ou a janela de 24 horas tenha expirado, proibindo qualquer exclusão automática de registros de alerta.

#### Scenario: Sincronização após término de pendência
- **WHEN** a sincronização é executada e uma pendência de alta, infecção, permanência ou limpeza deixa de estar ativa
- **THEN** o sistema SHALL manter os alertas correspondentes na tabela de alertas, sem excluir nenhum registro de alerta

### Requirement: Simplificação Visual e Unificação de Alertas
O sistema MUST unificar o visual de todos os alertas no frontend de forma que sejam apresentados com o mesmo padrão visual, cores, ícones e comportamento, independente do tipo original (crítico, aviso ou informativo) ou categoria.

#### Scenario: Exibição de alertas de diferentes tipos
- **WHEN** o usuário visualiza a lista de alertas ou o popover de notificações rápidas contendo alertas dos tipos crítico, aviso ou informativo
- **THEN** o frontend SHALL renderizar todos eles com o mesmo layout, a mesma cor azul/informativa, e o mesmo ícone padrão

### Requirement: Alerta de Cancelamento de Alta pelo NIR
O sistema MUST gerar uma notificação/alerta direcionado para a equipe da UTI toda vez que o perfil NIR (ou Administradores sob esse contexto) cancelar uma solicitação de alta de paciente.

#### Scenario: Geração de alerta para a UTI
- **WHEN** a rotina de sincronização de alertas detecta no histórico de ações que uma alta foi cancelada pelo NIR
- **THEN** o sistema SHALL criar um novo alerta com o título "Cancelamento de Alta pelo NIR", com o perfil alvo definido como nulo (visível para UTI) e contendo o motivo correspondente

### Requirement: Alerta de Cirurgia Finalizada para a UTI
O sistema MUST gerar um alerta automático direcionado para o perfil UTI sempre que um solicitante sinalizar a conclusão de uma cirurgia.

#### Scenario: Geração de alerta de cirurgia finalizada
- **WHEN** a rotina de sincronização de alertas detecta que uma cirurgia foi finalizada para um leito reservado
- **THEN** o sistema SHALL gerar um alerta do tipo "aviso" com título "Cirurgia Finalizada" e mensagem contendo o prontuário do paciente pronto para encaminhamento direcionado para a UTI (perfil_alvo = None)

### Requirement: Alerta de Encaminhamento Liberado para o Solicitante
O sistema MUST gerar um alerta automático direcionado para o setor solicitante original (COB, HEM, ou BC) quando a UTI autorizar o encaminhamento do paciente.

#### Scenario: Geração de alerta de encaminhamento autorizado
- **WHEN** a rotina de sincronização de alertas detecta que a UTI liberou o encaminhamento para uma reserva
- **THEN** o sistema SHALL gerar um alerta do tipo "info" direcionado especificamente para o setor solicitante original (perfil_alvo = setor solicitante) informando que o paciente já pode ser transferido

### Requirement: Alerta de Liberação Cancelada para o Solicitante
O sistema MUST gerar um alerta automático direcionado para o setor solicitante original (COB, HEM, ou BC) quando a UTI cancelar a liberação de encaminhamento do paciente.

#### Scenario: Geração de alerta de liberação de encaminhamento cancelada
- **WHEN** a rotina de sincronização de alertas detecta que a UTI cancelou a liberação de encaminhamento para uma reserva
- **THEN** o sistema SHALL gerar um alerta do tipo "critico" direcionado especificamente para o setor solicitante original (perfil_alvo = setor solicitante) informando que a liberação de encaminhamento foi cancelada e o transporte deve ser suspenso

### Requirement: Alerta Sonoro para o NIR
O sistema MUST emitir um alerta sonoro periódico na tela inicial para operadores do NIR quando houver notificações pendentes de ciência.

#### Scenario: Novo alerta chega ao NIR e toca o bipe
- **WHEN** o usuário com perfil NIR possui 1 ou mais alertas não lidos (`unreadAlertsCount > 0`)
- **THEN** o sistema SHALL reproduzir a sequência de bipes a cada 30 segundos

#### Scenario: Operador do NIR dá ciência e o som cessa
- **WHEN** o operador do NIR marca todos os alertas como lidos (`unreadAlertsCount` vai a 0)
- **THEN** o sistema SHALL parar de emitir o alerta sonoro

