import React from 'react';
import { TaskItem } from '@/entities/task/TaskItem';
import { Task } from '@/entities/types';
import { useI18n } from '@/shared/lib/i18n';

interface TaskListProps {
  title: string;
  tasks: Task[];
  onSeeAll?: () => void;
}

export const TaskListWidget: React.FC<TaskListProps> = ({ title, tasks, onSeeAll }) => {
  const { t } = useI18n();

  return (
    <section className="flex flex-col gap-md">
      <div className="flex items-center justify-between px-xs">
        <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider">{title}</h3>
        {onSeeAll && (
          <button onClick={onSeeAll} className="text-xs font-semibold text-primary-start">{t('seeAll')}</button>
        )}
      </div>

      <div className="flex flex-col gap-sm">
        {tasks.map(task => (
          <TaskItem key={task.id} task={task} />
        ))}
      </div>
    </section>
  );
};
