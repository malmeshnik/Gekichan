import React, { useState, useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import api from '../api/client';
import { useAuthStore } from '../store';

const AuthProvider = ({ children }) => {
  const { token, setToken, setUser, logout } = useAuthStore();
  const [loading, setLoading] = useState(true);
  const [isDevMode, setIsDevMode] = useState(false);
  const [devTelegramId, setDevTelegramId] = useState('');

  useEffect(() => {
    const initAuth = async () => {
      // Check if running in Telegram
      if (WebApp.initData) {
        try {
          const response = await api.post('/auth/telegram/', {
            init_data: WebApp.initData, // This might need parsing on backend if it expects telegram_id
          });
          setToken(response.data.access);
          setUser(response.data.user);
        } catch (error) {
          console.error('Telegram auth failed', error);
        }
      } else if (token) {
        setLoading(false);
        return;
      } else {
        setIsDevMode(true);
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const handleDevLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/auth/telegram/', {
        telegram_id: parseInt(devTelegramId, 10)
      });
      setToken(response.data.access);
      // setUser(response.data.user); // Backend response only has access/refresh
      setIsDevMode(false);
    } catch (error) {
      alert('Dev login failed.');
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  if (isDevMode && !token) {
    return (
      <div className="flex flex-col items-center justify-center h-screen p-4 bg-gray-50">
        <div className="w-full max-w-sm p-6 bg-white rounded-xl shadow-md">
          <h1 className="text-xl font-bold mb-4 text-center">Dev Mode Login</h1>
          <p className="text-sm text-gray-600 mb-6 text-center">
            Enter a Telegram ID to simulate login.
          </p>
          <form onSubmit={handleDevLogin}>
            <input
              type="number"
              placeholder="Telegram ID (e.g. 12345678)"
              value={devTelegramId}
              onChange={(e) => setDevTelegramId(e.target.value)}
              className="w-full p-3 border rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
            <button type="submit" className="w-full bg-blue-600 text-white p-3 rounded-lg font-medium hover:bg-blue-700 transition-colors">
              Login as Dev
            </button>
          </form>
        </div>
      </div>
    );
  }

  return children;
};

export default AuthProvider;
