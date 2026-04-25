import axios from 'axios';

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

    // Handle 401 re-auth
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

    // Handle 500 errors and show message
    if (error.response?.status >= 500) {
       alert('Something went wrong. Please try again later.');
    }

    // Handle network errors
    if (!error.response && error.message === 'Network Error') {
       alert('No connection. Please check your internet.');
    }

    return Promise.reject(error);
  }
);

export default api;
