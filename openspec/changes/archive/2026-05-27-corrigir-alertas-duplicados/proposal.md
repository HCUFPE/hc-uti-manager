## Why

O mecanismo de geração de alertas está criando duplicatas de alertas de testes e execuções repetidas porque a comparação de datas entre eventos e alertas falha na precisão de microssegundos/fuso no SQLite local, e a rotina de exclusão de obsoletos está desativada. Além disso, a validação de alertas para solicitações de cirurgias "para hoje" falha porque o campo `data_cirurgia` no banco SQLite é armazenado com hífens (`DD-MM-YYYY`), não sendo normalizado para comparação com `hoje_bsb` (`YYYY-MM-DD`). Finalmente, solicitações canceladas são omitidas pelo provider, impedindo que o histórico recente cruze os dados do solicitante.

## What Changes

- **Limpeza do Banco Local**: Excluir alertas duplicados e de teste remanescentes no banco SQLite local.
- **Normalização de Datas**: Corrigir a função `_validar_data_hoje` no `AlertaController` para normalizar e comparar corretamente os formatos `DD-MM-YYYY` e `DD/MM/YYYY` em relação a `YYYY-MM-DD`.
- **Inclusão de Solicitações Canceladas**: Implementar o método `get_todas_completo()` em `SolicitacaoLeitoProvider` para retornar todas as solicitações (incluindo as com status `"Cancelada"`), permitindo que `AlertaController._analisar_historico` identifique o perfil do solicitante em cancelamentos de reserva recentes.
- **Deduplicação de Alertas**: Refinar a comparação de tempo de `_sincronizar_alertas` para tolerar diferenças de fuso horário e variação de relógio de forma mais flexível.

## Capabilities

### New Capabilities
*(Nenhuma nova capacidade necessária)*

### Modified Capabilities
*(Nenhuma modificação nos requisitos de especificação de alto nível)*

## Impact

- **Backend**: `src/controllers/alerta_controller.py` e `src/providers/implementations/solicitacao_leito_provider.py`.
- **Banco de Dados**: Modifica o estado do banco local `data/app.db`.
