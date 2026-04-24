import React from 'react';
import { Task } from '../types';
import { Card } from '../../shared/ui/Card';
import { Badge } from '../../shared/ui/Badge';
import { CheckCircle2, Circle, Clock } from 'lucide-react';

interface TaskItemProps {
  task: Task;
  onToggle?: (id: string) => void;
}

export const TaskItem: React.FC<TaskItemProps> = ({ task, onToggle }) => {
  const isDone = task.status === 'done';

  return (
    <Card className="flex items-center gap-md py-sm">
      <button
        onClick={() => onToggle?.(task.id)}
        className={`transition-colors ${isDone ? 'text-primary-start' : 'text-text-secondary'}`}
      >
        {isDone ? <CheckCircle2 size={24} /> : <Circle size={24} />}
      </button>

      <div className="flex-1 min-w-0">
        <h4 className={`text-sm font-medium truncate ${isDone ? 'text-text-secondary line-through' : 'text-text-primary'}`}>
          {task.title}
        </h4>
        <div className="flex items-center gap-2 mt-1">
          {task.project_name && (
            <Badge variant="secondary">{task.project_name}</Badge>
          )}
          {task.deadline && (
            <div className="flex items-center gap-1 text-[10px] text-text-secondary">
              <Clock size={10} />
              <span>{new Date(task.deadline).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};
