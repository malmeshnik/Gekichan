import { useState, useEffect } from "react";
import { useAuthStore } from "@/entities/auth/authStore";
import { useNavigate } from "react-router-dom";
import { Button } from "@/shared/ui/button";
import { SurfacePanel } from "@/shared/ui/surface-panel";

export function LoginPage() {
  const [telegramId, setTelegramId] = useState("");
  const { login, isLoading } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    const autoLogin = async () => {
      // If we have initData, try auto-login
      if (window.Telegram?.WebApp?.initData) {
        try {
          await login();
          navigate("/");
        } catch (error) {
          console.error("Auto-login failed:", error);
        }
      }
    };
    autoLogin();
  }, [login, navigate]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (telegramId) {
        localStorage.setItem("telegramId", telegramId);
      }
      await login();
      navigate("/");
    } catch (error) {
      alert("Помилка входу. Перевірте дані.");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-container-padding">
      <SurfacePanel variant="glass" className="w-full max-w-sm p-6 space-y-4">
        <h1 className="typography-headline-md text-center text-text-main">Вхід</h1>

        {isLoading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        ) : (
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="typography-label text-text-muted">Telegram ID (для тестування)</label>
              <input
                type="number"
                value={telegramId}
                onChange={(e) => setTelegramId(e.target.value)}
                className="w-full rounded-lg bg-surface-container-highest p-3 text-text-main outline-none border border-outline/20 focus:border-primary/50"
                placeholder="Введіть ваш ID"
              />
            </div>
            <Button type="submit" className="w-full" disabled={isLoading}>
              Увійти
            </Button>
            <p className="typography-label text-center text-text-muted">
              У Telegram Mini App вхід відбудеться автоматично
            </p>
          </form>
        )}
      </SurfacePanel>
    </div>
  );
}
