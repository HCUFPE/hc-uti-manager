import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUiStore = defineStore('ui', () => {
  const isLoading = ref(false);
  const isTvMode = ref(localStorage.getItem('hc_uti_tv_mode') === 'true');

  function setLoading(loading: boolean) {
    isLoading.value = loading;
  }

  function toggleTvMode() {
    isTvMode.value = !isTvMode.value;
    localStorage.setItem('hc_uti_tv_mode', String(isTvMode.value));
  }

  return { isLoading, setLoading, isTvMode, toggleTvMode };
});
