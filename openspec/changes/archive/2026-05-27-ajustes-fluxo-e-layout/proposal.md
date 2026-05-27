## Why

1. **Fuso Horário nas Altas**: A data/hora exibida para solicitações de alta no frontend não está ajustada para o fuso horário de Brasília (-3h), diferentemente de todas as outras entidades do sistema.
2. **Extrapolação de Layout**: As tags "Alta Solicitada" (Status Badge) e "Destino Definido" nos cartões de leito no dashboard extrapolam a largura física do card em resoluções menores (como notebooks) devido ao alinhamento horizontal flex e propriedade `whitespace-nowrap`.
3. **Bloqueio de Edição de Prontuário**: Embora o backend possua o fluxo de troca de paciente na edição (cancelando a solicitação antiga, criando uma nova e transferindo a reserva de leito), o frontend bloqueia e desabilita o campo de prontuário quando o formulário é aberto em modo de edição.

## What Changes

- **Ajuste de Fuso Horário**: Subtrair 3 horas no método `listar_altas()` do `AltasController` antes de formatar a data/hora para o frontend.
- **Melhorias de Layout (BedCard)**:
  - Reposicionar a tag "Destino Definido" abaixo da linha de cabeçalho do `BedCard.vue` para que tenha espaço próprio.
  - Remover a classe `whitespace-nowrap` e adicionar suporte à quebra de linha para a tag de destino definido.
- **Habilitação de Edição de Prontuário**:
  - Remover a propriedade `disabled` do input de prontuário durante a edição no frontend.
  - Exibir o botão "Buscar" no modal de edição para permitir que o usuário consulte os novos dados do paciente no AGHU.

## Capabilities

### New Capabilities
*(Nenhuma nova capacidade necessária)*

### Modified Capabilities
- `solicitacao-leitos`: Permitir a alteração do prontuário durante a edição de solicitações e a consulta dos dados atualizados no AGHU.

## Impact

- **Backend**: `src/controllers/altas_controller.py`
- **Frontend**: `frontend/src/components/BedCard.vue` e `frontend/src/views/Solicitacoes.vue`
