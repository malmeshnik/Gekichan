import { useState, useEffect, useMemo } from "react";
import { useTaskStore } from "@/entities/task/taskStore";
import { useProjectStore } from "@/entities/project/projectStore";
import { BottomSheet } from "@/shared/ui/bottom-sheet";
import { Button } from "@/shared/ui/button";
import { ChevronRight, Folder, FolderX, Calendar, User } from "lucide-react";
import { cn } from "@/shared/lib/cn";

interface CreateTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialProjectId?: number | null;
}

export function CreateTaskModal({ isOpen, onClose, initialProjectId }: CreateTaskModalProps) {
  const { createTask } = useTaskStore();
  const { projects, fetchProjects } = useProjectStore();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<"low" | "medium" | "high">("medium");
  const [status, setStatus] = useState<"todo" | "in_progress" | "done">("todo");
  const [projectId, setProjectId] = useState<number | null>(initialProjectId || null);
  const [assigneeId, setAssigneeId] = useState<number | null>(null);
  const [deadline, setDeadline] = useState("");

  const [isProjectSheetOpen, setIsProjectSheetOpen] = useState(false);
  const [isAssigneeSheetOpen, setIsAssigneeSheetOpen] = useState(false);

  useEffect(() => {
    if (isOpen && projects.length === 0) fetchProjects();
    if (isOpen) {
        setProjectId(initialProjectId || null);
        setTitle("");
        setDescription("");
        setPriority("medium");
        setStatus("todo");
        setAssigneeId(null);
        setDeadline("");
    }
  }, [isOpen, initialProjectId, projects.length, fetchProjects]);

  const selectedProject = useMemo(() =>
    projectId ? projects.find(p => p.id === projectId) : null
  , [projectId, projects]);

  const projectMembers = useMemo(() => {
    return selectedProject?.members || [];
  }, [selectedProject]);

  const selectedAssignee = useMemo(() => {
    return projectMembers.find(m => m.user === assigneeId);
  }, [assigneeId, projectMembers]);

  const handleCreate = async () => {
    try {
        await createTask({
            title: title.trim(),
            description: description.trim(),
            priority,
            project: projectId || undefined,
            status,
            assignee: assigneeId || undefined,
            deadline: deadline ? `${deadline}T12:00:00Z` : undefined
        });
        onClose();
    } catch (error) {
        console.error("Failed to create task", error);
    }
  };

  return (
    <>
      <BottomSheet isOpen={isOpen} onClose={onClose} title="Нове завдання">
        <div className="flex flex-col gap-5 mt-2 max-h-[70vh] overflow-y-auto px-1 pb-4 no-scrollbar">
          <div className="flex flex-col gap-1.5">
            <label className="typography-label text-text-muted ml-1">Що потрібно зробити?</label>
            <input
              autoFocus
              className="w-full rounded-2xl border border-outline/30 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50 transition-colors"
              placeholder="Назва завдання..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="typography-label text-text-muted ml-1">Опис (необов'язково)</label>
            <textarea
              className="w-full rounded-2xl border border-outline/30 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50 min-h-[100px] resize-none transition-colors"
              placeholder="Додайте деталі..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Статус</label>
                <div className="relative">
                    <select
                        className="w-full rounded-2xl border border-outline/30 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50 appearance-none transition-colors"
                        value={status}
                        onChange={(e) => setStatus(e.target.value as any)}
                    >
                        <option value="todo">Треба зробити</option>
                        <option value="in_progress">У процесі</option>
                        <option value="done">Виконано</option>
                    </select>
                    <ChevronRight size={18} className="absolute right-4 top-1/2 -translate-y-1/2 rotate-90 text-text-muted pointer-events-none" />
                </div>
            </div>
            <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Пріоритет</label>
                <div className="relative">
                    <select
                        className={cn(
                            "w-full rounded-2xl border border-outline/30 bg-surface-container-highest p-4 outline-none focus:border-primary/50 appearance-none transition-colors font-medium",
                            priority === 'high' ? "text-danger" : priority === 'medium' ? "text-primary" : "text-text-muted"
                        )}
                        value={priority}
                        onChange={(e) => setPriority(e.target.value as any)}
                    >
                        <option value="high">Високий</option>
                        <option value="medium">Середній</option>
                        <option value="low">Низький</option>
                    </select>
                    <ChevronRight size={18} className="absolute right-4 top-1/2 -translate-y-1/2 rotate-90 text-text-muted pointer-events-none" />
                </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Проєкт</label>
                <button
                  onClick={() => setIsProjectSheetOpen(true)}
                  className="flex items-center justify-between w-full rounded-2xl border border-outline/30 bg-surface-container-highest p-4 text-left transition-colors hover:bg-surface-container-high"
                >
                  <div className="flex items-center gap-2 overflow-hidden">
                    {selectedProject ? (
                        <Folder size={18} className="text-primary shrink-0" />
                    ) : (
                        <FolderX size={18} className="text-text-muted shrink-0" />
                    )}
                    <span className={cn("typography-body-sm truncate", !selectedProject && "text-text-muted")}>
                      {selectedProject?.name || "Особисте"}
                    </span>
                  </div>
                </button>
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Виконавець</label>
                <button
                  disabled={!projectId}
                  onClick={() => setIsAssigneeSheetOpen(true)}
                  className={cn(
                      "flex items-center justify-between w-full rounded-2xl border border-outline/30 bg-surface-container-highest p-4 text-left transition-colors",
                      projectId ? "hover:bg-surface-container-high" : "opacity-50 cursor-not-allowed"
                  )}
                >
                  <div className="flex items-center gap-2 overflow-hidden">
                    <User size={18} className={cn("shrink-0", selectedAssignee ? "text-primary" : "text-text-muted")} />
                    <span className={cn("typography-body-sm truncate", !selectedAssignee && "text-text-muted")}>
                      {selectedAssignee?.user_detail?.first_name || "Немає"}
                    </span>
                  </div>
                </button>
              </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="typography-label text-text-muted ml-1">Дедлайн</label>
            <div className="relative">
                <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
                <input
                    type="date"
                    className="w-full rounded-2xl border border-outline/30 bg-surface-container-highest p-4 pl-12 text-text-main outline-none focus:border-primary/50 transition-colors"
                    value={deadline}
                    onChange={(e) => setDeadline(e.target.value)}
                />
            </div>
          </div>

          <Button
            fullWidth
            className="h-14 mt-2 shadow-lg shadow-primary/20"
            onClick={handleCreate}
            disabled={!title.trim()}
          >
            Створити завдання
          </Button>
        </div>
      </BottomSheet>

      <BottomSheet
        isOpen={isProjectSheetOpen}
        onClose={() => setIsProjectSheetOpen(false)}
        title="Оберіть проєкт"
      >
        <div className="flex flex-col gap-2 mt-2 max-h-[50vh] overflow-y-auto no-scrollbar pb-4">
          <button
            onClick={() => {
              setProjectId(null);
              setAssigneeId(null);
              setIsProjectSheetOpen(false);
            }}
            className={cn(
              "flex items-center gap-4 w-full rounded-xl p-4 text-left transition-colors",
              projectId === null ? "bg-primary/10 border border-primary/20" : "hover:bg-surface-container-highest"
            )}
          >
            <FolderX size={24} className={projectId === null ? "text-primary" : "text-text-muted"} />
            <div className="flex flex-col">
                <span className={cn("font-medium", projectId === null ? "text-primary" : "text-text-main")}>
                    Без проєкту
                </span>
                <span className="text-[10px] uppercase text-text-muted">Особисте завдання</span>
            </div>
          </button>

          {projects.map((p) => (
            <button
              key={p.id}
              onClick={() => {
                setProjectId(p.id);
                setAssigneeId(null);
                setIsProjectSheetOpen(false);
              }}
              className={cn(
                "flex items-center gap-4 w-full rounded-xl p-4 text-left transition-colors",
                projectId === p.id ? "bg-primary/10 border border-primary/20" : "hover:bg-surface-container-highest"
              )}
            >
              <Folder size={24} className={projectId === p.id ? "text-primary" : "text-text-muted"} />
              <div className="flex flex-col">
                <span className={cn("font-medium", projectId === p.id ? "text-primary" : "text-text-main")}>
                    {p.name}
                </span>
                <span className="text-[10px] uppercase text-text-muted">{p.tasks_count} завдань</span>
              </div>
            </button>
          ))}
        </div>
      </BottomSheet>

      <BottomSheet
        isOpen={isAssigneeSheetOpen}
        onClose={() => setIsAssigneeSheetOpen(false)}
        title="Оберіть виконавця"
      >
        <div className="flex flex-col gap-2 mt-2 max-h-[50vh] overflow-y-auto no-scrollbar pb-4">
          <button
            onClick={() => {
              setAssigneeId(null);
              setIsAssigneeSheetOpen(false);
            }}
            className={cn(
              "flex items-center gap-4 w-full rounded-xl p-4 text-left transition-colors",
              assigneeId === null ? "bg-primary/10 border border-primary/20" : "hover:bg-surface-container-highest"
            )}
          >
            <div className="h-10 w-10 rounded-full bg-surface-container-highest border border-outline/20 flex items-center justify-center">
                <User size={20} className="text-text-muted" />
            </div>
            <div className="flex flex-col">
                <span className={cn("font-medium", assigneeId === null ? "text-primary" : "text-text-main")}>
                    Не призначено
                </span>
            </div>
          </button>

          {projectMembers.map((m) => (
            <button
              key={m.id}
              onClick={() => {
                setAssigneeId(m.user);
                setIsAssigneeSheetOpen(false);
              }}
              className={cn(
                "flex items-center gap-4 w-full rounded-xl p-4 text-left transition-colors",
                assigneeId === m.user ? "bg-primary/10 border border-primary/20" : "hover:bg-surface-container-highest"
              )}
            >
              <div className="h-10 w-10 rounded-full bg-surface-container-highest border border-outline/20 overflow-hidden">
                <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${m.user}`} alt="avatar" />
              </div>
              <div className="flex flex-col">
                <span className={cn("font-medium", assigneeId === m.user ? "text-primary" : "text-text-main")}>
                    {m.user_detail?.first_name || `User ${m.user}`}
                </span>
                <span className="text-[10px] uppercase text-text-muted">{m.role}</span>
              </div>
            </button>
          ))}
        </div>
      </BottomSheet>
    </>
  );
}
