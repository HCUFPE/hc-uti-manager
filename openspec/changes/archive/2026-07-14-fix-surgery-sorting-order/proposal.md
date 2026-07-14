## Why

Quando um paciente possui mais de uma cirurgia agendada ativa no AGHU (por exemplo, uma hoje e outra na próxima semana), o sistema incorretamente prioriza a data mais distante no futuro devido à ordenação simples `ORDER BY cir.dthr_inicio_cirg DESC LIMIT 1`. Isso impede a visualização da cirurgia imediata de hoje no painel.

## What Changes

- **Ajustar Ordenação SQL:** Modificar o arquivo de consulta SQL `obter_cirurgia_aghu.sql` para ordenar as cirurgias priorizando primeiro datas futuras/atuais mais próximas de hoje, e caso não existam, trazer a cirurgia passada mais recente.

## Capabilities

### New Capabilities

### Modified Capabilities
- `internacao-leitos`: Priorização correta de cirurgias próximas de hoje para exibição de reservas nos leitos.

## Impact

- **SQL Backend:** `src/providers/sql/solicitacao/obter_cirurgia_aghu.sql`
