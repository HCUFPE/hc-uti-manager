<template>
  <section class="space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div class="space-y-1">
        <h2 class="text-3xl font-bold text-slate-900">Solicitações de Vaga</h2>
      </div>
      <div class="flex flex-wrap items-center gap-4">
        <div class="flex items-center gap-2">
          <label class="text-sm font-medium text-slate-600">Filtrar Solicitações:</label>
          <input 
            v-model="filtroData" 
            type="date" 
            class="rounded-md border border-slate-200 px-3 py-1.5 text-sm text-slate-600 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            title="Filtrar por data da cirurgia"
          />
          <UiButton v-if="filtroData" variant="outline" size="sm" @click="filtroData = ''" class="shadow-sm">Limpar</UiButton>
        </div>
        <UiButton size="sm" class="shadow-sm" @click="showModalNova = true">
          <PlusIcon class="h-5 w-5 text-white" />
          Nova Solicitação
        </UiButton>
      </div>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-16">
      <div class="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
      <span class="ml-3 text-slate-500">Carregando solicitacoes...</span>
    </div>

    <div v-else-if="solicitacoesFiltradas.length === 0" class="rounded-xl border border-slate-200 bg-white py-16 text-center shadow-sm">
      <p class="text-slate-500">
        {{ filtroData ? 'Nenhuma solicitação com cirurgia prevista para esta data.' : 'Nenhuma solicitação de vaga encontrada.' }}
      </p>
    </div>

    <div v-else class="grid gap-4">
      <article
        v-for="sol in solicitacoesFiltradas"
        :key="sol.id"
        class="rounded-xl border border-slate-200 bg-white shadow-sm"
      >
        <header class="flex flex-wrap items-start justify-between gap-4 border-b border-slate-100 px-5 py-4">
          <div>
            <p class="text-xs font-semibold uppercase tracking-wide text-slate-500">Prontuario</p>
            <p class="text-lg font-semibold text-slate-900">{{ sol.prontuario }}</p>
            <p class="mt-1 text-sm text-slate-600">
              {{ sol.idade }} anos
              <span class="text-slate-400">•</span>
              {{ sol.especialidade }}
            </p>
            <p class="mt-1 text-xs text-slate-400">{{ formatarDataHoraBR(sol.dataHora) }}</p>
          </div>
          <UiBadge :class="statusClass[sol.status]">
            {{ sol.status === 'Pendente' ? 'Aguardando Reserva de Leito' : (sol.status === 'Reservado' ? 'Leito Reservado' : sol.status) }}
          </UiBadge>
        </header>

        <div class="px-5 py-4">
          <div class="grid gap-4 sm:grid-cols-3">
            <div>
              <p class="text-xs uppercase tracking-wide text-slate-500">Tipo</p>
              <p class="mt-1 font-medium text-slate-900">{{ sol.tipo }}</p>
            </div>
            <div>
              <p class="text-xs uppercase tracking-wide text-slate-500">Data Prevista da Cirurgia</p>
              <p class="mt-1 font-medium text-slate-900">{{ sol.data_cirurgia ? formatarDataBR(sol.data_cirurgia) : 'Não informada' }}</p>
            </div>
            <div>
              <p class="text-xs uppercase tracking-wide text-slate-500">Turno</p>
              <p class="mt-1 font-medium text-slate-900">{{ sol.turno }}</p>
            </div>
          </div>

          <!-- Status detalhado removido conforme solicitado -->

          <div class="mt-4 flex flex-wrap gap-2">
            <UiButton
              v-if="sol.status === 'Pendente'"
              size="sm"
              @click="abrirModalReserva(sol)"
            >
              Reservar Leito
            </UiButton>
            <UiButton
              v-if="sol.status === 'Pendente'"
              size="sm"
              variant="outline"
              @click="abrirModalEdicao(sol)"
            >
              <PencilSquareIcon class="h-4 w-4 mr-1" />
              Editar
            </UiButton>
            <UiButton
              v-if="sol.status === 'Pendente'"
              size="sm"
              variant="destructive"
              @click="cancelarSolicitacao(sol.id)"
            >
              Cancelar Solicitacao
            </UiButton>
            <UiButton
              v-else-if="sol.status === 'Reservado'"
              size="sm"
              variant="outline"
              disabled
              title="Cancele a reserva no mapa de leitos para liberar"
            >
              Reservado
            </UiButton>
          </div>
        </div>
      </article>
    </div>

    <!-- Modal de Reserva -->
    <Modal :show="showModalReserva" @close="showModalReserva = false">
      <template #header>Reservar Leito para Prontuario {{ solSelecionada?.prontuario }}</template>
      <div class="space-y-4">
        <p class="text-sm text-slate-600">Selecione um leito disponivel ou em processo de alta:</p>
        
        <div v-if="loadingLeitos" class="flex justify-center py-4">
          <div class="h-6 w-6 animate-spin rounded-full border-2 border-blue-600 border-t-transparent"></div>
        </div>
        
        <div v-else-if="leitosDisponiveis.length === 0" class="text-center py-4 text-slate-500 italic">
          Nenhum leito disponivel para reserva no momento.
        </div>
        
        <div v-else class="grid grid-cols-2 gap-2 max-h-60 overflow-y-auto p-1">
          <button
            v-for="leito in leitosDisponiveis"
            :key="leito.lto_lto_id"
            class="flex flex-col items-start rounded-lg border p-3 text-left transition"
            :class="leitoEscolhido === leito.lto_lto_id ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-slate-200 hover:bg-slate-50'"
            @click="leitoEscolhido = leito.lto_lto_id"
          >
            <span class="font-bold text-slate-900">Leito {{ leito.lto_lto_id }}</span>
            <span class="text-xs text-slate-500 capitalize">{{ leito.status }} {{ leito.alta_solicitada ? '(Alta solicitada)' : '' }}</span>
          </button>
        </div>
      </div>
      <template #footer>
        <UiButton variant="outline" @click="showModalReserva = false">Cancelar</UiButton>
        <UiButton :disabled="!leitoEscolhido || submetendo" @click="confirmarReserva">
          {{ submetendo ? 'Reservando...' : 'Confirmar Reserva' }}
        </UiButton>
      </template>
    </Modal>

    <!-- Modal Nova/Editar Solicitacao -->
    <Modal :show="showModalNova" @close="fecharModalNova">
      <template #header>{{ isEditing ? 'Editar Solicitação' : 'Nova Solicitação' }}</template>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700">Prontuario</label>
          <input
            v-model="formNova.prontuario"
            type="text"
            class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700">Idade</label>
          <input
            v-model="formNova.idade"
            type="number"
            class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700">Especialidade</label>
          <select
            v-model="formNova.especialidade"
            class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          >
            <option value="" disabled>Selecione uma especialidade</option>
            <option value="BUCO (BUCOMAXILOFACIAL)">BUCO (BUCOMAXILOFACIAL)</option>
            <option value="CARDÍACA">CARDÍACA</option>
            <option value="CCP (CABEÇA E PESCOÇO)">CCP (CABEÇA E PESCOÇO)</option>
            <option value="CIPE (PEDIÁTRICA)">CIPE (PEDIÁTRICA)</option>
            <option value="ENDOSCOPIA">ENDOSCOPIA</option>
            <option value="GERAL">GERAL</option>
            <option value="GINECOLOGIA">GINECOLOGIA</option>
            <option value="HISTEROSCOPIA">HISTEROSCOPIA</option>
            <option value="NEUROLOGIA">NEUROLOGIA</option>
            <option value="OFTALMOLOGIA">OFTALMOLOGIA</option>
            <option value="ONCOLOGIA">ONCOLOGIA</option>
            <option value="ONCOMASTO (MASTOLOGIA)">ONCOMASTO (MASTOLOGIA)</option>
            <option value="ORL (OTORRINOLARINGOLOGIA)">ORL (OTORRINOLARINGOLOGIA)</option>
            <option value="ORTOPEDIA">ORTOPEDIA</option>
            <option value="PLÁSTICA">PLÁSTICA</option>
            <option value="PROCTOLOGIA">PROCTOLOGIA</option>
            <option value="TORÁCICA">TORÁCICA</option>
            <option value="TRANS">TRANS</option>
            <option value="UROLOGIA">UROLOGIA</option>
            <option value="VASCULAR">VASCULAR</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700">Tipo</label>
          <select
            v-model="formNova.tipo"
            class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          >
            <option value="" disabled>Selecione um Tipo</option>
            <option value="Clinico">Clinico</option>
            <option value="Cirurgico">Cirurgico</option>
            <option value="HEM">HEM</option>
            <option value="Obstetrico">Obstetrico</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700">Data Prevista da Cirurgia</label>
          <input
            v-model="formNova.data_cirurgia"
            type="date"
            :min="hoje"
            class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700">Turno</label>
          <select
            v-model="formNova.turno"
            class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          >
            <option value="" disabled>Selecione um Turno</option>
            <option value="Manhã">Manhã</option>
            <option value="Tarde">Tarde</option>
            <option value="Noite">Noite</option>
          </select>
        </div>
      </div>
      <template #footer>
        <UiButton variant="outline" @click="fecharModalNova">Cancelar</UiButton>
        <UiButton :disabled="submetendoNova" @click="salvarNova">
          {{ submetendoNova ? 'Salvando...' : (isEditing ? 'Salvar Alterações' : 'Salvar') }}
        </UiButton>
      </template>
    </Modal>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { PlusIcon, PencilSquareIcon } from '@heroicons/vue/24/outline';
import { useToast } from 'vue-toastification';
import UiBadge from '../components/ui/Badge.vue';
import UiButton from '../components/ui/Button.vue';
import Modal from '../components/Modal.vue';
import api from '../services/api';

type SolicitacaoStatus = 'Pendente' | 'Reservado' | 'Cancelada';

type Solicitacao = {
  id: string;
  prontuario: string;
  idade: number;
  especialidade: string;
  tipo: string;
  status: SolicitacaoStatus;
  turno: string;
  data_cirurgia?: string;
  destino?: string;
  dataHora: string;
};

const solicitacoes = ref<Solicitacao[]>([]);
const leitosDisponiveis = ref<any[]>([]);
const loading = ref(false);
const loadingLeitos = ref(false);
const submetendo = ref(false);
const showModalReserva = ref(false);
const solSelecionada = ref<Solicitacao | null>(null);
const leitoEscolhido = ref<string | null>(null);
const toast = useToast();

// Filtro e Nova Solicitação
const filtroData = ref('');
const showModalNova = ref(false);
const submetendoNova = ref(false);
const isEditing = ref(false);
const formNova = ref({
  prontuario: '',
  idade: null as number | null,
  especialidade: '',
  tipo: '',
  data_cirurgia: '',
  turno: ''
});

const hoje = new Date().toISOString().split('T')[0];

function formatarDataBR(dataISO: string) {
  if (!dataISO) return '';
  const [ano, mes, dia] = dataISO.split('-');
  return `${dia}/${mes}/${ano}`;
}

function formatarDataHoraBR(dataHoraISO: string) {
  if (!dataHoraISO) return '';
  // Espera formato "YYYY-MM-DD HH:MM"
  const [data, hora] = dataHoraISO.split(' ');
  if (!data) return dataHoraISO;
  const [ano, mes, dia] = data.split('-');
  return `${dia}/${mes}/${ano} ${hora || ''}`;
}

const solicitacoesFiltradas = computed(() => {
  let lista = [...solicitacoes.value];

  // 1. Aplicar Filtro (se houver)
  if (filtroData.value) {
    lista = lista.filter(sol => sol.data_cirurgia === filtroData.value);
  }

  // 2. Aplicar Ordenação
  const ordemTurno: Record<string, number> = { 'Manhã': 1, 'Tarde': 2, 'Noite': 3 };

  return lista.sort((a, b) => {
    // Comparar Data da Cirurgia (coloca quem não tem data no final)
    const dataA = a.data_cirurgia || '9999-12-31';
    const dataB = b.data_cirurgia || '9999-12-31';

    if (dataA !== dataB) {
      return dataA.localeCompare(dataB);
    }

    // Se a data for igual, compara o Turno
    const pesoA = ordemTurno[a.turno] || 99;
    const pesoB = ordemTurno[b.turno] || 99;
    
    return pesoA - pesoB;
  });
});

async function carregar() {
  loading.value = true;
  try {
    const resp = await api.get('/api/solicitacoes-leito');
    solicitacoes.value = resp.data;
  } catch (e: any) {
    console.error(e);
    toast.error('Erro ao carregar solicitacoes.');
  } finally {
    loading.value = false;
  }
}

async function abrirModalReserva(sol: Solicitacao) {
  solSelecionada.value = sol;
  leitoEscolhido.value = null;
  showModalReserva.value = true;
  loadingLeitos.value = true;
  try {
    const resp = await api.get('/api/leitos/disponiveis-para-reserva');
    leitosDisponiveis.value = resp.data;
  } catch (e: any) {
    toast.error('Erro ao buscar leitos disponiveis.');
  } finally {
    loadingLeitos.value = false;
  }
}

async function confirmarReserva() {
  if (!solSelecionada.value || !leitoEscolhido.value) return;
  submetendo.value = true;
  try {
    await api.post(`/api/solicitacoes-leito/${solSelecionada.value.id}/reservar`, {
      leito_id: leitoEscolhido.value
    });
    toast.success('Reserva realizada com sucesso!');
    showModalReserva.value = false;
    await carregar();
  } catch (e: any) {
    toast.error('Erro ao realizar reserva.');
  } finally {
    submetendo.value = false;
  }
}

async function cancelarSolicitacao(id: string) {
  try {
    await api.delete(`/api/solicitacoes-leito/${id}`);
    toast.warning('Solicitação cancelada.');
    await carregar();
  } catch (e: any) {
    toast.error('Erro ao cancelar solicitação.');
  }
}

async function abrirModalEdicao(sol: Solicitacao) {
  isEditing.value = true;
  solSelecionada.value = sol;
  formNova.value = {
    prontuario: sol.prontuario,
    idade: sol.idade,
    especialidade: sol.especialidade,
    tipo: sol.tipo,
    data_cirurgia: sol.data_cirurgia || '',
    turno: sol.turno
  };
  showModalNova.value = true;
}

function fecharModalNova() {
  showModalNova.value = false;
  isEditing.value = false;
  solSelecionada.value = null;
  formNova.value = { prontuario: '', idade: null, especialidade: '', tipo: '', data_cirurgia: '', turno: '' };
}

async function salvarNova() {
  if (!formNova.value.prontuario || !formNova.value.idade || !formNova.value.especialidade || !formNova.value.tipo || !formNova.value.turno) {
    toast.error('Preencha os campos obrigatorios.');
    return;
  }
  submetendoNova.value = true;
  try {
    if (isEditing.value && solSelecionada.value) {
      await api.patch(`/api/solicitacoes-leito/${solSelecionada.value.id}`, formNova.value);
      toast.success('Solicitacao atualizada com sucesso!');
    } else {
      await api.post('/api/solicitacoes-leito', formNova.value);
      toast.success('Solicitacao criada com sucesso!');
    }
    fecharModalNova();
    await carregar();
  } catch (e: any) {
    toast.error(isEditing.value ? 'Erro ao atualizar solicitação.' : 'Erro ao criar solicitação.');
    console.error(e);
  } finally {
    submetendoNova.value = false;
  }
}

const statusClass: Record<string, string> = {
  Pendente: 'border-rose-300 bg-rose-500/80 text-rose-100',
  Reservado: 'border-emerald-300 bg-emerald-500/80 text-emerald-100',
  Cancelada: 'border-slate-300 bg-slate-500/80 text-slate-100',
};

onMounted(carregar);
</script>
