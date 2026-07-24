## 1. Altas Controller

- [x] 1.1 Atualizar `src/controllers/altas_controller.py` no método `atualizar_destino` para verificar se `alvo.leito_destino` já possuía um valor (não nulo e não vazio) antes de receber o novo destino. Se sim, registrar a ação como `"Alterou destino de alta"`, caso contrário, manter `"Definiu destino de alta"`.

## 2. Alerta Controller & Engine

- [x] 2.1 Atualizar a assinatura e chamadas dos métodos `_processar_evento_historico` e `_gerar_alerta_por_tipo` em `src/controllers/alerta_controller.py` para receber a `acao` do evento histórico.
- [x] 2.2 Atualizar o mapeamento de títulos para o tipo `alteracao_destino` em `_gerar_alerta_por_tipo` de forma que, se a `acao` for `"Alterou destino de alta"`, o título do alerta seja `"Alterou o Destino de Alta"`.
