## Context

Atualmente o fluxo de cancelamento de uma solicitação de leito (que acontece na rota `DELETE /api/solicitacoes/{sol_id}`) não exige nem armazena o motivo pelo qual a exclusão está sendo solicitada. Para que os gestores consigam analisar a taxa de suspensão de cirurgias ou recusas por outras razões, o sistema precisa captar e armazenar o motivo do cancelamento a partir de uma lista pré-definida.

## Goals / Non-Goals

**Goals:**
- Atualizar a interface do Frontend (Vue) para que o botão de "Cancelar Solicitação" abra um modal de confirmação com um dropdown (Select) contendo as opções de cancelamento.
- Modificar o controller e router no backend para aceitarem o motivo de cancelamento.
- Gravar o motivo no `HistoricoProvider` para que fique disponível na timeline do paciente.

**Non-Goals:**
- Criar um painel de gerenciamento dinâmico (CRUD) desses motivos de cancelamento; a lista (Motivo A, Motivo B, Motivo C) será implementada de forma estática no Frontend/Backend neste momento.

## Decisions

- **Armazenamento no Backend**: A rota de cancelamento no backend mudará de `DELETE` sem payload para aceitar os dados do motivo via query string ou, preferencialmente, usaremos um `POST /{sol_id}/cancelar` (ou ler payload em DELETE se o framework suportar, mas FastAPI aceita body em DELETE se definido, mas pode ser ruim em proxies. Optaremos por aceitar o motivo via query params no DELETE ou modificar a model).
- **Lista de Motivos**:
  - Motivo A
  - Motivo B
  - Motivo C
- **Histórico**: O motivo capturado será salvo na tabela de Histórico, com a `acao="Cancelou solicitação de vaga"` e nos `detalhes` adicionaremos `Motivo: <motivo>`.

## Risks / Trade-offs

- **[Risco] Compatibilidade**: O frontend atual chama o backend sem o parâmetro motivo. Durante o deploy simultâneo, se o backend passar a exigir, pode quebrar o client que não enviou.
- **Mitigação**: O parâmetro motivo pode ser inicialmente opcional no backend ou feito num deploy casado, e o backend deve garantir que se o motivo não for enviado ele registre "Motivo não informado".
