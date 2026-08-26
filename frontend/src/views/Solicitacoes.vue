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
                <!-- Botão Finalizar Cirurgia -->
                <UiButton
                  v-if="!sol.cirurgia_finalizada"
                  size="sm"
                  class="bg-amber-500 hover:bg-amber-600 text-white font-bold px-4 border-none shadow-sm flex items-center gap-1"
                  @click="abrirModalPassagemCaso(sol)"
                >
                  <CheckIcon class="h-4 w-4 mr-1 text-white" />
                  Finalizar Cirurgia
                </UiButton>
                
                <!-- Botão Editar Passagem de Caso -->
                <UiButton
                  v-else-if="sol.cirurgia_finalizada && !sol.encaminhamento_liberado"
                  size="sm"
                  class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 border-none shadow-sm flex items-center gap-1"
                  @click="abrirModalPassagemCaso(sol)"
                >
                  <PencilSquareIcon class="h-4 w-4 mr-1 text-white" />
                  Editar Passagem
                </UiButton>

                <!-- Status de Cirurgia Concluída (quando já liberado pela UTI) -->
                <UiButton
                  v-else
                  size="sm"
                  disabled
                  class="bg-emerald-600 border-none text-white font-bold px-4 shadow-sm opacity-100 cursor-not-allowed flex items-center gap-1"
                >
                  <CheckIcon class="h-4 w-4 mr-1 text-white" />
                  Cirurgia Concluída
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
        <button 
          @click="concluidaExpandida = !concluidaExpandida"
          class="mb-6 flex items-center justify-between w-full rounded-xl border border-slate-200 bg-slate-50/50 p-4 transition hover:bg-slate-100/50 focus:outline-none"
        >
          <div class="flex items-center gap-3">
            <div class="h-8 w-1 rounded bg-blue-500"></div>
            <h2 class="text-xl font-bold text-slate-800">Solicitações Concluídas (Paciente no Leito)</h2>
            <span class="rounded-full bg-blue-100 px-3 py-1 text-sm font-bold text-blue-600">
              {{ solicitacoesConcluidas.length }}
            </span>
          </div>
          <ChevronUpIcon v-if="concluidaExpandida" class="h-5 w-5 text-slate-500 mr-2" />
          <ChevronDownIcon v-else class="h-5 w-5 text-slate-500 mr-2" />
        </button>

        <div v-if="concluidaExpandida" class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                <p v-if="sol.atualizado_em" class="text-[10px] text-slate-500 mt-1 font-medium">
                  Concluído em: {{ formatarDataHoraBR(sol.atualizado_em) }}
                </p>
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
        <div v-else-if="leitosDisponiveisFiltrados.length === 0" class="text-center py-4 text-slate-500 italic">
          Nenhum leito disponível para reserva no momento.
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
              <option value="P5">P5</option>
              <option value="P6">P6</option>
              <option value="P7">P7</option>
              <option value="P8">P8</option>
              <option value="P9">P9</option>
              <option value="P10">P10 (Menor)</option>
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
    <Modal :show="showModalConfirmacaoTrocaProntuario" @close="showModalConfirmacaoTrocaProntuario = false">
      <template #header>Alteração de Paciente</template>
      <div class="space-y-4 text-left">
        <p class="text-sm text-slate-600">
          Você está alterando o prontuário desta solicitação do paciente anterior <strong>{{ solSelecionada?.nome || 'N/D' }}</strong> (Prontuário {{ solSelecionada?.prontuario }}) para o novo paciente <strong>{{ dadosAghu?.nome }}</strong> (Prontuário {{ formNova.prontuario }}).
        </p>
        <p class="text-sm font-semibold text-slate-700">
          O que deseja fazer com a solicitação do paciente anterior?
        </p>
        <div class="rounded-lg border border-slate-100 bg-slate-50 p-3 space-y-2 text-xs text-slate-500">
          <p>• <strong>Cancelar Antiga:</strong> Remove o paciente anterior da fila / cancela sua solicitação.</p>
          <p>• <strong>Voltar para a Fila:</strong> Mantém o paciente anterior ativo na lista de solicitações pendentes (voltando a aguardar reserva se ele estava reservado).</p>
        </div>
      </div>
      <template #footer>
        <UiButton variant="outline" @click="showModalConfirmacaoTrocaProntuario = false">Cancelar Alteração</UiButton>
        <UiButton variant="outline" @click="confirmarSalvarEdicao(false)" class="text-blue-600 border-blue-200 hover:bg-blue-50">
          Voltar para a Fila
        </UiButton>
        <UiButton @click="confirmarSalvarEdicao(true)" class="bg-red-600 text-white hover:bg-red-700 border-none">
          Cancelar Antiga
        </UiButton>
      </template>
    </Modal>

    <!-- Modal Passagem de Caso -->
    <Modal :show="showModalPassagemCaso" @close="fecharModalPassagemCaso" size="lg">
      <template #header>
        <div class="flex items-center justify-between w-full">
          <span>{{ modoEdicaoPassagem ? 'Editar Passagem de Caso' : 'Passagem de Caso' }} - Prontuário {{ solSelecionada?.prontuario }}</span>
        </div>
      </template>
      <div class="space-y-6 text-left max-h-[70vh] overflow-y-auto overflow-x-hidden px-1">
        
        <!-- Identificação Básica -->
        <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm space-y-4">
          <h3 class="text-sm font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
            <span class="w-1.5 h-4 bg-blue-600 rounded-full"></span> Identificação Básica
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="flex items-center gap-2">
              <input type="checkbox" id="cirurgia_nao_realizada" v-model="passagemCasoForm.cirurgia_nao_realizada" @change="lidarMudancaCirurgiaNaoRealizada" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
              <label for="cirurgia_nao_realizada" class="text-sm font-semibold text-red-600">CIRURGIA NÃO REALIZADA</label>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Procedimento Realizado *</label>
              <input type="text" v-model="passagemCasoForm.procedimento_realizado" :disabled="passagemCasoForm.cirurgia_nao_realizada" placeholder="Nome do procedimento realizado" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-slate-100 disabled:text-slate-400" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Anestesia *</label>
              <input type="text" v-model="passagemCasoForm.anestesia" placeholder="Ex: Geral, Raqui, Epidural" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Alergias *</label>
              <div class="mt-2 space-y-2">
                <div class="flex items-center gap-4">
                  <label class="flex items-center gap-1.5 text-sm cursor-pointer">
                    <input type="radio" value="Não" v-model="passagemCasoForm.alergias.opcao" /> Não
                  </label>
                  <label class="flex items-center gap-1.5 text-sm cursor-pointer">
                    <input type="radio" value="Sim" v-model="passagemCasoForm.alergias.opcao" /> Sim
                  </label>
                </div>
                <input v-if="passagemCasoForm.alergias.opcao === 'Sim'" type="text" v-model="passagemCasoForm.alergias.detalhe" placeholder="Quais alergias?" class="w-full rounded-md border border-slate-200 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
              </div>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Isolamento *</label>
              <select 
                v-model="passagemCasoForm.isolamento" 
                class="mt-1 w-full rounded-md border border-slate-200 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white"
              >
                <option value="" disabled>Selecione uma opção...</option>
                <option value="Não">Não</option>
                <option value="Contato">Contato</option>
                <option value="Gotículas">Gotículas</option>
                <option value="Aerossóis">Aerossóis</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Respiratório -->
        <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm space-y-4">
          <h3 class="text-sm font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
            <span class="w-1.5 h-4 bg-blue-600 rounded-full"></span> Respiratório *
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <span class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Via Aérea (Selecione uma opção)</span>
              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm cursor-pointer">
                  <input type="radio" value="Espontânea" v-model="passagemCasoForm.respiratorio.via_aerea" @change="passagemCasoForm.respiratorio.via_aerea_outro_detalhe = ''" /> Espontânea
                </label>
                <label class="flex items-center gap-2 text-sm cursor-pointer">
                  <input type="radio" value="TOT" v-model="passagemCasoForm.respiratorio.via_aerea" @change="passagemCasoForm.respiratorio.via_aerea_outro_detalhe = ''" /> TOT
                </label>
                <label class="flex items-center gap-2 text-sm cursor-pointer">
                  <input type="radio" value="Traqueostomia" v-model="passagemCasoForm.respiratorio.via_aerea" @change="passagemCasoForm.respiratorio.via_aerea_outro_detalhe = ''" /> Traqueostomia
                </label>
                <div class="space-y-2">
                  <label class="flex items-center gap-2 text-sm cursor-pointer">
                    <input type="radio" value="Outro" v-model="passagemCasoForm.respiratorio.via_aerea" /> Outro
                  </label>
                  <input v-if="passagemCasoForm.respiratorio.via_aerea === 'Outro'" type="text" v-model="passagemCasoForm.respiratorio.via_aerea_outro_detalhe" placeholder="Descreva a via aérea" class="w-full rounded-md border border-slate-200 px-3 py-1.5 text-xs focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
                </div>
              </div>
            </div>
            <div>
              <span class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Suporte (Selecione uma opção)</span>
              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm cursor-pointer">
                  <input type="radio" value="Ar ambiente" v-model="passagemCasoForm.respiratorio.suporte" /> Ar ambiente
                </label>
                <label class="flex items-center gap-2 text-sm cursor-pointer">
                  <input type="radio" value="O2 cateter" v-model="passagemCasoForm.respiratorio.suporte" /> O₂ cateter
                </label>
                <label class="flex items-center gap-2 text-sm cursor-pointer">
                  <input type="radio" value="Máscara" v-model="passagemCasoForm.respiratorio.suporte" /> Máscara
                </label>
                <label class="flex items-center gap-2 text-sm cursor-pointer">
                  <input type="radio" value="Ventilação mecânica" v-model="passagemCasoForm.respiratorio.suporte" /> Ventilação mecânica
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Cardiovascular/Hemodinâmico -->
        <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm space-y-4">
          <h3 class="text-sm font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
            <span class="w-1.5 h-4 bg-blue-600 rounded-full"></span> Cardiovascular/Hemodinâmico *
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Hemodinâmica</span>
              <div class="flex gap-4">
                <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Estável" v-model="passagemCasoForm.cardiovascular.hemodinamica" /> Estável</label>
                <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Instável" v-model="passagemCasoForm.cardiovascular.hemodinamica" /> Instável</label>
              </div>
            </div>
            <div>
              <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Drogas Vasoativas</span>
              <div class="space-y-2">
                <div class="flex gap-4">
                  <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Não" v-model="passagemCasoForm.cardiovascular.drogas_vasoativas.opcao" @change="passagemCasoForm.cardiovascular.drogas_vasoativas.detalhe = ''" /> Não</label>
                  <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Sim" v-model="passagemCasoForm.cardiovascular.drogas_vasoativas.opcao" /> Sim</label>
                </div>
                <input v-if="passagemCasoForm.cardiovascular.drogas_vasoativas.opcao === 'Sim'" type="text" v-model="passagemCasoForm.cardiovascular.drogas_vasoativas.detalhe" placeholder="Droga/vazão" class="w-full rounded-md border border-slate-200 px-3 py-1.5 text-xs focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
              </div>
            </div>
            <div>
              <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Necessidade de reposição volêmica</span>
              <div class="flex gap-4">
                <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Não" v-model="passagemCasoForm.cardiovascular.reposicao_volemica" /> Não</label>
                <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Sim" v-model="passagemCasoForm.cardiovascular.reposicao_volemica" /> Sim</label>
              </div>
            </div>
            <div>
              <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Transfusão</span>
              <div class="space-y-2">
                <div class="flex gap-4">
                  <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Não" v-model="passagemCasoForm.cardiovascular.transfusao.opcao" @change="passagemCasoForm.cardiovascular.transfusao.detalhe = ''" /> Não</label>
                  <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Sim" v-model="passagemCasoForm.cardiovascular.transfusao.opcao" /> Sim</label>
                </div>
                <input v-if="passagemCasoForm.cardiovascular.transfusao.opcao === 'Sim'" type="text" v-model="passagemCasoForm.cardiovascular.transfusao.detalhe" placeholder="Hemocomponente/quantidade" class="w-full rounded-md border border-slate-200 px-3 py-1.5 text-xs focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
              </div>
            </div>
          </div>
        </div>

        <!-- Sangramento e Balanço -->
        <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm space-y-4">
          <h3 class="text-sm font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
            <span class="w-1.5 h-4 bg-blue-600 rounded-full"></span> Sangramento e Balanço *
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Sangramento Estimado</span>
              <select v-model="passagemCasoForm.sangramento_balanco.sangramento_estimado" class="w-full rounded-md border border-slate-200 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                <option value="" disabled>Selecione uma opção</option>
                <option value="Mínimo">Mínimo</option>
                <option value="Pequeno">Pequeno</option>
                <option value="Moderado">Moderado</option>
                <option value="Importante">Importante</option>
                <option value="Não se aplica">Não se aplica</option>
              </select>
              <div v-if="passagemCasoForm.sangramento_balanco.sangramento_estimado === 'Importante'" class="mt-2 flex items-center gap-2">
                <span class="text-xs text-slate-500">Volume estimado:</span>
                <input type="number" v-model="passagemCasoForm.sangramento_balanco.sangramento_volume" placeholder="mL" class="w-24 rounded-md border border-slate-200 px-2 py-1 text-xs focus:border-blue-500" />
                <span class="text-xs text-slate-500">mL</span>
              </div>
            </div>
            <div>
              <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Diurese Intraoperatória</span>
              <div class="flex items-center gap-3">
                <label class="flex items-center gap-1.5"><input type="radio" value="valor" v-model="passagemCasoForm.sangramento_balanco.diurese_intraoperatoria.opcao" /> Diurese (mL)</label>
                <label class="flex items-center gap-1.5"><input type="radio" value="Não se aplica" v-model="passagemCasoForm.sangramento_balanco.diurese_intraoperatoria.opcao" /> Não se aplica</label>
              </div>
              <div v-if="passagemCasoForm.sangramento_balanco.diurese_intraoperatoria.opcao === 'valor'" class="mt-2 flex items-center gap-2">
                <input type="number" v-model="passagemCasoForm.sangramento_balanco.diurese_intraoperatoria.valor" placeholder="Volume diurese" class="w-32 rounded-md border border-slate-200 px-2 py-1 text-xs focus:border-blue-500" />
                <span class="text-xs text-slate-500">mL</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Acessos, dispositivos e feridas -->
        <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm space-y-4">
          <h3 class="text-sm font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
            <span class="w-1.5 h-4 bg-blue-600 rounded-full"></span> Acessos, Dispositivos e Feridas *
          </h3>
          <div class="space-y-4 text-sm">
            <div>
              <span class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Acessos Venosos (Selecione pelo menos um) *</span>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                
                <!-- Periferico -->
                <div class="flex flex-col gap-1 border border-slate-100 rounded-lg p-2 bg-slate-50/50">
                  <div class="flex items-center gap-2">
                    <input type="checkbox" id="acesso_periferico" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.periferico" />
                    <label for="acesso_periferico" class="text-sm font-semibold text-slate-700 cursor-pointer">Periférico</label>
                  </div>
                  <div v-if="passagemCasoForm.acessos_dispositivos.acessos_venosos.periferico" class="mt-1 space-y-1.5">
                    <div class="flex items-center gap-2">
                      <span class="text-xs text-slate-500 shrink-0">Local *:</span>
                      <input type="text" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.periferico_local" placeholder="Ex: MSE" class="flex-1 rounded-md border border-slate-200 px-2 py-0.5 text-xs focus:border-blue-500" />
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-xs text-slate-500 shrink-0">Data Criação:</span>
                      <input type="date" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.periferico_data" class="flex-1 rounded-md border border-slate-200 px-2 py-0.5 text-xs focus:border-blue-500 bg-white" />
                    </div>
                  </div>
                </div>

                <!-- CVC -->
                <div class="flex flex-col gap-1 border border-slate-100 rounded-lg p-2 bg-slate-50/50">
                  <div class="flex items-center gap-2">
                    <input type="checkbox" id="acesso_cvc" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.cvc" />
                    <label for="acesso_cvc" class="text-sm font-semibold text-slate-700 cursor-pointer">CVC</label>
                  </div>
                  <div v-if="passagemCasoForm.acessos_dispositivos.acessos_venosos.cvc" class="mt-1 space-y-1.5">
                    <div class="flex items-center gap-2">
                      <span class="text-xs text-slate-500 shrink-0">Local *:</span>
                      <input type="text" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.cvc_local" placeholder="Ex: Subclávia D" class="flex-1 rounded-md border border-slate-200 px-2 py-0.5 text-xs focus:border-blue-500" />
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-xs text-slate-500 shrink-0">Data Criação:</span>
                      <input type="date" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.cvc_data" class="flex-1 rounded-md border border-slate-200 px-2 py-0.5 text-xs focus:border-blue-500 bg-white" />
                    </div>
                  </div>
                </div>

                <!-- PICC -->
                <div class="flex flex-col gap-1 border border-slate-100 rounded-lg p-2 bg-slate-50/50">
                  <div class="flex items-center gap-2">
                    <input type="checkbox" id="acesso_picc" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.picc" />
                    <label for="acesso_picc" class="text-sm font-semibold text-slate-700 cursor-pointer">PICC</label>
                  </div>
                  <div v-if="passagemCasoForm.acessos_dispositivos.acessos_venosos.picc" class="mt-1 space-y-1.5">
                    <div class="flex items-center gap-2">
                      <span class="text-xs text-slate-500 shrink-0">Local *:</span>
                      <input type="text" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.picc_local" placeholder="Ex: Basílica E" class="flex-1 rounded-md border border-slate-200 px-2 py-0.5 text-xs focus:border-blue-500" />
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-xs text-slate-500 shrink-0">Data Criação:</span>
                      <input type="date" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.picc_data" class="flex-1 rounded-md border border-slate-200 px-2 py-0.5 text-xs focus:border-blue-500 bg-white" />
                    </div>
                  </div>
                </div>

                <!-- Outro -->
                <div class="flex flex-col gap-1 border border-slate-100 rounded-lg p-2 bg-slate-50/50">
                  <div class="flex items-center gap-2">
                    <input type="checkbox" id="acesso_outro" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.outro" />
                    <label for="acesso_outro" class="text-sm font-semibold text-slate-700 cursor-pointer">Outro Acesso Venoso</label>
                  </div>
                  <div v-if="passagemCasoForm.acessos_dispositivos.acessos_venosos.outro" class="mt-1 space-y-1.5">
                    <div class="flex items-center gap-2">
                      <span class="text-xs text-slate-500 shrink-0">Descrição *:</span>
                      <input type="text" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.outro_detalhe" placeholder="Descreva o tipo e local" class="flex-1 rounded-md border border-slate-200 px-2 py-0.5 text-xs focus:border-blue-500" />
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-xs text-slate-500 shrink-0">Data Criação:</span>
                      <input type="date" v-model="passagemCasoForm.acessos_dispositivos.acessos_venosos.outro_data" class="flex-1 rounded-md border border-slate-200 px-2 py-0.5 text-xs focus:border-blue-500 bg-white" />
                    </div>
                  </div>
                </div>

              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">PAI</span>
                <div class="space-y-2">
                  <div class="flex gap-4">
                    <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Não" v-model="passagemCasoForm.acessos_dispositivos.pai.opcao" @change="passagemCasoForm.acessos_dispositivos.pai.local = ''" /> Não</label>
                    <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Sim" v-model="passagemCasoForm.acessos_dispositivos.pai.opcao" /> Sim</label>
                  </div>
                  <input v-if="passagemCasoForm.acessos_dispositivos.pai.opcao === 'Sim'" type="text" v-model="passagemCasoForm.acessos_dispositivos.pai.local" placeholder="Local" class="w-full rounded-md border border-slate-200 px-3 py-1.5 text-xs focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
                </div>
              </div>
              <div>
                <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Sonda Vesical</span>
                <div class="space-y-2">
                  <div class="flex gap-4">
                    <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Não" v-model="passagemCasoForm.acessos_dispositivos.sonda_vesical.opcao" @change="passagemCasoForm.acessos_dispositivos.sonda_vesical.n_sonda = ''" /> Não</label>
                    <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Sim" v-model="passagemCasoForm.acessos_dispositivos.sonda_vesical.opcao" /> Sim</label>
                  </div>
                  <input v-if="passagemCasoForm.acessos_dispositivos.sonda_vesical.opcao === 'Sim'" type="text" v-model="passagemCasoForm.acessos_dispositivos.sonda_vesical.n_sonda" placeholder="Nº da Sonda" class="w-full rounded-md border border-slate-200 px-3 py-1.5 text-xs focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
                </div>
              </div>
              <div>
                <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Ferida Operatória</span>
                <div class="space-y-2">
                  <div class="flex gap-4">
                    <label class="flex items-center gap-1.5 cursor-pointer">
                      <input type="radio" :value="true" v-model="passagemCasoForm.acessos_dispositivos.ferida_operatoria.nao_se_aplica" @change="lidarMudancaNaoSeAplicaFerida" /> Não
                    </label>
                    <label class="flex items-center gap-1.5 cursor-pointer">
                      <input type="radio" :value="false" v-model="passagemCasoForm.acessos_dispositivos.ferida_operatoria.nao_se_aplica" /> Sim
                    </label>
                  </div>
                  <input v-if="passagemCasoForm.acessos_dispositivos.ferida_operatoria.nao_se_aplica === false" type="text" v-model="passagemCasoForm.acessos_dispositivos.ferida_operatoria.local" placeholder="Local da Ferida" class="w-full rounded-md border border-slate-200 px-3 py-1.5 text-xs focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
                </div>
              </div>
              <div>
                <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Drenos</span>
                <div class="space-y-2">
                  <div class="flex gap-4">
                    <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Não" v-model="passagemCasoForm.acessos_dispositivos.drenos.opcao" @change="passagemCasoForm.acessos_dispositivos.drenos.tipo_local = ''" /> Não</label>
                    <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Sim" v-model="passagemCasoForm.acessos_dispositivos.drenos.opcao" /> Sim</label>
                  </div>
                  <input v-if="passagemCasoForm.acessos_dispositivos.drenos.opcao === 'Sim'" type="text" v-model="passagemCasoForm.acessos_dispositivos.drenos.tipo_local" placeholder="Tipo e local" class="w-full rounded-md border border-slate-200 px-3 py-1.5 text-xs focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
                </div>
              </div>
            </div>
            
            <div class="border-t pt-3">
              <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Outros Dispositivos (Opcional)</span>
              <div class="flex flex-wrap gap-4">
                <label class="flex items-center gap-1.5 cursor-pointer"><input type="checkbox" v-model="passagemCasoForm.acessos_dispositivos.outros.sng_sne" /> SNG/SNE</label>
                <label class="flex items-center gap-1.5 cursor-pointer"><input type="checkbox" v-model="passagemCasoForm.acessos_dispositivos.outros.ostomia" /> Ostomia</label>
                <div class="flex items-center gap-2">
                  <input type="checkbox" v-model="passagemCasoForm.acessos_dispositivos.outros.outro" />
                  <span>Outro:</span>
                  <input v-if="passagemCasoForm.acessos_dispositivos.outros.outro" type="text" v-model="passagemCasoForm.acessos_dispositivos.outros.outro_detalhe" placeholder="Qual?" class="rounded-md border border-slate-200 px-2 py-0.5 text-xs focus:border-blue-500" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Medicamentos -->
        <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm space-y-4">
          <h3 class="text-sm font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
            <span class="w-1.5 h-4 bg-blue-600 rounded-full"></span> Medicamentos
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Antibiótico *</span>
              <div class="space-y-2">
                <div class="flex gap-4">
                  <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Não" v-model="passagemCasoForm.medicamentos.antibiotico.opcao" @change="passagemCasoForm.medicamentos.antibiotico.detalhe = ''" /> Não</label>
                  <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" value="Sim" v-model="passagemCasoForm.medicamentos.antibiotico.opcao" /> Sim</label>
                </div>
                <input v-if="passagemCasoForm.medicamentos.antibiotico.opcao === 'Sim'" type="text" v-model="passagemCasoForm.medicamentos.antibiotico.detalhe" placeholder="Qual e horário" class="w-full rounded-md border border-slate-200 px-3 py-1.5 text-xs focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
              </div>
            </div>
            <div>
              <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Outras medicações relevantes</span>
              <input type="text" v-model="passagemCasoForm.medicamentos.outras_medicacoes" placeholder="Outros medicamentos administrados" class="w-full rounded-md border border-slate-200 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 mt-2" />
            </div>
          </div>
        </div>

        <!-- Intercorrências durante o ato anestésico-cirúrgico -->
        <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm space-y-4">
          <h3 class="text-sm font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
            <span class="w-1.5 h-4 bg-blue-600 rounded-full"></span> Intercorrências durante o ato anestésico-cirúrgico
          </h3>
          <div class="text-sm space-y-4">
            <div class="grid grid-cols-2 md:grid-cols-3 gap-2">
              <label class="flex items-center gap-1.5"><input type="checkbox" v-model="passagemCasoForm.intercorrencias.nao_houve" @change="if(passagemCasoForm.intercorrencias.nao_houve) { passagemCasoForm.intercorrencias.hipotensao=false; passagemCasoForm.intercorrencias.hipertensao=false; passagemCasoForm.intercorrencias.arritmia=false; passagemCasoForm.intercorrencias.dessaturacao=false; passagemCasoForm.intercorrencias.broncoespasmo=false; passagemCasoForm.intercorrencias.sangramento_importante=false; passagemCasoForm.intercorrencias.reacao_medicamentosa=false;  passagemCasoForm.intercorrencias.parada_cardiorespiratoria=false; passagemCasoForm.intercorrencias.dificil_via_aerea=false; passagemCasoForm.intercorrencias.outro=false; }" /> Não houve</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" v-model="passagemCasoForm.intercorrencias.hipotensao" :disabled="passagemCasoForm.intercorrencias.nao_houve" /> Hipotensão</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" v-model="passagemCasoForm.intercorrencias.hipertensao" :disabled="passagemCasoForm.intercorrencias.nao_houve" /> Hipertensão</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" v-model="passagemCasoForm.intercorrencias.arritmia" :disabled="passagemCasoForm.intercorrencias.nao_houve" /> Arritmia</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" v-model="passagemCasoForm.intercorrencias.dessaturacao" :disabled="passagemCasoForm.intercorrencias.nao_houve" /> Dessaturação</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" v-model="passagemCasoForm.intercorrencias.broncoespasmo" :disabled="passagemCasoForm.intercorrencias.nao_houve" /> Broncoespasmo</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" v-model="passagemCasoForm.intercorrencias.sangramento_importante" :disabled="passagemCasoForm.intercorrencias.nao_houve" /> Sangramento importante</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" v-model="passagemCasoForm.intercorrencias.reacao_medicamentosa" :disabled="passagemCasoForm.intercorrencias.nao_houve" /> Reação medicamentosa</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" v-model="passagemCasoForm.intercorrencias.parada_cardiorespiratoria" :disabled="passagemCasoForm.intercorrencias.nao_houve" /> Parada cardiorrespiratória</label>
              <label class="flex items-center gap-1.5"><input type="checkbox" v-model="passagemCasoForm.intercorrencias.dificil_via_aerea" :disabled="passagemCasoForm.intercorrencias.nao_houve" /> Difícil via aérea</label>
              <div class="flex items-center gap-2">
                <input type="checkbox" v-model="passagemCasoForm.intercorrencias.outro" :disabled="passagemCasoForm.intercorrencias.nao_houve" />
                <span>Outro:</span>
                <input v-if="passagemCasoForm.intercorrencias.outro" type="text" v-model="passagemCasoForm.intercorrencias.outro_detalhe" placeholder="Descreva" class="rounded-md border border-slate-200 px-2 py-0.5 text-xs focus:border-blue-500" />
              </div>
            </div>
            <div>
              <span class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Descrição da intercorrência/conduta (Opcional)</span>
              <textarea v-model="passagemCasoForm.intercorrencias.descricao_conduta" placeholder="Descreva condutas adotadas..." rows="3" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-blue-500"></textarea>
            </div>
          </div>
        </div>

        <!-- Responsável -->
        <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm space-y-4">
          <h3 class="text-sm font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
            <span class="w-1.5 h-4 bg-blue-600 rounded-full"></span> Profissional Responsável *
          </h3>
          <div>
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Profissional responsável pela passagem *</label>
            <input type="text" v-model="passagemCasoForm.profissional_responsavel" placeholder="Nome Completo / CRM / COREN" class="mt-1 w-full rounded-md border border-slate-200 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
          </div>
        </div>

        <!-- Alerta de campos faltantes -->
        <div v-if="listaCamposFaltantes.length > 0" class="bg-amber-50 border border-amber-200 rounded-lg p-3 text-xs text-amber-800 space-y-1 mt-4">
          <p class="font-bold flex items-center gap-1.5 text-amber-900">
            <ExclamationTriangleIcon class="w-4 h-4 text-amber-600 shrink-0" />
            Aguardando o preenchimento de campos obrigatórios:
          </p>
          <ul class="list-disc list-inside grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-1 pl-1">
            <li v-for="err in listaCamposFaltantes" :key="err" class="text-amber-700">{{ err }}</li>
          </ul>
        </div>

      </div>
      <template #footer>
        <UiButton variant="outline" @click="fecharModalPassagemCaso" :disabled="submetendo">
          Cancelar
        </UiButton>
        
        <UiButton v-if="modoEdicaoPassagem" @click="salvarEdicaoPassagemCaso" :disabled="submetendo || !formPassagemCasoValido" class="bg-blue-600 text-white hover:bg-blue-700">
          {{ submetendo ? 'Salvando...' : 'Salvar Alterações' }}
        </UiButton>
        <UiButton v-else @click="confirmarFinalizarComPassagem" :disabled="submetendo || !formPassagemCasoValido" class="bg-blue-600 text-white hover:bg-blue-700">
          {{ submetendo ? 'Salvando...' : 'Salvar e Finalizar' }}
        </UiButton>
      </template>
    </Modal>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { PlusIcon, PencilSquareIcon, TrashIcon, ClipboardIcon, CheckIcon, ClockIcon, CheckCircleIcon, MagnifyingGlassIcon, ExclamationTriangleIcon, ChevronDownIcon, ChevronUpIcon } from '@heroicons/vue/24/outline';
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
  atualizado_em?: string;
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
const leitosDisponiveisFiltrados = computed(() => {
  if (!solSelecionada.value || !solSelecionada.value.destino) return leitosDisponiveis.value;
  const leitoAtualNumero = solSelecionada.value.destino.replace(/^leito\s+/i, '').trim();
  if (!leitoAtualNumero) return leitosDisponiveis.value;
  return leitosDisponiveis.value.filter(l => l.lto_lto_id !== leitoAtualNumero);
});
const toast = useToast();

const filtroData = ref('');
const showModalNova = ref(false);
const submetendoNova = ref(false);
const isEditing = ref(false);

const MOTIVOS_CANCELAMENTO = [
  'Cirurgia suspensa por outros motivos',
  'Paciente encaminhado para enfermaria de origem após a cirurgia',
  'Alteração do mapa cirúrgico',
  'Paciente já ocupa um leito na UTI'
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
  // Se for UTI (e não admin), os motivos permitidos são Falta de vaga de UTI ou Paciente já ocupa leito
  if (authStore.isUTI && !authStore.isAdmin) {
    return ['Falta de vaga de UTI', 'Paciente já ocupa um leito na UTI'];
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
const showModalConfirmacaoTrocaProntuario = ref(false);
const concluidaExpandida = ref(false);

const showModalPassagemCaso = ref(false);
const idSolicitacaoFinalizacao = ref("");
const modoEdicaoPassagem = ref(false);

function criarFormPassagemCasoPadrao() {
  return {
    cirurgia_nao_realizada: false,
    procedimento_realizado: "",
    anestesia: "",
    alergias: {
      opcao: "",
      detalhe: ""
    },
    isolamento: "",
    respiratorio: {
      via_aerea: "",
      via_aerea_outro_detalhe: "",
      suporte: ""
    },
    cardiovascular: {
      hemodinamica: "",
      drogas_vasoativas: {
        opcao: "",
        detalhe: ""
      },
      reposicao_volemica: "",
      transfusao: {
        opcao: "",
        detalhe: ""
      }
    },
    sangramento_balanco: {
      sangramento_estimado: "",
      sangramento_volume: null as number | null,
      diurese_intraoperatoria: {
        opcao: "",
        valor: null as number | null
      }
    },
    acessos_dispositivos: {
      acessos_venosos: {
        periferico: false,
        periferico_local: "",
        periferico_data: "",
        cvc: false,
        cvc_local: "",
        cvc_data: "",
        picc: false,
        picc_local: "",
        picc_data: "",
        outro: false,
        outro_detalhe: "",
        outro_data: ""
      },
      pai: {
        opcao: "",
        local: ""
      },
      sonda_vesical: {
        opcao: "",
        n_sonda: ""
      },
      ferida_operatoria: {
        local: "",
        nao_se_aplica: null as any
      },
      drenos: {
        opcao: "",
        tipo_local: ""
      },
      outros: {
        sng_sne: false,
        ostomia: false,
        outro: false,
        outro_detalhe: ""
      }
    },
    medicamentos: {
      antibiotico: {
        opcao: "",
        detalhe: ""
      },
      outras_medicacoes: ""
    },
    intercorrencias: {
      nao_houve: false,
      hipotensao: false,
      hipertensao: false,
      arritmia: false,
      dessaturacao: false,
      broncoespasmo: false,
      sangramento_importante: false,
      reacao_medicamentosa: false,
      parada_cardiorespiratoria: false,
      dificil_via_aerea: false,
      outro: false,
      outro_detalhe: "",
      descricao_conduta: ""
    },
    profissional_responsavel: ""
  };
}

const passagemCasoForm = ref(criarFormPassagemCasoPadrao());


function lidarMudancaNaoSeAplicaFerida() {
  if (passagemCasoForm.value.acessos_dispositivos.ferida_operatoria.nao_se_aplica) {
    passagemCasoForm.value.acessos_dispositivos.ferida_operatoria.local = "";
  }
}

function lidarMudancaCirurgiaNaoRealizada() {
  if (passagemCasoForm.value.cirurgia_nao_realizada) {
    passagemCasoForm.value.procedimento_realizado = "";
  }
}

const listaCamposFaltantes = computed(() => {
  const f = passagemCasoForm.value;
  const erros: string[] = [];

  if (!f.cirurgia_nao_realizada && !f.procedimento_realizado.trim()) {
    erros.push("Procedimento Realizado");
  }

  if (!f.anestesia.trim()) {
    erros.push("Anestesia");
  }

  if (!f.isolamento) {
    erros.push("Isolamento");
  }

  if (f.alergias.opcao !== 'Não' && f.alergias.opcao !== 'Sim') {
    erros.push("Alergias");
  } else if (f.alergias.opcao === 'Sim' && !f.alergias.detalhe.trim()) {
    erros.push("Detalhe da Alergia");
  }

  if (!f.respiratorio.via_aerea) {
    erros.push("Via Aérea");
  } else if (f.respiratorio.via_aerea === 'Outro' && !f.respiratorio.via_aerea_outro_detalhe.trim()) {
    erros.push("Especificação de Outro em Via Aérea");
  }

  if (!f.respiratorio.suporte) {
    erros.push("Suporte Respiratório");
  }

  if (f.cardiovascular.hemodinamica !== 'Estável' && f.cardiovascular.hemodinamica !== 'Instável') {
    erros.push("Hemodinâmica");
  }

  if (f.cardiovascular.drogas_vasoativas.opcao !== 'Não' && f.cardiovascular.drogas_vasoativas.opcao !== 'Sim') {
    erros.push("Opção de Drogas Vasoativas");
  } else if (f.cardiovascular.drogas_vasoativas.opcao === 'Sim' && !f.cardiovascular.drogas_vasoativas.detalhe.trim()) {
    erros.push("Especificação de Drogas Vasoativas");
  }

  if (f.cardiovascular.reposicao_volemica !== 'Não' && f.cardiovascular.reposicao_volemica !== 'Sim') {
    erros.push("Reposição Volêmica");
  }

  if (f.cardiovascular.transfusao.opcao !== 'Não' && f.cardiovascular.transfusao.opcao !== 'Sim') {
    erros.push("Opção de Transfusão");
  } else if (f.cardiovascular.transfusao.opcao === 'Sim' && !f.cardiovascular.transfusao.detalhe.trim()) {
    erros.push("Especificação de Transfusão");
  }

  if (!f.sangramento_balanco.sangramento_estimado) {
    erros.push("Sangramento Estimado");
  } else if (f.sangramento_balanco.sangramento_estimado === 'Importante' && !f.sangramento_balanco.sangramento_volume) {
    erros.push("Volume do Sangramento Estimado");
  }

  if (f.sangramento_balanco.diurese_intraoperatoria.opcao !== 'valor' && f.sangramento_balanco.diurese_intraoperatoria.opcao !== 'Não se aplica') {
    erros.push("Opção de Diurese Intraoperatória");
  } else if (f.sangramento_balanco.diurese_intraoperatoria.opcao === 'valor' && (f.sangramento_balanco.diurese_intraoperatoria.valor === null || String(f.sangramento_balanco.diurese_intraoperatoria.valor).trim() === '')) {
    erros.push("Volume da Diurese");
  }

  const acessosChecked = f.acessos_dispositivos.acessos_venosos.periferico || 
    f.acessos_dispositivos.acessos_venosos.cvc || 
    f.acessos_dispositivos.acessos_venosos.picc || 
    f.acessos_dispositivos.acessos_venosos.outro;

  if (!acessosChecked) {
    erros.push("Acessos Venosos (Selecione pelo menos um)");
  } else {
    if (f.acessos_dispositivos.acessos_venosos.periferico && !f.acessos_dispositivos.acessos_venosos.periferico_local.trim()) {
      erros.push("Local do Acesso Periférico");
    }
    if (f.acessos_dispositivos.acessos_venosos.cvc && !f.acessos_dispositivos.acessos_venosos.cvc_local.trim()) {
      erros.push("Local do Acesso CVC");
    }
    if (f.acessos_dispositivos.acessos_venosos.picc && !f.acessos_dispositivos.acessos_venosos.picc_local.trim()) {
      erros.push("Local do Acesso PICC");
    }
    if (f.acessos_dispositivos.acessos_venosos.outro && !f.acessos_dispositivos.acessos_venosos.outro_detalhe.trim()) {
      erros.push("Especificação de Outro Acesso Venoso");
    }
  }

  if (f.acessos_dispositivos.pai.opcao !== 'Não' && f.acessos_dispositivos.pai.opcao !== 'Sim') {
    erros.push("Opção de PAI");
  } else if (f.acessos_dispositivos.pai.opcao === 'Sim' && !f.acessos_dispositivos.pai.local.trim()) {
    erros.push("Local do PAI");
  }

  if (f.acessos_dispositivos.sonda_vesical.opcao !== 'Não' && f.acessos_dispositivos.sonda_vesical.opcao !== 'Sim') {
    erros.push("Opção de Sonda Vesical");
  } else if (f.acessos_dispositivos.sonda_vesical.opcao === 'Sim' && !f.acessos_dispositivos.sonda_vesical.n_sonda.trim()) {
    erros.push("Nº da Sonda Vesical");
  }

  if (f.acessos_dispositivos.ferida_operatoria.nao_se_aplica === null || f.acessos_dispositivos.ferida_operatoria.nao_se_aplica === undefined) {
    erros.push("Opção de Ferida Operatória");
  } else if (!f.acessos_dispositivos.ferida_operatoria.nao_se_aplica && !f.acessos_dispositivos.ferida_operatoria.local.trim()) {
    erros.push("Local da Ferida Operatória");
  }

  if (f.acessos_dispositivos.drenos.opcao !== 'Não' && f.acessos_dispositivos.drenos.opcao !== 'Sim') {
    erros.push("Opção de Drenos");
  } else if (f.acessos_dispositivos.drenos.opcao === 'Sim' && !f.acessos_dispositivos.drenos.tipo_local.trim()) {
    erros.push("Tipo/local do Dreno");
  }

  if (f.medicamentos.antibiotico.opcao !== 'Não' && f.medicamentos.antibiotico.opcao !== 'Sim') {
    erros.push("Opção de Antibiótico");
  } else if (f.medicamentos.antibiotico.opcao === 'Sim' && !f.medicamentos.antibiotico.detalhe.trim()) {
    erros.push("Qual/horário do Antibiótico");
  }

  const hasIntercorrencia = f.intercorrencias.nao_houve || 
    f.intercorrencias.hipotensao || 
    f.intercorrencias.hipertensao || 
    f.intercorrencias.arritmia || 
    f.intercorrencias.dessaturacao || 
    f.intercorrencias.broncoespasmo || 
    f.intercorrencias.sangramento_importante || 
    f.intercorrencias.reacao_medicamentosa || 
    f.intercorrencias.parada_cardiorespiratoria || 
    f.intercorrencias.dificil_via_aerea || 
    f.intercorrencias.outro;

  if (!hasIntercorrencia) {
    erros.push("Intercorrências (marque 'Não houve' ou pelo menos uma ocorrência)");
  } else if (f.intercorrencias.outro && !f.intercorrencias.outro_detalhe.trim()) {
    erros.push("Descrição do Outro em Intercorrências");
  }

  if (!f.profissional_responsavel.trim()) {
    erros.push("Profissional Responsável");
  }

  return erros;
});

const formPassagemCasoValido = computed(() => {
  return listaCamposFaltantes.value.length === 0;
});

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

    // Nível 2: Prioridade (P1 < P2 < P3...)
    const getPrioridadeValor = (p: string | undefined) => {
      if (!p || !p.startsWith('P')) return 999;
      const num = parseInt(p.substring(1));
      return isNaN(num) ? 999 : num;
    };
    const prioA = getPrioridadeValor(a.prioridade);
    const prioB = getPrioridadeValor(b.prioridade);
    if (prioA !== prioB) return prioA - prioB;

    // Nível 4: Horário de Início da Cirurgia (crescente)
    const horaA = a.hora_cirurgia || '99:99';
    const horaB = b.hora_cirurgia || '99:99';
    if (horaA !== horaB) return horaA.localeCompare(horaB);

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
    const { data } = await api.get(`/api/leitos/disponiveis?incluir_reservados=${isRemanejamento.value}`);
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
  if (isEditing.value && solSelecionada.value && String(formNova.value.prontuario) !== String(solSelecionada.value.prontuario)) {
    showModalConfirmacaoTrocaProntuario.value = true;
    return;
  }

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
  } catch (error: any) {
    console.error('Erro ao salvar:', error);
    toast.error(error.response?.data?.detail || 'Erro ao salvar solicitação.');
  } finally {
    submetendoNova.value = false;
  }
}

async function confirmarSalvarEdicao(cancelarAntiga: boolean) {
  showModalConfirmacaoTrocaProntuario.value = false;
  submetendoNova.value = true;
  try {
    if (solSelecionada.value) {
      const payload = {
        ...formNova.value,
        cancelar_antiga: cancelarAntiga
      };
      await api.patch(`/api/solicitacoes/${solSelecionada.value.id}`, payload);
      toast.success('Solicitação atualizada e paciente alterado!');
      fecharModalNova();
      carregarSolicitacoes();
    }
  } catch (error: any) {
    console.error('Erro ao salvar edição com troca de paciente:', error);
    toast.error(error.response?.data?.detail || 'Erro ao atualizar solicitação.');
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

function abrirModalPassagemCaso(sol: any) {
  solSelecionada.value = sol;
  idSolicitacaoFinalizacao.value = sol.id;
  modoEdicaoPassagem.value = false;
  
  if (sol.passagem_caso) {
    let parsed = sol.passagem_caso;
    if (typeof parsed === 'string') {
      try {
        parsed = JSON.parse(parsed);
      } catch (e) {
        console.error("Erro ao fazer parse da passagem de caso:", e);
      }
    }
    
    if (parsed && typeof parsed === 'object') {
      // Faz o merge com os valores padrão para garantir reatividade total
      const form = Object.assign(criarFormPassagemCasoPadrao(), JSON.parse(JSON.stringify(parsed)));
      
      // Converte dados respiratórios legados (objetos com booleans) para o novo formato flat string
      if (parsed.respiratorio) {
        if (typeof parsed.respiratorio.via_aerea === 'object' && parsed.respiratorio.via_aerea !== null) {
          const va = parsed.respiratorio.via_aerea;
          if (va.espontanea) form.respiratorio.via_aerea = "Espontânea";
          else if (va.tot) form.respiratorio.via_aerea = "TOT";
          else if (va.traqueostomia) form.respiratorio.via_aerea = "Traqueostomia";
          else if (va.outro) {
            form.respiratorio.via_aerea = "Outro";
            form.respiratorio.via_aerea_outro_detalhe = va.outro_detalhe || "";
          }
        }
        if (typeof parsed.respiratorio.suporte === 'object' && parsed.respiratorio.suporte !== null) {
          const sup = parsed.respiratorio.suporte;
          if (sup.ar_ambiente) form.respiratorio.suporte = "Ar ambiente";
          else if (sup.o2_cateter) form.respiratorio.suporte = "O2 cateter";
          else if (sup.mascara) form.respiratorio.suporte = "Máscara";
          else if (sup.ventilacao_mecanica) form.respiratorio.suporte = "Ventilação mecânica";
        }
      }
      
      passagemCasoForm.value = form;
      modoEdicaoPassagem.value = true;
      showModalPassagemCaso.value = true;
      return;
    }
  }
  
  passagemCasoForm.value = criarFormPassagemCasoPadrao();
  if (sol.procedimento) {
    passagemCasoForm.value.procedimento_realizado = sol.procedimento;
  }
  showModalPassagemCaso.value = true;
}

function fecharModalPassagemCaso() {
  showModalPassagemCaso.value = false;
  idSolicitacaoFinalizacao.value = "";
  modoEdicaoPassagem.value = false;
  passagemCasoForm.value = criarFormPassagemCasoPadrao();
}

async function confirmarFinalizarComPassagem() {
  await executarConfirmarCirurgiaFinalizada(idSolicitacaoFinalizacao.value, passagemCasoForm.value);
}

async function salvarEdicaoPassagemCaso() {
  submetendo.value = true;
  try {
    const id = idSolicitacaoFinalizacao.value;
    await api.put(`/api/solicitacoes/${id}/passagem-caso`, { passagem_caso: passagemCasoForm.value });
    toast.success('Passagem de caso atualizada com sucesso.');
    fecharModalPassagemCaso();
    await carregarSolicitacoes();
  } catch (error: any) {
    console.error('Erro ao editar passagem de caso:', error);
    toast.error(error.response?.data?.detail || 'Não foi possível atualizar passagem de caso.');
  } finally {
    submetendo.value = false;
  }
}

async function executarConfirmarCirurgiaFinalizada(id: string, passagem: any) {
  submetendo.value = true;
  try {
    const payload = { passagem_caso: passagem };
    await api.post(`/api/solicitacoes/${id}/cirurgia-finalizada`, payload);
    toast.success('Cirurgia sinalizada como finalizada.');
    await carregarSolicitacoes();
    fecharModalPassagemCaso();
  } catch (error: any) {
    console.error('Erro ao marcar cirurgia finalizada:', error);
    toast.error(error.response?.data?.detail || 'Não foi possível marcar cirurgia como finalizada.');
  } finally {
    submetendo.value = false;
  }
}

let solicitacoesIntervalId: any = null;

onMounted(() => {
  carregarSolicitacoes();
  solicitacoesIntervalId = setInterval(carregarSolicitacoes, 120000);
});

onUnmounted(() => {
  if (solicitacoesIntervalId) {
    clearInterval(solicitacoesIntervalId);
  }
});
</script>
