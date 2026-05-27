import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useStatsStore } from "@/entities/stats/statsStore";
import { useProjectStore } from "@/entities/project/projectStore";
import { TopAppBar } from "@/widgets/top-app-bar";
import { BottomNavigation } from "@/widgets/bottom-navigation";
import { ProductivityChart } from "@/pages/stats/components/ProductivityChart";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { cn } from "@/shared/lib/cn";
import { Users, Target, Clock, Trophy, ArrowLeft } from "lucide-react";
import { formatFocusTime } from "@/shared/lib/format/time";
import { useNavigate } from "react-router-dom";

export function ProjectAnalyticsPage() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const { productivityStats, fetchProductivity } = useStatsStore();
  const { projects, fetchProjects } = useProjectStore();
  const [period, setPeriod] = useState<"day" | "week" | "month" | "year">("week");

  useEffect(() => {
    if (projectId) {
        fetchProductivity({ period, projectId }); 
    }
    if (projects.length === 0) fetchProjects();
  }, [projectId, period, fetchProductivity, fetchProjects, projects.length]);

  const project = projects.find(p => String(p.id) === String(projectId));

  if (!project) return null;

  const stats = productivityStats;

  return (
    <div className="min-h-screen bg-background flex flex-col pb-24">
      <TopAppBar />

      <main className="flex-1 px-container-padding pt-20 flex flex-col gap-6">
        <header className="flex flex-col gap-1">
            <button
                onClick={() => navigate(-1)}
                className="flex items-center gap-2 text-primary text-xs font-bold uppercase tracking-wider mb-2"
            >
                <ArrowLeft size={14} /> Назад
            </button>
            <h1 className="text-2xl font-bold text-white">Аналітика проєкту</h1>
            <p className="text-sm text-white/40">{project.name}</p>
        </header>

        {/* Overview Cards */}
        <div className="grid grid-cols-2 gap-4">
            <SurfacePanel variant="glass" className="p-4 flex flex-col gap-1">
                <Target size={20} className="text-primary mb-1" />
                <span className="text-2xl font-bold">{stats?.tasks_completed_today || 0}</span>
                <span className="text-[10px] uppercase text-text-muted font-bold">Завершено задач</span>
            </SurfacePanel>
            <SurfacePanel variant="glass" className="p-4 flex flex-col gap-1">
                <Clock size={20} className="text-secondary mb-1" />
                <span className="text-xl font-bold">{formatFocusTime(stats?.focus_today_seconds || 0)}</span>
                <span className="text-[10px] uppercase text-text-muted font-bold">Час у фокусі</span>
            </SurfacePanel>
        </div>

        {/* Chart Section */}
        <section className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
                <div className="flex-1 flex gap-2 p-1 bg-white/5 rounded-xl">
                    {["day", "week", "month"].map((p) => (
                    <button
                        key={p}
                        onClick={() => setPeriod(p as any)}
                        className={cn(
                        "flex-1 py-2 text-[10px] uppercase font-bold rounded-lg transition-all",
                        period === p
                            ? "bg-surface-elevated text-white shadow-sm"
                            : "text-white/40 hover:text-white/60"
                        )}
                    >
                        {p === 'day' ? 'День' : p === 'week' ? 'Тиждень' : 'Місяць'}
                    </button>
                    ))}
                </div>
            </div>

            {stats?.chart_data && (
                <ProductivityChart
                    data={stats.chart_data}
                    period={period}
                />
            )}
        </section>

        {/* Leaderboard / Team Section */}
        {stats?.leaderboard && stats.leaderboard.length > 0 && (
            <section className="flex flex-col gap-4">
                <div className="flex items-center gap-2">
                    <Trophy size={18} className="text-yellow-500" />
                    <h2 className="text-sm font-bold uppercase tracking-wider text-white/60">Топ виконавців</h2>
                </div>
                <div className="flex flex-col gap-2">
                    {stats.leaderboard.map((member: any, index) => (
                        <SurfacePanel key={member.username} variant="glass" className="p-3 flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-xs">
                                    {index + 1}
                                </div>
                                <div className="flex flex-col">
                                    <span className="text-sm font-medium">{member.first_name || member.username}</span>
                                    <span className="text-[10px] text-text-muted uppercase">@{member.username}</span>
                                </div>
                            </div>
                            <div className="flex flex-col items-end">
                                <span className="text-sm font-bold text-primary">{member.completed_tasks}</span>
                                <span className="text-[9px] text-text-muted uppercase">задач</span>
                            </div>
                        </SurfacePanel>
                    ))}
                </div>
            </section>
        )}

        {/* Member Focus Stats (Admin Only View - simplified for now) */}
        {stats?.member_focus_stats && stats.member_focus_stats.length > 0 && (
            <section className="flex flex-col gap-4">
                <div className="flex items-center gap-2">
                    <Users size={18} className="text-secondary" />
                    <h2 className="text-sm font-bold uppercase tracking-wider text-white/60">Активність команди</h2>
                </div>
                <div className="flex flex-col gap-2">
                    {stats.member_focus_stats.map((member: any) => (
                        <SurfacePanel key={member.username} variant="glass" className="p-3 flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <div className="h-8 w-8 rounded-full overflow-hidden border border-outline/20">
                                    <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${member.username}`} alt="avatar" />
                                </div>
                                <span className="text-sm font-medium">{member.first_name || member.username}</span>
                            </div>
                            <span className="text-xs font-medium text-secondary">{formatFocusTime(member.total_focus_seconds)}</span>
                        </SurfacePanel>
                    ))}
                </div>
            </section>
        )}
      </main>

      <BottomNavigation />
    </div>
  );
}
