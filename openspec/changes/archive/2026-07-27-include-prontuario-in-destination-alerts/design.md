## Goals / Non-Goals

**Goals:**
- Incluir o prontuário do paciente nos textos descritivos das mensagens de alerta de destino definido, alterado e liberado.
- Garantir que a versão seja incrementada para `1.4.9`.

## Decisions

### Modificação em `AlertaController`

1. Em `src/controllers/alerta_controller.py` no bloco `elif tipo in ["alteracao_destino", "destino_disponivel", "destino_pendente"]:` (linhas 274 a 297):
   - Formatamos a mensagem para incluir o prontuário no formato `f"{detalhes} (Prontuário {pront_alerta})"` se o prontuário estiver disponível e não for "Desconhecido".
   
2. Incremento de versão:
   - `frontend/src/config/version.ts`
   - `frontend/package.json`
   - `src/main.py`
