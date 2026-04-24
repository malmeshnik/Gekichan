import React from 'react';
import { TaskItem } from '../entities/task/TaskItem';
import { Task } from '../entities/types';

interface TaskListProps {
  title: string;
  tasks: Task[];
  onSeeAll?: () => void;
}

export const TaskListWidget: React.FC<TaskListProps> = ({ title, tasks, onSeeAll }) => {
  return (
    <section className="flex flex-col gap-md">
      <div className="flex items-center justify-between px-xs">
        <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider">{title}</h3>
        {onSeeAll && (
          <button onClick={onSeeAll} className="text-xs font-semibold text-primary-start">See All</button>
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
