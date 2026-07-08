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

      <!-- Loading Skeleton -->
      <div v-if="loading" class="px-6 py-12 text-center text-slate-400 animate-pulse font-semibold">
        Carregando perfis...
      </div>

      <!-- Collapsible Groups -->
      <div v-else class="divide-y divide-slate-200/60">
        <div v-for="(group, key) in groupedPerfis" :key="key" class="overflow-hidden">
          <!-- Accordion Header -->
          <button 
            @click="expandedGroups[key] = !expandedGroups[key]" 
            class="w-full flex items-center justify-between px-6 py-4 bg-slate-50/50 hover:bg-slate-50 transition text-left"
          >
            <div class="flex items-center gap-3">
              <span class="font-bold text-slate-700 text-sm md:text-base">{{ group.label }}</span>
              <span class="rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-bold text-blue-700">
                {{ group.users.length }}
              </span>
            </div>
            <ChevronDownIcon 
              class="h-5 w-5 text-slate-400 transition-transform duration-200"
              :class="{ 'rotate-180': expandedGroups[key] }"
            />
          </button>

          <!-- Accordion Content -->
          <div v-show="expandedGroups[key]" class="overflow-x-auto border-t border-slate-200/50">
            <table class="w-full text-left border-collapse" v-if="group.users.length > 0">
              <thead>
                <tr class="text-xs uppercase tracking-wider text-slate-400 bg-slate-50/30 border-b border-slate-200/50">
                  <th class="px-6 py-2.5 font-semibold">Usuário (Nome/Login)</th>
                  <th class="px-6 py-2.5 font-semibold">Lotação</th>
                  <th class="px-6 py-2.5 font-semibold">E-mail</th>
                  <th class="px-6 py-2.5 font-semibold">Perfil</th>
                  <th class="px-6 py-2.5 font-semibold text-right">Ações</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="item in group.users" :key="item.username" class="hover:bg-slate-50/50 transition">
                  <td class="px-6 py-3.5">
                    <div class="font-semibold text-slate-800">{{ item.nome_completo || 'Sem Nome' }}</div>
                    <div class="text-xs text-slate-400">{{ item.username }}</div>
                  </td>
                  <td class="px-6 py-3.5 text-sm text-slate-600">{{ item.lotacao || 'N/D' }}</td>
                  <td class="px-6 py-3.5 text-sm text-slate-500">{{ item.email || 'N/D' }}</td>
                  <td class="px-6 py-3.5">
                    <span 
                      class="px-2.5 py-0.5 rounded-full text-xs font-bold border whitespace-nowrap"
                      :class="getRoleStyle(item.perfil)"
                    >
                      {{ item.perfil }}
                    </span>
                  </td>
                  <td class="px-6 py-3.5 text-right flex justify-end gap-2">
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
              </tbody>
            </table>
            <div v-else class="px-6 py-6 text-center text-slate-400 text-sm italic">
              Nenhum usuário cadastrado neste grupo.
            </div>
          </div>
        </div>
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
import { PlusIcon, TrashIcon, XMarkIcon, PencilSquareIcon, ChevronDownIcon } from '@heroicons/vue/24/outline';
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

const expandedGroups = ref<Record<string, boolean>>({
  nir: false,
  uti: false,
  bc: false,
  hem: false,
  cob: false,
  admin: false,
  comum: false
});

const groupedPerfis = computed(() => {
  const groups: Record<string, { label: string; roles: string[]; users: any[] }> = {
    admin: { label: "Administrador", roles: ["Administrador"], users: [] },
    bc: { label: "Bloco Cirúrgico (BC) / BC-Admin", roles: ["BC", "BC-Admin"], users: [] },
    cob: { label: "Centro Obstétrico (COB) / COB-Admin", roles: ["COB", "COB-Admin"], users: [] },
    comum: { label: "Comum", roles: ["Comum"], users: [] },
    hem: { label: "Hemodinâmica (HEM) / HEM-Admin", roles: ["HEM", "HEM-Admin"], users: [] },
    nir: { label: "NIR / NIR-Admin", roles: ["NIR", "NIR-Admin"], users: [] },
    uti: { label: "UTI / UTI-Admin", roles: ["UTI", "UTI-Admin"], users: [] }
  };
  
  perfis.value.forEach(user => {
    const perfil = user.perfil;
    for (const key in groups) {
      if (groups[key].roles.includes(perfil)) {
        groups[key].users.push(user);
        return;
      }
    }
    groups.comum.users.push(user);
  });

  // Alphabetical sort within each group by complex name or username
  for (const key in groups) {
    groups[key].users.sort((a, b) => {
      const nameA = (a.nome_completo || a.username || "").toLowerCase();
      const nameB = (b.nome_completo || b.username || "").toLowerCase();
      return nameA.localeCompare(nameB);
    });
  }

  return groups;
});

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
