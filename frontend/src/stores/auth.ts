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
  const isUTI = computed(() => perfil.value === 'UTI' || perfil.value === 'Administrador');
  const isNIR = computed(() => perfil.value === 'NIR' || perfil.value === 'Administrador');
  const isSolicitante = computed(() => perfil.value === 'Solicitante de Leito' || perfil.value === 'Administrador');
  
  // Para manter compatibilidade com componentes que usam isCoordination
  const isCoordination = computed(() => ['Administrador', 'UTI', 'NIR'].includes(perfil.value));

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
    if (accessToken.value.startsWith('mock-token-')) {
      // Skip remote fetch when using mock auth so the session survives refresh
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
    isAuthenticated, 
    isAdmin, 
    isUTI,
    isNIR,
    isSolicitante,
    isCoordination,
    login, 
    logout,
    setToken,
    clearToken,
    fetchUser,
    initializeAuth
  };
});
