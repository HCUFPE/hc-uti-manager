## Context

1. **Fuso Horário**: Em `AltasController.listar_altas`, a data/hora é formatada diretamente do campo `alta.criado_em` (armazenado em UTC/GMT) sem desconto de fuso horário, o que resulta em horários exibidos com 3 horas a mais do que o horário real de Brasília.
2. **Layout dos Badges**: O container superior do `BedCard.vue` é um flexbox horizontal. Tags longas de status e destino definido disputam espaço com o título do leito. No notebook, isso resulta em extrapolação horizontal das bordas.
3. **Edição de Prontuário**: A view `Solicitacoes.vue` bloqueia a edição do input de prontuário, mesmo que a API local suporte a alteração através do fluxo automático de cancelamento de solicitação antiga + criação de nova mantendo a reserva.

## Goals / Non-Goals

**Goals:**
- Ajustar fuso horário (-3h) nas solicitações de alta.
- Modificar o layout do `BedCard.vue` para impedir a extrapolação do grid.
- Desbloquear a alteração do prontuário no modal de edição no frontend.

**Non-Goals:**
- Redesenhar a interface do dashboard ou alterar outras views além de `BedCard` e `Solicitacoes`.
- Alterar as tabelas ou regras de negócio do banco local.

## Decisions

### 1. Fuso Horário no AltasController
- **Abordagem**: Subtrair `timedelta(hours=3)` da propriedade `alta.criado_em` no `listar_altas`.
- **Raciocínio**: Consistente com a forma como `Alerta.to_dict()` e `HistoricoAcao.to_dict()` lidam com fusos locais no SQLite.

### 2. Mudança de Layout em BedCard.vue
- **Abordagem**: Retirar a tag "Destino Definido" do flex superior e colocá-la na linha de baixo (fora do flexbox do cabeçalho), removendo `whitespace-nowrap` e adicionando classes CSS flexíveis (`whitespace-normal`, `break-words`).
- **Raciocínio**: Isso elimina a disputa de espaço horizontal na linha superior, permitindo que a tag ocupe a largura completa do card e quebre linhas normalmente.

### 3. Edição do Prontuário no Frontend
- **Abordagem**: 
  - Atualizar a propriedade `:disabled` do input de prontuário para depender apenas de `buscandoAghu` (e não mais de `isEditing`).
  - Atualizar o botão "Buscar" para ser exibido sempre, permitindo a busca por prontuário novo no AGHU mesmo durante a edição.

## Risks / Trade-offs

- **[Risco]** O usuário submeter um prontuário inválido ou não buscar os dados no AGHU durante a edição.
  - **[Mitigação]** O botão "Salvar" continuará bloqueado caso a busca no AGHU não tenha sido realizada/concluída com sucesso (`(!isEditing && !dadosAghu)` ou dados do AGHU inválidos).
