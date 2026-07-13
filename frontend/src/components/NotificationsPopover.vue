<template>
  <div class="relative z-50" ref="container">
    <button
      ref="trigger"
      @click.stop="toggle"
      class="relative inline-flex h-10 w-10 items-center justify-center rounded-lg text-slate-600 transition-colors duration-150 hover:bg-blue-500 hover:text-white focus:outline-none focus:ring-2 focus:ring-blue-200"
      aria-label="Abrir notificacoes"
    >
      <Bell class="h-5 w-5" />
      <span
        v-if="totalUnreadCount > 0"
        class="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-[10px] font-bold text-white shadow"
      >
        {{ totalUnreadCount }}
      </span>
    </button>

    <transition name="fade">
      <div
        v-if="open"
        ref="panel"
        class="absolute right-0 mt-3 w-80 origin-top-right rounded-2xl border border-slate-200 bg-white shadow-xl z-50"
      >
        <div class="flex items-center justify-between border-b border-slate-100 px-4 py-3">
          <h3 class="font-semibold text-slate-900">Notificacoes</h3>
          <span class="text-xs text-slate-500">{{ totalUnreadCount }} nao lidas</span>
        </div>

        <div class="max-h-96 overflow-auto p-2">
          <div
            v-for="notification in notifications"
            :key="notification.id"
            class="rounded-lg p-3 transition hover:bg-slate-50"
            :class="notification.unread ? 'bg-blue-50/40' : ''"
          >
            <div class="flex gap-3">
              <div
                class="flex h-10 w-10 items-center justify-center rounded-full text-sm font-semibold"
                :class="[typeConfig[notification.type].bg, typeConfig[notification.type].color]"
              >
                <component :is="typeConfig[notification.type].icon" class="h-5 w-5" />
              </div>
              <div class="min-w-0 flex-1">
                <div class="flex items-start justify-between gap-2">
                  <p class="text-sm font-semibold text-slate-900 leading-tight">{{ notification.title }}</p>
                  <span
                    v-if="notification.unread"
                    class="mt-1 inline-flex h-2 w-2 shrink-0 rounded-full bg-blue-500"
                    aria-label="Nao lida"
                  />
                </div>
                <p class="mt-1 text-xs text-slate-600 wrap-break-words">{{ notification.description }}</p>
                <div class="mt-2 flex items-center justify-between">
                  <div class="flex items-center gap-1 text-[11px] text-slate-500">
                    <Clock3 class="h-3 w-3" />
                    <span>{{ notification.time }}</span>
                  </div>
                  <button
                    v-if="notification.unread"
                    @click.stop="markAsRead(notification.id)"
                    class="text-[10px] font-bold text-blue-600 hover:text-blue-700 bg-blue-50 px-2 py-0.5 rounded transition cursor-pointer"
                  >
                    Ciente
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="border-t border-slate-100 p-3">
          <button
            type="button"
            class="w-full rounded-lg px-3 py-2 text-sm font-semibold text-slate-700 transition hover:bg-blue-50 hover:text-blue-700"
            @click="goToAlerts"
          >
            Ver todas as notificacoes
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import {
  Bell,
  Clock3,
} from 'lucide-vue-next';
import api from '../services/api';

type NotificationType = 'alert' | 'admission' | 'discharge';

type NotificationItem = {
  id: number;
  type: NotificationType;
  title: string;
  description: string;
  time: string;
  unread: boolean;
};

const notifications = ref<NotificationItem[]>([]);
const totalUnreadCount = ref(0);

const fetchNotifications = async () => {
  try {
    const response = await api.get('/api/alertas');
    const alertas = response.data;
    
    const allUnread = alertas.filter((a: any) => !a.lido);
    totalUnreadCount.value = allUnread.length;
    
    // Pegamos apenas os não lidos para o popover, limitando a 5 recentes
    const unreadAlerts = allUnread.slice(0, 5);
    
    notifications.value = unreadAlerts.map((a: any) => {
      // Mapear categoria/tipo para os ícones do popover
      let nType: NotificationType = 'alert';
      if (a.categoria === 'Gargalo' && a.titulo.includes('Vaga')) nType = 'admission';
      if (a.categoria === 'Gargalo' && a.titulo.includes('Alta')) nType = 'discharge';
      
      return {
        id: a.id,
        type: nType,
        title: a.titulo,
        description: a.mensagem.substring(0, 50) + (a.mensagem.length > 50 ? '...' : ''),
        time: a.dataHora,
        unread: !a.lido
      };
    });
  } catch (error) {
    console.error('Erro ao buscar notificacoes:', error);
  }
};

const markAsRead = async (id: number) => {
  try {
    await api.put(`/api/alertas/${id}/lido`, { lido: true });
    notifications.value = notifications.value.filter(n => n.id !== id);
    totalUnreadCount.value = Math.max(0, totalUnreadCount.value - 1);
  } catch (error) {
    console.error('Erro ao marcar alerta como lido:', error);
  }
};

const typeConfig: Record<
  NotificationType,
  {
    icon: any;
    bg: string;
    color: string;
  }
> = {
  alert: {
    icon: Bell,
    bg: 'bg-blue-50',
    color: 'text-blue-600',
  },
  admission: {
    icon: Bell,
    bg: 'bg-blue-50',
    color: 'text-blue-600',
  },
  discharge: {
    icon: Bell,
    bg: 'bg-blue-50',
    color: 'text-blue-600',
  },
};

const open = ref(false);
const trigger = ref<HTMLElement | null>(null);
const panel = ref<HTMLElement | null>(null);
const router = useRouter();


const toggle = () => {
  open.value = !open.value;
  if (open.value) {
    fetchNotifications(); // Refresh ao abrir
  }
};

const close = () => {
  open.value = false;
};

const goToAlerts = () => {
  close();
  router.push('/alertas');
};

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as Node;
  if (
    !open.value ||
    (trigger.value && trigger.value.contains(target)) ||
    (panel.value && panel.value.contains(target))
  ) {
    return;
  }
  close();
};

let intervalId: any;

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  fetchNotifications();
  // Poll a cada 60s
  intervalId = setInterval(fetchNotifications, 60000);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
  if (intervalId) clearInterval(intervalId);
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
