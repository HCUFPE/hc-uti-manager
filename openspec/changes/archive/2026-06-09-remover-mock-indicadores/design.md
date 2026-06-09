## Context

No provedor de indicadores gerais (`IndicadoresProvider`), o método `get_indicadores_gerais` calcula várias métricas para exibição em painéis administrativos/indicadores. Para a métrica de tempo médio de liberação de encaminhamento (`tempo_medio_liberacao_encaminhamento`), há uma verificação que injeta o valor mockado `45.2` caso o cálculo resulte em zero/ausente e a variável de ambiente `ENV` seja igual a `"development"`. Isso confunde os usuários e testes ao limpar a base de dados.

## Goals / Non-Goals

**Goals:**
- Remover completamente o fallback mockado de `45.2` no cálculo do tempo médio de liberação de encaminhamento.
- Garantir que, na ausência de dados no banco, o indicador retorne `0.0`.

**Non-Goals:**
- Modificar o cálculo real do tempo médio quando há dados válidos no banco.
- Alterar outros indicadores ou gráficos operacionais não relacionados.

## Decisions

- **Remoção Direta do Fallback**: Removeremos as linhas 359 a 362 de `src/providers/implementations/indicadores_provider.py` que aplicam o fallback mockado.
- **Retorno Padrão**: O cálculo base `(sum(tempos) / len(tempos)) if tempos else 0.0` já garante o retorno de `0.0` quando a lista de tempos estiver vazia, então nenhuma lógica de fallback adicional é necessária.

## Risks / Trade-offs

- **Risco**: Impactar testes automatizados que possam depender do valor mockado `45.2` no ambiente de desenvolvimento.
- **Mitigação**: Executar a suíte de testes e, se houver testes dependendo desse mock, adaptá-los para refletir o comportamento real (retorno de `0.0` com base limpa).
