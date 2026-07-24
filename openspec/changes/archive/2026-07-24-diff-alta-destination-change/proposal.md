## Why

Atualmente, quando o NIR define ou altera o leito de destino para uma solicitação de alta da UTI, o sistema registra no histórico com a ação "Definiu destino de alta" (tipo `alteracao_destino`) e emite um alerta com o título "Destino de Alta Definido". Isso não diferencia quando o destino está sendo cadastrado pela primeira vez de quando ele está sendo alterado (editado), dificultando a percepção da UTI sobre as mudanças feitas pelo NIR.

## What Changes

- Backend: Modificar `AltasController.atualizar_destino` para verificar se já existia um leito de destino definido anteriormente.
- Backend: Se já existia um destino e ele for alterado, registrar a ação no histórico como "Alterou destino de alta" (mantendo o tipo do histórico como `alteracao_destino` ou criando um específico).
- Backend: Modificar a engine de alertas em `AlertaController._processar_evento_historico` / `_gerar_alerta_por_tipo` para que, se a ação registrada for de alteração, o título do alerta seja "Alterou o Destino de Alta" em vez de "Destino de Alta Definido".

## Capabilities

### New Capabilities
- `diff-alta-destination-change`: Diferenciar visualmente no histórico e nos alertas quando o NIR redefine um destino de alta já estabelecido.

### Modified Capabilities

## Impact

- `src/controllers/altas_controller.py`
- `src/controllers/alerta_controller.py`
