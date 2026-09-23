## Context

No `BedCard.vue`, o badge de status do leito hoje prioriza `bloqueadoClinico` para exibir a badge `Reservado`. No entanto, quando o leito no censo do AGHU possui o status `higienizacao` (ou `LIMPEZA`), a equipe de plantão precisa enxergar visualmente que a limpeza do leito físico ainda está em andamento enquanto o leito se encontra reservado.

## Goals / Non-Goals

**Goals:**
- Exibir a pílula de status amarela (`bg-amber-50 text-amber-700 border-amber-200/80 shadow-sm`) com o ícone `ArrowPathIcon` e o texto `Higienização` logo abaixo do badge de status prioritário para qualquer leito reservado (seja `proximoPaciente` de cirurgia ou `bloqueadoClinico`).
- Preservar a badge principal no topo (`Reservado`).

**Non-Goals:**
- Alterar as regras de bloqueio do leito ou permissões do NIR.

## Decisions

1. **Repasse do Status Original no Backend (`leitos_controller.py`)**:
   - Garantir que a propriedade `status_aghu_original` seja enviada no JSON do leito quando o status retornado pelo censo do AGHU for `higienizacao` / `LIMPEZA`.

2. **Renderização no `BedCard.vue`**:
   - Sob o badge `<StatusBadge :status="bloqueadoClinico ? 'reservado' : status" />`, incluir a pílula amarela condicional:
     ```html
     <span 
       v-if="(bloqueadoClinico || proximoPaciente) && (status === 'higienizacao' || (statusAghuOriginal && ['higienizacao', 'limpeza'].includes(statusAghuOriginal)))" 
       class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold leading-none border shadow-sm bg-amber-50 text-amber-700 border-amber-200/80 mt-0.5"
     >
       <ArrowPathIcon class="h-3.5 w-3.5 shrink-0 text-amber-700" />
       <span>Higienização</span>
     </span>
     ```

## Risks / Trade-offs

- [Risk] Poluição visual no card.
  - *Mitigation*: Usar tipografia reduzida (`11px`), alinhada à direita abaixo do badge, mantendo o card limpo e elegante.
