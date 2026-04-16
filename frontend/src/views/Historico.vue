<template>
  <section class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-3xl font-bold text-slate-900">Histórico de Ações</h2>
      <span class="text-sm text-slate-500">{{ total }} registros encontrados</span>
    </div>

    <!-- Filtros -->
    <article class="rounded-xl border border-slate-200 bg-white shadow-sm">
      <div class="px-5 py-4">
        <div class="flex flex-wrap gap-3">
          <!-- Busca livre -->
          <div class="relative flex-1 min-w-60">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              v-model="buscaInput"
              type="text"
              placeholder="Buscar por ação, detalhe ou operador..."
              class="w-full rounded-md border border-slate-200 bg-white px-10 py-2 text-sm text-slate-800 shadow-sm placeholder:text-slate-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              @keyup.enter="aplicarFiltros"
            />
          </div>

          <!-- Filtro por tipo -->
          <select
            v-model="tipoFiltro"
            class="rounded-md border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            @change="aplicarFiltros"
          >
            <option value="">Todos os tipos</option>
            <option v-for="(cfg, key) in tipoConfig" :key="key" :value="key">
              {{ cfg.label }}
            </option>
          </select>

          <UiButton class="h-10" @click="aplicarFiltros">Buscar</UiButton>
          <UiButton class="h-10" variant="outline" @click="limparFiltros">Limpar</UiButton>
        </div>
      </div>
    </article>

    <!-- Estado de carregamento -->
    <div v-if="loading" class="flex justify-center py-16">
      <div class="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
    </div>

    <!-- Erro -->
    <div
      v-else-if="erro"
      class="rounded-xl border border-red-200 bg-red-50 p-6 text-center text-red-700"
    >
      {{ erro }}
    </div>

    <!-- Sem resultados -->
    <div
      v-else-if="historico.length === 0"
      class="rounded-xl border border-slate-200 bg-white p-12 text-center text-slate-500"
    >
      <ClockIcon class="mx-auto mb-3 h-10 w-10 text-slate-300" />
      <p class="font-medium">Nenhum registro encontrado.</p>
      <p class="mt-1 text-sm">As ações realizadas no sistema aparecerão aqui.</p>
    </div>

    <!-- Lista -->
    <div v-else class="space-y-3">
      <article
        v-for="item in historico"
        :key="item.id"
        class="rounded-xl border border-slate-200 bg-white shadow-sm"
      >
        <div class="p-4">
          <div class="flex items-start justify-between">
            <div class="flex-1 space-y-2">
              <div class="flex flex-wrap items-center gap-3">
                <UiBadge :class="tipoConfig[item.tipo]?.color || tipoConfig.status.color">
                  {{ tipoConfig[item.tipo]?.label || item.tipo }}
                </UiBadge>
                <h3 class="font-semibold text-slate-900">{{ item.acao }}</h3>
              </div>
              <p class="text-sm text-slate-600">{{ item.detalhes }}</p>
              <div class="flex flex-wrap items-center gap-4 pt-2 text-xs text-slate-500">
                <div class="flex items-center gap-1">
                  <UserIcon class="h-3 w-3" />
                  <span>{{ item.operador }}</span>
                </div>
                <div class="flex items-center gap-1">
                  <ClockIcon class="h-3 w-3" />
                  <span>{{ item.dataHora }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </article>
    </div>

    <!-- Paginação -->
    <div v-if="!loading && historico.length > 0" class="flex items-center justify-between">
      <span class="text-sm text-slate-500">
        Exibindo {{ offset + 1 }}–{{ Math.min(offset + limit, total) }} de {{ total }}
      </span>
      <div class="flex gap-2">
        <UiButton
          variant="outline"
          size="sm"
          :disabled="offset === 0"
          @click="paginar(-1)"
        >
          ← Anterior
        </UiButton>
        <UiButton
          variant="outline"
          size="sm"
          :disabled="offset + limit >= total"
          @click="paginar(1)"
        >
          Próxima →
        </UiButton>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { MagnifyingGlassIcon, UserIcon, ClockIcon } from '@heroicons/vue/24/outline';
import { ref, onMounted } from 'vue';
import UiBadge from '../components/ui/Badge.vue';
import UiButton from '../components/ui/Button.vue';
import api from '../services/api';

type HistoricoItem = {
  id: string;
  operador: string;
  tipo: string;
  acao: string;
  detalhes: string;
  dataHora: string;
};

const tipoConfig: Record<string, { color: string; label: string }> = {
  alta:         { color: 'border border-rose-300 bg-rose-500/80 text-rose-100',     label: 'Alta' },
  reserva:      { color: 'border border-emerald-300 bg-emerald-500/80 text-emerald-100', label: 'Reserva' },
  destino:      { color: 'border border-blue-300 bg-blue-500/80 text-blue-100',     label: 'Destino' },
  cancelamento: { color: 'border border-red-300 bg-red-500/80 text-red-100',        label: 'Cancelamento' },
  solicitacao:  { color: 'border border-amber-300 bg-amber-500/80 text-amber-800',  label: 'Solicitação' },
  status:       { color: 'border border-slate-300 bg-slate-500/80 text-slate-100',  label: 'Status' },
};

const historico = ref<HistoricoItem[]>([]);
const loading = ref(true);
const erro = ref<string | null>(null);

const buscaInput = ref('');
const tipoFiltro = ref('');

const limit = ref(30);
const offset = ref(0);
const total = ref(0);

const busca = ref('');
const tipoAtivo = ref('');

const fetchHistorico = async () => {
  loading.value = true;
  erro.value = null;
  try {
    const params: Record<string, any> = {
      limit: limit.value,
      offset: offset.value,
    };
    if (busca.value) params.busca = busca.value;
    if (tipoAtivo.value) params.tipo = tipoAtivo.value;

    const { data } = await api.get('/api/historico', { params });
    historico.value = data;
    // Atualiza total estimado (se a API retornou menos que o limite, é a última página)
    if (offset.value === 0) {
      total.value = data.length < limit.value ? data.length : limit.value * 10; // estimativa
    }
    if (data.length < limit.value) {
      total.value = offset.value + data.length;
    }
  } catch (err) {
    erro.value = 'Falha ao carregar o histórico de ações.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const aplicarFiltros = () => {
  busca.value = buscaInput.value.trim();
  tipoAtivo.value = tipoFiltro.value;
  offset.value = 0;
  fetchHistorico();
};

const limparFiltros = () => {
  buscaInput.value = '';
  tipoFiltro.value = '';
  busca.value = '';
  tipoAtivo.value = '';
  offset.value = 0;
  fetchHistorico();
};

const paginar = (direcao: 1 | -1) => {
  offset.value = Math.max(0, offset.value + direcao * limit.value);
  fetchHistorico();
};

onMounted(fetchHistorico);
</script>
