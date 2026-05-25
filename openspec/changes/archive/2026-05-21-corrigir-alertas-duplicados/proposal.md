## Why

Durante os testes, os alertas do sistema (especialmente os gerados a partir do histórico de ações, como os de UTI) foram exibidos de forma duplicada no painel de alertas do usuário. Isso polui a interface de usuário e prejudica a usabilidade da aplicação. Este ajuste visa corrigir o mecanismo de geração/sincronização de alertas para garantir que cada evento único do histórico resulte em apenas um único alerta ativo no banco de dados.

## What Changes

- Correção no critério de correspondência de alertas existentes no método de sincronização (`_sincronizar_alertas`).
- Substituição da comparação direta de igualdade estrita de data/hora (`criado_em`) por uma comparação com margem de tolerância (ou truncamento de segundos/milissegundos) para evitar que divergências sutis de precisão do SQLite invalidem a busca por registros existentes.
- Atribuição do timestamp real (`criado_em` / `atualizado_em`) da solicitação de alta aos alertas gerados por ela, garantindo que novas solicitações futuras gerem novos alertas e que a comparação de duplicados ocorra de forma correta.
- **Preservação de Histórico:** Garantir que nenhum alerta do tipo "Gargalo" (ou gerado por histórico) seja removido pelo sistema ao expirar ou quando a condição deixar de ser ativa.

## Capabilities

### New Capabilities
- `alertas`: Mecanismo de geração e sincronização de alertas de leitos e fluxo

### Modified Capabilities
<!-- None -->

## Impact

- `src/controllers/alerta_controller.py`: Ajuste no fluxo de geração e sincronização de alertas.
- Banco de dados SQLite local: Prevenção do crescimento desnecessário da tabela `alertas`.
