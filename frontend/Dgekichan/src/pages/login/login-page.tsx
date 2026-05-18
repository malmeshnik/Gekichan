import { useState } from "react";
import { useAuthStore } from "@/entities/auth/authStore";
import { useNavigate } from "react-router-dom";
import { Button } from "@/shared/ui/button";
import { SurfacePanel } from "@/shared/ui/surface-panel";

export function LoginPage() {
  const [telegramId, setTelegramId] = useState("");
  const { login, isLoading } = useAuthStore();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!telegramId) return;
    try {
      await login(parseInt(telegramId));
      navigate("/");
    } catch (error) {
      alert("Помилка входу. Перевірте ID.");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-container-padding">
      <SurfacePanel variant="glass" className="w-full max-w-sm p-6 space-y-4">
        <h1 className="typography-headline-md text-center text-text-main">Вхід</h1>
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="typography-label text-text-muted">Telegram ID</label>
            <input
              type="number"
              value={telegramId}
              onChange={(e) => setTelegramId(e.target.value)}
              className="w-full rounded-lg bg-surface-container-highest p-3 text-text-main outline-none border border-outline/20 focus:border-primary/50"
              placeholder="Введіть ваш ID"
            />
          </div>
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Вхід..." : "Увійти"}
          </Button>
        </form>
      </SurfacePanel>
    </div>
  );
}
