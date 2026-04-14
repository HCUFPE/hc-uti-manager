<template>
  <section class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-3xl font-bold text-slate-900">Indicadores Operacionais</h2>
    </div>

    <div v-if="loading" class="flex justify-center py-16">
      <div class="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
    </div>
    <div v-else-if="erro" class="rounded-xl border border-red-200 bg-red-50 p-6 text-center text-red-700">
      {{ erro }}
    </div>
    <div v-else class="space-y-6">
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
        <article
          v-for="ind in indicadoresCalculados"
          :key="ind.titulo"
          class="rounded-xl border border-slate-200 bg-white shadow-sm"
        >
          <header class="flex items-start justify-between gap-3 border-b border-slate-100 px-5 py-4">
            <p class="text-sm font-medium text-slate-600">{{ ind.titulo }}</p>
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

      <article class="rounded-xl border border-slate-200 bg-white shadow-sm">
        <header class="border-b border-slate-100 px-5 py-4">
          <h3 class="text-lg font-semibold text-slate-900">Grafico de Ocupacao Semanal</h3>
        </header>
        <div class="p-5 h-80">
          <Line v-if="graficosData.ocupacao" :data="graficosData.ocupacao" :options="lineOptions" />
        </div>
      </article>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <article class="rounded-xl border border-slate-200 bg-white shadow-sm">
          <header class="border-b border-slate-100 px-5 py-4">
            <h3 class="text-lg font-semibold text-slate-900">Distribuicao por Especialidade</h3>
          </header>
          <div class="p-5 h-80 flex justify-center">
            <Pie v-if="graficosData.especialidade" :data="graficosData.especialidade" :options="pieOptions" />
          </div>
        </article>

        <article class="rounded-xl border border-slate-200 bg-white shadow-sm">
          <header class="border-b border-slate-100 px-5 py-4">
            <h3 class="text-lg font-semibold text-slate-900">Solicitacoes de Vaga por Tipo</h3>
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
const loading = ref(true);
const erro = ref<string | null>(null);

const fetchResumo = async () => {
  try {
    const { data } = await api.get('/api/indicadores/resumo');
    resumo.value = data.resumo;
    graficosRaw.value = data.graficos;
  } catch (err) {
    erro.value = 'Falha ao carregar os indicadores operacionais.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchResumo);

const iconMap: Record<string, any> = {
  ocupacao_atual: UsersIcon,
  tempo_permanencia: ClockIcon,
  solicitacoes_vaga: ClipboardDocumentCheckIcon,
  altas_realizadas: ArrowRightOnRectangleIcon,
};

const titleMap: Record<string, string> = {
  ocupacao_atual: 'Taxa de Ocupacao',
  tempo_permanencia: 'Tempo Medio de Permanencia',
  solicitacoes_vaga: 'Solicitacoes de Vaga',
  altas_realizadas: 'Altas Direcionadas',
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

const graficosData = computed(() => {
  if (!graficosRaw.value || Object.keys(graficosRaw.value).length === 0) return {};

  const bgColors = [
    '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6'
  ];

  return {
    ocupacao: {
      labels: graficosRaw.value.ocupacao_semanal.labels,
      datasets: [
        {
          label: 'Taxa de Ocupação (%)',
          backgroundColor: '#eff6ff',
          borderColor: '#3b82f6',
          data: graficosRaw.value.ocupacao_semanal.data,
          fill: true,
          tension: 0.3
        }
      ]
    },
    especialidade: {
      labels: graficosRaw.value.distribuicao_especialidade.labels,
      datasets: [
        {
          backgroundColor: bgColors,
          data: graficosRaw.value.distribuicao_especialidade.data
        }
      ]
    },
    espera: {
      labels: graficosRaw.value.tempo_espera.labels,
      datasets: [
        {
          label: 'Volume de Solicitações',
          backgroundColor: '#3b82f6',
          data: graficosRaw.value.tempo_espera.data
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
    legend: { position: 'right' as const }
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
