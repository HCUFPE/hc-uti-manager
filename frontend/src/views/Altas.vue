<template>
  <section class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-3xl font-bold text-slate-900">Solicitacoes de Alta</h2>
        <!-- Use computed property to reflect active count based on filtered data -->
        <p class="mt-1 text-sm text-slate-500">{{ activeAltasCount }} solicitacao(s) ativa(s)</p>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex items-center justify-center py-16">
      <div class="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
      <span class="ml-3 text-slate-500">Carregando solicitacoes...</span>
    </div>

    <!-- Error state -->
    <div v-else-if="erro" class="rounded-xl border border-red-200 bg-red-50 p-6 text-center">
      <p class="font-medium text-red-700">{{ erro }}</p>
      <UiButton class="mt-4" size="sm" @click="carregar">Tentar novamente</UiButton>
    </div>

    <!-- Empty state -->
    <div v-else-if="activeAltasList.length === 0" class="rounded-xl border border-slate-200 bg-white py-16 text-center shadow-sm">
      <p class="text-slate-500">Nenhuma solicitacao de alta ativa no momento.</p>
    </div>

    <!-- List -->
    <div v-else class="grid gap-4">
      <article
        v-for="alta in activeAltasList"
        :key="alta.id"
        class="rounded-xl border border-slate-200 bg-white shadow-sm"
      >
        <header class="flex flex-wrap items-start justify-between gap-4 border-b border-slate-100 px-5 py-4">
          <div>
            <p class="text-xs font-semibold uppercase tracking-wide text-slate-500">Prontuario</p>
            <p class="text-lg font-semibold text-slate-900">{{ alta.prontuario }}</p>
            <p v-if="alta.nomePaciente" class="mt-0.5 text-sm text-slate-700">{{ alta.nomePaciente }}</p>
            <div class="mt-1 flex items-center gap-2 text-sm text-slate-600">
              <ClockIcon class="h-4 w-4" />
              <span>{{ alta.dataHora }}</span>
            </div>
          </div>
          <UiBadge :class="statusClass[alta.status]">
            {{ statusText[alta.status] }}
          </UiBadge>
        </header>

        <div class="px-5 py-4">
          <div class="flex flex-wrap items-center gap-3">
            <div class="flex-1">
              <p class="text-xs uppercase tracking-wide text-slate-500">Leito Atual</p>
              <p class="text-xl font-bold text-slate-900">Leito {{ alta.leitoAtual }}</p>
            </div>
            <ArrowRightIcon class="h-5 w-5 text-slate-400" />
            <div class="flex-1">
              <p class="text-xs uppercase tracking-wide text-slate-500">Destino</p>
              <p class="font-semibold text-slate-900">{{ alta.leitoDestino || 'Pendente' }}</p>
            </div>
          </div>

          <div
            v-if="alta.necessidadesEspeciais"
            class="mt-4 border-l-4 border-blue-500 pl-3"
          >
            <p class="text-sm font-medium text-slate-700">Necessidades Especiais</p>
            <p class="mt-1 text-sm text-slate-600">{{ alta.necessidadesEspeciais }}</p>
          </div>

          <div class="mt-4 flex flex-wrap gap-2">
            <template v-if="alta.status === 'pendente'">
              <UiButton v-if="authStore.isAdmin || authStore.isNIR" size="sm" @click="openDestino(alta)">
                Indicar Destino
              </UiButton>
              <UiButton v-if="authStore.isAdmin || authStore.isUTI" size="sm" variant="destructive" @click="cancelarAlta(alta.id)">
                Cancelar Alta
              </UiButton>
            </template>
            <template v-else-if="alta.status === 'definida'">
              <div class="flex flex-wrap items-center gap-2">
                <UiButton v-if="authStore.isAdmin || authStore.isNIR" size="sm" variant="outline" @click="openDestino(alta)">
                  Alterar Destino
                </UiButton>
                
                <UiButton 
                  v-if="(authStore.isAdmin || authStore.isNIR) && !alta.destinoDisponivel" 
                  size="sm" 
                  class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold" 
                  @click="marcarDisponivel(alta.id)"
                >
                  <CheckCircleIcon class="h-4 w-4 mr-1.5" />
                  Destino Disponível
                </UiButton>
                
                <div v-if="alta.destinoDisponivel" class="flex items-center gap-2">
                  <UiBadge variant="outline" class="border-emerald-500 text-emerald-700 bg-emerald-50 font-bold py-1.5">
                    <CheckCircleIcon class="h-4 w-4 mr-1.5" />
                    DESTINO LIBERADO
                  </UiBadge>
                  
                  <UiButton 
                    v-if="authStore.isAdmin || authStore.isNIR" 
                    size="sm" 
                    variant="ghost" 
                    class="text-rose-600 hover:text-rose-700 hover:bg-rose-50 px-2"
                    @click="cancelarDisponibilidade(alta.id)"
                  >
                    Remover Liberação
                  </UiButton>
                </div>
                
                <UiButton v-if="authStore.isAdmin || authStore.isUTI" size="sm" variant="destructive" @click="cancelarAlta(alta.id)">
                  Cancelar Alta
                </UiButton>
              </div>
            </template>
            <template v-else-if="alta.status === 'cancelada'">
              <UiBadge variant="outline" class="border-slate-300 text-slate-500">Cancelada</UiBadge>
            </template>
          </div>
        </div>
      </article>
    </div>

    <!-- Modal para definir destino -->
    <Modal :show="showModalDestino" @close="showModalDestino = false">
      <template #header>Definir Destino de Alta</template>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700">Leito de Destino</label>
          <input
            v-model="formDestino.leitoDestino"
            type="text"
            placeholder="Ex: Enfermaria 2B - Leito 12"
            class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          />
        </div>
      </div>
      <template #footer>
        <UiButton variant="outline" @click="showModalDestino = false">Cancelar</UiButton>
        <UiButton @click="salvarDestino">Salvar</UiButton>
      </template>
    </Modal>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'; // Import computed
import { ClockIcon, ArrowRightIcon, CheckCircleIcon } from '@heroicons/vue/24/outline';
import { useToast } from 'vue-toastification';
import UiBadge from '../components/ui/Badge.vue';
import UiButton from '../components/ui/Button.vue';
import Modal from '../components/Modal.vue';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';

type AltaStatus = 'pendente' | 'definida' | 'cancelada';

type Alta = {
  id: string;
  prontuario: string;
  nomePaciente?: string;
  especialidade?: string;
  leitoAtual: string;
  leitoDestino: string;
  dataHora: string;
  necessidadesEspeciais?: string;
  status: AltaStatus;
  destinoDisponivel: boolean;
};

const altas = ref<Alta[]>([]);
const loading = ref(false);
const erro = ref<string | null>(null);
const showModalDestino = ref(false);
const altaSelecionada = ref<Alta | null>(null);
const formDestino = ref({ leitoDestino: '' });
const toast = useToast();
const authStore = useAuthStore();

async function carregar() {
  loading.value = true;
  erro.value = null;
  try {
    const resp = await api.get('/api/altas');
    // Filter out cancelled alta requests from the frontend list
    altas.value = resp.data.filter((a: Alta) => a.status !== 'cancelada');
  } catch (e: any) {
    erro.value = 'Erro ao carregar solicitacoes de alta. Verifique a conexao com o servidor.';
    console.error('Erro ao buscar altas:', e);
  } finally {
    loading.value = false;
  }
}

// Computed property for active alta count
// This now correctly reflects the length of the filtered list
const activeAltasCount = computed(() => altas.value.length);

// Computed property for filtered list (used for v-for)
// This should now reflect the filtered data from 'altas.value'
const activeAltasList = computed(() => altas.value);


function openDestino(alta: Alta) {
  altaSelecionada.value = alta;
  // Se o destino for o placeholder de pendência, deixamos vazio para mostrar o placeholder do input
  const valorAtual = alta.leitoDestino || '';
  formDestino.value.leitoDestino = valorAtual.includes('Pendente') ? '' : valorAtual;
  showModalDestino.value = true;
}

async function salvarDestino() {
  if (!altaSelecionada.value) return;
  try {
    await api.put(`/api/altas/${altaSelecionada.value.id}`, formDestino.value);
    toast.success('Destino atualizado com sucesso.');
    showModalDestino.value = false;
    await carregar(); // Re-fetch to update the list
  } catch (e: any) {
    toast.error('Erro ao atualizar destino.');
    console.error(e);
  }
}

async function cancelarAlta(id: string) {
  try {
    await api.delete(`/api/altas/${id}`);
    toast.success('Solicitacao de alta cancelada.');
    await carregar(); // Re-fetch to update the list and count
  } catch (e: any) {
    toast.error('Erro ao cancelar alta.');
    console.error(e);
  }
}

async function marcarDisponivel(id: string) {
  try {
    await api.patch(`/api/altas/${id}/disponivel`, { disponivel: true });
    toast.success('Destino marcado como disponível.');
    await carregar();
  } catch (e: any) {
    toast.error('Erro ao atualizar status do destino.');
    console.error(e);
  }
}

async function cancelarDisponibilidade(id: string) {
  try {
    await api.patch(`/api/altas/${id}/disponivel`, { disponivel: false });
    toast.warning('Liberação de destino removida.');
    await carregar();
  } catch (e: any) {
    toast.error('Erro ao cancelar disponibilidade.');
    console.error(e);
  }
}

const statusClass: Record<string, string> = {
  pendente: 'border-amber-300 bg-amber-500/70 text-amber-800',
  definida: 'border-emerald-300 bg-emerald-500/80 text-emerald-100',
  cancelada: 'border-slate-300 bg-slate-500/80 text-slate-100',
};

const statusText: Record<string, string> = {
  pendente: 'Aguardando NIR',
  definida: 'Destino Definido',
  cancelada: 'Cancelada',
};

onMounted(carregar);
</script>
