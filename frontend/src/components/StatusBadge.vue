<template>
  <span
    class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold leading-none border shadow-sm transition-all duration-300"
    :class="badgeClass"
  >
    <component :is="iconComponent" class="h-3.5 w-3.5 shrink-0" />
    <span>{{ label }}</span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { 
  CheckCircleIcon, 
  UserIcon, 
  ArrowPathIcon, 
  NoSymbolIcon, 
  ArrowRightOnRectangleIcon, 
  CalendarDaysIcon 
} from '@heroicons/vue/24/outline';

type BedStatus = 'disponivel' | 'ocupado' | 'higienizacao' | 'desativado' | 'alta' | 'reservado';

const props = defineProps<{
  status: BedStatus;
}>();

const statusConfig: Record<BedStatus, { label: string; className: string; icon: any }> = {
  disponivel: {
    label: 'Disponível',
    className: 'bg-emerald-50 text-emerald-700 border-emerald-200/80 shadow-emerald-50/50',
    icon: CheckCircleIcon,
  },
  ocupado: {
    label: 'Ocupado',
    className: 'bg-blue-50 text-blue-700 border-blue-200/80 shadow-blue-50/50',
    icon: UserIcon,
  },
  higienizacao: {
    label: 'Higienização',
    className: 'bg-amber-50 text-amber-700 border-amber-200/80 shadow-amber-50/50',
    icon: ArrowPathIcon,
  },
  desativado: {
    label: 'Desativado',
    className: 'bg-slate-50 text-slate-600 border-slate-300/80 shadow-slate-50/50',
    icon: NoSymbolIcon,
  },
  alta: {
    label: 'Alta Solicitada',
    className: 'bg-rose-50 text-rose-700 border-rose-200/80 shadow-rose-50/50 font-bold animate-pulse',
    icon: ArrowRightOnRectangleIcon,
  },
  reservado: {
    label: 'Reservado',
    className: 'bg-purple-50 text-purple-700 border-purple-200/80 shadow-purple-50/50',
    icon: CalendarDaysIcon,
  },
};

const selectedConfig = computed(() => statusConfig[props.status]);
const label = computed(() => selectedConfig.value.label);
const badgeClass = computed(() => selectedConfig.value.className);
const iconComponent = computed(() => selectedConfig.value.icon);
</script>
