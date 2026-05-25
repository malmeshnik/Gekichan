import { useState, useEffect, useMemo, useRef } from "react";
import { useTaskStore } from "@/entities/task/taskStore";
import { apiClient } from "@/shared/api/client";
import { useProjectStore } from "@/entities/project/projectStore";
import { BottomSheet } from "@/shared/ui/bottom-sheet";
import { Button } from "@/shared/ui/button";
import { CustomCalendar } from "@/pages/stats/components/CustomCalendar";
import { 
  ChevronRight, Folder, FolderX, Calendar, Clock, 
  User, Paperclip, X, FileText, Image as ImageIcon 
} from "lucide-react";
import { cn } from "@/shared/lib/cn";

interface CreateTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialProjectId?: number | null;
}

export function CreateTaskModal({ isOpen, onClose, initialProjectId }: CreateTaskModalProps) {
  const { projects, fetchProjects } = useProjectStore();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<"low" | "medium" | "high">("medium");
  const [status, setStatus] = useState<"todo" | "in_progress" | "done">("todo");
  const [projectId, setProjectId] = useState<number | null>(initialProjectId || null);
  const [assigneeId, setAssigneeId] = useState<number | null>(null);
  const [deadline, setDeadline] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [isProjectSheetOpen, setIsProjectSheetOpen] = useState(false);
  const [isAssigneeSheetOpen, setIsAssigneeSheetOpen] = useState(false);
  const [isCalendarOpen, setIsCalendarOpen] = useState(false); // Стейт для нашого iOS поповера

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
        setFiles([]);
        setIsCalendarOpen(false); // Закриваємо календар при чистому відкритті модалки
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
        const { uploadAttachment } = useTaskStore.getState();

        // Django зазвичай очікує ISO формат локального або Z-часу
        const response = await apiClient.post("/tasks/", {
            title: title.trim(),
            description: description.trim(),
            priority,
            project: projectId || undefined,
            status,
            assignee: assigneeId || undefined,
            deadline: deadline ? new Date(deadline).toISOString() : undefined
        });

        const newTask = response.data;

        for (const file of files) {
            await uploadAttachment(newTask.id, file);
        }

        const currentActiveFilter = (document.querySelector('[data-active-filter]') as any)?.dataset?.filter || "all";
        await useTaskStore.getState().fetchTasks(projectId ? { project: projectId, period: currentActiveFilter } : { period: currentActiveFilter });

        onClose();
    } catch (error) {
        console.error("Failed to create task", error);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
        const newFiles = Array.from(e.target.files);
        setFiles(prev => [...prev, ...newFiles]);
    }
  };

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
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

          {/* НОВИЙ БЛОК ДЕДЛАЙНУ З iOS ПОПОВЕРОМ */}
          <div className="flex flex-col gap-1.5">
            <label className="typography-label text-text-muted ml-1">Дедлайн</label>
            <div className="relative">
                {/* Кнопка-тригер */}
                <button
                  type="button"
                  onClick={() => setIsCalendarOpen(!isCalendarOpen)}
                  className={cn(
                    "w-full flex items-center gap-3 rounded-2xl border border-outline/30 bg-surface-container-highest p-4 text-left transition-colors hover:bg-surface-container-high",
                    isCalendarOpen && "border-primary/50"
                  )}
                >
                  <Calendar size={18} className={deadline ? "text-primary" : "text-text-muted"} />
                  <span className={cn("typography-body-sm", !deadline && "text-text-muted")}>
                    {deadline ? (
                      <span className="flex items-center gap-2">
                        {new Date(deadline).toLocaleDateString('uk-UA', { day: 'numeric', month: 'long', year: 'numeric' })}
                        <span className="text-text-muted/40">|</span>
                        <Clock size={14} className="text-text-muted" />
                        {new Date(deadline).toLocaleTimeString('uk-UA', { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    ) : (
                      "Встановити дедлайн"
                    )}
                  </span>
                </button>

                {/* Швидке видалення дедлайну */}
                {deadline && (
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation(); // Щоб не відкривався календар
                      setDeadline("");
                      setIsCalendarOpen(false);
                    }}
                    className="absolute right-4 top-1/2 -translate-y-1/2 p-1 hover:bg-white/10 rounded-full text-danger transition-colors"
                  >
                    <X size={16} />
                  </button>
                )}

                {/* ПОВНІСТЮ СТАТИЧНИЙ iOS ПОПОВЕР СУВОРO ПО ЦЕНТРУ ЕКРАНА */}
                {isCalendarOpen && (
                  <>
                    {/* Backdrop */}
                    <div 
                      className="fixed inset-0 z-[100] bg-black/40 backdrop-blur-[2px] transition-opacity animate-in fade-in duration-200" 
                      onClick={() => setIsCalendarOpen(false)} 
                    />

                    {/* Центрований контейнер */}
                    <div className="fixed inset-0 z-[101] flex items-center justify-center p-4 pointer-events-none">
                      <div className="pointer-events-auto w-full max-w-sm animate-in fade-in zoom-in-95 duration-200 shadow-2xl">
                        <CustomCalendar 
                          mode="single"
                          showTime={true} 
                          initialStart={deadline || null}
                          onSelectDate={(selectedDate) => {
                            // Переводимо у формат ISO без літери Z (локальний час для Django)
                            const offset = selectedDate.getTimezoneOffset() * 60000;
                            const localISOTime = new Date(selectedDate.getTime() - offset).toISOString().slice(0, 19);
                            
                            setDeadline(localISOTime); 
                            setIsCalendarOpen(false);
                          }}
                        />
                      </div>
                    </div>
                  </>
                )}
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="typography-label text-text-muted ml-1">Атачменти (макс. 10МБ)</label>
            <div className="flex flex-col gap-2">
                <div className="flex flex-wrap gap-2">
                    {files.map((file, index) => (
                        <div key={index} className="flex items-center gap-2 bg-surface-container-high px-3 py-2 rounded-xl border border-outline/10 max-w-full">
                            {file.type.startsWith('image/') ? <ImageIcon size={14} className="text-primary" /> : <FileText size={14} className="text-text-muted" />}
                            <span className="text-xs truncate max-w-[150px]">{file.name}</span>
                            <button onClick={() => removeFile(index)} className="p-1 hover:bg-white/10 rounded-full">
                                <X size={14} className="text-danger" />
                            </button>
                        </div>
                    ))}
                </div>
                <button
                    onClick={() => fileInputRef.current?.click()}
                    className="flex items-center justify-center gap-2 w-full rounded-2xl border border-dashed border-outline/30 bg-surface-container-highest/50 p-4 text-text-muted hover:border-primary/50 hover:bg-primary/5 transition-all"
                >
                    <Paperclip size={18} />
                    <span className="typography-body-sm">Додати файли</span>
                </button>
                <input
                    type="file"
                    ref={fileInputRef}
                    className="hidden"
                    multiple
                    onChange={handleFileChange}
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

      {/* Проєкт Sheet */}
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

      {/* Виконавець Sheet */}
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