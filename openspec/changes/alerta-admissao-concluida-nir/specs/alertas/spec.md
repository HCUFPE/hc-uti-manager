## ADDED Requirements

### Requirement: Alerta de Admissão Concluída no AGHU para o NIR
O sistema MUST gerar automaticamente um alerta direcionado especificamente para o perfil NIR toda vez que a sincronização inteligente do censo detectar que um paciente (que possuía reserva ativa, cirurgia finalizada e encaminhamento liberado) foi fisicamente admitido no leito da UTI no AGHU.

#### Scenario: Geração automática de alerta de admissão concluída
- **WHEN** a sincronização inteligente do censo conclui automaticamente uma admissão no leito de UTI
- **THEN** o sistema SHALL criar um novo alerta com o título "Admissão Concluída (AGHU)" da categoria "Gargalo", contendo o nome e prontuário do paciente, direcionado para o perfil NIR (`perfil_alvo = "NIR"`)

### Requirement: Alerta Sonoro Diferenciado de Admissão para o NIR
O sistema MUST reproduzir um efeito sonoro (tom/melodia) diferente do bipe padrão do NIR sempre que houver algum alerta não lido do tipo "Admissão Concluída (AGHU)" pendente de ciência para o usuário com perfil NIR.

#### Scenario: Reprodução de som de admissão diferenciado no NIR
- **WHEN** o usuário com perfil NIR possui 1 ou mais alertas não lidos do tipo "Admissão Concluída (AGHU)" e nenhum alerta padrão pendente
- **THEN** o sistema SHALL reproduzir periodicamente (a cada 30 segundos) o arquivo de áudio diferenciado correspondente (ex: `admissao.mp3`)

#### Scenario: Prioridade para alertas padrão se houver ambos pendentes
- **WHEN** o usuário possui alertas padrão pendentes E alertas do tipo "Admissão Concluída (AGHU)" pendentes
- **THEN** o sistema SHALL priorizar a reprodução do bipe de alerta padrão (6 bipes rápidos) em vez da melodia de admissão

### Requirement: Estilo Visual Diferenciado para Alertas de Admissão no Frontend
O sistema MUST renderizar os alertas do tipo "Admissão Concluída (AGHU)" no frontend com um estilo visual, ícone e cor diferenciados (ex: padrão esmeralda/verde), destacando-os visualmente dos demais alertas informativos ou de aviso que usam a cor azul padrão.

#### Scenario: Exibição estilizada do alerta de admissão no frontend
- **WHEN** o usuário visualiza a lista de alertas ou as notificações rápidas
- **THEN** o frontend SHALL renderizar o alerta "Admissão Concluída (AGHU)" utilizando bordas e destaques na cor verde/esmeralda e um ícone de sucesso (ex: CheckCircleIcon)
