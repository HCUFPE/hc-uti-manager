<template>
  <div class="min-h-screen bg-slate-100 text-slate-900 overflow-hidden">
    <div class="flex h-screen overflow-hidden">
      <SidebarNav v-if="authStore.isAuthenticated" :collapsed="sidebarCollapsed" @toggle="toggleSidebar" />

      <div
        class="flex min-w-0 flex-1 flex-col transition-[padding] duration-200"
        :class="!authStore.isAuthenticated ? 'pl-0' : (sidebarCollapsed ? 'pl-20' : 'pl-64')"
      >
        <header class="sticky top-0 z-20 border-b border-slate-200 bg-white px-6 py-4 shadow-sm">
          <div class="flex items-center justify-between gap-3">
            <div class="space-y-0.5">
              <h1 class="text-xl font-semibold text-slate-900">{{ headerTitle }}</h1>
            </div>
            <div class="flex items-center gap-3">
              <ProfileDropdown v-if="authStore.isAuthenticated" />
              <router-link
                v-else
                to="/login"
                class="rounded-full border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-700 transition hover:bg-slate-50"
              >
                Login
              </router-link>
            </div>
          </div>
        </header>

        <main class="flex-1 overflow-y-auto bg-slate-50 px-5 py-6 md:px-8 md:py-8">
          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import SidebarNav from '../components/SidebarNav.vue';
import ProfileDropdown from '../components/ProfileDropdown.vue';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';
import { useToast } from 'vue-toastification';

const route = useRoute();
const authStore = useAuthStore();
const toast = useToast();
const sidebarCollapsed = ref(false);
const unreadCount = ref(0);

const fetchBackgroundAlerts = async () => {
  if (authStore.isAuthenticated) {
    try {
      await api.post('/api/alertas/gerar');
      const response = await api.get('/api/alertas/unread-count');
      const newCount = response.data.count;
      
      if (newCount > unreadCount.value && authStore.user?.perfil !== 'Administrador' && route.path !== '/alertas') {
        toast.info(`Você tem ${newCount} alerta(s) não lido(s).`, {
          timeout: 5000,
          onClick: () => { window.location.href = '/alertas'; }
        });
      }
      unreadCount.value = newCount;
    } catch (err) {
      console.error('Erro ao sincronizar alertas:', err);
    }
  }
};

onMounted(() => {
  fetchBackgroundAlerts();
  // Atualiza alertas em background a cada 2 minutos
  const interval = setInterval(fetchBackgroundAlerts, 120000);
  
  onUnmounted(() => {
    clearInterval(interval);
  });
});

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value;
};

const headerTitle = computed(() => {
  if (typeof route.meta.title === 'string') {
    return route.meta.title;
  }
  return 'Gestão de Leitos UTI';
});
</script>
