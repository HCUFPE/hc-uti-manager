## Context

Adição de novos elementos informativos ao dashboard de indicadores.

## Decisions

### 1. Backend: `src/providers/implementations/indicadores_provider.py`
Extrair motivos do histórico de ações de cancelamento no período:
```python
motivos_cancelamento = {}
for ev in cancelamentos_sol_periodo:
    if ev.detalhes and " - Motivo: " in ev.detalhes:
        partes = ev.detalhes.split(" - Motivo: ")
        if len(partes) > 1:
            motivo = partes[1].strip()
            motivos_cancelamento[motivo] = motivos_cancelamento.get(motivo, 0) + 1
    else:
        motivos_cancelamento["Não Informado"] = motivos_cancelamento.get("Não Informado", 0) + 1
```
E retornar na chave `motivos_cancelamento` no dicionário `detalhado`.

### 2. Frontend: `frontend/src/views/Indicadores.vue`
- Adicionar tabela de motivos de cancelamento na coluna da esquerda.
- Redesenhar layout do card da pizza de especialidades para incluir legenda lateral com contagem.
