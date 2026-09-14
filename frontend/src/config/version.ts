/**
 * Single Source of Truth Version Store (Frontend)
 * Carrega dinamicamente a partir do Backend (/api/health).
 * Você SÓ PRECISA alterar a versão no arquivo backend 'src/version.py'.
 */
import { ref } from 'vue';
import api from '../services/api';

// Valores padrão enquanto a API responde
export const APP_VERSION = ref('1.7.0');
export const LAST_UPDATE = ref('14/09/2026 às 15:00h');
export const APP_NAME = ref('HC-UTI Manager');
export const SYSTEM_TITLE = ref('Gestão de Leitos UTI');

export async function fetchSystemConfig() {
  try {
    const response = await api.get('/api/health');
    if (response.data) {
      if (response.data.version) APP_VERSION.value = response.data.version;
      if (response.data.last_update) LAST_UPDATE.value = response.data.last_update;
      if (response.data.app_name) APP_NAME.value = response.data.app_name;
      if (response.data.system_title) SYSTEM_TITLE.value = response.data.system_title;
    }
  } catch (error) {
    // Mantém fallback caso a API demore a responder
  }
}

// Inicializa automaticamente
fetchSystemConfig();
