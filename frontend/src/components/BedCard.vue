<template>
  <article
    class="relative rounded-2xl border p-5 transition-all duration-300 hover:-translate-y-1.5 hover:shadow-xl backdrop-blur-sm"
    :class="[
      temConflito ? 'border-red-500 ring-4 ring-red-500/10 shadow-red-100 bg-white/90' : 
      (sinalizacaoTransferencia ? 'border-rose-200 ring-4 ring-rose-500/5 shadow-rose-100 bg-white/90' : 
      bloqueadoClinico ? 'border-indigo-400 bg-indigo-50/40 ring-4 ring-indigo-500/10 shadow-indigo-100' :
      (proximoPaciente && cirurgiaFinalizada && !encaminhamentoLiberado) ? 
        (authStore.isUTI ? 'animate-pulse-warning border-amber-300' : 'border-amber-300 bg-amber-50/60 ring-4 ring-amber-400/10 shadow-amber-100') :
      (proximoPaciente && encaminhamentoLiberado) ? 'border-emerald-300 bg-emerald-50/60 ring-4 ring-emerald-400/10 shadow-emerald-100' :
      'border-slate-200 shadow-slate-100/50 bg-white/90')
    ]"
  >
    <!-- Icone de Alerta (Conflito ou Transferencia) -->
    <div
      v-if="temConflito || sinalizacaoTransferencia"
      class="absolute -top-2 -right-2 rounded-full p-2 shadow"
      :class="temConflito ? 'bg-red-600 text-white' : 'bg-rose-100 text-rose-600'"
      :title="temConflito ? 'Conflito de reserva' : 'Alta solicitada'"
    >
      <ExclamationTriangleIcon v-if="temConflito" class="h-4 w-4" />
      <ClockIcon v-else class="h-4 w-4" />
    </div>

    <div class="flex items-start justify-between gap-3">
      <div class="space-y-2">
        <div>
          <p class="text-xs font-semibold uppercase tracking-widest text-slate-500">Leito</p>
          <h3 class="text-2xl font-bold text-slate-900">Leito {{ leitoNumero }}</h3>
        </div>
        <UiBadge :class="['border-transparent text-white', tipoClass]">
          {{ tipoConfig.label }}
        </UiBadge>
      </div>

      <div class="flex flex-col items-end gap-1.5 shrink-0">
        <StatusBadge :status="bloqueadoClinico ? 'reservado' : status" />
      </div>
    </div>

    <!-- Tag de Destino Definido (NIR) -->
    <div 
      v-if="destinoDefinido"
      class="mt-3 inline-flex items-center gap-1 rounded-full px-3 py-1 text-[10px] font-bold leading-none border shadow-sm transition-all duration-500 whitespace-normal break-words max-w-full w-fit"
      :class="destinoDisponivel 
        ? 'bg-emerald-100 text-emerald-700 border-emerald-200' 
        : 'bg-amber-100 text-amber-700 border-amber-200'"
    >
      <MapPinIcon class="h-3 w-3 shrink-0" :class="destinoDisponivel ? 'text-emerald-600' : 'text-amber-600'" />
      <span>Destino Definido: {{ destinoDefinido }}{{ destinoDisponivel ? ' Disponível' : '' }}</span>
    </div>

    <div class="mt-4 space-y-4 text-sm text-slate-700">
      <div v-if="pacienteAtual" class="space-y-1 border-l-4 border-blue-500 pl-4 bg-blue-50/30 py-1 rounded-r-lg">
        <p class="text-xs font-semibold uppercase tracking-widest text-slate-500">Paciente Atual</p>
        <p class="text-base font-bold text-slate-900">Prontuário: {{ pacienteAtual.prontuario }}</p>
        <p v-if="pacienteAtual.nome" class="text-xs font-semibold text-slate-500 leading-none my-1">
          {{ pacienteAtual.nome }}
        </p>
        <p class="text-slate-600">
          {{ pacienteAtual.idade }} anos
          <span v-if="pacienteAtual.dataNascimento" class="text-xs text-slate-500">
            ({{ formatarNascimento(pacienteAtual.dataNascimento) }})
          </span>
          - {{ pacienteAtual.especialidade }}
        </p>
      </div>

      <div v-if="bloqueadoClinico" class="space-y-1 border-l-4 border-indigo-500 pl-4 bg-indigo-50/30 py-2 rounded-r-lg animate-fade-in">
        <p class="text-xs font-semibold uppercase tracking-widest text-slate-500">Reserva Preventiva</p>
        <p class="text-base font-bold text-indigo-900">Clínico/COB/HEM</p>
        <p class="text-xs text-slate-600">Leito reservado preventivamente pela UTI.</p>
      </div>

      <div v-else-if="proximoPaciente" class="space-y-1 border-l-4 border-emerald-500 pl-4 bg-emerald-50/30 py-1 rounded-r-lg">
        <p class="text-xs font-semibold uppercase tracking-widest text-slate-500">Próximo Paciente</p>
        <p class="text-base font-bold text-slate-900">Prontuário: {{ proximoPaciente.prontuario }}</p>
        <p v-if="proximoPaciente.nome" class="text-xs font-semibold text-slate-500 leading-none my-1">
          {{ proximoPaciente.nome }}
        </p>
        <p class="text-slate-600">{{ proximoPaciente.idade }} anos - {{ proximoPaciente.especialidade }}</p>
        
        <!-- Detalhes da Cirurgia -->
        <div v-if="proximoPaciente.dataCirurgia" class="mt-2 flex flex-wrap gap-2">
          <div class="flex items-center gap-1 rounded bg-slate-100 px-1.5 py-0.5 text-[11px] font-medium text-slate-600 border border-slate-200">
            Cirurgia: {{ formatarDataHoraCirurgia(proximoPaciente.dataCirurgia, proximoPaciente.horaCirurgia) }}
          </div>
          <div v-if="proximoPaciente.turno" class="flex items-center gap-1 rounded bg-blue-50 px-1.5 py-0.5 text-[11px] font-medium text-blue-600 border border-blue-100 uppercase">
            Turno: {{ proximoPaciente.turno }}
          </div>
        </div>
        <div v-if="cirurgiaFinalizada && !encaminhamentoLiberado" class="mt-2 flex flex-wrap items-center gap-1.5 text-[11px] font-bold text-amber-700">
          <span class="inline-block h-2 w-2 rounded-full bg-amber-500 animate-pulse"></span>
          Cirurgia Concluída
          <span v-if="proximoPaciente?.horaCirurgiaFinalizada" class="flex items-center gap-0.5 rounded-full bg-amber-100 px-2 py-0.5 font-medium text-amber-800 border border-amber-200">
            <ClockIcon class="h-3.5 w-3.5 text-amber-600 shrink-0" />
            {{ obterTempoDecorrido(proximoPaciente.horaCirurgiaFinalizada) }}
          </span>
        </div>
        <div v-else-if="encaminhamentoLiberado" class="mt-2 flex flex-wrap items-center gap-1.5 text-[11px] font-bold text-emerald-700">
          <span class="inline-block h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
          Encaminhamento Liberado
        </div>
        <UiBadge
          v-if="tipoReserva"
          variant="outline"
          class="border-emerald-200 bg-emerald-50 text-emerald-700"
        >
          {{ tipoReserva }}
        </UiBadge>
      </div>

      <p v-else-if="!bloqueadoClinico" class="pl-4 text-slate-500">Sem reserva</p>
      
      <!-- Alerta de Conflito -->
      <div v-if="temConflito" class="mt-2 rounded-lg bg-red-50 p-3 border border-red-200">
        <div class="flex items-start gap-2">
          <ExclamationTriangleIcon class="h-5 w-5 text-red-600 shrink-0" />
          <div>
            <p class="text-xs font-bold text-red-700 uppercase">Conflito detectado</p>
            <p class="text-[11px] leading-tight text-red-600 mt-0.5">
              Leito ocupado por outro paciente no AGHU. Verifique a reserva.
            </p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="authStore.isAdmin || authStore.isUTI" class="mt-5 flex flex-wrap gap-2">
      <button
        v-if="status === 'ocupado'"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-700 transition hover:bg-slate-50"
        @click="$emit('solicitar-alta')"
      >
        Solicitar Alta
      </button>
      <button
        v-if="status === 'alta'"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs font-semibold text-red-700 transition hover:bg-red-100"
        @click="$emit('cancelar-alta')"
      >
        Cancelar Alta
      </button>
      <button
        v-if="['disponivel', 'higienizacao', 'alta'].includes(status) && !proximoPaciente && !bloqueadoClinico"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-indigo-200 bg-indigo-50 px-3 py-2 text-xs font-semibold text-indigo-700 transition hover:bg-indigo-100"
        @click="emit('reservar-clinico')"
      >
        Reservar Clínico/COB/HEM
      </button>
      <button
        v-if="bloqueadoClinico"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-700 transition hover:bg-slate-50"
        @click="emit('cancelar-reserva-clinica')"
      >
        Cancelar Reserva
      </button>
      <button
        v-if="proximoPaciente && cirurgiaFinalizada && !encaminhamentoLiberado"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-amber-200 bg-amber-500 px-3 py-2 text-xs font-bold text-white transition hover:bg-amber-600 shadow-sm"
        @click="handleCliqueLiberar"
      >
        Liberar Encaminhamento
      </button>
      <button
        v-if="proximoPaciente && encaminhamentoLiberado"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-red-200 bg-red-600 px-3 py-2 text-xs font-bold text-white transition hover:bg-red-700 shadow-sm"
        @click="emit('cancelar-liberacao', solicitacaoId!)"
      >
        Cancelar Liberação
      </button>
      <!-- Botão permanente Ver Passagem de Caso se houver passagem cadastrada -->
      <button
        v-if="props.passagemCaso"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-xs font-semibold text-slate-700 transition hover:bg-slate-100"
        @click="showModalHandover = true"
      >
        Ver Passagem
      </button>

      <button
        v-if="proximoPaciente || bloqueadoClinico"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-blue-200 bg-blue-50 px-3 py-2 text-xs font-semibold text-blue-700 transition hover:bg-blue-100"
        @click="emit('mudar-leito', props.solicitacaoId || 0, props.leitoNumero)"
      >
        Mudar Leito
      </button>
      <button
        v-if="proximoPaciente"
        class="inline-flex flex-1 items-center justify-center rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-700 transition hover:bg-slate-50"
        @click="$emit('cancelar-reserva')"
      >
        Cancelar Reserva
      </button>
    </div>

    <!-- Modal de Checkpoint de Passagem de Caso (UTI) -->
    <Modal :show="showModalHandover" @close="showModalHandover = false" size="lg">
      <template #header>Passagem de Caso - Prontuário {{ proximoPaciente?.prontuario }}</template>
      <div class="space-y-4 text-left p-1 max-h-[70vh] overflow-y-auto">
        <p class="text-sm text-slate-600">
          Atenção! Informações clínicas de passagem de caso fornecidas pelo Bloco Cirúrgico:
        </p>
        
        <div v-if="parsedPassagemCaso" class="space-y-4">
          <!-- Se for objeto estruturado (Formulário) -->
          <div v-if="typeof parsedPassagemCaso === 'object' && parsedPassagemCaso !== null" class="space-y-4 text-xs">
            
             <!-- Identificação e Alergias -->
             <div class="grid grid-cols-2 gap-2 border-b pb-2">
               <div><strong>Procedimento:</strong> {{ parsedPassagemCaso.cirurgia_nao_realizada ? 'CIRURGIA NÃO REALIZADA' : parsedPassagemCaso.procedimento_realizado }}</div>
               <div><strong>Anestesia:</strong> {{ parsedPassagemCaso.anestesia || 'Não informada' }}</div>
                <div class="col-span-2 flex flex-wrap gap-x-4">
                  <div><strong>Alergias:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.alergias?.opcao }} {{ ['SIM', 'Sim'].includes(parsedPassagemCaso.alergias?.opcao) ? `- ${parsedPassagemCaso.alergias?.detalhe}` : '' }}</span></div>
                  <div><strong>Isolamento:</strong> <span class="text-slate-600 font-bold" :class="parsedPassagemCaso.isolamento !== 'Não' ? 'text-red-600' : 'text-slate-600'">{{ parsedPassagemCaso.isolamento || 'Não' }}</span></div>
                </div>
             </div>
 
             <!-- Respiratório -->
             <div class="border-b pb-2">
               <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Respiratório</h4>
               <div class="grid grid-cols-2 gap-2">
                 <div>
                   <strong>Via aérea:</strong> <span class="text-slate-600">{{ typeof parsedPassagemCaso.respiratorio?.via_aerea === 'object' ? [parsedPassagemCaso.respiratorio?.via_aerea?.espontanea ? 'Espontânea' : '', parsedPassagemCaso.respiratorio?.via_aerea?.tot ? 'TOT' : '', parsedPassagemCaso.respiratorio?.via_aerea?.traqueostomia ? 'Traqueostomia' : '', parsedPassagemCaso.respiratorio?.via_aerea?.outro ? `Outro (${parsedPassagemCaso.respiratorio?.via_aerea?.outro_detalhe})` : ''].filter(Boolean).join(', ') : (parsedPassagemCaso.respiratorio?.via_aerea === 'Outro' ? `Outro (${parsedPassagemCaso.respiratorio?.via_aerea_outro_detalhe})` : parsedPassagemCaso.respiratorio?.via_aerea) }}</span>
                 </div>
                 <div>
                   <strong>Suporte:</strong> <span class="text-slate-600">{{ typeof parsedPassagemCaso.respiratorio?.suporte === 'object' ? [parsedPassagemCaso.respiratorio?.suporte?.ar_ambiente ? 'Ar ambiente' : '', parsedPassagemCaso.respiratorio?.suporte?.o2_cateter ? 'O₂ cateter' : '', parsedPassagemCaso.respiratorio?.suporte?.mascara ? 'Máscara' : '', parsedPassagemCaso.respiratorio?.suporte?.ventilacao_mecanica ? 'Ventilação mecânica' : ''].filter(Boolean).join(', ') : parsedPassagemCaso.respiratorio?.suporte }}</span>
                 </div>
               </div>
             </div>
 
             <!-- Cardiovascular -->
             <div class="border-b pb-2">
               <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Cardiovascular</h4>
               <div class="grid grid-cols-2 gap-2">
                 <div><strong>Hemodinâmica:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.cardiovascular?.hemodinamica }}</span></div>
                 <div>
                   <strong>Drogas vasoativas:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.cardiovascular?.drogas_vasoativas?.opcao }} {{ parsedPassagemCaso.cardiovascular?.drogas_vasoativas?.opcao === 'Sim' ? `- ${parsedPassagemCaso.cardiovascular?.drogas_vasoativas?.detalhe}` : '' }}</span>
                 </div>
                 <div><strong>Reposição volêmica:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.cardiovascular?.reposicao_volemica }}</span></div>
                 <div>
                   <strong>Transfusão:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.cardiovascular?.transfusao?.opcao }} {{ parsedPassagemCaso.cardiovascular?.transfusao?.opcao === 'Sim' ? `- ${parsedPassagemCaso.cardiovascular?.transfusao?.detalhe}` : '' }}</span>
                 </div>
               </div>
             </div>
 
             <!-- Sangramento e Balanço -->
             <div class="border-b pb-2">
               <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Sangramento e Balanço</h4>
               <div class="grid grid-cols-2 gap-2">
                 <div>
                   <strong>Sangramento estimado:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.sangramento_balanco?.sangramento_estimado }} {{ parsedPassagemCaso.sangramento_balanco?.sangramento_estimado === 'Importante' ? `- ${parsedPassagemCaso.sangramento_balanco?.sangramento_volume} mL` : '' }}</span>
                 </div>
                 <div>
                   <strong>Diurese intraoperatória:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.sangramento_balanco?.diurese_intraoperatoria?.opcao === 'valor' ? `${parsedPassagemCaso.sangramento_balanco?.diurese_intraoperatoria?.valor} mL` : 'Não se aplica' }}</span>
                 </div>
               </div>
             </div>
 
             <!-- Acessos, Dispositivos e Feridas -->
             <div class="border-b pb-2">
               <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Acessos, Dispositivos e Feridas</h4>
               <div class="grid grid-cols-2 gap-2">
                 <div>
                   <strong>Acessos venosos:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.nao_se_aplica ? 'Não se aplica' : [parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.periferico ? `Periférico (${parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.periferico_local}${parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.periferico_data ? ' - Criação: ' + parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.periferico_data.split('-').reverse().join('/') : ''})` : '', parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.cvc ? `CVC (${parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.cvc_local}${parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.cvc_data ? ' - Criação: ' + parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.cvc_data.split('-').reverse().join('/') : ''})` : '', parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.picc ? `PICC (${parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.picc_local}${parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.picc_data ? ' - Criação: ' + parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.picc_data.split('-').reverse().join('/') : ''})` : '', parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.outro ? `Outro (${parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.outro_detalhe}${parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.outro_data ? ' - Criação: ' + parsedPassagemCaso.acessos_dispositivos?.acessos_venosos?.outro_data.split('-').reverse().join('/') : ''})` : ''].filter(Boolean).join(', ') }}</span>
                 </div>
                 <div>
                   <strong>PAI:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.acessos_dispositivos?.pai?.opcao }} {{ parsedPassagemCaso.acessos_dispositivos?.pai?.opcao === 'Sim' ? `- ${parsedPassagemCaso.acessos_dispositivos?.pai?.local}` : '' }}</span>
                 </div>
                 <div>
                   <strong>Sonda vesical:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.acessos_dispositivos?.sonda_vesical?.opcao }} {{ parsedPassagemCaso.acessos_dispositivos?.sonda_vesical?.opcao === 'Sim' ? `- Nº ${parsedPassagemCaso.acessos_dispositivos?.sonda_vesical?.n_sonda}` : '' }}</span>
                 </div>
                 <div>
                   <strong>Ferida operatória:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.acessos_dispositivos?.ferida_operatoria?.nao_se_aplica ? 'Não' : parsedPassagemCaso.acessos_dispositivos?.ferida_operatoria?.local }}</span>
                 </div>
                 <div>
                   <strong>Drenos:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.acessos_dispositivos?.drenos?.opcao }} {{ parsedPassagemCaso.acessos_dispositivos?.drenos?.opcao === 'Sim' ? `- ${parsedPassagemCaso.acessos_dispositivos?.drenos?.tipo_local}` : '' }}</span>
                 </div>
                 <div>
                   <strong>Outros dispositivos:</strong> <span class="text-slate-600">{{ [parsedPassagemCaso.acessos_dispositivos?.outros?.sng_sne ? 'SNG/SNE' : '', parsedPassagemCaso.acessos_dispositivos?.outros?.ostomia ? 'Ostomia' : '', parsedPassagemCaso.acessos_dispositivos?.outros?.outro ? `Outro (${parsedPassagemCaso.acessos_dispositivos?.outros?.outro_detalhe})` : ''].filter(Boolean).join(', ') || 'Nenhum' }}</span>
                 </div>
               </div>
             </div>
 
             <!-- Medicamentos -->
             <div class="border-b pb-2">
               <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Medicamentos</h4>
               <div class="grid grid-cols-2 gap-2">
                 <div>
                   <strong>Antibiótico:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.medicamentos?.antibiotico?.opcao }} {{ parsedPassagemCaso.medicamentos?.antibiotico?.opcao === 'Sim' ? `- ${parsedPassagemCaso.medicamentos?.antibiotico?.detalhe}` : '' }}</span>
                 </div>
                 <div><strong>Outras medicações:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.medicamentos?.outras_medicacoes || 'Nenhuma' }}</span></div>
               </div>
             </div>
 
             <!-- Intercorrências -->
             <div class="border-b pb-2">
               <h4 class="font-bold text-slate-800 uppercase text-[10px] tracking-wider mb-1">Intercorrências no ato</h4>
               <div class="space-y-1">
                 <div>
                   <strong>Intercorrências:</strong> <span class="text-slate-600">{{ parsedPassagemCaso.intercorrencias?.nao_houve ? 'Não houve' : [parsedPassagemCaso.intercorrencias?.hipotensao ? 'Hipotensão' : '', parsedPassagemCaso.intercorrencias?.hipertensao ? 'Hipertensão' : '', parsedPassagemCaso.intercorrencias?.arritmia ? 'Arritmia' : '', parsedPassagemCaso.intercorrencias?.dessaturacao ? 'Dessaturação' : '', parsedPassagemCaso.intercorrencias?.broncoespasmo ? 'Broncoespasmo' : '', parsedPassagemCaso.intercorrencias?.sangramento_importante ? 'Sangramento importante' : '', parsedPassagemCaso.intercorrencias?.reacao_medicamentosa ? 'Reação medicamentosa' : '', parsedPassagemCaso.intercorrencias?.parada_cardiorespiratoria ? 'Parada cardiorrespiratória' : '', parsedPassagemCaso.intercorrencias?.dificil_via_aerea ? 'Difícil via aérea' : '', parsedPassagemCaso.intercorrencias?.outro ? `Outro (${parsedPassagemCaso.intercorrencias?.outro_detalhe})` : ''].filter(Boolean).join(', ') }}</span>
                 </div>
                 <div v-if="parsedPassagemCaso.intercorrencias?.descricao_conduta">
                   <strong>Descrição/Conduta:</strong>
                   <span class="text-slate-600 block bg-slate-50 p-2 rounded mt-1 whitespace-pre-wrap">{{ parsedPassagemCaso.intercorrencias?.descricao_conduta }}</span>
                 </div>
               </div>
             </div>

            <!-- Responsável -->
            <div class="pt-1">
              <strong>Profissional Responsável pela Passagem:</strong>
              <span class="text-slate-700 font-semibold block text-sm mt-1 bg-blue-50/50 p-2 rounded border border-blue-100/50">{{ parsedPassagemCaso.profissional_responsavel }}</span>
            </div>

          </div>
          
          <!-- Se for string pura legada -->
          <div v-else class="rounded-xl border border-amber-100 bg-amber-50/50 p-4 text-sm text-amber-900 font-medium whitespace-pre-wrap">
            {{ parsedPassagemCaso }}
          </div>
        </div>
      </div>
      <template #footer>
        <button
          class="rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 cursor-pointer"
          @click="showModalHandover = false"
        >
          {{ props.encaminhamentoLiberado ? 'Fechar' : 'Cancelar' }}
        </button>
        <button
          v-if="!props.encaminhamentoLiberado"
          class="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-bold text-white transition hover:bg-emerald-700 cursor-pointer"
          @click="confirmarLiberacao"
        >
          Ciente e Liberar Transporte
        </button>
      </template>
    </Modal>
  </article>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { ExclamationTriangleIcon, ClockIcon, MapPinIcon } from '@heroicons/vue/24/outline';
import StatusBadge from './StatusBadge.vue';
import UiBadge from './ui/Badge.vue';
import Modal from './Modal.vue';

type BedStatus = 'disponivel' | 'ocupado' | 'higienizacao' | 'desativado' | 'alta' | 'reservado';
type BedType = 'cirurgico' | 'hem' | 'obstetrico' | 'uti' | 'outro' | 'nao_definido';

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

const props = defineProps<{
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
  showActions?: boolean;
  cirurgiaFinalizada?: boolean;
  encaminhamentoLiberado?: boolean;
  solicitacaoId?: number;
  bloqueadoClinico?: boolean;
  passagemCaso?: string;
}>();

const authStore = useAuthStore();

const showModalHandover = ref(false);

const parsedPassagemCaso = computed(() => {
  if (!props.passagemCaso) return null;
  if (typeof props.passagemCaso === 'object') return props.passagemCaso;
  try {
    return JSON.parse(props.passagemCaso);
  } catch (e) {
    return props.passagemCaso;
  }
});

const handleCliqueLiberar = () => {
  if (props.passagemCaso) {
    showModalHandover.value = true;
  } else {
    emit('liberar-encaminhamento', props.solicitacaoId!);
  }
};

const confirmarLiberacao = () => {
  showModalHandover.value = false;
  emit('liberar-encaminhamento', props.solicitacaoId!, parsedPassagemCaso.value);
};

const emit = defineEmits<{
  'solicitar-alta': [];
  'cancelar-alta': [];
  'cancelar-reserva': [];
  'reservar-clinico': [];
  'cancelar-reserva-clinica': [];
  'liberar-encaminhamento': [solicitacaoId: number, passagemCasoAvaliada?: any];
  'cancelar-liberacao': [solicitacaoId: number];
  'mudar-leito': [solicitacaoId: number, leitoNumero: string];
}>();

const tipoPalette: Record<BedType, { label: string; className: string }> = {
  cirurgico: { label: 'Cirúrgico', className: 'bg-blue-600/80' },
  hem: { label: 'HEM', className: 'bg-rose-600/80' },
  obstetrico: { label: 'Obstétrico', className: 'bg-purple-600/80' },
  uti: { label: 'UTI', className: 'bg-indigo-600/80' },
  outro: { label: 'Outro', className: 'bg-slate-700/80' },
  nao_definido: { label: 'Não definido', className: 'bg-slate-400/90' },
};

const tipoConfig = computed(() => tipoPalette[props.tipo] || tipoPalette.outro);
const tipoClass = computed(() => tipoConfig.value.className);

const formatarDataHoraCirurgia = (dataStr?: string, horaStr?: string) => {
  if (!dataStr) return '';
  const dataFormatada = dataStr.includes('-') ? dataStr.split('-').reverse().join('/') : dataStr;
  return horaStr ? `${dataFormatada} - ${horaStr}` : dataFormatada;
};

const formatarNascimento = (dataStr?: string) => {
  if (!dataStr) return '';
  const dataApenas = dataStr.split('T')[0];
  if (dataApenas.includes('-')) {
    const parts = dataApenas.split('-');
    if (parts.length === 3) {
      if (parts[0].length === 4) {
        return `${parts[2]}/${parts[1]}/${parts[0]}`;
      } else {
        return `${parts[0]}/${parts[1]}/${parts[2]}`;
      }
    }
  }
  return dataApenas;
};

const currentTime = ref(new Date());
let timerId: any = null;

onMounted(() => {
  timerId = setInterval(() => {
    currentTime.value = new Date();
  }, 60000);
});

onUnmounted(() => {
  if (timerId) clearInterval(timerId);
});

const obterTempoDecorrido = (dataIso?: string) => {
  if (!dataIso) return '';
  const dateFim = new Date(dataIso);
  const diffMs = currentTime.value.getTime() - dateFim.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  if (diffMins < 0) return '0m';
  if (diffMins < 60) return `${diffMins}m`;
  const horas = Math.floor(diffMins / 60);
  const mins = diffMins % 60;
  return `${horas}h ${mins}m`;
};
</script>
