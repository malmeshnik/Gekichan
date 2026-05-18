import { Flame, Sparkles, PartyPopper } from "lucide-react";
import { Badge } from "@/shared/ui/badge";
import { useAuthStore } from "@/entities/auth/authStore";
import { getTimeBasedGreeting } from "@/shared/lib/greetings";
import { useMemo } from "react";

export function TopAppBar() {
  const { user } = useAuthStore();
  const greeting = getTimeBasedGreeting();

  const streakBadge = useMemo(() => {
    if (!user) return null;

    if (user.streak > 0) {
      return (
        <Badge variant="tertiary" className="h-9 gap-1.5 rounded-full border border-outline/50 bg-surface-container-high/90 px-3 backdrop-blur-xl transition-all duration-300 hover:border-secondary/30 hover:bg-surface-container-highest">
          <Flame size={14} fill="currentColor" className="text-secondary drop-shadow-[0_0_8px_rgba(221,183,255,0.45)]" />
          <span className="typography-label text-text-main">{user.streak} streak</span>
        </Badge>
      );
    }

    // New user logic (account created < 24h ago)
    const isNew = new Date().getTime() - new Date(user.created_at).getTime() < 86400000;
    if (isNew) {
        return (
            <Badge variant="tertiary" className="h-9 gap-1.5 rounded-full border border-secondary/20 bg-secondary/5 px-3 backdrop-blur-xl">
              <PartyPopper size={14} className="text-secondary" />
              <span className="typography-label text-secondary">Новачок</span>
            </Badge>
        );
    }

    return (
        <Badge variant="tertiary" className="h-9 gap-1.5 rounded-full border border-primary/20 bg-primary/5 px-3 backdrop-blur-xl">
          <Sparkles size={14} className="text-primary" />
          <span className="typography-label text-primary">Починаємо!</span>
        </Badge>
    );
  }, [user]);

  return (
    <header
      className="
        fixed
        inset-x-0
        top-0
        z-50
        h-16
        border-b
        border-outline/40
        bg-background/60
        backdrop-blur-2xl
        shadow-[var(--shadow-topbar)]
      "
    >
      <div
        className="
          mx-auto
          flex
          h-full
          w-full
          max-w-md
          items-center
          justify-between
          px-container-padding
        "
      >
        {/* Left */}
        <div
          className="
            flex
            items-center
            gap-stack-sm
          "
        >
          {/* Avatar */}
          <div
            className="
              relative
              h-9
              w-9
              overflow-hidden
              rounded-full
              border
              border-outline/50
              bg-surface-container-high
              shadow-[var(--shadow-neon)]
            "
          >
            <img
              alt="User Avatar"
              className="
                h-full
                w-full
                object-cover
              "
              src={user?.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${user?.first_name || 'User'}`}
            />

            {/* Neon ring */}
            <div
              className="
                absolute
                inset-0
                rounded-full
                ring-1
                ring-primary/20
              "
            />
          </div>

          {/* User Greeting */}
          <div className="flex flex-col leading-tight">
            <span className="typography-label text-text-muted text-[10px] uppercase tracking-wider">
              {greeting}
            </span>
            <span
              className="
                typography-headline-sm
                text-primary
                tracking-tight
              "
            >
              {user?.first_name || "Гість"}
            </span>
          </div>
        </div>

        {/* Right */}
        {streakBadge}
      </div>
    </header>
  );
}
