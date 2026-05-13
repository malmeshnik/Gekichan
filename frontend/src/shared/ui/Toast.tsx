import React, { useEffect, useState } from 'react';
import { CheckCircle2, XCircle, Info } from 'lucide-react';

export type ToastType = 'success' | 'error' | 'info';

interface Toast {
  id: string;
  message: string;
  type: ToastType;
}

export const ToastContainer: React.FC = () => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  // Listen for custom events
  useEffect(() => {
    const handleAddToast = (event: any) => {
      const { message, type } = event.detail;
      const id = Math.random().toString(36).substr(2, 9);
      setToasts(prev => [...prev, { id, message, type }]);

      setTimeout(() => {
        setToasts(prev => prev.filter(t => t.id !== id));
      }, 3000);
    };

    window.addEventListener('add-toast', handleAddToast);
    return () => window.removeEventListener('add-toast', handleAddToast);
  }, []);

  return (
    <div className="fixed top-4 left-1/2 -translate-x-1/2 z-[100] flex flex-col gap-2 w-full max-w-xs px-md">
      {toasts.map(toast => (
        <div
          key={toast.id}
          className={`flex items-center gap-md p-md rounded-2xl border backdrop-blur-md shadow-2xl animate-in slide-in-from-top duration-300 ${
            toast.type === 'success' ? 'bg-green-500/10 border-green-500/20 text-green-500' :
            toast.type === 'error' ? 'bg-red-500/10 border-red-500/20 text-red-500' :
            'bg-primary-start/10 border-primary-start/20 text-primary-start'
          }`}
        >
          {toast.type === 'success' && <CheckCircle2 size={18} />}
          {toast.type === 'error' && <XCircle size={18} />}
          {toast.type === 'info' && <Info size={18} />}
          <span className="text-sm font-bold">{toast.message}</span>
        </div>
      ))}
    </div>
  );
};

export const showToast = (message: string, type: ToastType = 'info') => {
  window.dispatchEvent(new CustomEvent('add-toast', {
    detail: { message, type }
  }));
};
