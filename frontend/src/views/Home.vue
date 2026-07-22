<template>
  <section class="space-y-6">
    <div v-if="!uiStore.isTvMode" class="space-y-3 mb-12">
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
              isFilterActive(option.value)
                ? 'border-blue-200 bg-blue-50 text-blue-700 shadow-sm'
                : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
            "
            @click="toggleStatusFilter(option.value)"
          >
            <span class="h-2 w-2 rounded-full" :class="dotColor(option.value)" />
            {{ option.label }}
          </button>
        </TransitionGroup>
        <button
          v-if="authStore.isUTI"
          class="flex items-center gap-2 rounded-lg border px-3 py-1.5 text-sm font-medium transition shadow-sm cursor-pointer select-none"
          :class="isMuted ? 'border-red-200 bg-red-50 text-red-600 hover:bg-red-100' : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'"
          @click="toggleMute"
          :title="isMuted ? 'Ativar alerta sonoro' : 'Desativar alerta sonoro'"
        >
          <template v-if="isMuted">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-5 w-5 shrink-0 text-red-500">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 9.75 19.5 12m0 0 2.25 2.25M19.5 12l2.25-2.25M19.5 12l-2.25 2.25m-10.5-6 4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
            </svg>
            <span class="text-xs font-semibold">Som Mudo</span>
          </template>
          <template v-else>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-5 w-5 shrink-0 text-slate-500">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
            </svg>
            <span class="text-xs font-semibold">Som Ativo</span>
          </template>
        </button>
        <button
          class="flex items-center gap-2 rounded-lg border px-3 py-1.5 text-sm font-medium transition shadow-sm cursor-pointer select-none"
          :class="uiStore.isTvMode ? 'border-blue-200 bg-blue-50 text-blue-700 hover:bg-blue-100' : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'"
          @click="uiStore.toggleTvMode"
          :title="uiStore.isTvMode ? 'Sair do Modo TV' : 'Ativar Modo TV'"
        >
          <TvIcon class="h-5 w-5 shrink-0" :class="uiStore.isTvMode ? 'text-blue-600' : 'text-slate-500'" />
          <span class="text-xs font-semibold">{{ uiStore.isTvMode ? 'Sair da TV' : 'Modo TV' }}</span>
        </button>
        <NotificationsPopover v-if="uiStore.isTvMode" />
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
      :class="uiStore.isTvMode ? 'grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8' : 'grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'"
    >
      <BedCard
        v-for="leito in leitosFiltrados"
        :key="leito.leitoNumero"
        v-bind="leito"
        @solicitar-alta="handleSolicitarAlta(leito)"
        @cancelar-alta="handleCancelarAlta(leito)"
        @cancelar-reserva="handleCancelarReserva(leito)"
        @liberar-encaminhamento="handleLiberarEncaminhamento"
        @cancelar-liberacao="handleCancelarLiberacao"
        @mudar-leito="handleMudarLeito"
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
          <label class="block text-sm font-medium text-slate-700 mb-3">Necessidades Especiais</label>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 bg-slate-50 p-4 rounded-xl border border-slate-100">
            <label
              v-for="opcao in OPCOES_NECESSIDADES"
              :key="opcao"
              class="flex items-start gap-2.5 p-2 rounded-lg hover:bg-slate-200/50 cursor-pointer transition-all select-none"
            >
              <input
                type="checkbox"
                :value="opcao"
                v-model="selectedNecessidades"
                @change="onNecessidadeChange(opcao)"
                class="mt-0.5 h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500/20 cursor-pointer"
              />
              <span class="text-sm font-medium text-slate-700">{{ opcao }}</span>
            </label>
          </div>
        </div>
      </div>
      
      <template #footer>
        <UiButton :disabled="submetendoAlta" variant="outline" @click="showModalAlta = false">Cancelar</UiButton>
        <UiButton :disabled="submetendoAlta" class="bg-blue-600 hover:bg-blue-700" @click="confirmarSolicitacaoAlta">
          {{ submetendoAlta ? 'Enviando...' : 'Confirmar Solicitação' }}
        </UiButton>
      </template>
    </Modal>

    <!-- Modal Cancelar Alta (UTI) -->
    <Modal :show="showModalCancelAlta" @close="fecharModalCancelAlta">
      <template #header>Cancelar Alta</template>
      <div class="space-y-4 py-2">
        <p class="text-sm text-slate-600">Selecione o motivo para cancelar a solicitação de alta:</p>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Motivo <span class="text-red-500">*</span></label>
          <select v-model="motivoCancelAlta" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200">
            <option value="" disabled selected>Selecione um motivo</option>
            <option v-for="m in MOTIVOS_CANCELAMENTO_ALTA" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>
      </div>
      <template #footer>
        <UiButton variant="outline" @click="fecharModalCancelAlta">Voltar</UiButton>
        <UiButton :disabled="!motivoCancelAlta" class="bg-red-600 text-white hover:bg-red-700 border-none" @click="confirmarCancelarAlta">
          Confirmar Cancelamento
        </UiButton>
      </template>
    </Modal>

    <!-- Modal Cancelar Reserva (UTI) -->
    <Modal :show="showModalCancelReserva" @close="showModalCancelReserva = false">
      <template #header>Cancelar Reserva - Leito {{ leitoCancelReserva?.leitoNumero }}</template>
      <div class="space-y-4 py-2">
        <p class="text-sm text-slate-600">Selecione o motivo para cancelar a reserva do leito:</p>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Motivo <span class="text-red-500">*</span></label>
          <select v-model="motivoCancelReserva" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200">
            <option value="" disabled selected>Selecione um motivo</option>
            <option v-for="m in MOTIVOS_CANCELAMENTO_RESERVA" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>
      </div>
      <template #footer>
        <UiButton variant="outline" @click="showModalCancelReserva = false">Voltar</UiButton>
        <UiButton :disabled="!motivoCancelReserva" class="bg-red-600 text-white hover:bg-red-700 border-none" @click="confirmarCancelarReserva">
          Confirmar Cancelamento
        </UiButton>
      </template>
    </Modal>

    <!-- Modal Mudar Leito (UTI) -->
    <Modal :show="showModalMudarLeito" @close="showModalMudarLeito = false">
      <template #header>Mudar Leito Reservado</template>
      <div class="space-y-4 py-2">
        <p class="text-sm text-slate-600">Selecione o novo leito disponível para transferir a reserva:</p>
        <div v-if="loadingLeitos" class="flex justify-center py-4">
          <div class="h-6 w-6 animate-spin rounded-full border-2 border-blue-600 border-t-transparent"></div>
        </div>
        <div v-else-if="leitosDisponiveisFiltrados.length === 0" class="text-center py-4 text-slate-500 italic">
          Nenhum leito disponível no momento.
        </div>
        <div v-else class="grid grid-cols-2 gap-2 max-h-60 overflow-y-auto p-1">
          <button
            v-for="leito in leitosDisponiveisFiltrados"
            :key="leito.lto_lto_id"
            class="flex flex-col items-start rounded-lg border p-3 text-left transition"
            :class="leitoEscolhido === leito.lto_lto_id ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-slate-200 hover:bg-slate-50'"
            @click="leitoEscolhido = leito.lto_lto_id"
          >
            <span class="font-bold text-slate-900 flex justify-between w-full items-center">
              <span>Leito {{ leito.lto_lto_id }}</span>
              <span v-if="leito.ja_tem_reserva" class="text-[10px] bg-amber-100 text-amber-800 px-1.5 py-0.5 rounded font-bold uppercase tracking-wide">
                Troca
              </span>
            </span>
            <span class="text-xs text-slate-500">
              <span v-if="leito.ja_tem_reserva" class="text-amber-600 font-medium">
                Reservado (Pront. {{ leito.prontuario_proximo }})
              </span>
              <span v-else class="capitalize">
                {{ leito.status }} {{ leito.alta_solicitada ? '(Alta solicitada)' : '' }}
              </span>
            </span>
          </button>
        </div>
      </div>
      <template #footer>
        <UiButton variant="outline" @click="showModalMudarLeito = false">Cancelar</UiButton>
        <UiButton :disabled="!leitoEscolhido || submetendo" @click="confirmarMudarLeito">
          {{ submetendo ? 'Mudando...' : 'Confirmar Mudança' }}
        </UiButton>
      </template>
    </Modal>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { FunnelIcon, TvIcon } from '@heroicons/vue/24/outline';
import { ChevronRightIcon } from '@heroicons/vue/20/solid';
import BedCard from '../components/BedCard.vue';
import UiButton from '../components/ui/Button.vue';
import { useToast } from 'vue-toastification';
import api from '../services/api';
import Modal from '../components/Modal.vue';
import { useAuthStore } from '../stores/auth';
import { useUiStore } from '../stores/ui';
import NotificationsPopover from '../components/NotificationsPopover.vue';

type BedStatus = 'disponivel' | 'ocupado' | 'higienizacao' | 'desativado' | 'alta' | 'reservado';
type BedType = 'cirurgico' | 'hem' | 'obstetrico' | 'uti' | 'outro' | 'nao_definido';
type StatusFilter = BedStatus | 'todos';

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
  cirurgiaFinalizada?: boolean;
  encaminhamentoLiberado?: boolean;
  solicitacaoId?: number;
};

const leitos = ref<Leito[]>([]);
const toast = useToast();
const authStore = useAuthStore();
const uiStore = useUiStore();

const leitosNotificados = ref<Set<string>>(new Set());
let soundIntervalId: any = null;

const verificarETocarSomCirurgias = () => {
  if (authStore.isUTI) {
    const temCirurgiaPendente = leitos.value.some(
      (l) => l.proximoPaciente && l.cirurgiaFinalizada && !l.encaminhamentoLiberado
    );
    if (temCirurgiaPendente) {
      uiStore.tocarAlertaSonoro();
    }
  }
};

const reiniciarSoundTimer = () => {
  if (soundIntervalId) {
    clearInterval(soundIntervalId);
  }
  verificarETocarSomCirurgias();
  soundIntervalId = setInterval(verificarETocarSomCirurgias, 30000); // Executa o bipe a cada 30 segundos se houver cirurgia pendente
};

const loadLeitos = async () => {
  try {
    const response = await api.get('/api/leitos');
    const novosLeitos = response.data.map((l: any) => ({
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
        nome: l.nome_paciente || undefined,
        idade: l.idade_atual || 0,
        especialidade: l.especialidade_atual || 'ND',
        dataNascimento: l.data_nascimento || undefined,
      } : undefined,
      proximoPaciente: l.prontuario_proximo ? {
        prontuario: String(l.prontuario_proximo),
        nome: l.nome_proximo || undefined,
        idade: l.idade_proximo || 0,
        especialidade: l.especialidade_proximo || 'ND',
        dataCirurgia: l.data_cirurgia_proximo,
        horaCirurgia: l.hora_cirurgia_proximo || undefined,
        turno: l.turno_proximo,
        horaCirurgiaFinalizada: l.cirurgia_finalizada_em || undefined,
      } : undefined,
      temConflito: l.conflito_reserva || false,
      destinoDefinido: l.leito_destino,
      destinoDisponivel: l.destino_disponivel || false,
      cirurgiaFinalizada: l.cirurgia_finalizada || false,
      encaminhamentoLiberado: l.encaminhamento_liberado || false,
      solicitacaoId: l.solicitacao_id,
    }));

    // Identificar leitos com cirurgia concluída e encaminhamento pendente de liberação
    const leitosComCirurgiaConcluida = novosLeitos.filter(
      (l: any) => l.proximoPaciente && l.cirurgiaFinalizada && !l.encaminhamentoLiberado
    );
    
    let deveTocarSom = false;
    const idsAtuais = new Set<string>();
    
    for (const leito of leitosComCirurgiaConcluida) {
      idsAtuais.add(leito.leitoNumero);
      if (!leitosNotificados.value.has(leito.leitoNumero)) {
        deveTocarSom = true;
      }
    }
    
    leitosNotificados.value = idsAtuais;
    
    if (deveTocarSom && authStore.isUTI) {
      uiStore.tocarAlertaSonoro();
      reiniciarSoundTimer(); // Reinicia o timer para sincronizar com o bipe imediato
    }

    leitos.value = novosLeitos;
  } catch (error) {
    console.error('Erro ao buscar leitos:', error);
    toast.error('Falha ao carregar leitos. Verifique a conexao.');
  }
};

let leitosIntervalId: any = null;

onMounted(() => {
  loadLeitos();
  leitosIntervalId = setInterval(loadLeitos, 120000);
  reiniciarSoundTimer();
});

onUnmounted(() => {
  if (leitosIntervalId) {
    clearInterval(leitosIntervalId);
  }
  if (soundIntervalId) {
    clearInterval(soundIntervalId);
  }
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

const statusFilters = ref<StatusFilter[]>([]);
const filtrosAbertos = ref(false);

const isFilterActive = (val: StatusFilter) => {
  if (val === 'todos') {
    return statusFilters.value.length === 0;
  }
  return statusFilters.value.includes(val);
};

const toggleStatusFilter = (val: StatusFilter) => {
  if (val === 'todos') {
    statusFilters.value = [];
    return;
  }
  const idx = statusFilters.value.indexOf(val);
  if (idx > -1) {
    statusFilters.value.splice(idx, 1);
  } else {
    statusFilters.value.push(val);
  }
};

const leitosFiltrados = computed(() => {
  if (statusFilters.value.length === 0) return leitos.value;
  return leitos.value.filter(leito => statusFilters.value.includes(leito.status));
});

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
const submetendoAlta = ref(false);
const leitoSelecionado = ref<Leito | null>(null);
const formAlta = ref({ necessidadesEspeciais: '' });
const selectedNecessidades = ref<string[]>([]);

const OPCOES_NECESSIDADES = [
  'Em uso de O2',
  'Gestante',
  'Isolamento de contato',
  'Isolamento respiratório',
  'Necessidade de aspiração',
  'Necessidade de ventilador no leito',
  'Puérpera',
  'Nenhum'
];

const onNecessidadeChange = (opcao: string) => {
  if (opcao === 'Nenhum') {
    if (selectedNecessidades.value.includes('Nenhum')) {
      selectedNecessidades.value = ['Nenhum'];
    }
  } else {
    selectedNecessidades.value = selectedNecessidades.value.filter(n => n !== 'Nenhum');
  }
};

const showModalCancelAlta = ref(false);
const motivoCancelAlta = ref('');
const MOTIVOS_CANCELAMENTO_ALTA = [
  'Piora Clínica',
  'Leito de Enfermaria Indisponível'
];

const showModalCancelReserva = ref(false);
const motivoCancelReserva = ref('');
const leitoCancelReserva = ref<Leito | null>(null);

const MOTIVOS_CANCELAMENTO_RESERVA = [
  'Pedido de vaga clínica (emergência)',
  'Pedido de vaga pela hemodinâmica',
  'Pedido de vaga pelo COB (emergência)',
  'Problemas relacionados a equipamentos',
  'Falta de vaga na enfermaria para paciente de alta',
  'Cancelamento de alta da UTI'
];

const handleSolicitarAlta = (leito: Leito) => {
  leitoSelecionado.value = leito;
  formAlta.value.necessidadesEspeciais = '';
  selectedNecessidades.value = ['Nenhum']; // Inicia com Nenhum selecionado por padrão
  showModalAlta.value = true;
};

const confirmarSolicitacaoAlta = async () => {
  if (!leitoSelecionado.value) return;
  submetendoAlta.value = true;
  
  // Serializa a lista de necessidades selecionadas
  const selecionadas = selectedNecessidades.value.filter(n => n !== 'Nenhum');
  if (selecionadas.length === 0) {
    formAlta.value.necessidadesEspeciais = 'Nenhum';
  } else {
    formAlta.value.necessidadesEspeciais = selecionadas.join(', ');
  }
  
  try {
    await api.post(`/api/altas/${leitoSelecionado.value.leitoNumero}`, formAlta.value);
    toast.success(`Alta solicitada para o leito ${leitoSelecionado.value.leitoNumero}.`);
    showModalAlta.value = false;
    await loadLeitos();
  } catch (e: any) {
    console.error(e);
    toast.error('Erro ao solicitar alta.');
  } finally {
    submetendoAlta.value = false;
  }
};

const handleCancelarAlta = async (leito: Leito) => {
  leitoSelecionado.value = leito;
  motivoCancelAlta.value = '';
  showModalCancelAlta.value = true;
};

const fecharModalCancelAlta = () => {
  showModalCancelAlta.value = false;
  leitoSelecionado.value = null;
  motivoCancelAlta.value = '';
};

const confirmarCancelarAlta = async () => {
  if (!leitoSelecionado.value || !motivoCancelAlta.value) return;
  
  try {
    const resp = await api.get('/api/altas');
    const solicitacao = resp.data.find((a: any) => a.leitoAtual === leitoSelecionado.value!.leitoNumero && a.status !== 'cancelada');
    
    if (solicitacao) {
      await api.delete(`/api/altas/${solicitacao.id}?motivo=${encodeURIComponent(motivoCancelAlta.value)}`);
      toast.warning(`Alta cancelada para o leito ${leitoSelecionado.value!.leitoNumero}.`);
      await loadLeitos();
    }
    fecharModalCancelAlta();
  } catch (e: any) {
    console.error(e);
    toast.error('Erro ao cancelar alta.');
  }
};

const handleCancelarReserva = (leito: Leito) => {
  leitoCancelReserva.value = leito;
  motivoCancelReserva.value = '';
  showModalCancelReserva.value = true;
};

const confirmarCancelarReserva = async () => {
  if (!leitoCancelReserva.value || !motivoCancelReserva.value) return;
  
  try {
    await api.delete(`/api/leitos/${leitoCancelReserva.value.leitoNumero}/reserva?motivo=${encodeURIComponent(motivoCancelReserva.value)}`);
    toast.warning(`Reserva cancelada para o leito ${leitoCancelReserva.value.leitoNumero}.`);
    await loadLeitos();
    showModalCancelReserva.value = false;
    leitoCancelReserva.value = null;
    motivoCancelReserva.value = '';
  } catch (e: any) {
    console.error(e);
    toast.error('Erro ao cancelar reserva.');
  }
};

const handleLiberarEncaminhamento = async (solicitacaoId: number) => {
  try {
    await api.post(`/api/solicitacoes/${solicitacaoId}/liberar-encaminhamento`);
    toast.success('Encaminhamento do paciente liberado com sucesso.');
    await loadLeitos();
  } catch (error: any) {
    console.error(error);
    toast.error('Erro ao liberar encaminhamento.');
  }
};

const handleCancelarLiberacao = async (solicitacaoId: number) => {
  try {
    await api.post(`/api/solicitacoes/${solicitacaoId}/cancelar-liberacao`);
    toast.warning('Liberação do encaminhamento cancelada. Alerta enviado ao solicitante.');
    await loadLeitos();
  } catch (error: any) {
    console.error(error);
    toast.error('Erro ao cancelar liberação.');
  }
};

const showModalMudarLeito = ref(false);
const solIdParaMudarLeito = ref<number | null>(null);
const leitoEscolhido = ref<string | null>(null);
const leitosDisponiveis = ref<any[]>([]);
const leitoOrigemMudarLeito = ref<string | null>(null);
const leitosDisponiveisFiltrados = computed(() => {
  console.log('leitosDisponiveisFiltrados - Origem:', leitoOrigemMudarLeito.value, 'Disponiveis:', leitosDisponiveis.value);
  if (!leitoOrigemMudarLeito.value) return leitosDisponiveis.value;
  return leitosDisponiveis.value.filter(l => l.lto_lto_id !== leitoOrigemMudarLeito.value);
});
const loadingLeitos = ref(false);
const submetendo = ref(false);

const carregarLeitosDisponiveis = async () => {
  loadingLeitos.value = true;
  try {
    const { data } = await api.get('/api/leitos/disponiveis?incluir_reservados=true');
    leitosDisponiveis.value = data;
  } catch (error) {
    console.error('Erro ao buscar leitos disponíveis:', error);
  } finally {
    loadingLeitos.value = false;
  }
};

const handleMudarLeito = (solicitacaoId: number, leitoNumero: string) => {
  console.log('handleMudarLeito called with:', solicitacaoId, leitoNumero);
  solIdParaMudarLeito.value = solicitacaoId;
  leitoOrigemMudarLeito.value = leitoNumero;
  leitoEscolhido.value = null;
  showModalMudarLeito.value = true;
  carregarLeitosDisponiveis();
};

const confirmarMudarLeito = async () => {
  if (!solIdParaMudarLeito.value || !leitoEscolhido.value) return;
  submetendo.value = true;
  try {
    await api.post(`/api/solicitacoes/${solIdParaMudarLeito.value}/remanejar-reserva`, {
      leito_id: leitoEscolhido.value
    });
    toast.success('Reserva remanejada com sucesso!');
    showModalMudarLeito.value = false;
    await loadLeitos();
  } catch (error: any) {
    console.error(error);
    toast.error(error.response?.data?.detail || 'Erro ao remanejar reserva.');
  } finally {
    submetendo.value = false;
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
