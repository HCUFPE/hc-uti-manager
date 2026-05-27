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
        <UiButton v-if="authStore.isAdmin || authStore.isSolicitante" size="sm" class="shadow-sm" @click="showModalNova = true">
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
            <div class="p-4">
              <div class="flex items-start justify-between mb-4">
                <div class="space-y-1 text-left">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-600 border border-slate-200">
                      Prontuário {{ sol.prontuario }}
                    </span>
                    <span class="text-[10px] font-normal text-slate-400">{{ formatarDataHoraBR(sol.dataHora) }}</span>
                  </div>
                  <h4 class="text-lg font-bold text-slate-800 leading-tight mt-1">{{ sol.nome || 'Paciente AGHU' }}</h4>
                  <p class="text-xs font-normal text-slate-500">
                    {{ sol.idade }} anos • {{ sol.especialidade }}
                  </p>
                  <p v-if="sol.procedimento" class="text-xs font-medium text-slate-600 italic">
                    Procedimento: {{ sol.procedimento }}
                  </p>
                </div>
                <span class="rounded-full bg-rose-500 px-3 py-1 text-[10px] font-bold text-white shadow-sm shrink-0">
                  Aguardando Reserva de Leito
                </span>
              </div>

              <!-- Middle Row: Details -->
              <div class="grid grid-cols-5 gap-6 py-3 border-t border-slate-50 text-left">
                <div class="space-y-0.5">
                  <p class="text-[10px] font-medium uppercase tracking-wider text-slate-400">Tipo</p>
                  <p class="text-sm font-semibold text-slate-700">{{ sol.tipo }}</p>
                </div>
                <div class="space-y-0.5">
                  <p class="text-[10px] font-medium uppercase tracking-wider text-slate-400">Data Prevista da Cirurgia</p>
                  <p class="text-sm font-semibold text-slate-700">{{ sol.data_cirurgia ? formatarDataBR(sol.data_cirurgia) : 'Não informada' }}</p>
                </div>
                <div class="space-y-0.5">
                  <p class="text-[10px] font-medium uppercase tracking-wider text-slate-400">Horário</p>
                  <p class="text-sm font-semibold text-slate-700">{{ sol.hora_cirurgia || '--:--' }}</p>
                </div>
                <div class="space-y-0.5">
                  <p class="text-[10px] font-medium uppercase tracking-wider text-slate-400">Turno</p>
                  <p class="text-sm font-semibold text-slate-700">{{ sol.turno }}</p>
                </div>
                <div class="space-y-0.5">
                  <p class="text-[10px] font-medium uppercase tracking-wider text-slate-400">Prioridade</p>
                  <p class="text-sm font-semibold" :class="sol.prioridade === 'P1' ? 'text-red-600' : 'text-slate-700'">
                    {{ sol.prioridade || '---' }}
                  </p>
                </div>
              </div>

              <!-- Action Row -->
              <div class="mt-4 flex items-center gap-2">
                <!-- UTI/NIR ou o Dono podem gerenciar (reservar é só UTI/NIR) -->
                <template v-if="authStore.isUTI">
                  <UiButton size="sm" @click="abrirModalReserva(sol)" class="bg-blue-600 text-white hover:bg-blue-700 shadow-sm px-4">
                    Reservar Leito
                  </UiButton>
                </template>

                <UiButton 
                  v-if="podeGerenciar(sol)" 
                  size="sm" 
                  variant="outline" 
                  @click="abrirModalEdicao(sol)" 
                  class="shadow-sm"
                >
                  <PencilSquareIcon class="h-4 w-4 mr-1 text-slate-500" />
                  Editar
                </UiButton>
                
                <UiButton 
                  v-if="podeGerenciar(sol) || authStore.isUTI" 
                  size="sm" 
                  @click="abrirModalCancelamento(sol.id, false)" 
                  class="bg-red-600 text-white hover:bg-red-700 border-none shadow-sm px-4"
                >
                  <TrashIcon class="h-4 w-4 mr-1" />
                  Cancelar Solicitação
                </UiButton>
              </div>
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
              <div class="grid grid-cols-1 md:grid-cols-7 gap-6 w-full text-left">
                <div class="space-y-1 md:col-span-2 text-left">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-600 border border-slate-200">
                      Prontuário {{ sol.prontuario }}
                    </span>
                  </div>
                  <h4 class="text-lg font-bold text-slate-800 leading-tight mt-1">{{ sol.nome || 'Paciente AGHU' }}</h4>
                  <p class="text-xs text-slate-500">
                    {{ sol.idade }} anos • {{ sol.especialidade }}
                  </p>
                  <p v-if="sol.procedimento" class="text-xs font-medium text-slate-600 italic truncate" :title="sol.procedimento">
                    Procedimento: {{ sol.procedimento }}
                  </p>
                </div>
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-emerald-500">Leito Reservado</p>
                  <p class="text-lg font-black text-emerald-700">{{ sol.destino || '---' }}</p>
                </div>
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Data Cirurgia</p>
                  <p class="text-base font-bold text-slate-700">{{ sol.data_cirurgia ? formatarDataBR(sol.data_cirurgia) : '-' }}</p>
                </div>
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Horário</p>
                  <p class="text-base font-bold text-slate-700">{{ sol.hora_cirurgia || '--:--' }}</p>
                </div>
                <div class="space-y-1">
                  <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Turno</p>
                  <p class="text-base font-bold text-slate-700">{{ sol.turno }}</p>
                </div>
                <div class="flex flex-col items-end justify-center">
                  <span class="rounded-full border border-emerald-300 bg-emerald-500 px-3 py-1 text-[10px] font-bold uppercase tracking-tighter text-white shadow-sm">
                    Reservado
                  </span>
                </div>
              </div>
            </div>
            <!-- Ações para Reservados -->
            <div v-if="authStore.isAdmin || authStore.isUTI || podeGerenciar(sol)" class="flex items-center gap-2 border-t border-emerald-50 bg-emerald-50/30 px-6 py-3">
              <template v-if="authStore.isSolicitante && podeGerenciar(sol)">
                <UiButton
                  size="sm"
                  :disabled="sol.cirurgia_finalizada"
                  :class="[
                    sol.cirurgia_finalizada 
                      ? 'bg-emerald-600 border-none text-white font-bold px-4 shadow-sm opacity-100 cursor-not-allowed'
                      : 'bg-amber-500 hover:bg-amber-600 text-white font-bold px-4 border-none shadow-sm flex items-center gap-1'
                  ]"
                  @click="confirmarCirurgiaFinalizada(sol.id)"
                >
                  <CheckIcon class="h-4 w-4 mr-1 text-white" />
                  {{ sol.cirurgia_finalizada ? 'Cirurgia Concluída' : 'Cirurgia Finalizada' }}
                </UiButton>
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
                  @click="abrirModalCancelamento(sol.id, false)" 
                  class="bg-red-600 text-white hover:bg-red-700 border-none shadow-sm px-4"
                >
                  <TrashIcon class="h-4 w-4 mr-1" />
                  Cancelar Solicitação
                </UiButton>
              </template>
              <div class="ml-auto flex items-center gap-2">
                <span 
                  v-if="sol.cirurgia_finalizada && !sol.encaminhamento_liberado"
                  class="inline-flex items-center rounded-full bg-amber-50 px-2.5 py-1 text-xs font-bold text-amber-800 border border-amber-200"
                >
                  <ClockIcon class="h-3.5 w-3.5 mr-1 text-amber-600 animate-pulse" />
                  Aguardando Liberação da UTI
                </span>
                <span 
                  v-else-if="sol.encaminhamento_liberado"
                  class="inline-flex items-center rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-bold text-emerald-800 border border-emerald-200"
                >
                  <CheckCircleIcon class="h-3.5 w-3.5 mr-1 text-emerald-600" />
                  Transporte Autorizado para UTI!
                </span>
              </div>
              <UiButton 
                v-if="authStore.isAdmin || authStore.isUTI"
                size="sm" 
                @click="abrirModalMudarLeito(sol)" 
                class="bg-blue-600 text-white hover:bg-blue-700 border-none shadow-sm px-4 flex items-center gap-1"
              >
                <PencilSquareIcon class="h-4 w-4 mr-1" />
                Mudar Leito
              </UiButton>
              <UiButton 
                v-if="authStore.isAdmin || authStore.isUTI"
                size="sm" 
                @click="abrirModalCancelamento(sol.id, true)" 
                class="bg-rose-600 text-white hover:bg-rose-700 border-none shadow-sm px-4"
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

      <!-- SEÇÃO 3: SOLICITAÇÕES CONCLUÍDAS -->
      <section v-if="solicitacoesConcluidas.length > 0">
        <div class="mb-6 flex items-center gap-3">
          <div class="h-8 w-1 rounded bg-blue-500"></div>
          <h2 class="text-xl font-bold text-slate-800">Solicitações Concluídas (Paciente no Leito)</h2>
          <span class="rounded-full bg-blue-100 px-3 py-1 text-sm font-bold text-blue-600">
            {{ solicitacoesConcluidas.length }}
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <article
            v-for="sol in solicitacoesConcluidas"
            :key="sol.id"
            class="overflow-hidden rounded-xl border border-slate-100 bg-slate-50/50 p-4 shadow-sm"
          >
            <div class="flex items-center justify-between">
              <div class="space-y-1 text-left">
                <div class="flex items-center gap-2">
                  <span class="rounded-full bg-slate-200 px-2 py-0.5 text-[9px] font-semibold text-slate-700 border border-slate-300">
                    Prontuário {{ sol.prontuario }}
                  </span>
                </div>
                <h4 class="text-base font-bold text-slate-800 leading-tight mt-0.5">{{ sol.nome || 'Paciente AGHU' }}</h4>
                <p class="text-xs text-slate-600">{{ sol.especialidade }} • {{ sol.destino }}</p>
              </div>
              <div class="text-right">
                <span class="rounded-full bg-blue-100 px-2 py-1 text-[10px] font-bold uppercase text-blue-700">Concluída</span>
                <p class="text-[10px] text-slate-400 mt-1">Sincronizado com AGHU</p>
              </div>
            </div>
          </article>
        </div>
      </section>

    </div>

    <!-- Modais -->
    <Modal :show="showModalReserva" @close="showModalReserva = false">
      <template #header>{{ isRemanejamento ? 'Mudar Leito' : 'Reservar Leito' }} para Prontuário {{ solSelecionada?.prontuario }}</template>
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
          {{ submetendo ? (isRemanejamento ? 'Mudando...' : 'Reservando...') : (isRemanejamento ? 'Confirmar Mudança' : 'Confirmar Reserva') }}
        </UiButton>
      </template>
    </Modal>

    <Modal :show="showModalNova" @close="fecharModalNova">
      <template #header>{{ isEditing ? 'Editar Solicitação' : 'Nova Solicitação' }}</template>
      <div class="space-y-4">
        <!-- Input de Prontuário com botão de Buscar -->
        <div class="flex items-end gap-2 text-left">
          <div class="flex-1">
            <label class="block text-sm font-medium text-slate-700">Prontuário <span class="text-red-500">*</span></label>
            <input 
              v-model="formNova.prontuario" 
              type="text" 
              placeholder="Digite o prontuário" 
              class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 disabled:bg-slate-100 disabled:text-slate-500" 
              :disabled="buscandoAghu"
              @blur="buscarPacienteAghu"
              @keyup.enter="buscarPacienteAghu"
            />
          </div>
          <UiButton 
            type="button" 
            variant="outline" 
            size="sm" 
            class="h-[38px] px-3 flex items-center justify-center gap-1 shadow-sm shrink-0" 
            :disabled="!formNova.prontuario || buscandoAghu"
            @click="buscarPacienteAghu"
          >
            <MagnifyingGlassIcon class="h-4 w-4 text-slate-500" />
            Buscar
          </UiButton>
        </div>

        <div class="grid grid-cols-2 gap-4 text-left">
          <!-- Campo Tipo -->
          <div>
            <label class="block text-sm font-medium text-slate-700">Tipo <span class="text-red-500">*</span></label>
            <select 
              v-model="formNova.tipo" 
              class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 disabled:bg-slate-50 disabled:text-slate-500"
              :disabled="!authStore.isAdmin && !authStore.isUTI && tiposDisponiveis.length === 1"
            >
              <option value="" disabled selected>Selecione o Tipo</option>
              <option v-for="t in tiposDisponiveis" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>

          <!-- Campo Prioridade -->
          <div>
            <label class="block text-sm font-medium text-slate-700">Prioridade</label>
            <select v-model="formNova.prioridade" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200">
              <option value="">Nenhuma (Padrão)</option>
              <option value="P1">P1 (Maior)</option>
              <option value="P2">P2</option>
              <option value="P3">P3</option>
              <option value="P4">P4</option>
              <option value="P5">P5 (Menor)</option>
            </select>
          </div>
        </div>

        <!-- Card de dados do paciente (AGHU) - Somente Leitura -->
        <div v-if="buscandoAghu" class="rounded-xl border border-slate-100 bg-slate-50/50 p-6 flex flex-col items-center justify-center space-y-2">
          <div class="h-6 w-6 animate-spin rounded-full border-2 border-blue-600 border-t-transparent"></div>
          <span class="text-xs text-slate-500 font-medium">Buscando paciente no AGHU...</span>
        </div>

        <div v-else-if="erroAghu" class="rounded-xl border border-rose-100 bg-rose-50/50 p-4 text-sm text-rose-600 flex items-start gap-2.5 text-left">
          <ExclamationTriangleIcon class="h-5 w-5 text-rose-500 shrink-0 mt-0.5" />
          <div class="space-y-1">
            <p class="font-semibold text-rose-700">Atenção</p>
            <p class="text-xs text-rose-600/90">{{ erroAghu }}</p>
          </div>
        </div>

        <div v-else-if="dadosAghu" class="rounded-xl border border-slate-100 bg-slate-50/50 p-4 space-y-3.5 text-left transition duration-300">
          <div class="border-b border-slate-200/60 pb-2.5">
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Paciente localizado</span>
            <h4 class="text-base font-bold text-slate-800 leading-snug">{{ dadosAghu.nome }}</h4>
            <p class="text-xs text-slate-500 font-medium mt-0.5">
              <template v-if="dadosAghu.data_nascimento">
                Data de Nascimento: {{ dadosAghu.data_nascimento }} ({{ dadosAghu.idade }} anos)
              </template>
              <template v-else>
                {{ dadosAghu.idade }} anos
              </template>
              • Prontuário {{ dadosAghu.prontuario }}
            </p>

          </div>
          
          <div class="grid grid-cols-2 gap-x-4 gap-y-3 text-xs">
            <div class="space-y-0.5">
              <span class="text-[10px] font-medium uppercase tracking-wider text-slate-400">Especialidade</span>
              <p class="font-semibold text-slate-700">{{ dadosAghu.especialidade }}</p>
            </div>
            <div class="space-y-0.5">
              <span class="text-[10px] font-medium uppercase tracking-wider text-slate-400">Procedimento Principal</span>
              <p class="font-semibold text-slate-700 truncate" :title="dadosAghu.procedimento">{{ dadosAghu.procedimento || 'Não especificado' }}</p>
            </div>
            <div class="space-y-0.5">
              <span class="text-[10px] font-medium uppercase tracking-wider text-slate-400">Data e Hora da Cirurgia</span>
              <p class="font-semibold text-slate-700">
                {{ formatarDataBR(dadosAghu.data_cirurgia) }} às {{ dadosAghu.hora_cirurgia || '--:--' }}
              </p>
            </div>
            <div class="space-y-0.5">
              <span class="text-[10px] font-medium uppercase tracking-wider text-slate-400">Turno Mapeado</span>
              <p class="font-semibold text-slate-700">{{ dadosAghu.turno }}</p>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <UiButton variant="outline" @click="fecharModalNova">Cancelar</UiButton>
        <UiButton 
          :disabled="submetendoNova || !formNova.prontuario || !formNova.tipo || buscandoAghu || !dadosAghu || (dadosAghu.prontuario !== formNova.prontuario)" 
          @click="salvarNova"
        >
          {{ submetendoNova ? 'Salvando...' : 'Salvar' }}
        </UiButton>
      </template>
    </Modal>
    <Modal :show="showModalCancelamento" @close="showModalCancelamento = false">
      <template #header>{{ isCancelamentoReserva ? 'Cancelar Reserva' : 'Cancelar Solicitação' }}</template>
      <div class="space-y-4">
        <p class="text-sm text-slate-600">Por favor, selecione o motivo do cancelamento:</p>
        <div>
          <label class="block text-sm font-medium text-slate-700">Motivo <span class="text-red-500">*</span></label>
          <select v-model="motivoCancelamento" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200">
            <option value="" disabled selected>Selecione um motivo</option>
            <option v-for="m in motivosAtuais" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>
      </div>
      <template #footer>
        <UiButton variant="outline" @click="showModalCancelamento = false">Voltar</UiButton>
        <UiButton :disabled="!motivoCancelamento || submetendo" @click="confirmarAcaoCancelamento" class="bg-red-600 text-white hover:bg-red-700 border-none">
          {{ submetendo ? 'Cancelando...' : 'Confirmar Cancelamento' }}
        </UiButton>
      </template>
    </Modal>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { PlusIcon, PencilSquareIcon, TrashIcon, ClipboardIcon, CheckIcon, ClockIcon, CheckCircleIcon, MagnifyingGlassIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline';
import { useToast } from 'vue-toastification';
import UiButton from '../components/ui/Button.vue';
import Modal from '../components/Modal.vue';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();

type SolicitacaoStatus = 'Pendente' | 'Reservado' | 'Cancelada' | 'Concluída';

type Solicitacao = {
  id: string;
  prontuario: string;
  nome?: string;
  idade: number;
  especialidade: string;
  procedimento?: string;
  tipo: string;
  status: SolicitacaoStatus;
  turno: string;
  data_cirurgia?: string;
  hora_cirurgia?: string;
  prioridade?: string;
  destino?: string;
  dataHora: string;
  perfil_solicitante?: string;
  cirurgia_finalizada?: boolean;
  encaminhamento_liberado?: boolean;
};

const solicitacoes = ref<Solicitacao[]>([]);
const leitosDisponiveis = ref<any[]>([]);
const loading = ref(false);
const loadingLeitos = ref(false);
const submetendo = ref(false);
const showModalReserva = ref(false);
const isRemanejamento = ref(false);
const solSelecionada = ref<Solicitacao | null>(null);
const leitoEscolhido = ref<string | null>(null);
const toast = useToast();

const filtroData = ref('');
const showModalNova = ref(false);
const submetendoNova = ref(false);
const isEditing = ref(false);

const MOTIVOS_CANCELAMENTO = [
  'Cirurgia suspensa por outros motivos',
  'Paciente encaminhado para enfermaria de origem após a cirurgia',
  'Alteração do mapa cirúrgico'
];
const MOTIVOS_CANCELAMENTO_RESERVA = [
  'Pedido de vaga clínica (emergência)',
  'Pedido de vaga pela hemodinâmica',
  'Pedido de vaga pelo COB (emergência)',
  'Problemas relacionados a equipamentos',
  'Falta de vaga na enfermaria para paciente de alta',
  'Cancelamento de alta da UTI'
];

const motivosAtuais = computed(() => {
  if (isCancelamentoReserva.value) {
    return MOTIVOS_CANCELAMENTO_RESERVA;
  }
  // Se for UTI (e não admin), o motivo único de cancelamento da solicitação deve ser "Falta de vaga de UTI"
  if (authStore.isUTI && !authStore.isAdmin) {
    return ['Falta de vaga de UTI'];
  }
  // Se for Administrador, pode escolher tanto os normais quanto o de UTI
  if (authStore.isAdmin) {
    return [...MOTIVOS_CANCELAMENTO, 'Falta de vaga de UTI'];
  }
  return MOTIVOS_CANCELAMENTO;
});

const showModalCancelamento = ref(false);
const motivoCancelamento = ref('');
const idCancelamento = ref('');
const isCancelamentoReserva = ref(false);

const formNova = ref({
  prontuario: '',
  idade: null as number | null,
  especialidade: '',
  tipo: '',
  data_cirurgia: '',
  turno: '',
  prioridade: ''
});

const dadosAghu = ref<{
  prontuario: string;
  nome: string;
  idade: number;
  data_nascimento?: string;
  especialidade: string;
  procedimento: string;
  data_cirurgia: string;
  hora_cirurgia: string;
  turno: string;
} | null>(null);
const buscandoAghu = ref(false);
const erroAghu = ref('');

const tiposDisponiveis = computed(() => {
  const perfil = authStore.user?.perfil || '';
  if (perfil.includes('COB')) return ['Obstetrico'];
  if (perfil.includes('HEM')) return ['HEM'];
  if (perfil.includes('BC')) return ['Cirurgico'];
  // Admin e UTI veem tudo
  return ['Clinico', 'Cirurgico', 'HEM', 'Obstetrico'];
});

watch(showModalNova, (val) => {
  if (val && !isEditing.value) {
    if (tiposDisponiveis.value.length === 1) {
      formNova.value.tipo = tiposDisponiveis.value[0];
    }
  }
});

const solicitacoesFiltradas = computed(() => {
  let lista = [...solicitacoes.value];
  
  // 1. Aplicar filtro de data se existir
  if (filtroData.value) {
    lista = lista.filter(s => s.data_cirurgia === filtroData.value);
  }

  // 2. Ordenação Multinível
  return lista.sort((a, b) => {
    // Nível 1: Data Prevista da Cirurgia
    const dataA = a.data_cirurgia || '9999-99-99';
    const dataB = b.data_cirurgia || '9999-99-99';
    if (dataA !== dataB) return dataA.localeCompare(dataB);

    // Nível 2: Turno (Manhã < Tarde < Noite)
    const pesoTurno: Record<string, number> = { 'Manhã': 1, 'Tarde': 2, 'Noite': 3 };
    const turnoA = pesoTurno[a.turno] || 99;
    const turnoB = pesoTurno[b.turno] || 99;
    if (turnoA !== turnoB) return turnoA - turnoB;

    // Nível 3: Horário de Início da Cirurgia (crescente)
    const horaA = a.hora_cirurgia || '99:99';
    const horaB = b.hora_cirurgia || '99:99';
    if (horaA !== horaB) return horaA.localeCompare(horaB);

    // Nível 4: Prioridade (P1 < P2 < P3...)
    const getPrioridadeValor = (p: string | undefined) => {
      if (!p || !p.startsWith('P')) return 999;
      const num = parseInt(p.substring(1));
      return isNaN(num) ? 999 : num;
    };
    const prioA = getPrioridadeValor(a.prioridade);
    const prioB = getPrioridadeValor(b.prioridade);
    if (prioA !== prioB) return prioA - prioB;

    // Nível 5: Data da Solicitação (Desempate por ordem de chegada)
    return a.dataHora.localeCompare(b.dataHora);
  });
});

const solicitacoesPendentes = computed(() => solicitacoesFiltradas.value.filter(s => s.status === 'Pendente'));
const solicitacoesReservadas = computed(() => solicitacoesFiltradas.value.filter(s => s.status === 'Reservado'));
const solicitacoesConcluidas = computed(() => solicitacoesFiltradas.value.filter(s => s.status === 'Concluída'));

async function carregarSolicitacoes() {
  loading.value = true;
  try {
    const { data } = await api.get('/api/solicitacoes');
    solicitacoes.value = data;
  } catch (error) {
    console.error('Erro ao carregar solicitações:', error);
    toast.error('Não foi possível carregar as solicitações.');
  } finally {
    loading.value = false;
  }
}

async function carregarLeitosDisponiveis() {
  loadingLeitos.value = true;
  try {
    const { data } = await api.get('/api/leitos/disponiveis');
    leitosDisponiveis.value = data;
  } catch (error) {
    console.error('Erro ao carregar leitos:', error);
  } finally {
    loadingLeitos.value = false;
  }
}

function abrirModalReserva(sol: Solicitacao) {
  solSelecionada.value = sol;
  leitoEscolhido.value = null;
  isRemanejamento.value = false;
  showModalReserva.value = true;
  carregarLeitosDisponiveis();
}

function abrirModalMudarLeito(sol: Solicitacao) {
  solSelecionada.value = sol;
  leitoEscolhido.value = null;
  isRemanejamento.value = true;
  showModalReserva.value = true;
  carregarLeitosDisponiveis();
}

async function confirmarReserva() {
  if (!solSelecionada.value || !leitoEscolhido.value) return;
  submetendo.value = true;
  try {
    if (isRemanejamento.value) {
      await api.post(`/api/solicitacoes/${solSelecionada.value.id}/remanejar-reserva`, {
        leito_id: leitoEscolhido.value
      });
      toast.success('Reserva remanejada com sucesso!');
    } else {
      await api.post(`/api/solicitacoes/${solSelecionada.value.id}/reservar`, {
        leito_id: leitoEscolhido.value
      });
      toast.success('Leito reservado com sucesso!');
    }
    showModalReserva.value = false;
    carregarSolicitacoes();
  } catch (error: any) {
    console.error('Erro ao salvar reserva:', error);
    toast.error(error.response?.data?.detail || 'Erro ao salvar reserva.');
  } finally {
    submetendo.value = false;
  }
}

function abrirModalCancelamento(id: string, isReserva: boolean = false) {
  idCancelamento.value = id;
  isCancelamentoReserva.value = isReserva;
  
  // Se houver apenas um motivo possível, já pré-seleciona ele
  const currentMotivos = motivosAtuais.value;
  if (currentMotivos.length === 1) {
    motivoCancelamento.value = currentMotivos[0];
  } else {
    motivoCancelamento.value = '';
  }
  
  showModalCancelamento.value = true;
}

async function confirmarAcaoCancelamento() {
  if (isCancelamentoReserva.value) {
    await confirmarCancelamentoReserva();
  } else {
    await confirmarCancelamentoSolicitacao();
  }
}

async function confirmarCancelamentoSolicitacao() {
  if (!idCancelamento.value || !motivoCancelamento.value) return;
  submetendo.value = true;
  try {
    await api.delete(`/api/solicitacoes/${idCancelamento.value}?motivo=${encodeURIComponent(motivoCancelamento.value)}`);
    toast.success('Solicitação cancelada!');
    showModalCancelamento.value = false;
    carregarSolicitacoes();
  } catch (error: any) {
    toast.error(error.response?.data?.detail || 'Erro ao cancelar solicitação.');
  } finally {
    submetendo.value = false;
  }
}

async function confirmarCancelamentoReserva() {
  if (!idCancelamento.value || !motivoCancelamento.value) return;
  submetendo.value = true;
  try {
    await api.post(`/api/solicitacoes/${idCancelamento.value}/cancelar-reserva?motivo=${encodeURIComponent(motivoCancelamento.value)}`);
    toast.success('Reserva cancelada!');
    showModalCancelamento.value = false;
    carregarSolicitacoes();
  } catch (error: any) {
    toast.error(error.response?.data?.detail || 'Erro ao cancelar reserva.');
  } finally {
    submetendo.value = false;
  }
}

async function buscarPacienteAghu() {
  const pront = formNova.value.prontuario.trim();
  if (!pront) {
    dadosAghu.value = null;
    erroAghu.value = '';
    return;
  }
  
  buscandoAghu.value = true;
  erroAghu.value = '';
  try {
    const { data } = await api.get(`/api/solicitacoes/consultar-aghu/${pront}`);
    dadosAghu.value = data;
    // Preenche no formNova para que a validação/envio ocorra corretamente
    formNova.value.idade = data.idade;
    formNova.value.especialidade = data.especialidade;
    formNova.value.data_cirurgia = data.data_cirurgia;
    formNova.value.turno = data.turno;
  } catch (error: any) {
    console.error('Erro ao buscar no AGHU:', error);
    dadosAghu.value = null;
    erroAghu.value = error.response?.data?.detail || 'Paciente ou cirurgia não encontrada no AGHU.';
    toast.error(erroAghu.value);
  } finally {
    buscandoAghu.value = false;
  }
}

function fecharModalNova() {
  showModalNova.value = false;
  isEditing.value = false;
  formNova.value = {
    prontuario: '',
    idade: null,
    especialidade: '',
    tipo: '',
    data_cirurgia: '',
    turno: '',
    prioridade: ''
  };
  dadosAghu.value = null;
  erroAghu.value = '';
  buscandoAghu.value = false;
}

function abrirModalEdicao(sol: Solicitacao) {
  solSelecionada.value = sol;
  isEditing.value = true;
  formNova.value = {
    prontuario: sol.prontuario,
    idade: sol.idade,
    especialidade: sol.especialidade,
    tipo: sol.tipo,
    data_cirurgia: sol.data_cirurgia || '',
    turno: sol.turno,
    prioridade: sol.prioridade || ''
  };
  dadosAghu.value = {
    prontuario: sol.prontuario,
    nome: sol.nome || '',
    idade: sol.idade,
    especialidade: sol.especialidade,
    procedimento: sol.procedimento || '',
    data_cirurgia: sol.data_cirurgia || '',
    hora_cirurgia: sol.hora_cirurgia || '',
    turno: sol.turno
  };
  showModalNova.value = true;
}

async function salvarNova() {
  submetendoNova.value = true;
  try {
    if (isEditing.value && solSelecionada.value) {
      await api.patch(`/api/solicitacoes/${solSelecionada.value.id}`, formNova.value);
      toast.success('Solicitação atualizada!');
    } else {
      await api.post('/api/solicitacoes', formNova.value);
      toast.success('Solicitação criada!');
    }
    fecharModalNova();
    carregarSolicitacoes();
  } catch (error) {
    console.error('Erro ao salvar:', error);
    toast.error('Erro ao salvar solicitação.');
  } finally {
    submetendoNova.value = false;
  }
}

function formatarDataHoraBR(dataStr: string) {
  if (!dataStr) return '';
  const [data, hora] = dataStr.split(' ');
  const [ano, mes, dia] = data.split('-');
  return `${dia}/${mes}/${ano} ${hora || ''}`;
}

function formatarDataBR(dataStr: string) {
  if (!dataStr) return '';
  const [ano, mes, dia] = dataStr.split('-');
  return `${dia}/${mes}/${ano}`;
}

// Verifica se o usuário atual pode cancelar/gerenciar esta solicitação específica
function podeGerenciar(sol: any) {
  if (!sol) return false;
  
  const userPerfil = authStore.perfil || "";
  const userGrupo = userPerfil.replace("-Admin", "").trim().toUpperCase();
  const solPerfil = (sol.perfil_solicitante || "").trim().toUpperCase();
  
  if (authStore.isAdmin) return true;
  
  if (!userGrupo || userGrupo === "COMUM") return false;
  if (!solPerfil) return false;
  
  return solPerfil === userGrupo;
}

async function confirmarCirurgiaFinalizada(id: string) {
  try {
    await api.post(`/api/solicitacoes/${id}/cirurgia-finalizada`);
    toast.success('Cirurgia sinalizada como finalizada.');
    await carregarSolicitacoes();
  } catch (error) {
    console.error('Erro ao marcar cirurgia finalizada:', error);
    toast.error('Não foi possível marcar cirurgia como finalizada.');
  }
}

onMounted(() => {
  carregarSolicitacoes();
});
</script>
