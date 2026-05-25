## Context

O sistema atualmente possui alertas com três níveis de severidade (`critico`, `aviso`, `info`) e diversas categorias (`Gargalo`, `Infeccioso`, `Permanencia`, `Limpeza`). Além disso, a rotina de sincronização de alertas descarta/deleta registros de alertas das categorias `Infeccioso`, `Permanencia` e `Limpeza` quando a condição que originou o alerta deixa de ser ativa. O usuário solicitou que todos os alertas tenham a mesma aparência visual (sem distinção de cores ou categorias) e que nenhum alerta seja deletado automaticamente, preservando o histórico completo.

## Goals / Non-Goals

**Goals:**
- Unificar o estilo visual, ícones e cores de todos os alertas na interface (`Alertas.vue` e `NotificationsPopover.vue`).
- Impedir qualquer exclusão automática de alertas na sincronização do backend (`alerta_controller.py`).

**Non-Goals:**
- Modificar o esquema de banco de dados (as tabelas e colunas permanecem as mesmas para preservar compatibilidade).
- Alterar as regras de geração de alertas (os alertas continuam sendo criados normalmente no banco, apenas não são apagados nem estilizados de forma diferente na tela).

## Decisions

- **Unificação Visual no Frontend**: Mapear todas as severidades (`critico`, `aviso`, `info`) para o mesmo estilo visual azul e ícone de informação (`InformationCircleIcon`) no componente `Alertas.vue`. Em `NotificationsPopover.vue`, mapear todos os tipos para o ícone padrão de sino (`Bell`) e estilo azul neutro.
- **Remoção da Lógica de Limpeza de Alertas Obsoletos**: Remover o bloco de remoção física no método `_sincronizar_alertas` em `src/controllers/alerta_controller.py`. Com isso, alertas antigos não serão mais deletados quando as condições de leito/alta mudarem.

## Risks / Trade-offs

- **Crescimento do Banco de Dados**:
  - *Risco*: Sem a exclusão de alertas antigos, a tabela de alertas acumulará registros indefinidamente.
  - *Mitigação*: Os alertas são pequenos registros de texto. A tabela local SQLite suporta facilmente dezenas de milhares de registros. Se futuramente houver lentidão, um índice por `criado_em` ou paginação na listagem pode ser implementado.
