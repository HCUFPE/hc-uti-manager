## Why

Nos alertas de destino de alta definido, liberado e alterado, o prontuário do paciente não aparece no texto descritivo. Para facilitar a identificação do paciente, o prontuário deve ser incluído entre parênteses no final da mensagem do alerta.

## What Changes

- Backend: Modificar `AlertaController._gerar_alerta_por_tipo` em `src/controllers/alerta_controller.py` para incluir o número do prontuário (quando disponível) na mensagem dos alertas relacionados ao destino de alta (`alteracao_destino`, `destino_disponivel`, `destino_pendente`).
- Versão: Incrementar a versão da aplicação para `1.4.9`.

## Capabilities

### New Capabilities

### Modified Capabilities
- `include-prontuario-in-destination-alerts`: Inclusão do prontuário na mensagem dos alertas de destino de alta.

## Impact

- `src/controllers/alerta_controller.py`
- `frontend/src/config/version.ts`
- `frontend/package.json`
- `src/main.py`
