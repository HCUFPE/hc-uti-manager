<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="px-6 py-4 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
        <div>
          <h2 class="text-lg font-bold text-slate-800">Gestão de Perfis de Acesso</h2>
          <p class="text-sm text-slate-500">Defina o perfil de acesso para cada usuário</p>
        </div>
        <button 
          @click="abrirModalNovo"
          class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition"
        >
          <PlusIcon class="h-4 w-4" />
          Novo Usuário
        </button>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="text-xs uppercase tracking-wider text-slate-400 bg-slate-50 border-b border-slate-200">
              <th class="px-6 py-3 font-semibold">Usuário (Nome/Login)</th>
              <th class="px-6 py-3 font-semibold">Lotação</th>
              <th class="px-6 py-3 font-semibold">E-mail</th>
              <th class="px-6 py-3 font-semibold">Perfil Atribuído</th>
              <th class="px-6 py-3 font-semibold text-right">Ações</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-if="loading" class="animate-pulse">
              <td colspan="5" class="px-6 py-8 text-center text-slate-400">Carregando perfis...</td>
            </tr>
            <tr v-else v-for="item in perfis" :key="item.username" class="hover:bg-slate-50 transition">
              <td class="px-6 py-4">
                <div class="font-semibold text-slate-800">{{ item.nome_completo || 'Sem Nome' }}</div>
                <div class="text-xs text-slate-400">{{ item.username }}</div>
              </td>
              <td class="px-6 py-4 text-sm text-slate-600">{{ item.lotacao || 'N/D' }}</td>
              <td class="px-6 py-4 text-sm text-slate-500">{{ item.email || 'N/D' }}</td>
              <td class="px-6 py-4">
                <span 
                  class="px-2.5 py-1 rounded-full text-xs font-bold border"
                  :class="getRoleStyle(item.perfil)"
                >
                  {{ item.perfil }}
                </span>
              </td>
              <td class="px-6 py-4 text-right flex justify-end gap-2">
                <button 
                  v-if="authStore.canManageUser(item.perfil)"
                  @click="abrirModalEdicao(item)"
                  class="text-blue-600 hover:text-blue-800 p-2 hover:bg-blue-50 rounded-lg transition"
                  title="Editar perfil"
                >
                  <PencilSquareIcon class="h-4 w-4" />
                </button>
                <button 
                  v-if="authStore.canManageUser(item.perfil)"
                  @click="removerPerfil(item.username)"
                  class="text-rose-600 hover:text-rose-800 p-2 hover:bg-rose-50 rounded-lg transition"
                  title="Remover perfil customizado"
                >
                  <TrashIcon class="h-4 w-4" />
                </button>
              </td>
            </tr>
            <tr v-if="!loading && perfis.length === 0">
              <td colspan="5" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center gap-2 text-slate-400">
                  <ShieldExclamationIcon class="h-12 w-12 opacity-20" />
                  <p>Nenhum perfil customizado cadastrado.</p>
                  <p class="text-xs">Todos os demais usuários entram como "Comum".</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Adicionar/Editar -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
      <div class="bg-white rounded-2xl shadow-xl border border-slate-200 w-full max-w-md overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-200 flex justify-between items-center bg-slate-50">
          <h3 class="font-bold text-slate-800">{{ isEditing ? 'Editar Perfil' : 'Atribuir Perfil' }}</h3>
          <button @click="showAddModal = false" class="text-slate-400 hover:text-slate-600">
            <XMarkIcon class="h-5 w-5" />
          </button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Login da Rede (AD)</label>
            <div class="relative">
              <input 
                v-model="form.username"
                type="text" 
                placeholder="ex: daniel.turmina"
                :disabled="isEditing"
                class="w-full rounded-lg border border-slate-200 px-4 py-2.5 text-sm focus:border-blue-500 focus:ring-4 focus:ring-blue-100 outline-none transition disabled:bg-slate-100 disabled:text-slate-500"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Perfil de Acesso</label>
            <select 
              v-model="form.perfil"
              class="w-full rounded-lg border border-slate-200 px-4 py-2.5 text-sm focus:border-blue-500 focus:ring-4 focus:ring-blue-100 outline-none transition bg-white"
            >
              <option v-for="p in availableProfiles" :key="p" :value="p">{{ p }}</option>
            </select>
          </div>
        </div>
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-200 flex justify-end gap-3">
          <button 
            @click="showAddModal = false"
            class="px-4 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition"
          >
            Cancelar
          </button>
          <button 
            @click="salvar"
            :disabled="submitting || !form.username"
            class="px-6 py-2 text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg shadow-sm transition"
          >
            {{ submitting ? 'Salvando...' : 'Salvar Usuário' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { PlusIcon, TrashIcon, XMarkIcon, ShieldExclamationIcon, PencilSquareIcon } from '@heroicons/vue/24/outline';
import api from '../services/api';
import { useToast } from 'vue-toastification';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const availableProfiles = computed(() => authStore.getAssignableProfiles());

const toast = useToast();
const loading = ref(false);
const submitting = ref(false);
const showAddModal = ref(false);
const isEditing = ref(false);
const perfis = ref<any[]>([]);

const form = ref({
  username: '',
  perfil: 'Comum',
  nome_completo: '',
  lotacao: '',
  email: ''
});

function abrirModalNovo() {
  form.value = { username: '', perfil: 'Comum', nome_completo: '', lotacao: '', email: '' };
  isEditing.value = false;
  showAddModal.value = true;
}

function abrirModalEdicao(item: any) {
  form.value.username = item.username;
  form.value.perfil = item.perfil;
  form.value.nome_completo = item.nome_completo || '';
  form.value.lotacao = item.lotacao || '';
  form.value.email = item.email || '';
  isEditing.value = true;
  showAddModal.value = true;
}

async function carregarPerfis() {
  loading.value = true;
  try {
    const { data } = await api.get('/api/admin/perfis');
    perfis.value = data;
  } catch (error) {
    toast.error('Erro ao carregar perfis.');
  } finally {
    loading.value = false;
  }
}

async function salvar() {
  submitting.value = true;
  try {
    await api.post('/api/admin/perfis', form.value);
    toast.success('Perfil atualizado com sucesso!');
    showAddModal.value = false;
    form.value = { username: '', perfil: 'Comum', nome_completo: '', lotacao: '', email: '' };
    await carregarPerfis();
  } catch (error) {
    toast.error('Erro ao salvar perfil.');
  } finally {
    submitting.value = false;
  }
}

async function removerPerfil(username: string) {
  if (!confirm(`Deseja remover o perfil customizado de ${username}? ele voltará a ser "Comum".`)) return;
  
  try {
    await api.delete(`/api/admin/perfis/${username}`);
    toast.success('Perfil removido.');
    await carregarPerfis();
  } catch (error) {
    toast.error('Erro ao remover perfil.');
  }
}

function getRoleStyle(role: string) {
  switch (role) {
    case 'Administrador': return 'bg-purple-50 text-purple-700 border-purple-200';
    case 'UTI-Admin': return 'bg-blue-100 text-blue-800 border-blue-300';
    case 'UTI': return 'bg-blue-50 text-blue-700 border-blue-200';
    case 'NIR-Admin': return 'bg-amber-100 text-amber-800 border-amber-300';
    case 'NIR': return 'bg-amber-50 text-amber-700 border-amber-200';
    case 'COB-Admin': return 'bg-emerald-100 text-emerald-800 border-emerald-300';
    case 'COB': return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    case 'BC-Admin': return 'bg-teal-100 text-teal-800 border-teal-300';
    case 'BC': return 'bg-teal-50 text-teal-700 border-teal-200';
    case 'HEM-Admin': return 'bg-cyan-100 text-cyan-800 border-cyan-300';
    case 'HEM': return 'bg-cyan-50 text-cyan-700 border-cyan-200';
    default: return 'bg-slate-50 text-slate-600 border-slate-200';
  }
}

onMounted(carregarPerfis);
</script>
