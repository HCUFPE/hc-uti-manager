<template>
  <section class="space-y-6">
    <!-- Título e Filtro de Período -->
    <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <h2 class="text-3xl font-bold text-slate-900">Indicadores Operacionais</h2>
      
      <!-- Painel de Filtros -->
      <div class="flex flex-wrap items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
        <div class="flex items-center gap-2">
          <label for="data-inicio" class="text-xs font-semibold text-slate-500">De:</label>
          <input
            id="data-inicio"
            type="date"
            v-model="dataInicio"
            class="rounded-lg border border-slate-300 px-2 py-1 text-sm text-slate-800 shadow-sm focus:border-blue-500 focus:outline-none"
          />
        </div>
        <div class="flex items-center gap-2">
          <label for="data-fim" class="text-xs font-semibold text-slate-500">Até:</label>
          <input
            id="data-fim"
            type="date"
            v-model="dataFim"
            class="rounded-lg border border-slate-300 px-2 py-1 text-sm text-slate-800 shadow-sm focus:border-blue-500 focus:outline-none"
          />
        </div>
        <div class="flex gap-2">
          <UiButton size="sm" class="h-8 text-xs" @click="fetchResumo">Filtrar</UiButton>
          <UiButton size="sm" variant="outline" class="h-8 text-xs" @click="limparFiltros">Limpar</UiButton>
        </div>
      </div>
    </div>

    <!-- Indicador de Carregamento -->
    <div v-if="loading" class="flex justify-center py-16">
      <div class="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
    </div>

    <!-- Mensagem de Erro -->
    <div v-else-if="erro" class="rounded-xl border border-red-200 bg-red-50 p-6 text-center text-red-700">
      {{ erro }}
    </div>

    <!-- Dashboard Principal -->
    <div v-else class="space-y-6">
      <!-- 4 Cards Principais de Visão Geral -->
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
        <article
          v-for="ind in indicadoresCalculados"
          :key="ind.titulo"
          class="rounded-xl border border-slate-200 bg-white shadow-sm hover:shadow transition-shadow"
        >
          <header class="flex items-start justify-between gap-3 border-b border-slate-100 px-5 py-4">
            <p class="text-sm font-semibold text-slate-600">{{ ind.titulo }}</p>
            <div class="rounded-lg bg-blue-50 p-2">
              <component :is="ind.icone" class="h-5 w-5 text-blue-600" />
            </div>
          </header>
          <div class="px-5 py-4">
            <div class="space-y-2">
              <div>
                <p class="text-4xl font-bold text-slate-900">{{ ind.valor }}</p>
                <p class="mt-1 text-sm text-slate-600">{{ ind.subtitulo }}</p>
              </div>
              <p class="border-t pt-2 text-xs text-slate-500">
                {{ ind.tendencia }}
              </p>
            </div>
          </div>
        </article>
      </div>

      <!-- Nova Seção: Tempos Médios de Processo e Fluxo (Gargalos) -->
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">

        <article class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Recepção Pós-Cirúrgico (BC)</p>
          <p class="mt-2 text-3xl font-extrabold text-slate-800">{{ detalhado.tempo_recepcao_bc_minutos ?? 0 }} min</p>
          <p class="mt-1 text-xs text-slate-500">Intervalo médio entre o fim cirúrgico e a entrada na UTI.</p>
        </article>

        <article class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Liberação Encaminhamento</p>
          <p class="mt-2 text-3xl font-extrabold text-slate-800 text-blue-600">{{ formatarTempoLiberacao(detalhado.tempo_liberacao_encaminhamento_minutos) }}</p>
          <p class="mt-1 text-xs text-slate-500">Espera média do fim da cirurgia até liberação de encaminhamento pela UTI.</p>
        </article>

        <article class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Acomodação de Alta (NIR)</p>
          <p class="mt-2 text-3xl font-extrabold text-slate-800">{{ detalhado.tempo_acomodacao_alta_horas ?? 0 }}h</p>
          <p class="mt-1 text-xs text-slate-500">Tempo desde a solicitação de alta até indicação de destino pós-UTI.</p>
        </article>

        <article class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Liberação de Leito de Acomodação</p>
          <p class="mt-2 text-3xl font-extrabold text-slate-800">{{ detalhado.tempo_liberacao_leito_horas ?? 0 }}h</p>
          <p class="mt-1 text-xs text-slate-500">Tempo desde a indicação do destino até a efetiva saída da UTI.</p>
        </article>

        <article class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Tempo de Higienização</p>
          <p class="mt-2 text-3xl font-extrabold text-slate-800 text-slate-800">{{ detalhado.tempo_higienizacao_minutos ?? 0 }} min</p>
          <p class="mt-1 text-xs text-slate-500">Tempo médio em que o leito da UTI fica com status de higienização.</p>
        </article>
      </div>

      <!-- Nova Seção: Taxas Operacionais, Horários e Relações de Volumes -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <!-- Taxas de Fluxo e Horário de Reserva -->
        <div class="space-y-6">
          <!-- Tabela Comparativa de Demandantes (Admissões vs Ocupação) -->
          <article class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 class="text-base font-bold text-slate-900 border-b pb-2 mb-3">Métricas por Demandante (Setor)</h3>
            <table class="w-full text-sm">
              <thead>
                <tr class="text-slate-400 border-b text-left">
                  <th class="pb-2 font-semibold">Demandante</th>
                  <th class="pb-2 font-semibold text-center">Internações</th>
                  <th class="pb-2 font-semibold text-right">Ocupação Média</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="dem in ['BC', 'HEM', 'COB', 'CLI']" :key="dem" class="text-slate-700">
                  <td class="py-2 font-medium">{{ dem === 'BC' ? 'Bloco Cirúrgico (BC)' : dem === 'HEM' ? 'Hemodinâmica (HEM)' : dem === 'COB' ? 'Obstetrícia (COB)' : 'Clínico / Outros (CLI)' }}</td>
                  <td class="py-2 text-center font-semibold">{{ detalhado.admissoes_semanais?.demandantes?.[dem] ?? 0 }}</td>
                  <td class="py-2 text-right font-semibold text-blue-600">{{ detalhado.tempo_ocupacao?.demandantes_horas?.[dem] ?? 0 }}h</td>
                </tr>
              </tbody>
            </table>
          </article>

          <!-- Tabela de Motivos de Cancelamento -->
          <article class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 class="text-base font-bold text-slate-900 border-b pb-2 mb-3">Principais motivos de cancelamento de solicitações</h3>
            <div v-if="!detalhado.motivos_cancelamento || Object.keys(detalhado.motivos_cancelamento).length === 0" class="text-sm text-slate-500 py-4 text-center">
              Nenhum cancelamento no período.
            </div>
            <table v-else class="w-full text-sm">
              <thead>
                <tr class="text-slate-400 border-b text-left">
                  <th class="pb-2 font-semibold">Motivo</th>
                  <th class="pb-2 font-semibold text-right">Qtd</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="(qtd, motivo) in detalhado.motivos_cancelamento" :key="motivo" class="text-slate-700">
                  <td class="py-2 font-medium">{{ motivo }}</td>
                  <td class="py-2 text-right font-bold text-slate-800">{{ qtd }}</td>
                </tr>
              </tbody>
            </table>
          </article>
        </div>        <!-- Resumos Volumétricos e Ciclo de Vida -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Quadro 1: Ciclo de Vida das Solicitações -->
          <article class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 class="text-base font-bold text-slate-900 border-b pb-2 mb-3">Ciclo de Vida das Solicitações (Pacientes)</h3>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-sm text-slate-700">
                <thead>
                  <tr class="bg-slate-50 text-slate-500 font-semibold border-b">
                    <th class="px-4 py-3">Situação do Paciente / Solicitação</th>
                    <th class="px-4 py-3 text-center">Volume Total</th>
                    <th class="px-4 py-3 text-right">Proporção / Relação</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr class="font-semibold bg-slate-50/50">
                    <td class="px-4 py-3">Solicitações Criadas (Demanda Total)</td>
                    <td class="px-4 py-3 text-center">{{ detalhado.volumes?.solicitacoes ?? 0 }}</td>
                    <td class="px-4 py-3 text-right">100%</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-3 pl-8 font-medium">├─ Concluídas (Pacientes Admitidos)</td>
                    <td class="px-4 py-3 text-center font-bold text-emerald-700">{{ detalhado.volumes?.concluidas_real ?? 0 }}</td>
                    <td class="px-4 py-3 text-right font-bold text-emerald-600">{{ detalhado.volumes?.percentual_concluidas ?? 0 }}% das criadas</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-3 pl-8 font-medium">├─ Canceladas (Fila / Desistências)</td>
                    <td class="px-4 py-3 text-center font-bold text-rose-700">{{ detalhado.volumes?.canceladas_real ?? 0 }}</td>
                    <td class="px-4 py-3 text-right font-bold text-rose-600">{{ detalhado.volumes?.percentual_canceladas ?? 0 }}% das criadas</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-3 pl-8 font-medium">├─ Reservas Ativas (Aguardando Entrada)</td>
                    <td class="px-4 py-3 text-center font-bold text-blue-700">{{ detalhado.volumes?.reservas_ativas ?? 0 }}</td>
                    <td class="px-4 py-3 text-right font-bold text-blue-600">{{ detalhado.volumes?.percentual_reservas_ativas ?? 0 }}% das criadas</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-3 pl-8 font-medium">└─ Pendentes na Fila (Aguardando Vaga)</td>
                    <td class="px-4 py-3 text-center font-bold text-amber-700">{{ detalhado.volumes?.pendentes_fila ?? 0 }}</td>
                    <td class="px-4 py-3 text-right font-bold text-amber-600">{{ detalhado.volumes?.percentual_pendentes_fila ?? 0 }}% das criadas</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </article>

          <!-- Quadro 2: Resumo de Ações da UTI e Altas -->
          <article class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 class="text-base font-bold text-slate-900 border-b pb-2 mb-3">Resumo de Ações da UTI e Altas (Trabalho)</h3>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-sm text-slate-700">
                <thead>
                  <tr class="bg-slate-50 text-slate-500 font-semibold border-b">
                    <th class="px-4 py-3">Ação Operacional Realizada</th>
                    <th class="px-4 py-3 text-center">Volume Total</th>
                    <th class="px-4 py-3 text-right">Descrição</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr>
                    <td class="px-4 py-3 font-medium">Reservas Efetuadas pela UTI</td>
                    <td class="px-4 py-3 text-center font-bold text-blue-600">{{ detalhado.volumes?.reservadas ?? 0 }}</td>
                    <td class="px-4 py-3 text-right text-slate-500">Cliques em "Reservar Leito"</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-3 font-medium">Reservas Canceladas pela UTI (Desfeitas)</td>
                    <td class="px-4 py-3 text-center font-bold text-rose-700">{{ detalhado.volumes?.cancelamento_reservas ?? 0 }}</td>
                    <td class="px-4 py-3 text-right text-slate-500">Cliques em "Cancelar Reserva"</td>
                  </tr>
                  <tr class="border-t-2">
                    <td class="px-4 py-3 font-medium">Altas Solicitadas pela UTI</td>
                    <td class="px-4 py-3 text-center font-bold text-indigo-700">{{ detalhado.volumes?.altas ?? 0 }}</td>
                    <td class="px-4 py-3 text-right text-slate-500">Solicitações de alta criadas</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-3 font-medium">Altas Pendentes (Aguardando Transferência)</td>
                    <td class="px-4 py-3 text-center font-bold text-indigo-500">{{ detalhado.volumes?.altas_pendentes ?? 0 }}</td>
                    <td class="px-4 py-3 text-right text-slate-500">Solicitações de alta ativas/pendentes</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-3 font-medium">Altas Concluídas (Transferências Físicas)</td>
                    <td class="px-4 py-3 text-center font-bold text-indigo-950">{{ detalhado.volumes?.altas_concluidas ?? 0 }}</td>
                    <td class="px-4 py-3 text-right text-slate-500">Pacientes que deixaram a UTI</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-3 font-medium">Altas Canceladas pela UTI / NIR</td>
                    <td class="px-4 py-3 text-center font-bold text-rose-700">{{ detalhado.volumes?.altas_canceladas ?? 0 }}</td>
                    <td class="px-4 py-3 text-right text-slate-500">Solicitações de alta canceladas</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </article>
        </div>
      </div>

      <!-- Gráfico de Ocupação Semanal -->
      <article class="rounded-xl border border-slate-200 bg-white shadow-sm">
        <header class="border-b border-slate-100 px-5 py-4">
          <h3 class="text-lg font-semibold text-slate-900">Gráfico de Ocupação Semanal</h3>
        </header>
        <div class="p-5 h-80">
          <Line v-if="graficosData.ocupacao" :data="graficosData.ocupacao" :options="lineOptions" />
        </div>
      </article>

      <!-- Gráficos de Especialidades e Tipos de Solicitação -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <article class="rounded-xl border border-slate-200 bg-white shadow-sm">
          <header class="border-b border-slate-100 px-5 py-4">
            <h3 class="text-lg font-semibold text-slate-900">Distribuição por Especialidade (Pacientes Internados)</h3>
          </header>
          <div class="p-5 flex flex-col md:flex-row items-center gap-6 justify-center">
            <div class="h-60 w-60 flex-shrink-0">
              <Pie v-if="graficosData.especialidade" :data="graficosData.especialidade" :options="pieOptions" />
            </div>
            <!-- Custom Legend with Numbers -->
            <div class="flex-1 w-full space-y-2 text-sm text-slate-600 max-h-60 overflow-y-auto pr-2">
              <div v-for="(label, idx) in graficosRaw.distribuicao_especialidade?.labels || []" :key="label" class="flex justify-between border-b pb-1">
                <div class="flex items-center gap-2">
                  <span class="h-3 w-3 rounded-full flex-shrink-0" :style="{ backgroundColor: bgColors[idx % bgColors.length] }"></span>
                  <span class="truncate max-w-[150px]" :title="label">{{ label }}</span>
                </div>
                <span class="font-bold text-slate-800">{{ graficosRaw.distribuicao_especialidade?.data?.[idx] ?? 0 }} leito(s)</span>
              </div>
            </div>
          </div>
        </article>

        <article class="rounded-xl border border-slate-200 bg-white shadow-sm">
          <header class="border-b border-slate-100 px-5 py-4">
            <h3 class="text-lg font-semibold text-slate-900">Solicitações de Vaga por Tipo</h3>
          </header>
          <div class="p-5 h-80">
            <Bar v-if="graficosData.espera" :data="graficosData.espera" :options="barOptions" />
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import {
  UsersIcon,
  ClockIcon,
  ClipboardDocumentCheckIcon,
  ArrowRightOnRectangleIcon,
} from '@heroicons/vue/24/outline';
import api from '../services/api';
import UiButton from '../components/ui/Button.vue';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler,
} from 'chart.js';
import { Line, Pie, Bar } from 'vue-chartjs';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const resumo = ref<Record<string, any>>({});
const graficosRaw = ref<Record<string, any>>({});
const detalhado = ref<Record<string, any>>({});
const loading = ref(true);
const erro = ref<string | null>(null);

// Filtros de data
const dataInicio = ref('');
const dataFim = ref('');

const initDates = () => {
  const now = new Date();
  const y = now.getFullYear();
  const m = now.getMonth();
  
  // Primeiro dia do mês atual
  const firstDay = new Date(y, m, 1);
  const offset1 = firstDay.getTimezoneOffset();
  const localFirstDay = new Date(firstDay.getTime() - (offset1 * 60 * 1000));
  dataInicio.value = localFirstDay.toISOString().split('T')[0];

  // Hoje
  const offset2 = now.getTimezoneOffset();
  const localNow = new Date(now.getTime() - (offset2 * 60 * 1000));
  dataFim.value = localNow.toISOString().split('T')[0];
};

const fetchResumo = async () => {
  loading.value = true;
  erro.value = null;
  try {
    const params: Record<string, string> = {};
    if (dataInicio.value) params.data_inicio = dataInicio.value;
    if (dataFim.value) params.data_fim = dataFim.value;

    const { data } = await api.get('/api/indicadores/resumo', { params });
    resumo.value = data.resumo;
    graficosRaw.value = data.graficos;
    detalhado.value = data.detalhado || {};
  } catch (err) {
    erro.value = 'Falha ao carregar os indicadores operacionais.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const formatarTempoLiberacao = (minutos?: number) => {
  if (minutos === undefined || minutos === null) return '0 min';
  const mins = Math.round(minutos);
  if (mins < 60) {
    return `${mins} min`;
  }
  const horas = Math.floor(mins / 60);
  const resto = mins % 60;
  return `${horas}h ${resto}m`;
};

const limparFiltros = () => {
  initDates();
  fetchResumo();
};

onMounted(() => {
  initDates();
  fetchResumo();
});

const iconMap: Record<string, any> = {
  ocupacao_atual: UsersIcon,
  tempo_permanencia: ClockIcon,
  solicitacoes_vaga: ClipboardDocumentCheckIcon,
  altas_realizadas: ArrowRightOnRectangleIcon,
};

const titleMap: Record<string, string> = {
  ocupacao_atual: 'Taxa de Ocupação',
  tempo_permanencia: 'Tempo de Permanência',
  solicitacoes_vaga: 'Solicitações de Vaga',
  altas_realizadas: 'Altas Solicitadas',
};

const indicadoresCalculados = computed(() => {
  if (!resumo.value || Object.keys(resumo.value).length === 0) return [];
  
  return Object.entries(resumo.value).map(([key, data]) => ({
    titulo: titleMap[key] || key,
    icone: iconMap[key] || UsersIcon,
    valor: data.valor,
    subtitulo: data.subtitulo,
    tendencia: data.tendencia,
  }));
});

const bgColors = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6'
];

const graficosData = computed(() => {
  if (!graficosRaw.value || Object.keys(graficosRaw.value).length === 0) return {};

  return {
    ocupacao: {
      labels: graficosRaw.value.ocupacao_semanal?.labels || [],
      datasets: [
        {
          label: 'Taxa de Ocupação (%)',
          backgroundColor: '#eff6ff',
          borderColor: '#3b82f6',
          data: graficosRaw.value.ocupacao_semanal?.data || [],
          fill: true,
          tension: 0.3
        }
      ]
    },
    especialidade: {
      labels: graficosRaw.value.distribuicao_especialidade?.labels || [],
      datasets: [
        {
          backgroundColor: bgColors,
          data: graficosRaw.value.distribuicao_especialidade?.data || []
        }
      ]
    },
    espera: {
      labels: graficosRaw.value.tempo_espera?.labels || [],
      datasets: [
        {
          label: 'Volume de Solicitações',
          backgroundColor: '#3b82f6',
          data: graficosRaw.value.tempo_espera?.data || []
        }
      ]
    }
  };
});

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: { min: 0, max: 100 }
  }
};

const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false }
  }
};

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: { beginAtZero: true, ticks: { stepSize: 1 } }
  }
};
</script>
