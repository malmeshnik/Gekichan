import React, { useEffect } from 'react';
import { Header } from '@/shared/ui/Header';
import { Card } from '@/shared/ui/Card';
import { StatsGrid } from '@/widgets/StatsGrid';
import { useStatsStore } from '@/entities/statsStore';
import { useI18n } from '@/shared/lib/i18n';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export const StatsPage: React.FC = () => {
  const { dashboard, fetchDashboardStats, isLoading } = useStatsStore();
  const { t } = useI18n();

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const chartData = dashboard?.last_7_days.map(d => ({
    name: new Date(d.date).toLocaleDateString(undefined, { weekday: 'short' }),
    focus: Math.floor(d.focus_time / 60),
    tasks: d.tasks_done
  })) || [];

  return (
    <div className="pb-32 min-h-screen">
      <Header title={t('productivity')} />

      <main className="px-md flex flex-col gap-lg">
        <StatsGrid />

        <section className="flex flex-col gap-md">
          <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider px-xs">
            {t('weeklyStats')}
          </h3>
          <Card className="h-64 py-lg pr-lg pl-0">
            {isLoading ? (
              <div className="w-full h-full flex items-center justify-center">
                 <div className="w-8 h-8 border-4 border-primary-start border-t-transparent rounded-full animate-spin" />
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#1F2937" />
                  <XAxis
                    dataKey="name"
                    axisLine={false}
                    tickLine={false}
                    tick={{ fill: '#9CA3AF', fontSize: 10 }}
                    dy={10}
                  />
                  <YAxis
                    axisLine={false}
                    tickLine={false}
                    tick={{ fill: '#9CA3AF', fontSize: 10 }}
                  />
                  <Tooltip
                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                    contentStyle={{ backgroundColor: '#111827', borderColor: '#1F2937', borderRadius: '12px' }}
                  />
                  <Bar dataKey="focus" radius={[4, 4, 0, 0]}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={index === chartData.length - 1 ? '#3B82F6' : '#1F2937'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </Card>
        </section>

        {/* Placeholder for dashboard extra stats */}
        <div className="grid grid-cols-2 gap-md">
           <Card className="flex flex-col gap-1">
              <span className="text-[10px] font-bold text-text-secondary uppercase tracking-widest">{t('productivityScore')}</span>
              <span className="text-2xl font-bold text-primary-start">82</span>
           </Card>
           <Card className="flex flex-col gap-1">
              <span className="text-[10px] font-bold text-text-secondary uppercase tracking-widest">{t('peakHour')}</span>
              <span className="text-2xl font-bold">11:00</span>
           </Card>
        </div>
      </main>
    </div>
  );
};
