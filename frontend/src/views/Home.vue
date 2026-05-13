<template>
  <section class="space-y-6">
    <div class="space-y-3 mb-12">
      <div class="flex items-center justify-between">
        <h2 class="text-3xl font-bold text-slate-900">Resumo dos Leitos</h2>
      </div>
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
        <div
          v-for="card in overviewCards"
          :key="card.title"
          class="rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
        >
          <p class="text-sm font-medium text-slate-600">{{ card.title }}</p>
          <p :class="['mt-2 text-3xl font-bold', card.color]">{{ card.value }}</p>
          <p v-if="card.caption" class="mt-1 text-xs text-slate-500">{{ card.caption }}</p>
        </div>
      </div>
    </div>
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h2 class="text-3xl font-bold text-slate-900">Visão Geral dos Leitos</h2>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <TransitionGroup
          name="fade-scale"
          tag="div"
          class="flex flex-wrap items-center gap-2"
        >
          <button
            v-for="option in statusFilterOptions"
            v-if="filtrosAbertos"
            :key="option.value"
            class="flex items-center gap-2 rounded-lg border px-3 py-1 text-sm font-medium transition"
            :class="
              statusFilter === option.value
                ? 'border-blue-200 bg-blue-50 text-blue-700 shadow-sm'
                : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
            "
            @click="setStatusFilter(option.value)"
          >
            <span class="h-2 w-2 rounded-full" :class="dotColor(option.value)" />
            {{ option.label }}
          </button>
        </TransitionGroup>
        <UiButton
          variant="outline"
          size="sm"
          class="shadow-sm"
          @click="toggleFiltros"
        >
          <FunnelIcon class="h-5 w-5 text-slate-600" />
          <ChevronRightIcon
            class="h-4 w-4 text-slate-500 transition-transform duration-200"
            :class="filtrosAbertos ? 'rotate-180' : ''"
          />
        </UiButton>
      </div>
    </div>

    <TransitionGroup
      name="list"
      tag="div"
      class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
    >
      <BedCard
        v-for="leito in leitosFiltrados"
        :key="leito.leitoNumero"
        v-bind="leito"
        @solicitar-alta="handleSolicitarAlta(leito)"
        @cancelar-alta="handleCancelarAlta(leito)"
        @cancelar-reserva="handleCancelarReserva(leito)"
      />
    </TransitionGroup>

    <!-- Modal Solicitar Alta (UTI) -->
    <Modal :show="showModalAlta" @close="showModalAlta = false">
      <template #header>
        Solicitar Alta - Leito {{ leitoSelecionado?.leitoNumero }}
      </template>
      
      <div class="space-y-4 py-2">
        <div class="rounded-lg bg-blue-50 p-3 border border-blue-100">
          <p class="text-xs text-blue-700">
            Informe abaixo qualquer necessidade especial para o transporte ou cuidados no destino (ex: O2, Isolamento).
          </p>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Necessidades Especiais</label>
          <textarea
            v-model="formAlta.necessidadesEspeciais"
            rows="4"
            placeholder="Ex: Oxigênio portatil, Maca reforçada, Isolamento de contato..."
            class="w-full rounded-lg border border-slate-200 px-4 py-3 text-sm focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-500/10 transition-all"
          />
        </div>
      </div>
      
      <template #footer>
        <UiButton variant="outline" @click="showModalAlta = false">Cancelar</UiButton>
        <UiButton class="bg-blue-600 hover:bg-blue-700" @click="confirmarSolicitacaoAlta">
          Confirmar Solicitação
        </UiButton>
      </template>
    </Modal>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import { FunnelIcon } from '@heroicons/vue/24/outline';
import { ChevronRightIcon } from '@heroicons/vue/20/solid';
import BedCard from '../components/BedCard.vue';
import UiButton from '../components/ui/Button.vue';
import { useToast } from 'vue-toastification';
import api from '../services/api';
import Modal from '../components/Modal.vue';

type BedStatus = 'disponivel' | 'ocupado' | 'higienizacao' | 'desativado' | 'alta' | 'reservado';
type BedType = 'cirurgico' | 'hem' | 'obstetrico' | 'uti' | 'outro' | 'nao_definido';
type StatusFilter = BedStatus | 'todos';

type Patient = {
  prontuario: string;
  idade: number;
  especialidade: string;
  dataCirurgia?: string;
  turno?: string;
};

type Leito = {
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
};

const leitos = ref<Leito[]>([]);
const toast = useToast();

const loadLeitos = async () => {
  try {
    const response = await api.get('/api/leitos');
    leitos.value = response.data.map((l: any) => ({
      leitoNumero: l.lto_lto_id,
      status: l.alta_solicitada ? 'alta' :
              (l.status || '').toLowerCase() === 'ocupado' ? 'ocupado' :
              l.prontuario_proximo ? 'reservado' :
              (l.status || '').toLowerCase() === 'desocupado' ? 'disponivel' :
              (l.status || '').toLowerCase() === 'limpeza' ? 'higienizacao' :
              (l.status || '').toLowerCase() === 'interditado' ? 'desativado' : 'disponivel',
      tipo: (l.tipo || 'outro').toLowerCase(),
      sinalizacaoTransferencia: l.alta_solicitada,
      pacienteAtual: l.prontuario_atual ? {
        prontuario: String(l.prontuario_atual),
        idade: l.idade_atual || 0,
        especialidade: l.especialidade_atual || 'ND',
      } : undefined,
      proximoPaciente: l.prontuario_proximo ? {
        prontuario: String(l.prontuario_proximo),
        idade: l.idade_proximo || 0,
        especialidade: l.especialidade_proximo || 'ND',
        dataCirurgia: l.data_cirurgia_proximo,
        turno: l.turno_proximo,
      } : undefined,
      temConflito: l.conflito_reserva || false,
      destinoDefinido: l.leito_destino,
      destinoDisponivel: l.destino_disponivel || false,
    }));
  } catch (error) {
    console.error('Erro ao buscar leitos:', error);
    toast.error('Falha ao carregar leitos. Verifique a conexao.');
  }
};

onMounted(() => {
  loadLeitos();
});

const overviewCards = computed(() => {
  const total = leitos.value.length;
  const ocupados = leitos.value.filter(l => ['ocupado', 'alta'].includes(l.status)).length;
  const disponiveis = leitos.value.filter(l => l.status === 'disponivel').length;
  const higienizacao = leitos.value.filter(l => l.status === 'higienizacao').length;
  const desativados = leitos.value.filter(l => l.status === 'desativado').length;
  const reservas = leitos.value.filter(l => l.proximoPaciente).length;

  const percOcupacao = total > 0 ? Math.round((ocupados / total) * 100) : 0;

  return [
    { title: 'Taxa de Ocupacao Global', value: `${percOcupacao}%`, color: 'text-blue-600', caption: `${ocupados} de ${total} leitos ocupados` },
    { title: 'Leitos Disponiveis', value: disponiveis.toString(), color: 'text-emerald-600' },
    { title: 'Leitos em Uso', value: ocupados.toString(), color: 'text-amber-500' },
    { title: 'Leitos em Higienizacao', value: higienizacao.toString(), color: 'text-indigo-500' },
    { title: 'Leitos Desativados', value: desativados.toString(), color: 'text-slate-500' },
    { title: 'Reservas Pendentes', value: reservas.toString(), color: 'text-purple-600' },
  ];
});

const statusFilterOptions: { label: string; value: StatusFilter }[] = [
  { label: 'Todos', value: 'todos' },
  { label: 'Disponíveis', value: 'disponivel' },
  { label: 'Ocupados', value: 'ocupado' },
  { label: 'Higienização', value: 'higienizacao' },
  { label: 'Desativados', value: 'desativado' },
  { label: 'Alta', value: 'alta' },
  { label: 'Reservado', value: 'reservado' },
];

const statusFilter = ref<StatusFilter>('todos');
const filtrosAbertos = ref(false);

const leitosFiltrados = computed(() => {
  if (statusFilter.value === 'todos') return leitos.value;
  return leitos.value.filter(leito => leito.status === statusFilter.value);
});

const setStatusFilter = (valor: StatusFilter) => {
  statusFilter.value = statusFilter.value === valor ? 'todos' : valor;
};

const toggleFiltros = () => {
  filtrosAbertos.value = !filtrosAbertos.value;
};

const dotColor = (valor: StatusFilter) => {
  switch (valor) {
    case 'disponivel':
      return 'bg-emerald-500';
    case 'ocupado':
      return 'bg-amber-500';
    case 'higienizacao':
      return 'bg-blue-500';
    case 'desativado':
      return 'bg-slate-400';
    case 'alta':
      return 'bg-fuchsia-500';
    case 'reservado':
      return 'bg-purple-500';
    default:
      return 'bg-slate-300';
  }
};

const showModalAlta = ref(false);
const leitoSelecionado = ref<Leito | null>(null);
const formAlta = ref({ necessidadesEspeciais: '' });

const handleSolicitarAlta = (leito: Leito) => {
  leitoSelecionado.value = leito;
  formAlta.value.necessidadesEspeciais = '';
  showModalAlta.value = true;
};

const confirmarSolicitacaoAlta = async () => {
  if (!leitoSelecionado.value) return;
  
  try {
    await api.post(`/api/altas/${leitoSelecionado.value.leitoNumero}`, formAlta.value);
    toast.success(`Alta solicitada para o leito ${leitoSelecionado.value.leitoNumero}.`);
    showModalAlta.value = false;
    await loadLeitos();
  } catch (e: any) {
    console.error(e);
    toast.error('Erro ao solicitar alta.');
  }
};

const handleCancelarAlta = async (leito: Leito) => {
  try {
    // Busca a solicitação pendente para este leito
    const resp = await api.get('/api/altas');
    const solicitacao = resp.data.find((a: any) => a.leitoAtual === leito.leitoNumero && a.status !== 'cancelada');
    
    if (solicitacao) {
      await api.delete(`/api/altas/${solicitacao.id}`);
      toast.warning(`Alta cancelada para o leito ${leito.leitoNumero}.`);
      await loadLeitos();
    }
  } catch (e: any) {
    console.error(e);
    toast.error('Erro ao cancelar alta.');
  }
};

const handleCancelarReserva = async (leito: Leito) => {
  try {
    await api.delete(`/api/leitos/${leito.leitoNumero}/reserva`);
    toast.warning(`Reserva cancelada para o leito ${leito.leitoNumero}.`);
    await loadLeitos();
  } catch (e: any) {
    console.error(e);
    toast.error('Erro ao cancelar reserva.');
  }
};
</script>

<style scoped>
.fade-scale-enter-active,
.fade-scale-leave-active,
.list-enter-active,
.list-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-scale-enter-from,
.fade-scale-leave-to,
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.98);
}

.list-move {
  transition: transform 0.3s ease;
}
</style>
