<template>
  <section class="space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-3 border-b pb-4 mb-6">
      <div class="flex items-center gap-4">
        <h2 class="text-3xl font-bold text-slate-900">Alertas do Sistema</h2>
        <UiButton v-if="alertasNaoLidos.length > 0" variant="outline" size="sm" @click="marcarTodosLidos" class="text-xs h-8">
          Marcar todos como lidos
        </UiButton>
      </div>
    </div>

    <div class="space-y-3">
      <article
        v-for="alerta in alertasFiltrados"
        :key="alerta.id"
        class="rounded-xl border shadow-sm transition group relative"
        :class="[
          alerta.lido ? alertConfig[alerta.tipo].readClass : alertConfig[alerta.tipo].cardClass,
          alerta.lido ? 'opacity-60 saturate-50' : 'hover:shadow-md'
        ]"
      >
        <div class="p-4" @click="openModal(alerta)" role="button" tabindex="0">
          <div class="flex items-start gap-4">
            <div
              class="rounded-full p-2"
              :class="alerta.lido ? 'bg-slate-100 text-slate-400' : alertConfig[alerta.tipo].iconBg"
            >
              <component
                :is="alertConfig[alerta.tipo].icon"
                class="h-5 w-5"
                :class="alerta.lido ? 'text-slate-400' : alertConfig[alerta.tipo].iconColor"
              />
            </div>
            <div class="flex-1 space-y-2">
              <div class="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h3
                    class="font-semibold"
                    :class="alerta.lido ? 'text-slate-500' : 'text-slate-900'"
                  >
                    {{ alerta.titulo }}
                  </h3>
                  <p
                    class="mt-1 text-sm"
                    :class="alerta.lido ? 'text-slate-400' : 'text-slate-600'"
                  >
                    {{ alerta.mensagem }}
                  </p>
                </div>
                <div class="flex items-center gap-2">
                  <!-- Botão Ciente com Estilo de Pílula (Badge) -->
                  <button 
                    v-if="!alerta.lido"
                    class="h-7 px-4 rounded-full text-[10px] font-bold uppercase tracking-wider transition-all shadow-sm hover:shadow-md hover:scale-105 active:scale-95"
                    :class="alertConfig[alerta.tipo].badgeClass"
                    @click.stop="marcarComoLido(alerta)"
                  >
                    Ciente
                  </button>
                </div>
              </div>
              <div
                class="flex items-center gap-2 text-xs"
                :class="alerta.lido ? 'text-slate-400' : 'text-slate-500'"
              >
                <ClockIcon class="h-3 w-3" />
                <span>{{ alerta.dataHora }}</span>
              </div>
            </div>
          </div>
        </div>
      </article>
    </div>

    <Modal :show="showModal" @close="closeModal">
      <template #header>
        {{ modalTitle }}
      </template>
      <div v-if="selectedAlert" class="space-y-3">
        <div
          class="rounded-lg border shadow-sm p-3"
          :class="[
            selectedAlert.lido ? alertConfig[selectedAlert.tipo].readClass : alertConfig[selectedAlert.tipo].cardClass,
            selectedAlert.lido ? 'opacity-70 saturate-50' : ''
          ]"
        >
          <div class="flex items-start gap-3">
            <div
              class="rounded-full p-2"
              :class="selectedAlert.lido ? 'bg-slate-100 text-slate-400' : alertConfig[selectedAlert.tipo].iconBg"
            >
              <component
                :is="alertConfig[selectedAlert.tipo].icon"
                class="h-4 w-4"
                :class="selectedAlert.lido ? 'text-slate-400' : alertConfig[selectedAlert.tipo].iconColor"
              />
            </div>
            <div class="flex-1 space-y-1">
              <div class="flex items-start justify-between gap-3">
                <div>
                  <h4
                    class="font-semibold text-sm"
                    :class="selectedAlert.lido ? 'text-slate-500' : 'text-slate-900'"
                  >
                    {{ selectedAlert.titulo }}
                  </h4>
                  <p
                    class="text-xs"
                    :class="selectedAlert.lido ? 'text-slate-400' : 'text-slate-600'"
                  >
                    {{ selectedAlert.mensagem }}
                  </p>
                </div>
                <UiBadge
                  :class="selectedAlert.lido ? 'border-slate-200 bg-slate-100 text-slate-500' : alertConfig[selectedAlert.tipo].badgeClass"
                >
                  {{ formatTipo(selectedAlert.tipo) }}
                </UiBadge>
              </div>
              <div
                class="flex items-center gap-2 text-[11px]"
                :class="selectedAlert.lido ? 'text-slate-400' : 'text-slate-500'"
              >
                <ClockIcon class="h-3 w-3" />
                <span>{{ selectedAlert.dataHora }}</span>
              </div>
            </div>
          </div>
        </div>
        <p class="text-sm text-slate-600">
          Confirme para alterar o status do alerta.
        </p>
      </div>
      <template #footer>
        <UiButton variant="outline" @click="closeModal">Não agora</UiButton>
        <UiButton @click="toggleRead">{{ primaryActionLabel }}</UiButton>
      </template>
    </Modal>
  </section>
</template>

<script setup lang="ts">
import {
  ExclamationTriangleIcon,
  ExclamationCircleIcon,
  InformationCircleIcon,
  ClockIcon,
} from '@heroicons/vue/24/outline';
import UiBadge from '../components/ui/Badge.vue';
import UiButton from '../components/ui/Button.vue';
import Modal from '../components/Modal.vue';
import { computed, ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import api from '../services/api';

type AlertType = 'critico' | 'aviso' | 'info';
type AlertCategory = 'Infeccioso' | 'Permanencia' | 'Gargalo' | 'Limpeza' | 'Outros';

type Alert = {
  id: string;
  tipo: AlertType;
  categoria: AlertCategory;
  titulo: string;
  mensagem: string;
  dataHora: string;
  lido?: boolean;
};

const alertas = ref<Alert[]>([]);
const toast = useToast();
const showModal = ref(false);
const selectedAlert = ref<Alert | null>(null);

async function fetchAlertas() {
  try {
    const response = await api.get('/api/alertas');
    alertas.value = response.data;
    
    // Dispara a atualização do motor de alertas em background
    // Não usamos 'await' aqui para não travar a UI
    api.post('/api/alertas/gerar').catch(err => console.error('Erro background sync:', err));
    
  } catch (error) {
    console.error('Erro ao buscar alertas:', error);
    toast.error('Erro ao carregar alertas.');
  }
}

onMounted(() => {
  fetchAlertas();
});

const alertConfig: Record<
  AlertType,
  {
    icon: any;
    iconColor: string;
    badgeClass: string;
    cardClass: string;
    readClass: string;
    iconBg: string;
  }
> = {
  critico: {
    icon: InformationCircleIcon,
    iconColor: 'text-blue-600',
    badgeClass: 'border border-blue-200 bg-blue-100 text-blue-800',
    cardClass: 'border-blue-200 bg-blue-100',
    readClass: 'border-slate-200 bg-slate-50',
    iconBg: 'bg-blue-100',
  },
  aviso: {
    icon: InformationCircleIcon,
    iconColor: 'text-blue-600',
    badgeClass: 'border border-blue-200 bg-blue-100 text-blue-800',
    cardClass: 'border-blue-200 bg-blue-100',
    readClass: 'border-slate-200 bg-slate-50',
    iconBg: 'bg-blue-100',
  },
  info: {
    icon: InformationCircleIcon,
    iconColor: 'text-blue-600',
    badgeClass: 'border border-blue-200 bg-blue-100 text-blue-800',
    cardClass: 'border-blue-200 bg-blue-100',
    readClass: 'border-slate-200 bg-slate-50',
    iconBg: 'bg-blue-100',
  },
};

const formatTipo = (tipo: AlertType) => 'Alerta';

const openModal = (alerta: Alert) => {
  selectedAlert.value = alerta;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  selectedAlert.value = null;
};

const modalTitle = computed(() =>
  selectedAlert.value?.lido ? 'Marcar alerta como não lido?' : 'Marcar pendência como lida/resolvida?'
);

const alertasFiltrados = computed(() => {
  return alertas.value;
});

const alertasNaoLidos = computed(() => {
  return alertasFiltrados.value.filter(a => !a.lido);
});

const primaryActionLabel = computed(() =>
  selectedAlert.value?.lido ? 'Marcar como não lida' : 'Sim, marcar como lida'
);

const marcarComoLido = async (alerta: Alert) => {
  try {
    await api.put(`/api/alertas/${alerta.id}/lido`, { lido: true });
    const idx = alertas.value.findIndex(a => a.id === alerta.id);
    if (idx >= 0) {
      alertas.value[idx].lido = true;
    }
    toast.success('Alerta arquivado.');
  } catch (error) {
    console.error('Erro ao marcar como lido:', error);
    toast.error('Erro ao atualizar alerta.');
  }
};

const marcarTodosLidos = async () => {
  try {
    await api.put('/api/alertas/lidos');
    alertas.value.forEach(a => {
      // Se estiver nos filtrados, marca como lido
      if (alertasFiltrados.value.some(f => f.id === a.id)) {
        a.lido = true;
      }
    });
    toast.success('Todos os alertas foram marcados como lidos.');
  } catch (error) {
    console.error('Erro ao marcar todos como lidos:', error);
    toast.error('Erro ao processar requisição.');
  }
};

const toggleRead = async () => {
  if (!selectedAlert.value) return;
  const idx = alertas.value.findIndex(a => a.id === selectedAlert.value?.id);
  if (idx >= 0) {
    const nextStatus = !alertas.value[idx].lido;
    try {
      await api.put(`/api/alertas/${selectedAlert.value.id}/lido`, { lido: nextStatus });
      const updated = { ...alertas.value[idx], lido: nextStatus };
      alertas.value[idx] = updated;
      selectedAlert.value = updated;
      toast.success(nextStatus ? 'Alerta marcado como lido/resolvido.' : 'Alerta marcado como não lido.');
    } catch (error) {
      console.error('Erro ao atualizar alerta:', error);
      toast.error('Erro ao atualizar status do alerta.');
    }
  }
  closeModal();
};
</script>
