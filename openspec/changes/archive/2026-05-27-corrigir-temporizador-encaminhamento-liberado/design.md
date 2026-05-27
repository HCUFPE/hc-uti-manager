## Context

Currently, `BedCard.vue` displays the elapsed time timer if `cirurgiaFinalizada` is true:
```html
<div v-if="cirurgiaFinalizada" class="...">
  ...
  <span v-if="proximoPaciente.horaCirurgiaFinalizada">
    {{ obterTempoDecorrido(proximoPaciente.horaCirurgiaFinalizada) }}
  </span>
</div>
```
When the referral is released by the UTI, `encaminhamentoLiberado` becomes `true`, but `cirurgiaFinalizada` remains `true` (since the surgery is still finalized). This causes the timer to keep displaying and counting up on the client side, even though the backend stopped counting and the card itself turned green.

We must change the logic to hide the clock and show a green "Encaminhamento Liberado" badge instead.

## Goals / Non-Goals

**Goals:**
- Stop the client-side wait timer and hide the clock/timer UI once the referral is released (`encaminhamentoLiberado` is `true`).
- Display a clear "Encaminhamento Liberado" status indicator with an emerald theme inside the card when the referral is released.

**Non-Goals:**
- Modify the backend duration tracking/logging logic.

## Decisions

### 1. Update Template Conditions in `BedCard.vue`
We will replace the existing status badge rendering for finalized surgeries:
- If `cirurgiaFinalizada && !encaminhamentoLiberado`: Render the yellow "Cirurgia Concluída" badge with the flashing amber dot and the reactive elapsed time timer.
- If `encaminhamentoLiberado`: Render a new green "Encaminhamento Liberado" badge with a flashing green/emerald dot.

```html
<div v-if="cirurgiaFinalizada && !encaminhamentoLiberado" class="mt-2 flex flex-wrap items-center gap-1.5 text-[11px] font-bold text-amber-700">
  <span class="inline-block h-2 w-2 rounded-full bg-amber-500 animate-pulse"></span>
  Cirurgia Concluída
  <span v-if="proximoPaciente?.horaCirurgiaFinalizada" class="flex items-center gap-0.5 rounded-full bg-amber-100 px-2 py-0.5 font-medium text-amber-800 border border-amber-200">
    <ClockIcon class="h-3.5 w-3.5 text-amber-600 shrink-0" />
    {{ obterTempoDecorrido(proximoPaciente.horaCirurgiaFinalizada) }}
  </span>
</div>
<div v-else-if="encaminhamentoLiberado" class="mt-2 flex flex-wrap items-center gap-1.5 text-[11px] font-bold text-emerald-700">
  <span class="inline-block h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
  Encaminhamento Liberado
</div>
```

## Risks / Trade-offs

- None identified.
