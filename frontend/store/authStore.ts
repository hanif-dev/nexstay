import { create } from 'zustand';
import api from '@/lib/axios';
import { jwtDecode } from 'jwt-decode';

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  user_type: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  checkAuth: () => void;
  login: (email: string, password: string) => Promise<void>;
  register: (data: object) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,

  checkAuth: () => {
    if (typeof window === 'undefined') { set({ isLoading: false }); return; }
    const token = localStorage.getItem('access_token');
    if (!token) { set({ isLoading: false }); return; }
    try {
      const decoded: { exp: number } = jwtDecode(token);
      if (decoded.exp * 1000 < Date.now()) {
        set({ user: null, isAuthenticated: false, isLoading: false });
        return;
      }
      api.get('/auth/profile/').then((res) => {
        set({ user: res.data, isAuthenticated: true, isLoading: false });
      }).catch(() => {
        set({ user: null, isAuthenticated: false, isLoading: false });
      });
    } catch {
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  },

  login: async (email, password) => {
    const res = await api.post('/auth/login/', { email, password });
    const { access, refresh, user } = res.data;
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
    }
    set({ user, isAuthenticated: true });
  },

  register: async (data) => {
    await api.post('/auth/register/', data);
  },

  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
    set({ user: null, isAuthenticated: false });
  },
}));
