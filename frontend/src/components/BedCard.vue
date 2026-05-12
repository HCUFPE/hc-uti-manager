<template>
  <article
    class="relative rounded-2xl border bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
    :class="[
      temConflito ? 'border-red-500 ring-2 ring-red-500/20' : 
      (sinalizacaoTransferencia ? 'border-rose-200 ring-2 ring-rose-100' : 'border-slate-200')
    ]"
  >
    <!-- Icone de Alerta (Conflito ou Transferencia) -->
    <div
      v-if="temConflito || sinalizacaoTransferencia"
      class="absolute -top-2 -right-2 rounded-full p-2 shadow"
      :class="temConflito ? 'bg-red-600 text-white' : 'bg-rose-100 text-rose-600'"
      :title="temConflito ? 'Conflito de reserva' : 'Alta solicitada'"
    >
      <ExclamationTriangleIcon v-if="temConflito" class="h-4 w-4" />
      <ClockIcon v-else class="h-4 w-4" />
    </div>

    <div class="flex items-start justify-between gap-3">
      <div class="space-y-2">
        <div>
          <p class="text-xs font-semibold uppercase tracking-widest text-slate-500">Leito</p>
          <h3 class="text-2xl font-bold text-slate-900">Leito {{ leitoNumero }}</h3>
        </div>
        <UiBadge :class="['border-transparent text-white', tipoClass]">
          {{ tipoConfig.label }}
        </UiBadge>
      </div>

      <StatusBadge :status="status" />
    </div>

    <div class="mt-4 space-y-4 text-sm text-slate-700">
      <div v-if="pacienteAtual" class="space-y-1 border-l-4 border-blue-500 pl-4">
        <p class="text-xs font-semibold uppercase tracking-widest text-slate-500">Paciente Atual</p>
        <p class="text-base font-bold text-slate-900">Prontuario: {{ pacienteAtual.prontuario }}</p>
        <p class="text-slate-600">{{ pacienteAtual.idade }} anos - {{ pacienteAtual.especialidade }}</p>
      </div>

      <div v-if="proximoPaciente" class="space-y-1 border-l-4 border-emerald-500 pl-4">
        <p class="text-xs font-semibold uppercase tracking-widest text-slate-500">Proximo Paciente</p>
        <p class="text-base font-bold text-slate-900">Prontuario: {{ proximoPaciente.prontuario }}</p>
        <p class="text-slate-600">{{ proximoPaciente.idade }} anos - {{ proximoPaciente.especialidade }}</p>
        
        <!-- Detalhes da Cirurgia -->
        <div v-if="proximoPaciente.dataCirurgia" class="mt-2 flex flex-wrap gap-2">
          <div class="flex items-center gap-1 rounded bg-slate-100 px-1.5 py-0.5 text-[11px] font-medium text-slate-600 border border-slate-200">
            Cirurgia: {{ proximoPaciente.dataCirurgia.includes('-') ? proximoPaciente.dataCirurgia.split('-').reverse().join('/') : proximoPaciente.dataCirurgia }}
          </div>
          <div v-if="proximoPaciente.turno" class="flex items-center gap-1 rounded bg-blue-50 px-1.5 py-0.5 text-[11px] font-medium text-blue-600 border border-blue-100 uppercase">
            Turno: {{ proximoPaciente.turno }}
          </div>
        </div>
        <UiBadge
          v-if="tipoReserva"
          variant="outline"
          class="border-emerald-200 bg-emerald-50 text-emerald-700"
        >
          {{ tipoReserva }}
        </UiBadge>
      </div>

      <p v-else class="pl-4 text-slate-500">Sem reserva</p>
      
      <!-- Alerta de Conflito -->
      <div v-if="temConflito" class="mt-2 rounded-lg bg-red-50 p-3 border border-red-200">
        <div class="flex items-start gap-2">
          <ExclamationTriangleIcon class="h-5 w-5 text-red-600 shrink-0" />
          <div>
            <p class="text-xs font-bold text-red-700 uppercase">Conflito detectado</p>
            <p class="text-[11px] leading-tight text-red-600 mt-0.5">
              Leito ocupado por outro paciente no AGHU. Verifique a reserva.
            </p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="authStore.isAdmin || authStore.isUTI" class="mt-5 flex gap-2">
      <button
        v-if="status === 'ocupado'"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-700 transition hover:bg-slate-50"
        @click="$emit('solicitar-alta')"
      >
        Solicitar Alta
      </button>
      <button
        v-if="status === 'alta'"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs font-semibold text-red-700 transition hover:bg-red-100"
        @click="$emit('cancelar-alta')"
      >
        Cancelar Alta
      </button>
      <button
        v-if="proximoPaciente"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-700 transition hover:bg-slate-50"
        @click="$emit('cancelar-reserva')"
      >
        Cancelar Reserva
      </button>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { ExclamationTriangleIcon, ClockIcon } from '@heroicons/vue/24/outline';
import StatusBadge from './StatusBadge.vue';
import UiBadge from './ui/Badge.vue';

type BedStatus = 'disponivel' | 'ocupado' | 'higienizacao' | 'desativado' | 'alta' | 'reservado';
type BedType = 'cirurgico' | 'hem' | 'obstetrico' | 'uti' | 'outro' | 'nao_definido';

type Patient = {
  prontuario: string;
  idade: number;
  especialidade: string;
  dataCirurgia?: string;
  turno?: string;
};

const props = defineProps<{
  leitoNumero: string;
  status: BedStatus;
  tipo: BedType;
  pacienteAtual?: Patient;
  proximoPaciente?: Patient;
  tipoReserva?: string;
  sinalizacaoTransferencia?: boolean;
  temConflito?: boolean;
  showActions?: boolean;
}>();

const authStore = useAuthStore();

defineEmits<{
  'solicitar-alta': [];
  'cancelar-alta': [];
  'cancelar-reserva': [];
}>();

const tipoPalette: Record<BedType, { label: string; className: string }> = {
  cirurgico: { label: 'Cirúrgico', className: 'bg-blue-600/80' },
  hem: { label: 'HEM', className: 'bg-rose-600/80' },
  obstetrico: { label: 'Obstétrico', className: 'bg-purple-600/80' },
  uti: { label: 'UTI', className: 'bg-indigo-600/80' },
  outro: { label: 'Outro', className: 'bg-slate-700/80' },
  nao_definido: { label: 'Não definido', className: 'bg-slate-400/90' },
};

const tipoConfig = computed(() => tipoPalette[props.tipo] || tipoPalette.outro);
const tipoClass = computed(() => tipoConfig.value.className);
</script>
