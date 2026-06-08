## Why

Atualmente, ao tentar cadastrar uma solicitação de prontuário duplicada, o backend retorna um detalhe específico, mas o frontend exibe uma mensagem genérica de erro ("Erro ao salvar solicitação."). O usuário deseja que a mensagem exibida na tela seja exatamente: "Solicitação para este prontuário já inserida.".

## What Changes

- Ajuste no detalhe de erro lançado pelo backend para retornar: `"Solicitação para este prontuário já inserida."`.
- Ajuste no frontend (`salvarNova`) para exibir o detalhe retornado pelo backend na notificação de erro, em vez de uma mensagem estática genérica.

## Capabilities

### New Capabilities

<!-- Nenhuma nova capability está sendo introduzida -->

### Modified Capabilities

- `solicitacao-leitos`: A mensagem de erro ao tentar inserir um prontuário com solicitação ativa deve ser amigável e exibir o texto correto do backend no frontend.

## Impact

- Afeta `criar_solicitacao` em `src/controllers/solicitacao_leito_controller.py`.
- Afeta `salvarNova` em `frontend/src/views/Solicitacoes.vue`.
