import React from 'react';
import { Header } from '../shared/ui/Header';
import { Card } from '../shared/ui/Card';
import { useI18n } from '../shared/lib/i18n';
import { useAuthStore } from '../entities/authStore';
import { Globe, LogOut, User as UserIcon } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const { lang, setLang, t } = useI18n();
  const { telegramId, logout } = useAuthStore();

  return (
    <div className="pb-32 min-h-screen">
      <Header title={t('settings')} />

      <main className="px-md flex flex-col gap-md">
        <Card className="flex flex-col gap-lg py-lg">
          {/* User info */}
          <div className="flex items-center gap-md">
            <div className="p-3 bg-primary-start/10 rounded-full text-primary-start">
              <UserIcon size={24} />
            </div>
            <div>
              <p className="text-xs text-text-secondary uppercase tracking-widest font-bold">{t('user')}</p>
              <p className="text-lg font-bold">{telegramId || t('notLoggedIn')}</p>
            </div>
          </div>

          <div className="h-px bg-border w-full" />

          {/* Language selection */}
          <div className="flex flex-col gap-md">
            <div className="flex items-center gap-2 text-text-secondary">
              <Globe size={18} />
              <span className="text-sm font-bold uppercase tracking-widest">{t('language')}</span>
            </div>

            <div className="flex gap-sm">
              <button
                onClick={() => setLang('en')}
                className={`flex-1 p-md rounded-2xl font-bold transition-all ${
                  lang === 'en'
                    ? 'bg-primary-start text-white shadow-lg shadow-primary-start/20'
                    : 'bg-background border border-border text-text-secondary'
                }`}
              >
                {t('english')}
              </button>
              <button
                onClick={() => setLang('ua')}
                className={`flex-1 p-md rounded-2xl font-bold transition-all ${
                  lang === 'ua'
                    ? 'bg-primary-start text-white shadow-lg shadow-primary-start/20'
                    : 'bg-background border border-border text-text-secondary'
                }`}
              >
                {t('ukrainian')}
              </button>
            </div>
          </div>

          <div className="h-px bg-border w-full" />

          {/* Logout */}
          <button
            onClick={logout}
            className="flex items-center justify-center gap-2 p-md w-full rounded-2xl border-2 border-dashed border-red-500/30 text-red-500 font-bold hover:bg-red-500/5 transition-colors"
          >
            <LogOut size={20} />
            <span className="uppercase tracking-widest text-sm">{t('logout')}</span>
          </button>
        </Card>
      </main>
    </div>
  );
};
