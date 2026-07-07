import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../services/api';

// Tipagem correta para suportar tanto MockAuth quanto Active Directory
interface User {
  username: string;
  perfil: string; // Administrador, UTI, NIR, Solicitante de Leito, Comum
  groups: string[];

  // Campos opcionais vindos do AD
  givenName?: string[];
  userPrincipalName?: string[];
  displayName?: string[];
  title?: string[];
  department?: string[];
  cn?: string[];
  mail?: string[];
  employeeNumber?: string[];
}

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('accessToken') || null);
  const user = ref<User | null>(null);

  try {
    const storedUser = localStorage.getItem('user');
    if (storedUser) user.value = JSON.parse(storedUser);
  } catch (error) {
    console.warn("Could not parse stored user", error);
  }

  const isAuthenticated = computed(() => !!accessToken.value);
  
  const perfil = computed(() => user.value?.perfil || 'Comum');

  const isAdmin = computed(() => perfil.value === 'Administrador');
  const isUTI = computed(() => ['UTI', 'UTI-Admin', 'Administrador'].includes(perfil.value));
  const isNIR = computed(() => ['NIR', 'NIR-Admin', 'Administrador'].includes(perfil.value));
  const isSolicitante = computed(() => [
    'COB', 'COB-Admin',
    'BC', 'BC-Admin',
    'HEM', 'HEM-Admin',
    'Administrador'
  ].includes(perfil.value));
  
  const isAnyAdmin = computed(() => [
    'Administrador', 'UTI-Admin', 'NIR-Admin', 
    'COB-Admin', 'BC-Admin', 'HEM-Admin'
  ].includes(perfil.value));
  
  // Para manter compatibilidade com componentes que usam isCoordination
  const isCoordination = computed(() => ['Administrador', 'UTI', 'UTI-Admin', 'NIR', 'NIR-Admin'].includes(perfil.value));

  // Helpers para controle de formulário na tela de AdminConfig
  function getAssignableProfiles(): string[] {
    if (isAdmin.value) {
      return [
        'Administrador', 'UTI-Admin', 'NIR-Admin', 
        'COB-Admin', 'BC-Admin', 'HEM-Admin',
        'UTI', 'NIR', 'COB', 'BC', 'HEM', 'Comum'
      ];
    }
    if (perfil.value === 'UTI-Admin') return ['UTI', 'Comum'];
    if (perfil.value === 'NIR-Admin') return ['NIR', 'Comum'];
    if (perfil.value === 'COB-Admin') return ['COB', 'Comum'];
    if (perfil.value === 'BC-Admin') return ['BC', 'Comum'];
    if (perfil.value === 'HEM-Admin') return ['HEM', 'Comum'];
    return [];
  }

  function canManageUser(targetUserPerfil: string): boolean {
    if (isAdmin.value) return true;
    if (perfil.value === 'UTI-Admin' && targetUserPerfil === 'UTI') return true;
    if (perfil.value === 'NIR-Admin' && targetUserPerfil === 'NIR') return true;
    if (perfil.value === 'COB-Admin' && targetUserPerfil === 'COB') return true;
    if (perfil.value === 'BC-Admin' && targetUserPerfil === 'BC') return true;
    if (perfil.value === 'HEM-Admin' && targetUserPerfil === 'HEM') return true;
    return false;
  }

  function setToken(token: string) {
    accessToken.value = token;
    localStorage.setItem('accessToken', token);
  }

  function clearToken() {
    accessToken.value = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('user');
    user.value = null;
  }

  function setUser(userData: User | null) {
    user.value = userData;
    if (userData) {
      localStorage.setItem('user', JSON.stringify(userData));
    } else {
      localStorage.removeItem('user');
    }
  }

  async function fetchUser() {
    if (!accessToken.value) {
      setUser(null);
      return;
    }
    try {
      const { data } = await api.get('/api/users/me');
      setUser(data);
    } catch (error) {
      console.error("Failed to fetch user info:", error);
      clearToken();
    }
  }

  async function login(username: string, password: string, rememberMe: boolean) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    if (rememberMe) {
      params.append('remember_me', 'true');
    }

    try {
      const { data } = await api.post('/api/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      setToken(data.access_token);
      await fetchUser();
    } catch (error: any) {
      console.error("Login failed:", error);
      throw error;
    }
  }

  async function logout(router?: any) {
    try {
      await api.post('/api/logout');
    } catch (error) {
      console.error("Logout failed, but clearing token anyway.", error);
    } finally {
      clearToken();
      if (router) {
        router.push({ name: 'Login' });
      }
    }
  }

  async function initializeAuth() {
    if (accessToken.value) {
      await fetchUser();
    } else {
      try {
        const { data } = await api.post('/api/token/refresh');
        if (data.access_token) {
          setToken(data.access_token);
          await fetchUser();
        }
      } catch {
        console.log("No valid refresh token found.");
      }
    }
  }

  return { 
    accessToken, 
    user, 
    perfil,
    isAuthenticated, 
    isAdmin, 
    isAnyAdmin,
    isUTI,
    isNIR,
    isSolicitante,
    isCoordination,
    getAssignableProfiles,
    canManageUser,
    login, 
    logout,
    setToken,
    clearToken,
    fetchUser,
    initializeAuth
  };
});
