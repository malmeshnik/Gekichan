import React from 'react';
import { CheckCircle2, Circle, Clock } from 'lucide-react';
import { Card } from '../../shared/ui/Card';
import { Task } from '../../shared/api/types';
import { useTaskStore } from '../../entities/taskStore';

interface TaskItemProps {
  task: Task;
}

export const TaskItem: React.FC<TaskItemProps> = ({ task }) => {
  const { updateTaskStatus } = useTaskStore();
  const isDone = task.status === 'done';

  const toggleStatus = (e: React.MouseEvent) => {
    e.stopPropagation();
    updateTaskStatus(task.id, isDone ? 'todo' : 'done');
  };

  return (
    <Card className={`group flex items-center gap-md py-md transition-all duration-300 ${isDone ? 'opacity-60 grayscale-[0.5]' : 'hover:border-primary-start/50'}`}>
      <button
        onClick={toggleStatus}
        className={`p-1 rounded-full transition-colors ${isDone ? 'text-green-500' : 'text-text-secondary group-hover:text-primary-start'}`}
      >
        {isDone ? <CheckCircle2 size={24} fill="currentColor" className="text-background" /> : <Circle size={24} />}
      </button>

      <div className="flex-1 min-w-0">
        <h4 className={`text-sm font-bold truncate ${isDone ? 'line-through text-text-secondary' : ''}`}>
          {task.title}
        </h4>
        <div className="flex items-center gap-sm mt-1">
          <span className="text-[10px] font-bold text-primary-start uppercase tracking-wider bg-primary-start/10 px-2 py-0.5 rounded">
             {task.project.slice(0, 8)}
          </span>
          {task.deadline && (
            <div className="flex items-center gap-1 text-text-secondary">
              <Clock size={10} />
              <span className="text-[10px] font-medium">{new Date(task.deadline).toLocaleDateString()}</span>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};
