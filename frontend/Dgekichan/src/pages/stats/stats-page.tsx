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
  const { productivityStats, fetchProductivity } = useStatsStore();
  const [period, setPeriod] = useState<"day" | "week" | "month" | "year">("week");
  const [showCalendar, setShowCalendar] = useState(false);
  const [customRange, setCustomRange] = useState<{ start: string; end: string } | null>(null);

  useEffect(() => {
    if (!customRange) {
        fetchProductivity({ period });
    }
  }, [period, fetchProductivity, customRange]);

  const handleDateSelect = (date: Date) => {
    const isoDate = date.toISOString().split('T')[0];
    setCustomRange({ start: isoDate, end: isoDate });
    fetchProductivity({ start: isoDate, end: isoDate });
    setShowCalendar(false);
  };

  const getPeriodLabel = () => {
    if (customRange) {
        if (customRange.start === customRange.end) return customRange.start;
        return `${customRange.start} — ${customRange.end}`;
    }
    const labels = {
        day: "Сьогодні",
        week: "Останній тиждень",
        month: "Останній місяць",
        year: "Останній рік"
    };
    return labels[period];
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
        <header className="flex flex-col gap-1">
            <h1 className="text-2xl font-bold text-white">Статистика</h1>
            <p className="text-sm text-white/40">{getPeriodLabel()}</p>
        </header>

        <BestDayCard date={productivityStats?.best_day?.date || null} />

        <div className="flex gap-stack-sm">
            <StreakCard
                type="focus"
                count={productivityStats?.focus_streak || 0}
                label="Днів без пропусків таймера"
            />
            <StreakCard
                type="tasks"
                count={productivityStats?.tasks_streak || 0}
                label="Днів виконання завдань"
            />
        </div>

        <section className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
                <div className="flex-1 flex gap-2 p-1 bg-white/5 rounded-xl mr-4">
                    {periods.map((p) => (
                    <button
                        key={p.id}
                        onClick={() => {
                            setCustomRange(null);
                            setPeriod(p.id);
                        }}
                        className={cn(
                        "flex-1 py-2 text-[10px] uppercase font-bold rounded-lg transition-all",
                        (period === p.id && !customRange)
                            ? "bg-surface-elevated text-white shadow-sm"
                            : "text-white/40 hover:text-white/60"
                        )}
                    >
                        {p.label}
                    </button>
                    ))}
                </div>
                <Button
                    variant={customRange ? "active" : "ghost"}
                    size="sm"
                    className="text-xs h-9"
                    onClick={() => setShowCalendar(!showCalendar)}
                >
                {showCalendar ? "Закрити" : "Календар"}
                </Button>
            </div>

            {showCalendar && (
                <CustomCalendar
                    mode="range"
                    initialStart={customRange?.start}
                    initialEnd={customRange?.end}
                    onSelectDate={handleDateSelect}
                    onSelectRange={(s, e) => {
                        const start = s.toISOString().split('T')[0];
                        const end = e.toISOString().split('T')[0];
                        setCustomRange({ start, end });
                        fetchProductivity({ start, end });
                        setShowCalendar(false);
                    }}
                />
            )}
        </section>

        {!showCalendar && productivityStats?.chart_data && (
            <ProductivityChart
                data={productivityStats.chart_data}
                period={customRange ? "custom" : period}
            />
        )}

        {!showCalendar && productivityStats?.ai_insight && (
            <div className="p-4 rounded-2xl bg-primary/5 border border-primary/10 text-sm text-white/80 leading-relaxed italic">
                "{productivityStats.ai_insight}"
            </div>
        )}
      </main>

      <BottomNavigation />
    </div>
  );
}
