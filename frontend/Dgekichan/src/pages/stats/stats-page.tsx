import { useEffect, useState } from "react";
import { useStatsStore } from "@/entities/stats/statsStore";
import { TopAppBar } from "@/widgets/top-app-bar";
import { BottomNavigation } from "@/widgets/bottom-navigation";
import { ProductivityChart } from "./components/ProductivityChart";
import { StreakCard } from "./components/StreakCard";
import { CustomCalendar } from "./components/CustomCalendar";
import { BestDayCard } from "./components/BestDayCard";
import { Button } from "@/shared/ui/button/button";
import { cn } from "@/shared/lib/cn";

export function StatsPage() {
  const { productivityStats, fetchProductivity, isLoading } = useStatsStore();
  const [period, setPeriod] = useState<"day" | "week" | "month" | "year">("week");
  const [showCalendar, setShowCalendar] = useState(false);

  useEffect(() => {
    fetchProductivity({ period });
  }, [period, fetchProductivity]);

  const handleDateSelect = (date: Date) => {
    const isoDate = date.toISOString().split('T')[0];
    fetchProductivity({ start: isoDate, end: isoDate });
    setShowCalendar(false);
  };

  const periods = [
    { id: "day", label: "День" },
    { id: "week", label: "Тиждень" },
    { id: "month", label: "Місяць" },
    { id: "year", label: "Рік" },
  ] as const;

  return (
    <div className="min-h-screen bg-background flex flex-col pb-24">
      <TopAppBar />

      <main className="flex-1 px-container-padding pt-20 flex flex-col gap-6">
        <header className="flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-white">Статистика</h1>
            <Button
                variant="ghost"
                size="sm"
                className="text-white/60"
                onClick={() => setShowCalendar(!showCalendar)}
            >
              {showCalendar ? "Закрити" : "Календар"}
            </Button>
          </div>

          {!showCalendar && (
            <div className="flex gap-2 p-1 bg-white/5 rounded-xl">
                {periods.map((p) => (
                <button
                    key={p.id}
                    onClick={() => setPeriod(p.id)}
                    className={cn(
                    "flex-1 py-2 text-xs font-medium rounded-lg transition-all",
                    period === p.id
                        ? "bg-surface-elevated text-white shadow-sm"
                        : "text-white/40 hover:text-white/60"
                    )}
                >
                    {p.label}
                </button>
                ))}
            </div>
          )}
        </header>

        {showCalendar ? (
            <CustomCalendar
                onSelectDate={handleDateSelect}
                onSelectRange={(s, e) => {
                    fetchProductivity({
                        start: s.toISOString().split('T')[0],
                        end: e.toISOString().split('T')[0]
                    });
                    setShowCalendar(false);
                }}
            />
        ) : (
            <>
                <div className="flex gap-stack-sm">
                    <StreakCard
                        type="focus"
                        count={productivityStats?.focus_streak || 0}
                        label="Днів без пропусків таймера"
                    />
                    <StreakCard
                        type="tasks"
                        count={productivityStats?.task_streak || 0}
                        label="Днів виконання завдань"
                    />
                </div>

                {productivityStats?.chart_data && (
                    <ProductivityChart
                        data={productivityStats.chart_data}
                        period={period}
                    />
                )}

                <BestDayCard date={productivityStats?.best_day || null} />

                {productivityStats?.ai_insight && (
                    <div className="p-4 rounded-2xl bg-primary/5 border border-primary/10 text-sm text-white/80 leading-relaxed italic">
                        "{productivityStats.ai_insight}"
                    </div>
                )}
            </>
        )}
      </main>

      <BottomNavigation />
    </div>
  );
}
