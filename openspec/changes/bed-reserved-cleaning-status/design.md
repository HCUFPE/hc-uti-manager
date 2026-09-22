## Context

No `BedCard.vue`, o badge de status do leito hoje prioriza `bloqueadoClinico` para exibir a badge `Reservado`. No entanto, quando o leito no censo do AGHU possui o status `higienizacao` (ou `LIMPEZA`), a equipe de plantão precisa enxergar visualmente que a limpeza do leito físico ainda está em andamento enquanto o leito se encontra reservado.

## Goals / Non-Goals

**Goals:**
- Exibir a indicação `🧹 Leito em Higienização` logo abaixo do badge `Reservado`, em texto menor (`text-xs font-medium text-amber-700 dark:text-amber-400 flex items-center gap-1 mt-1`), fora do badge roxo principal.
- Preservar a badge `Reservado` no topo como status prioritário.
- Permitir simulação visual na VM de Homologação (`10.34.0.151`) para validação pelo usuário.

**Non-Goals:**
- Alterar as regras de bloqueio do leito ou permissões do NIR.

## Decisions

1. **Repasse do Status Original no Backend (`leitos_controller.py`)**:
   - Garantir que a propriedade `status_original_aghu` ou `is_higienizacao` seja enviada no JSON do leito quando o status retornado pelo censo do AGHU for `higienizacao` / `LIMPEZA`.

2. **Renderização no `BedCard.vue`**:
   - Sob a div `<StatusBadge :status="bloqueadoClinico ? 'reservado' : status" />`, incluir a renderização condicional:
     ```html
     <span 
       v-if="bloqueadoClinico && statusEmHigienizacao" 
       class="text-[11px] font-semibold text-amber-600 flex items-center gap-1 mt-1 animate-pulse"
     >
       <SparklesIcon class="h-3 w-3 text-amber-500" />
       Higienização
     </span>
     ```

## Risks / Trade-offs

- [Risk] Poluição visual no card.
  - *Mitigation*: Usar tipografia reduzida (`11px`), alinhada à direita abaixo do badge, mantendo o card limpo e elegante.
