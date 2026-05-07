<template>
  <section class="space-y-6">
    <!-- Cabeçalho e Filtros -->
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
          <PlusIcon class="h-5 w-5 text-white mr-1" />
          Nova Solicitação
        </UiButton>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-16">
      <div class="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
      <span class="ml-3 text-slate-500">Carregando solicitações...</span>
    </div>

    <!-- Empty State Global -->
    <div v-else-if="solicitacoesFiltradas.length === 0" class="rounded-xl border border-slate-200 bg-white py-16 text-center shadow-sm">
      <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-slate-50 text-slate-300 mb-4">
        <ClipboardIcon class="h-8 w-8" />
      </div>
      <p class="text-slate-500">
        {{ filtroData ? 'Nenhuma solicitação com cirurgia prevista para esta data.' : 'Nenhuma solicitação de vaga encontrada.' }}
      </p>
    </div>

    <!-- Conteúdo com Seções -->
    <div v-else class="space-y-12">
      
      <!-- SEÇÃO 1: AGUARDANDO RESERVA -->
      <section>
        <div class="mb-6 flex items-center gap-3">
          <div class="h-8 w-1 rounded bg-rose-500"></div>
          <h2 class="text-xl font-bold text-slate-800">Aguardando Reserva de Leito</h2>
          <span class="rounded-full bg-rose-100 px-3 py-1 text-sm font-bold text-rose-600">
            {{ solicitacoesPendentes.length }}
          </span>
        </div>

        <div v-if="solicitacoesPendentes.length > 0" class="space-y-4">
          <article
            v-for="sol in solicitacoesPendentes"
            :key="sol.id"
            class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm transition hover:shadow-md"
          >
            <div class="flex items-start justify-between p-6">
              <div class="grid grid-cols-1 md:grid-cols-4 gap-6 w-full text-left">
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Prontuário</p>
                  <p class="text-xl font-black text-slate-800">{{ sol.prontuario }}</p>
                  <p class="text-sm text-slate-600">{{ sol.idade }} anos • {{ sol.especialidade }}</p>
                  <p class="text-[10px] text-slate-400">{{ formatarDataHoraBR(sol.dataHora) }}</p>
                </div>
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Tipo</p>
                  <p class="text-base font-bold text-slate-700">{{ sol.tipo }}</p>
                </div>
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Data Prevista</p>
                  <p class="text-base font-bold text-slate-700">{{ sol.data_cirurgia ? formatarDataBR(sol.data_cirurgia) : 'Não informada' }}</p>
                </div>
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Turno</p>
                  <p class="text-base font-bold text-slate-700">{{ sol.turno }}</p>
                </div>
              </div>
              <div class="flex flex-col items-end">
                <span class="rounded-full border border-rose-200 bg-rose-50 px-3 py-1 text-[10px] font-bold uppercase tracking-tighter text-rose-600">
                  Aguardando
                </span>
              </div>
            </div>

            <!-- Ações para Pendentes -->
            <div class="flex items-center gap-2 border-t border-slate-50 bg-slate-50/50 px-6 py-3">
              <UiButton size="sm" @click="abrirModalReserva(sol)" class="bg-blue-600 text-white hover:bg-blue-700 shadow-sm px-4">
                Reservar Leito
              </UiButton>
              <UiButton size="sm" variant="outline" @click="abrirModalEdicao(sol)" class="shadow-sm">
                <PencilSquareIcon class="h-4 w-4 mr-1 text-slate-500" />
                Editar
              </UiButton>
              <UiButton 
                size="sm" 
                @click="cancelarSolicitacao(sol.id)" 
                class="bg-red-600 text-white hover:bg-red-700 border-none shadow-sm px-4"
              >
                Cancelar Solicitação
              </UiButton>
            </div>
          </article>
        </div>
        <div v-else class="rounded-xl border border-dashed border-slate-200 py-12 text-center text-slate-400">
          Nenhuma solicitação aguardando reserva.
        </div>
      </section>

      <!-- SEÇÃO 2: SOLICITAÇÕES RESERVADAS -->
      <section>
        <div class="mb-6 flex items-center gap-3">
          <div class="h-8 w-1 rounded bg-emerald-500"></div>
          <h2 class="text-xl font-bold text-slate-800">Solicitações com Vagas Reservadas</h2>
          <span class="rounded-full bg-emerald-100 px-3 py-1 text-sm font-bold text-emerald-600">
            {{ solicitacoesReservadas.length }}
          </span>
        </div>

        <div v-if="solicitacoesReservadas.length > 0" class="space-y-4">
          <article
            v-for="sol in solicitacoesReservadas"
            :key="sol.id"
            class="overflow-hidden rounded-xl border border-emerald-100 bg-white shadow-sm transition hover:shadow-md opacity-90"
          >
            <div class="flex items-start justify-between p-6">
              <div class="grid grid-cols-1 md:grid-cols-5 gap-6 w-full text-left">
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Prontuário</p>
                  <p class="text-xl font-black text-slate-800">{{ sol.prontuario }}</p>
                  <p class="text-sm text-slate-600">{{ sol.idade }} anos</p>
                </div>
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-emerald-500">Leito Reservado</p>
                  <p class="text-lg font-black text-emerald-700">{{ sol.destino || '---' }}</p>
                </div>
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Turno</p>
                  <p class="text-base font-bold text-slate-700">{{ sol.turno }}</p>
                </div>
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Data Cirurgia</p>
                  <p class="text-base font-bold text-slate-700">{{ sol.data_cirurgia ? formatarDataBR(sol.data_cirurgia) : '-' }}</p>
                </div>
                <div class="flex flex-col items-end justify-center">
                  <span class="rounded-full border border-emerald-300 bg-emerald-500 px-3 py-1 text-[10px] font-bold uppercase tracking-tighter text-white shadow-sm">
                    Reservado
                  </span>
                </div>
              </div>
            </div>
            <!-- Ações para Reservados -->
            <div class="flex items-center gap-2 border-t border-emerald-50 bg-emerald-50/30 px-6 py-3">
              <UiButton
                size="sm"
                variant="outline"
                @click="abrirModalEdicao(sol)"
                class="border-emerald-200 bg-white text-emerald-700 hover:bg-emerald-50"
              >
                <PencilSquareIcon class="h-4 w-4 mr-1" />
                Editar
              </UiButton>
              <UiButton 
                size="sm" 
                @click="cancelarReserva(sol.id)" 
                class="bg-rose-600 text-white hover:bg-rose-700 border-none shadow-sm"
              >
                <TrashIcon class="h-4 w-4 mr-1" />
                Cancelar Reserva
              </UiButton>
              <p class="ml-auto text-[10px] font-medium italic text-emerald-600">
                Aguardando chegada no AGHU
              </p>
            </div>
          </article>
        </div>
        <div v-else class="rounded-xl border border-dashed border-slate-200 py-8 text-center text-slate-400">
          Nenhuma vaga reservada no momento.
        </div>
      </section>

    </div>

    <!-- Modais -->
    <Modal :show="showModalReserva" @close="showModalReserva = false">
      <template #header>Reservar Leito para Prontuário {{ solSelecionada?.prontuario }}</template>
      <div class="space-y-4">
        <p class="text-sm text-slate-600">Selecione um leito disponível ou em processo de alta:</p>
        <div v-if="loadingLeitos" class="flex justify-center py-4">
          <div class="h-6 w-6 animate-spin rounded-full border-2 border-blue-600 border-t-transparent"></div>
        </div>
        <div v-else-if="leitosDisponiveis.length === 0" class="text-center py-4 text-slate-500 italic">
          Nenhum leito disponível para reserva no momento.
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

    <Modal :show="showModalNova" @close="fecharModalNova">
      <template #header>{{ isEditing ? 'Editar Solicitação' : 'Nova Solicitação' }}</template>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700">Prontuário</label>
          <input v-model="formNova.prontuario" type="text" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-slate-700">Idade</label>
            <input v-model="formNova.idade" type="number" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200" />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700">Tipo</label>
            <select v-model="formNova.tipo" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200">
              <option value="Clinico">Clinico</option>
              <option value="Cirurgico">Cirurgico</option>
              <option value="HEM">HEM</option>
              <option value="Obstetrico">Obstetrico</option>
            </select>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700">Especialidade</label>
          <input v-model="formNova.especialidade" type="text" list="especialidades" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200" />
          <datalist id="especialidades">
            <option value="CARDÍACA" /><option value="CCP (CABEÇA E PESCOÇO)" /><option value="CIPE (PEDIÁTRICA)" /><option value="NEUROLOGIA" /><option value="ORTOPEDIA" /><option value="UROLOGIA" /><option value="VASCULAR" />
          </datalist>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-slate-700">Data Cirurgia</label>
            <input v-model="formNova.data_cirurgia" type="date" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200" />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700">Turno</label>
            <select v-model="formNova.turno" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200">
              <option value="Manhã">Manhã</option>
              <option value="Tarde">Tarde</option>
              <option value="Noite">Noite</option>
            </select>
          </div>
        </div>
      </div>
      <template #footer>
        <UiButton variant="outline" @click="fecharModalNova">Cancelar</UiButton>
        <UiButton :disabled="submetendoNova" @click="salvarNova">
          {{ submetendoNova ? 'Salvando...' : 'Salvar' }}
        </UiButton>
      </template>
    </Modal>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { PlusIcon, PencilSquareIcon, BookmarkIcon, TrashIcon, ClipboardIcon } from '@heroicons/vue/24/outline';
import { useToast } from 'vue-toastification';
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

const filtroData = ref('');
const showModalNova = ref(false);
const submetendoNova = ref(false);
const isEditing = ref(false);
const formNova = ref({
  prontuario: '',
  idade: null as number | null,
  especialidade: '',
  tipo: 'Cirurgico',
  data_cirurgia: '',
  turno: 'Manhã'
});

function formatarDataHoraBR(dataHoraISO: string) {
  if (!dataHoraISO) return '';
  const [data, hora] = dataHoraISO.split(' ');
  const [ano, mes, dia] = data.split('-');
  return `${dia}/${mes}/${ano} ${hora || ''}`;
}

function formatarDataBR(data: string) {
  if (!data) return '';
  const [ano, mes, dia] = data.split('-');
  return `${dia}/${mes}/${ano}`;
}

const solicitacoesFiltradas = computed(() => {
  let lista = [...solicitacoes.value];
  if (filtroData.value) {
    lista = lista.filter(sol => sol.data_cirurgia === filtroData.value);
  }
  const ordemTurno: Record<string, number> = { 'Manhã': 1, 'Tarde': 2, 'Noite': 3 };
  return lista.sort((a, b) => {
    const dataA = a.data_cirurgia || '9999-12-31';
    const dataB = b.data_cirurgia || '9999-12-31';
    if (dataA !== dataB) return dataA.localeCompare(dataB);
    return (ordemTurno[a.turno] || 99) - (ordemTurno[b.turno] || 99);
  });
});

const solicitacoesPendentes = computed(() => solicitacoesFiltradas.value.filter(s => s.status === 'Pendente'));
const solicitacoesReservadas = computed(() => solicitacoesFiltradas.value.filter(s => s.status === 'Reservado'));

async function carregar() {
  loading.value = true;
  try {
    const resp = await api.get('/api/solicitacoes-leito');
    solicitacoes.value = resp.data;
  } catch (e) {
    toast.error('Erro ao carregar solicitações.');
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
  } catch (e) {
    toast.error('Erro ao buscar leitos disponíveis.');
  } finally {
    loadingLeitos.value = false;
  }
}

async function confirmarReserva() {
  if (!solSelecionada.value || !leitoEscolhido.value) return;
  submetendo.value = true;
  try {
    await api.post(`/api/solicitacoes-leito/${solSelecionada.value.id}/reservar`, { leito_id: leitoEscolhido.value });
    toast.success('Reserva realizada com sucesso!');
    showModalReserva.value = false;
    await carregar();
  } catch (e) {
    toast.error('Erro ao realizar reserva.');
  } finally {
    submetendo.value = false;
  }
}

async function cancelarSolicitacao(id: string) {
  if (!confirm('Deseja realmente cancelar esta solicitação?')) return;
  try {
    await api.delete(`/api/solicitacoes-leito/${id}`);
    toast.warning('Solicitação cancelada.');
    await carregar();
  } catch (e) {
    toast.error('Erro ao cancelar solicitação.');
  }
}

async function cancelarReserva(id: string) {
  if (!confirm('Deseja liberar este leito? O paciente voltará para a fila de espera.')) return;
  try {
    await api.post(`/api/solicitacoes-leito/${id}/cancelar-reserva`);
    toast.success('Reserva cancelada. Paciente voltou para a fila.');
    await carregar();
  } catch (e) {
    toast.error('Erro ao cancelar reserva.');
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
  formNova.value = { prontuario: '', idade: null, especialidade: '', tipo: 'Cirurgico', data_cirurgia: '', turno: 'Manhã' };
}

async function salvarNova() {
  if (!formNova.value.prontuario || !formNova.value.idade || !formNova.value.especialidade || !formNova.value.turno) {
    toast.error('Preencha os campos obrigatórios.');
    return;
  }
  submetendoNova.value = true;
  try {
    if (isEditing.value && solSelecionada.value) {
      await api.patch(`/api/solicitacoes-leito/${solSelecionada.value.id}`, formNova.value);
      toast.success('Solicitação atualizada com sucesso!');
    } else {
      await api.post('/api/solicitacoes-leito', formNova.value);
      toast.success('Solicitação criada com sucesso!');
    }
    fecharModalNova();
    await carregar();
  } catch (e) {
    toast.error('Erro ao salvar solicitação.');
  } finally {
    submetendoNova.value = false;
  }
}

onMounted(carregar);
</script>
