import { Rocket } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { useStatsStore } from "@/entities/stats/statsStore";
import { useAuthStore } from "@/entities/auth/authStore";
import { useEffect } from "react";

export function HomeSmartStart() {
  const { productivityStats, fetchProductivity } = useStatsStore();
  const { user } = useAuthStore();

  useEffect(() => {
    fetchProductivity();
  }, [fetchProductivity]);

  const yesterdaySec = productivityStats?.focus_yesterday_seconds || 0;
  const goalSec = user?.daily_goal || 10800; // 3h default

  const yesterdayHours = (yesterdaySec / 3600).toFixed(1);
  const goalHours = (goalSec / 3600).toFixed(1);

  const progress = Math.min((yesterdaySec / goalSec) * 100, 100);

  return (
    <SurfacePanel
      variant="glass"
      className="
        mt-stack-md
        flex
        flex-col
        gap-stack-sm
        p-4
      "
    >
      {/* Top */}
      <div
        className="
          flex
          items-start
          justify-between
        "
      >
        {/* Left */}
        <div>
          <h2
            className="
              typography-headline-sm
              text-primary-soft
            "
          >
            Розумний Старт
          </h2>

          <p
            className="
              typography-body-md
              text-text-muted
            "
          >
            Вчора {yesterdayHours}г, Ціль {goalHours}г
          </p>
        </div>

        {/* Icon */}
        <div
          className="
            rounded-lg
            bg-surface-container-highest
            p-2
            text-primary
          "
        >
          <Rocket size={20} />
        </div>
      </div>

      {/* Progress */}
      <div
        className="
          mt-2
          h-2
          w-full
          overflow-hidden
          rounded-full
          bg-surface-container-highest
        "
      >
        <div
          className="
            h-full
            rounded-full
            bg-[linear-gradient(90deg,#4cd6ff_0%,#ddb7ff_100%)]
          "
          style={{
            width: `${progress}%`,
          }}
        />
      </div>

      {/* Bottom */}
      <p
        className="
          mt-1
          text-right
          typography-label
          text-text-main
        "
      >
        {progress >= 100 ? "Ціль виконана! 🔥" : `Прогрес ${Math.round(progress)}%`}
      </p>
    </SurfacePanel>
  );
}
