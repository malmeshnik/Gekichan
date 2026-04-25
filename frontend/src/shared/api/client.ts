import axios from 'axios';
import { showToast } from '../ui/Toast';
import { translations } from '../lib/i18n/translations';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

let isRefreshing = false;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const i18nStorage = localStorage.getItem('i18n-storage');
    const lang = i18nStorage ? JSON.parse(i18nStorage).state.language : 'en';
    const t = (key: keyof typeof translations['en']) => translations[lang as 'en' | 'ua'][key];

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
         return Promise.reject(error);
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const telegramId = localStorage.getItem('telegram_id');
        if (telegramId) {
          const response = await axios.post(`${import.meta.env.VITE_API_URL || '/api/'}auth/telegram/`, {
            telegram_id: telegramId,
          });
          const { access } = response.data;
          localStorage.setItem('token', access);
          api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
          originalRequest.headers['Authorization'] = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('token');
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    if (error.response?.status >= 500) {
       showToast(t('somethingWrong'), 'error');
    }

    if (!error.response && error.message === 'Network Error') {
       showToast(t('noConnection'), 'error');
    }

    return Promise.reject(error);
  }
);

export default api;
