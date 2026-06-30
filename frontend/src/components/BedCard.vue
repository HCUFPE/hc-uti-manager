<template>
  <article
    class="relative rounded-2xl border p-5 transition-all duration-300 hover:-translate-y-1.5 hover:shadow-xl backdrop-blur-sm"
    :class="[
      temConflito ? 'border-red-500 ring-4 ring-red-500/10 shadow-red-100 bg-white/90' : 
      (sinalizacaoTransferencia ? 'border-rose-200 ring-4 ring-rose-500/5 shadow-rose-100 bg-white/90' : 
      (proximoPaciente && cirurgiaFinalizada && !encaminhamentoLiberado) ? 
        (authStore.isUTI ? 'animate-pulse-warning border-amber-300' : 'border-amber-300 bg-amber-50/60 ring-4 ring-amber-400/10 shadow-amber-100') :
      (proximoPaciente && encaminhamentoLiberado) ? 'border-emerald-300 bg-emerald-50/60 ring-4 ring-emerald-400/10 shadow-emerald-100' :
      'border-slate-200 shadow-slate-100/50 bg-white/90')
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

      <div class="flex flex-col items-end gap-1.5 shrink-0">
        <StatusBadge :status="status" />
      </div>
    </div>

    <!-- Tag de Destino Definido (NIR) -->
    <div 
      v-if="destinoDefinido"
      class="mt-3 inline-flex items-center gap-1 rounded-full px-3 py-1 text-[10px] font-bold leading-none border shadow-sm transition-all duration-500 whitespace-normal break-words max-w-full w-fit"
      :class="destinoDisponivel 
        ? 'bg-emerald-100 text-emerald-700 border-emerald-200' 
        : 'bg-amber-100 text-amber-700 border-amber-200'"
    >
      <MapPinIcon class="h-3 w-3 shrink-0" :class="destinoDisponivel ? 'text-emerald-600' : 'text-amber-600'" />
      <span>Destino Definido: {{ destinoDefinido }}{{ destinoDisponivel ? ' Disponível' : '' }}</span>
    </div>

    <div class="mt-4 space-y-4 text-sm text-slate-700">
      <div v-if="pacienteAtual" class="space-y-1 border-l-4 border-blue-500 pl-4 bg-blue-50/30 py-1 rounded-r-lg">
        <p class="text-xs font-semibold uppercase tracking-widest text-slate-500">Paciente Atual</p>
        <p class="text-base font-bold text-slate-900">Prontuário: {{ pacienteAtual.prontuario }}</p>
        <p class="text-slate-600">
          {{ pacienteAtual.idade }} anos
          <span v-if="pacienteAtual.dataNascimento" class="text-xs text-slate-500">
            ({{ formatarNascimento(pacienteAtual.dataNascimento) }})
          </span>
          - {{ pacienteAtual.especialidade }}
        </p>
      </div>

      <div v-if="proximoPaciente" class="space-y-1 border-l-4 border-emerald-500 pl-4 bg-emerald-50/30 py-1 rounded-r-lg">
        <p class="text-xs font-semibold uppercase tracking-widest text-slate-500">Próximo Paciente</p>
        <p class="text-base font-bold text-slate-900">Prontuário: {{ proximoPaciente.prontuario }}</p>
        <p v-if="proximoPaciente.nome" class="text-xs font-semibold text-slate-500 leading-none my-1">
          {{ proximoPaciente.nome }}
        </p>
        <p class="text-slate-600">{{ proximoPaciente.idade }} anos - {{ proximoPaciente.especialidade }}</p>
        
        <!-- Detalhes da Cirurgia -->
        <div v-if="proximoPaciente.dataCirurgia" class="mt-2 flex flex-wrap gap-2">
          <div class="flex items-center gap-1 rounded bg-slate-100 px-1.5 py-0.5 text-[11px] font-medium text-slate-600 border border-slate-200">
            Cirurgia: {{ formatarDataHoraCirurgia(proximoPaciente.dataCirurgia, proximoPaciente.horaCirurgia) }}
          </div>
          <div v-if="proximoPaciente.turno" class="flex items-center gap-1 rounded bg-blue-50 px-1.5 py-0.5 text-[11px] font-medium text-blue-600 border border-blue-100 uppercase">
            Turno: {{ proximoPaciente.turno }}
          </div>
        </div>
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

    <div v-if="authStore.isAdmin || authStore.isUTI" class="mt-5 flex flex-wrap gap-2">
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
        v-if="proximoPaciente && cirurgiaFinalizada && !encaminhamentoLiberado"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-amber-200 bg-amber-500 px-3 py-2 text-xs font-bold text-white transition hover:bg-amber-600 shadow-sm"
        @click="emit('liberar-encaminhamento', solicitacaoId!)"
      >
        Liberar Encaminhamento
      </button>
      <button
        v-if="proximoPaciente && encaminhamentoLiberado"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-red-200 bg-red-600 px-3 py-2 text-xs font-bold text-white transition hover:bg-red-700 shadow-sm"
        @click="emit('cancelar-liberacao', solicitacaoId!)"
      >
        Cancelar Liberação
      </button>
      <button
        v-if="proximoPaciente"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-blue-200 bg-blue-50 px-3 py-2 text-xs font-semibold text-blue-700 transition hover:bg-blue-100"
        @click="emit('mudar-leito', solicitacaoId!)"
      >
        Mudar Leito
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
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { ExclamationTriangleIcon, ClockIcon, MapPinIcon } from '@heroicons/vue/24/outline';
import StatusBadge from './StatusBadge.vue';
import UiBadge from './ui/Badge.vue';

type BedStatus = 'disponivel' | 'ocupado' | 'higienizacao' | 'desativado' | 'alta' | 'reservado';
type BedType = 'cirurgico' | 'hem' | 'obstetrico' | 'uti' | 'outro' | 'nao_definido';

type Patient = {
  prontuario: string;
  nome?: string;
  idade: number;
  especialidade: string;
  dataCirurgia?: string;
  horaCirurgia?: string;
  turno?: string;
  horaCirurgiaFinalizada?: string;
  dataNascimento?: string;
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
  destinoDefinido?: string;
  destinoDisponivel?: boolean;
  showActions?: boolean;
  cirurgiaFinalizada?: boolean;
  encaminhamentoLiberado?: boolean;
  solicitacaoId?: number;
}>();

const authStore = useAuthStore();

const emit = defineEmits<{
  'solicitar-alta': [];
  'cancelar-alta': [];
  'cancelar-reserva': [];
  'liberar-encaminhamento': [solicitacaoId: number];
  'cancelar-liberacao': [solicitacaoId: number];
  'mudar-leito': [solicitacaoId: number];
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

const formatarDataHoraCirurgia = (dataStr?: string, horaStr?: string) => {
  if (!dataStr) return '';
  const dataFormatada = dataStr.includes('-') ? dataStr.split('-').reverse().join('/') : dataStr;
  return horaStr ? `${dataFormatada} - ${horaStr}` : dataFormatada;
};

const formatarNascimento = (dataStr?: string) => {
  if (!dataStr) return '';
  if (dataStr.includes('-')) {
    const parts = dataStr.split('-');
    if (parts.length === 3) {
      if (parts[0].length === 4) {
        return `${parts[2]}/${parts[1]}/${parts[0]}`;
      } else {
        return `${parts[0]}/${parts[1]}/${parts[2]}`;
      }
    }
  }
  return dataStr;
};

const currentTime = ref(new Date());
let timerId: any = null;

onMounted(() => {
  timerId = setInterval(() => {
    currentTime.value = new Date();
  }, 60000);
});

onUnmounted(() => {
  if (timerId) clearInterval(timerId);
});

const obterTempoDecorrido = (dataIso?: string) => {
  if (!dataIso) return '';
  const dateFim = new Date(dataIso);
  const diffMs = currentTime.value.getTime() - dateFim.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  if (diffMins < 0) return '0m';
  if (diffMins < 60) return `${diffMins}m`;
  const horas = Math.floor(diffMins / 60);
  const mins = diffMins % 60;
  return `${horas}h ${mins}m`;
};
</script>
