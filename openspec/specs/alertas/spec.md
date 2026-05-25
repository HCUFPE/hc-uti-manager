# alertas Specification

## Purpose
TBD - created by archiving change corrigir-alertas-duplicados. Update Purpose after archive.
## Requirements
### Requirement: Prevenção de Alertas Duplicados
O sistema MUST garantir que alertas gerados a partir do histórico de ações ou estados de leitos não sejam duplicados quando a rotina de sincronização for executada múltiplas vezes.

#### Scenario: Sincronização repetida de histórico
- **WHEN** a rotina de geração de alertas é executada repetidamente para os mesmos eventos de histórico com pequenas variações de milissegundos
- **THEN** o sistema SHALL identificar que o alerta já existe no banco e não criar um novo registro duplicado

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

