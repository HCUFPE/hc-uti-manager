## Context

Atualmente, o sistema apresenta duas falhas principais na lógica de geração de alertas e notificações no ambiente local:
1. **Falha na Detecção de Datas ("Para Hoje")**: A data da cirurgia é armazenada no SQLite local como `DD-MM-YYYY`, mas a validação de data no `AlertaController` assume que a data está em formato `DD/MM/YYYY` ou `YYYY-MM-DD`, fazendo com que os alertas de "solicitação para hoje" nunca sejam gerados.
2. **Duplicação de Alertas**: Como a limpeza de alertas obsoletos está desativada, a rotina tenta evitar duplicatas comparando o `criado_em` do alerta com o do histórico. No entanto, por incompatibilidade de precisão de segundos/fuso, essa comparação falha e o mesmo alerta é gerado repetidas vezes. Além disso, solicitações canceladas são omitidas do provider principal, fazendo com que o mapeador de alertas não encontre a solicitação correspondente e falhe em determinar o perfil do solicitante.

## Goals / Non-Goals

**Goals:**
- Corrigir a validação de data (`match_hoje`) para suportar de forma robusta e unificada os formatos de data (`DD/MM/YYYY`, `DD-MM-YYYY` e `YYYY-MM-DD`).
- Implementar `get_todas_completo()` em `SolicitacaoLeitoProvider` para carregar todas as solicitações (incluindo canceladas), garantindo que os dados de auditoria e perfil sejam correlacionados com o histórico.
- Eliminar a duplicação de alertas ao refinar o critério de comparação temporal no `_sincronizar_alertas`.
- Executar a limpeza de duplicatas e alertas de teste no banco SQLite local.

**Non-Goals:**
- Alterar o banco de dados de produção da VM (a VM não possui alertas duplicados de testes de fluxo).
- Redesenhar a arquitetura da tabela de alertas ou criar novas tabelas.

## Decisions

### 1. Normalização de Datas no Backend
- **Abordagem**: Implementar um parser flexível em `_validar_data_hoje` que:
  1. Extrai a data (removendo horários após espaços ou `T`).
  2. Identifica o separador utilizado (`/` ou `-`).
  3. Divide e rearranja os elementos se o primeiro elemento não for o ano (4 dígitos), garantindo o formato `YYYY-MM-DD` padronizado.
- **Raciocínio**: Essa abordagem evita que alterações futuras nos formatos de armazenamento do SQLite ou PostgreSQL quebrem a validação.

### 2. Recuperação de Solicitações Canceladas para Histórico
- **Abordagem**: Adicionar o método `get_todas_completo()` ao `SolicitacaoLeitoProvider` (que faz select sem a cláusula `where status != 'Cancelada'`) e utilizá-lo na rotina de histórico.
- **Raciocínio**: As ações de histórico (como cancelamento de solicitações ou reservas) por definição referem-se a solicitações canceladas. Filtrar solicitações ativas impede o cruzamento de dados.

### 3. Deduplicação Baseada em Chave Estrita e Tolerância Temporal
- **Abordagem**: No método `_sincronizar_alertas`, se um alerta com o mesmo título, mensagem, prontuário e perfil alvo for encontrado na base, ele será considerado duplicado se a diferença de timestamp for pequena ou inexistente, ou se a mensagem corresponder ao mesmo evento.
- **Raciocínio**: Garante consistência idêntica sem criar poluição de alertas duplicados.

## Risks / Trade-offs

- **[Risco]** Deletar alertas válidos no banco local.
  - **[Mitigação]** O script de limpeza local agrupa as entradas por chaves estritas (mensagem, título, prontuário) e remove apenas as duplicatas subsequentes, retendo a primeira instância de cada alerta.
