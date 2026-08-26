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
          <div class="relative flex-[2] min-w-60">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              v-model="buscaInput"
              type="text"
              placeholder="Buscar por ação, detalhe ou operador..."
              class="w-full rounded-md border border-slate-200 bg-white px-10 py-2 text-sm text-slate-800 shadow-sm placeholder:text-slate-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              @keyup.enter="aplicarFiltros"
            />
          </div>

          <!-- Busca por Prontuário -->
          <div class="relative flex-1 min-w-40">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              v-model="prontuarioInput"
              type="text"
              placeholder="Prontuário..."
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
            <option v-for="opt in filtroTipos" :key="opt.value" :value="opt.value">
              {{ opt.label }}
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
                <div v-if="item.prontuario && item.prontuario !== 'N/D'" class="flex items-center gap-1 rounded bg-slate-100 px-1.5 py-0.5 text-slate-700 font-semibold">
                  <span>Prontuário: {{ item.prontuario }}</span>
                </div>
                <div class="flex items-center gap-1">
                  <UserIcon class="h-3 w-3" />
                  <span>{{ item.operador }}</span>
                </div>
                <div class="flex items-center gap-1">
                  <ClockIcon class="h-3 w-3" />
                  <span>{{ item.dataHora }}</span>
                </div>
                
                <!-- Botão para ver passagem de caso -->
                <button 
                  v-if="['cirurgia_finalizada', 'passagem_caso', 'passagem_caso_editada'].includes(item.tipo) && obterSolicitacaoId(item.detalhes)"
                  @click="visualizarPassagemCaso(obterSolicitacaoId(item.detalhes)!)"
                  class="ml-auto flex items-center gap-1 text-blue-600 hover:text-blue-800 font-semibold cursor-pointer py-1"
                >
                  <EyeIcon class="h-3.5 w-3.5" />
                  <span>Ver Passagem</span>
                </button>
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
    <!-- Modal de Visualização da Passagem de Caso -->
    <div v-if="showHandoverModal" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
      <div class="bg-white rounded-2xl shadow-xl border border-slate-100 w-full max-w-2xl overflow-hidden flex flex-col max-h-[85vh]">
        <!-- Header -->
        <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
          <div>
            <h3 class="text-sm font-bold text-slate-800">Passagem de Caso do Paciente</h3>
            <p class="text-xs text-slate-500" v-if="selectedPacienteNome">
              {{ selectedPacienteNome }} (Prontuário: {{ selectedPacienteProntuario }})
            </p>
          </div>
          <button @click="showHandoverModal = false" class="text-slate-400 hover:text-slate-600 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Body -->
        <div class="p-6 overflow-y-auto space-y-4 text-xs text-slate-700">
          <div v-if="selectedPassagemCaso" class="space-y-4">
            
            <!-- Identificação e Alergias -->
            <div class="grid grid-cols-2 gap-2 border-b pb-2">
              <div><strong>Procedimento:</strong> {{ selectedPassagemCaso.cirurgia_nao_realizada ? 'CIRURGIA NÃO REALIZADA' : selectedPassagemCaso.procedimento_realizado }}</div>
              <div><strong>Anestesia:</strong> {{ selectedPassagemCaso.anestesia || 'Não informada' }}</div>
              <div class="col-span-2 flex flex-wrap gap-x-4">
                <div><strong>Alergias:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.alergias?.opcao }} {{ ['SIM', 'Sim'].includes(selectedPassagemCaso.alergias?.opcao) ? `- ${selectedPassagemCaso.alergias?.detalhe}` : '' }}</span></div>
                <div><strong>Isolamento:</strong> <span class="text-slate-600 font-bold" :class="selectedPassagemCaso.isolamento !== 'Não' ? 'text-red-600' : 'text-slate-600'">{{ selectedPassagemCaso.isolamento || 'Não' }}</span></div>
              </div>
            </div>

            <!-- Respiratório -->
            <div class="border-b pb-2">
              <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Respiratório</h4>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <strong>Via aérea:</strong> <span class="text-slate-600">{{ typeof selectedPassagemCaso.respiratorio?.via_aerea === 'object' ? [selectedPassagemCaso.respiratorio?.via_aerea?.espontanea ? 'Espontânea' : '', selectedPassagemCaso.respiratorio?.via_aerea?.tot ? 'TOT' : '', selectedPassagemCaso.respiratorio?.via_aerea?.traqueostomia ? 'Traqueostomia' : '', selectedPassagemCaso.respiratorio?.via_aerea?.outro ? `Outro (${selectedPassagemCaso.respiratorio?.via_aerea?.outro_detalhe})` : ''].filter(Boolean).join(', ') : (selectedPassagemCaso.respiratorio?.via_aerea === 'Outro' ? `Outro (${selectedPassagemCaso.respiratorio?.via_aerea_outro_detalhe})` : selectedPassagemCaso.respiratorio?.via_aerea) }}</span>
                </div>
                <div>
                  <strong>Suporte:</strong> <span class="text-slate-600">{{ typeof selectedPassagemCaso.respiratorio?.suporte === 'object' ? [selectedPassagemCaso.respiratorio?.suporte?.ar_ambiente ? 'Ar ambiente' : '', selectedPassagemCaso.respiratorio?.suporte?.o2_cateter ? 'O₂ cateter' : '', selectedPassagemCaso.respiratorio?.suporte?.mascara ? 'Máscara' : '', selectedPassagemCaso.respiratorio?.suporte?.ventilacao_mecanica ? 'Ventilação mecânica' : ''].filter(Boolean).join(', ') : selectedPassagemCaso.respiratorio?.suporte }}</span>
                </div>
              </div>
            </div>

            <!-- Cardiovascular -->
            <div class="border-b pb-2">
              <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Cardiovascular</h4>
              <div class="grid grid-cols-2 gap-2">
                <div><strong>Hemodinâmica:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.cardiovascular?.hemodinamica }}</span></div>
                <div>
                  <strong>Drogas vasoativas:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.cardiovascular?.drogas_vasoativas?.opcao }} {{ selectedPassagemCaso.cardiovascular?.drogas_vasoativas?.opcao === 'Sim' ? `- ${selectedPassagemCaso.cardiovascular?.drogas_vasoativas?.detalhe}` : '' }}</span>
                </div>
                <div><strong>Reposição volêmica:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.cardiovascular?.reposicao_volemica }}</span></div>
                <div>
                  <strong>Transfusão:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.cardiovascular?.transfusao?.opcao }} {{ selectedPassagemCaso.cardiovascular?.transfusao?.opcao === 'Sim' ? `- ${selectedPassagemCaso.cardiovascular?.transfusao?.detalhe}` : '' }}</span>
                </div>
              </div>
            </div>

            <!-- Sangramento e Balanço -->
            <div class="border-b pb-2">
              <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Sangramento e Balanço</h4>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <strong>Sangramento estimado:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.sangramento_balanco?.sangramento_estimado }} {{ selectedPassagemCaso.sangramento_balanco?.sangramento_estimado === 'Importante' ? `- ${selectedPassagemCaso.sangramento_balanco?.sangramento_volume} mL` : '' }}</span>
                </div>
                <div>
                  <strong>Diurese intraoperatória:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.sangramento_balanco?.diurese_intraoperatoria?.opcao === 'valor' ? `${selectedPassagemCaso.sangramento_balanco?.diurese_intraoperatoria?.valor} mL` : 'Não se aplica' }}</span>
                </div>
              </div>
            </div>

            <!-- Acessos, Dispositivos e Feridas -->
            <div class="border-b pb-2">
              <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Acessos, Dispositivos e Feridas</h4>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <strong>Acessos venosos:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.nao_se_aplica ? 'Não se aplica' : [selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.periferico ? `Periférico (${selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.periferico_local}${selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.periferico_data ? ' - Criação: ' + selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.periferico_data.split('-').reverse().join('/') : ''})` : '', selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.cvc ? `CVC (${selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.cvc_local}${selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.cvc_data ? ' - Criação: ' + selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.cvc_data.split('-').reverse().join('/') : ''})` : '', selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.picc ? `PICC (${selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.picc_local}${selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.picc_data ? ' - Criação: ' + selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.picc_data.split('-').reverse().join('/') : ''})` : '', selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.outro ? `Outro (${selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.outro_detalhe}${selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.outro_data ? ' - Criação: ' + selectedPassagemCaso.acessos_dispositivos?.acessos_venosos?.outro_data.split('-').reverse().join('/') : ''})` : ''].filter(Boolean).join(', ') }}</span>
                </div>
                <div>
                  <strong>PAI:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.acessos_dispositivos?.pai?.opcao }} {{ selectedPassagemCaso.acessos_dispositivos?.pai?.opcao === 'Sim' ? `- ${selectedPassagemCaso.acessos_dispositivos?.pai?.local}` : '' }}</span>
                </div>
                <div>
                  <strong>Sonda vesical:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.acessos_dispositivos?.sonda_vesical?.opcao }} {{ selectedPassagemCaso.acessos_dispositivos?.sonda_vesical?.opcao === 'Sim' ? `- Nº ${selectedPassagemCaso.acessos_dispositivos?.sonda_vesical?.n_sonda}` : '' }}</span>
                </div>
                <div>
                  <strong>Ferida operatória:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.acessos_dispositivos?.ferida_operatoria?.nao_se_aplica ? 'Não' : selectedPassagemCaso.acessos_dispositivos?.ferida_operatoria?.local }}</span>
                </div>
                <div>
                  <strong>Drenos:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.acessos_dispositivos?.drenos?.opcao }} {{ selectedPassagemCaso.acessos_dispositivos?.drenos?.opcao === 'Sim' ? `- ${selectedPassagemCaso.acessos_dispositivos?.drenos?.tipo_local}` : '' }}</span>
                </div>
                <div>
                  <strong>Outros dispositivos:</strong> <span class="text-slate-600">{{ [selectedPassagemCaso.acessos_dispositivos?.outros?.sng_sne ? 'SNG/SNE' : '', selectedPassagemCaso.acessos_dispositivos?.outros?.ostomia ? 'Ostomia' : '', selectedPassagemCaso.acessos_dispositivos?.outros?.outro ? `Outro (${selectedPassagemCaso.acessos_dispositivos?.outros?.outro_detalhe})` : ''].filter(Boolean).join(', ') || 'Nenhum' }}</span>
                </div>
              </div>
            </div>

            <!-- Medicamentos -->
            <div class="border-b pb-2">
              <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Medicamentos</h4>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <strong>Antibiótico:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.medicamentos?.antibiotico?.opcao }} {{ selectedPassagemCaso.medicamentos?.antibiotico?.opcao === 'Sim' ? `- ${selectedPassagemCaso.medicamentos?.antibiotico?.detalhe}` : '' }}</span>
                </div>
                <div><strong>Outras medicações:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.medicamentos?.outras_medicacoes || 'Nenhuma' }}</span></div>
              </div>
            </div>

            <!-- Intercorrências -->
            <div class="border-b pb-2">
              <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Intercorrências no ato</h4>
              <div class="space-y-1">
                <div>
                  <strong>Intercorrências:</strong> <span class="text-slate-600">{{ selectedPassagemCaso.intercorrencias?.nao_houve ? 'Não houve' : [selectedPassagemCaso.intercorrencias?.hipotensao ? 'Hipotensão' : '', selectedPassagemCaso.intercorrencias?.hipertensao ? 'Hipertensão' : '', selectedPassagemCaso.intercorrencias?.arritmia ? 'Arritmia' : '', selectedPassagemCaso.intercorrencias?.dessaturacao ? 'Dessaturação' : '', selectedPassagemCaso.intercorrencias?.broncoespasmo ? 'Broncoespasmo' : '', selectedPassagemCaso.intercorrencias?.sangramento_importante ? 'Sangramento importante' : '', selectedPassagemCaso.intercorrencias?.reacao_medicamentosa ? 'Reação medicamentosa' : '', selectedPassagemCaso.intercorrencias?.parada_cardiorespiratoria ? 'Parada cardiorrespiratória' : '', selectedPassagemCaso.intercorrencias?.dificil_via_aerea ? 'Difícil via aérea' : '', selectedPassagemCaso.intercorrencias?.outro ? `Outro (${selectedPassagemCaso.intercorrencias?.outro_detalhe})` : ''].filter(Boolean).join(', ') }}</span>
                </div>
                <div v-if="selectedPassagemCaso.intercorrencias?.descricao_conduta">
                  <strong>Descrição/Conduta:</strong>
                  <span class="text-slate-600 block bg-slate-50 p-2 rounded mt-1 whitespace-pre-wrap">{{ selectedPassagemCaso.intercorrencias?.descricao_conduta }}</span>
                </div>
              </div>
            </div>

            <!-- Responsável -->
            <div class="pt-1">
              <strong>Profissional Responsável:</strong> <span class="text-slate-600 font-semibold">{{ selectedPassagemCaso.profissional_responsavel || 'Não informado' }}</span>
            </div>

          </div>
          <div v-else class="text-center py-8 text-slate-400">
            <span v-if="loadingHandover">Carregando detalhes da passagem de caso...</span>
            <span v-else>Passagem de caso não cadastrada.</span>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-6 py-3 border-t border-slate-100 bg-slate-50 flex justify-end">
          <UiButton @click="showHandoverModal = false">Fechar</UiButton>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { MagnifyingGlassIcon, UserIcon, ClockIcon, EyeIcon } from '@heroicons/vue/24/outline';
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
  prontuario?: string;
};

const tipoConfig: Record<string, { color: string; label: string }> = {
  // Solicitações
  solicitacao:          { color: 'border border-amber-300 bg-amber-500/80 text-amber-100',  label: 'Solicitação' },
  nova_solicitacao:     { color: 'border border-amber-300 bg-amber-500/80 text-amber-100',  label: 'Solicitação' },
  conclusao:            { color: 'border border-emerald-300 bg-emerald-500/80 text-emerald-100', label: 'Admissão' },
  
  // Reservas
  reserva:                  { color: 'border border-emerald-300 bg-emerald-500/80 text-emerald-100', label: 'Reserva' },
  cancelamento_reserva:     { color: 'border border-red-300 bg-red-500/80 text-red-100',        label: 'Cancelamento' },
  cancelamento_solicitante: { color: 'border border-red-300 bg-red-500/80 text-red-100',        label: 'Cancelamento' },
  
  // Destinos
  destino:              { color: 'border border-blue-300 bg-blue-500/80 text-blue-100',     label: 'Destino' },
  alteracao_destino:    { color: 'border border-blue-300 bg-blue-500/80 text-blue-100',     label: 'Destino' },
  destino_disponivel:   { color: 'border border-blue-300 bg-blue-500/80 text-blue-100',     label: 'Destino' },
  destino_pendente:     { color: 'border border-blue-300 bg-blue-500/80 text-blue-100',     label: 'Destino' },

  // Altas / Cancelamentos de Alta
  alta:                 { color: 'border border-rose-300 bg-rose-500/80 text-rose-100',     label: 'Alta' },
  conclusao_alta:       { color: 'border border-rose-300 bg-rose-500/80 text-rose-100',     label: 'Alta' },
  cancelamento:         { color: 'border border-red-300 bg-red-500/80 text-red-100',        label: 'Cancelamento' },
  exclusao_solicitacao: { color: 'border border-red-300 bg-red-500/80 text-red-100',        label: 'Cancelamento' },

  // Outros
  status:               { color: 'border border-slate-300 bg-slate-500/80 text-slate-100',  label: 'Status' },
  edicao:               { color: 'border border-slate-300 bg-slate-500/80 text-slate-100',  label: 'Edição' },

  // Passagem de Caso
  cirurgia_finalizada:     { color: 'border border-blue-300 bg-blue-500/80 text-blue-100',     label: 'Cirurgia Finalizada' },
  passagem_caso:           { color: 'border border-indigo-300 bg-indigo-500/80 text-indigo-100', label: 'Passagem de Caso' },
  passagem_caso_editada:   { color: 'border border-indigo-300 bg-indigo-500/80 text-indigo-100', label: 'Passagem Editada' },
  encaminhamento_liberado: { color: 'border border-emerald-300 bg-emerald-500/80 text-emerald-100', label: 'Liberado' },
};

const filtroTipos = [
  { value: 'alta', label: 'Altas' },
  { value: 'solicitacao', label: 'Solicitações' },
  { value: 'reserva', label: 'Reservas' },
];

const historico = ref<HistoricoItem[]>([]);
const loading = ref(true);
const erro = ref<string | null>(null);

const buscaInput = ref('');
const prontuarioInput = ref('');
const tipoFiltro = ref('');

const limit = ref(30);
const offset = ref(0);
const total = ref(0);

const busca = ref('');
const prontuarioAtivo = ref('');
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
    if (prontuarioAtivo.value) params.prontuario = prontuarioAtivo.value;
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
  prontuarioAtivo.value = prontuarioInput.value.trim();
  tipoAtivo.value = tipoFiltro.value;
  offset.value = 0;
  fetchHistorico();
};

const limparFiltros = () => {
  buscaInput.value = '';
  prontuarioInput.value = '';
  tipoFiltro.value = '';
  busca.value = '';
  prontuarioAtivo.value = '';
  tipoAtivo.value = '';
  offset.value = 0;
  fetchHistorico();
};

const paginar = (direcao: 1 | -1) => {
  offset.value = Math.max(0, offset.value + direcao * limit.value);
  fetchHistorico();
};

const showHandoverModal = ref(false);
const loadingHandover = ref(false);
const selectedPassagemCaso = ref<any>(null);
const selectedPacienteNome = ref("");
const selectedPacienteProntuario = ref("");

function obterSolicitacaoId(detalhes: string): number | null {
  const match = detalhes.match(/solicitação\s*#(\d+)/i);
  return match ? parseInt(match[1]) : null;
}

const visualizarPassagemCaso = async (solId: number) => {
  try {
    selectedPassagemCaso.value = null;
    loadingHandover.value = true;
    showHandoverModal.value = true;
    const res = await api.get(`/api/solicitacoes/${solId}`);
    selectedPassagemCaso.value = res.data.passagem_caso;
    selectedPacienteNome.value = res.data.nome;
    selectedPacienteProntuario.value = res.data.prontuario;
  } catch (error) {
    console.error(error);
    selectedPassagemCaso.value = null;
    // Opcional: mantemos o modal aberto para exibir "Passagem de caso não cadastrada" se a solicitação não existir
    selectedPacienteNome.value = "";
    selectedPacienteProntuario.value = "";
  } finally {
    loadingHandover.value = false;
  }
};

onMounted(fetchHistorico);
</script>
