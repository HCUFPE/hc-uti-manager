import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUiStore = defineStore('ui', () => {
  const isLoading = ref(false);
  const isTvMode = ref(localStorage.getItem('hc_uti_tv_mode') === 'true');
  const isMuted = ref(localStorage.getItem('hc_uti_som_alerta') === 'true');

  function setLoading(loading: boolean) {
    isLoading.value = loading;
  }

  function toggleTvMode() {
    isTvMode.value = !isTvMode.value;
    localStorage.setItem('hc_uti_tv_mode', String(isTvMode.value));
  }

  function toggleMute() {
    isMuted.value = !isMuted.value;
    localStorage.setItem('hc_uti_som_alerta', String(isMuted.value));
  }

  function tocarAlertaSonoro() {
    if (isMuted.value) return;
    try {
      const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
      if (!AudioContextClass) return;
      const audioCtx = new AudioContextClass();
      
      const playBeep = (delay: number, freq: number, duration: number) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime + delay);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime + delay);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + delay + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(audioCtx.currentTime + delay);
        osc.stop(audioCtx.currentTime + delay + duration);
      };

      // Toca 6 bipes rápidos em sequência
      playBeep(0, 987.77, 0.12);
      playBeep(0.18, 987.77, 0.12);
      playBeep(0.36, 987.77, 0.12);
      playBeep(0.54, 987.77, 0.12);
      playBeep(0.72, 987.77, 0.12);
      playBeep(0.9, 987.77, 0.15);
    } catch (error) {
      console.warn('Falha ao reproduzir áudio de alerta:', error);
    }
  }

  function tocarAlertaAdmissao() {
    if (isMuted.value) return;
    try {
      const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
      if (!AudioContextClass) return;
      const audioCtx = new AudioContextClass();
      
      const playBeep = (delay: number, freq: number, duration: number) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime + delay);
        gain.gain.setValueAtTime(0.22, audioCtx.currentTime + delay); // Volume mais suave
        gain.gain.exponentialRampToValueAtTime(0.002, audioCtx.currentTime + delay + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(audioCtx.currentTime + delay);
        osc.stop(audioCtx.currentTime + delay + duration);
      };

      // Toca melodia ascendente de Dó Maior (C5 -> E5 -> G5) ainda mais longa e suave com sobreposição
      playBeep(0, 523.25, 1.0);     // Dó (inicia em 0.0s, dura 1.0s)
      playBeep(0.65, 659.25, 1.0);  // Mi (inicia em 0.65s, dura 1.0s)
      playBeep(1.3, 783.99, 1.3);   // Sol (inicia em 1.3s, dura 1.3s)
    } catch (error) {
      console.warn('Falha ao reproduzir áudio de alerta de admissão:', error);
    }
  }

  return { isLoading, setLoading, isTvMode, toggleTvMode, isMuted, toggleMute, tocarAlertaSonoro, tocarAlertaAdmissao };
});
