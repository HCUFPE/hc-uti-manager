## Context

Na tela de Indicadores, a tabela de motivos de cancelamento exibe cada swap de paciente como uma linha separada, pois a mensagem de motivo contêm os números de prontuário envolvidos (ex: "Alteração de Prioridade pós Solicitação (Prontuário X foi substituído pelo Prontuário Y)"). Isso impede o agrupamento e a contagem consolidada dos motivos.

## Goals / Non-Goals

**Goals:**
- Agrupar e consolidar motivos de cancelamento no backend removendo sufixos dinâmicos como ` (Prontuário X foi substituído pelo Prontuário Y)`.

**Non-Goals:**
- Alterar as strings que são gravadas no histórico. As strings brutas gravadas no histórico de ações devem permanecer inalteradas para fins de auditoria detalhada.

## Decisions

### 1. Limpeza do Motivo no Provedor de Indicadores
- **Decisão**: Ajustar a rotina de processamento de cancelamentos em `IndicadoresProvider.get_indicadores_gerais` (por volta da linha 400 em `indicadores_provider.py`). Após extrair o motivo com `split(" - Motivo: ")`, limpar a string se contiver `" (Prontuário"`:
  ```python
  if " (Prontuário" in motivo:
      motivo = motivo.split(" (Prontuário")[0].strip()
  ```
- **Raciocínio**: É o local mais simples e direto, mantendo o histórico de auditoria original inalterado.
