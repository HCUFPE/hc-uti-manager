## Context

A ordenação das cirurgias em `obter_cirurgia_aghu.sql` retorna a cirurgia com maior data cronológica (`DESC`), trazendo cirurgias de semanas futuras à frente de cirurgias agendadas para o dia de hoje.

## Goals / Non-Goals

**Goals:**
- Priorizar cirurgias futuras ou de hoje em relação a cirurgias do passado.
- Para cirurgias futuras ou de hoje, ordenar em ordem cronológica crescente (`ASC`), para obter a mais próxima.
- Para cirurgias passadas, ordenar em ordem cronológica decrescente (`DESC`), para obter a mais recente.

## Decisions

- **Modificação em `src/providers/sql/solicitacao/obter_cirurgia_aghu.sql`:**
  Ajustar a cláusula `ORDER BY` para ordenar a partir de dois critérios:
  ```sql
  ORDER BY 
    CASE WHEN cir.dthr_inicio_cirg >= CURRENT_DATE THEN 0 ELSE 1 END,
    CASE WHEN cir.dthr_inicio_cirg >= CURRENT_DATE 
         THEN (cir.dthr_inicio_cirg - CURRENT_DATE) 
         ELSE (CURRENT_DATE - cir.dthr_inicio_cirg) 
    END ASC
  ```
