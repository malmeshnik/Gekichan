import { useState, useEffect, useMemo } from "react";
import { Modal } from "@/shared/ui/modal";
import { Button } from "@/shared/ui/button";
import { useTaskStore, Task } from "@/entities/task/taskStore";
import { useProjectStore } from "@/entities/project/projectStore";
import { Calendar, User, Flag, Trash2, Bell } from "lucide-react";
import { cn } from "@/shared/lib/cn";

interface EditTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  task: any; // Using any to access more fields
}

export function EditTaskModal({ isOpen, onClose, task }: EditTaskModalProps) {
  const { updateTask, deleteTask } = useTaskStore();
  const { projects } = useProjectStore();

  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [status, setStatus] = useState(task.status);
  const [priority, setPriority] = useState(task.priority);
  const [projectId, setProjectId] = useState<number | undefined>(task.project);
  const [assigneeId, setAssigneeId] = useState<number | undefined>(task.assignee);
  const [deadline, setDeadline] = useState(task.deadline ? task.deadline.split('T')[0] : "");

  const projectMembers = useMemo(() => {
      if (!projectId) return [];
      const project = projects.find(p => p.id === projectId);
      return project?.members || [];
  }, [projectId, projects]);

  useEffect(() => {
    if (isOpen) {
      setTitle(task.title);
      setDescription(task.description || "");
      setStatus(task.status);
      setPriority(task.priority);
      setProjectId(task.project);
      setAssigneeId(task.assignee);
      setDeadline(task.deadline ? task.deadline.split('T')[0] : "");
    }
  }, [isOpen, task]);

  const handleSave = async () => {
    await updateTask(task.id, {
      title,
      description,
      status,
      priority,
      project: projectId,
      assignee: assigneeId,
      deadline: deadline ? `${deadline}T12:00:00Z` : null
    });
    onClose();
  };

  const handleDelete = async () => {
      if (confirm("Ви впевнені, що хочете видалити це завдання?")) {
          await deleteTask(task.id);
          onClose();
      }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Редагувати завдання">
      <div className="flex flex-col gap-5">
        <div className="flex flex-col gap-1.5">
          <label className="typography-label text-text-muted ml-1">Назва</label>
          <input
            type="text"
            className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="typography-label text-text-muted ml-1">Опис</label>
          <textarea
            className="min-h-[100px] w-full rounded-control border border-outline/50 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50 resize-none"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Статус</label>
                <select
                    className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-3 text-text-main outline-none focus:border-primary/50 appearance-none"
                    value={status}
                    onChange={(e) => setStatus(e.target.value as any)}
                >
                    <option value="todo">Треба зробити</option>
                    <option value="in_progress">У процесі</option>
                    <option value="done">Виконано</option>
                </select>
            </div>
            <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Пріоритет</label>
                <select
                    className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-3 text-text-main outline-none focus:border-primary/50 appearance-none"
                    value={priority}
                    onChange={(e) => setPriority(e.target.value as any)}
                >
                    <option value="high">Високий</option>
                    <option value="medium">Середній</option>
                    <option value="low">Низький</option>
                </select>
            </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Проєкт</label>
                <select
                    className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-3 text-text-main outline-none focus:border-primary/50 appearance-none"
                    value={projectId || ""}
                    onChange={(e) => {
                        const pid = e.target.value ? parseInt(e.target.value) : undefined;
                        setProjectId(pid);
                        setAssigneeId(undefined);
                    }}
                >
                    <option value="">Особисте</option>
                    {projects.map(p => (
                        <option key={p.id} value={p.id}>{p.name}</option>
                    ))}
                </select>
            </div>
            <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Виконавець</label>
                <select
                    className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-3 text-text-main outline-none focus:border-primary/50 appearance-none"
                    value={assigneeId || ""}
                    onChange={(e) => setAssigneeId(e.target.value ? parseInt(e.target.value) : undefined)}
                    disabled={!projectId}
                >
                    <option value="">Не призначено</option>
                    {projectMembers.map(m => (
                        <option key={m.id} value={m.user}>{m.user_detail?.first_name || `User ${m.user}`}</option>
                    ))}
                </select>
            </div>
        </div>

        <div className="flex flex-col gap-1.5">
            <label className="typography-label text-text-muted ml-1">Дедлайн</label>
            <div className="relative">
                <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
                <input
                    type="date"
                    className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-3 pl-12 text-text-main outline-none focus:border-primary/50"
                    value={deadline}
                    onChange={(e) => setDeadline(e.target.value)}
                />
            </div>
        </div>

        <div className="flex flex-col gap-3 p-4 bg-surface-container-highest/30 rounded-xl border border-outline/10">
            <span className="typography-label text-text-muted uppercase text-[10px] tracking-widest">Нагадування</span>
            <div className="flex flex-col gap-2">
                {[
                    { id: 'rem_24h', label: 'За 24 години' },
                    { id: 'rem_1h', label: 'За 1 годину' }
                ].map(rem => (
                    <label key={rem.id} className="flex items-center gap-3 cursor-pointer group">
                        <div className="h-5 w-5 rounded border border-outline/30 flex items-center justify-center group-hover:border-primary/50 transition-colors">
                            <Bell size={12} className="text-primary opacity-0 group-has-[:checked]:opacity-100" />
                        </div>
                        <input type="checkbox" className="hidden" />
                        <span className="typography-body-sm text-text-main">{rem.label}</span>
                    </label>
                ))}
            </div>
        </div>

        <div className="flex gap-3 mt-2">
            <Button variant="danger" className="h-14 px-4" onClick={handleDelete}>
                <Trash2 size={20} />
            </Button>
            <Button fullWidth className="h-14" onClick={handleSave}>
                Зберегти зміни
            </Button>
        </div>
      </div>
    </Modal>
  );
}
