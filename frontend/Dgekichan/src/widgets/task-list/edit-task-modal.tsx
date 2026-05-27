import { useState, useEffect, useMemo, useRef } from "react";
import { BottomSheet } from "@/shared/ui/bottom-sheet";
import { Button } from "@/shared/ui/button";
import { useTaskStore } from "@/entities/task/taskStore";
import { useProjectStore } from "@/entities/project/projectStore";
import { CustomCalendar} from "@/pages/stats/components/CustomCalendar";
import { Calendar, Clock, User, Trash2, ChevronRight, Folder, FolderX, Paperclip, X, FileText, Download } from "lucide-react";
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
  const [projectId, setProjectId] = useState<string | undefined>(task.project);
  const [assigneeId, setAssigneeId] = useState<number | undefined>(task.assignee);
  const [deadline, setDeadline] = useState(task.deadline ? task.deadline.substring(0, 16) : "");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [isProjectSheetOpen, setIsProjectSheetOpen] = useState(false);
  const [isAssigneeSheetOpen, setIsAssigneeSheetOpen] = useState(false);
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);

  const selectedProject = useMemo(() =>
    projectId ? projects.find(p => p.id === projectId) : null
  , [projectId, projects]);

  const projectMembers = useMemo(() => {
      return selectedProject?.members || [];
  }, [selectedProject]);

  const selectedAssignee = useMemo(() => {
    return projectMembers.find(m => m.user === assigneeId);
  }, [assigneeId, projectMembers]);

  useEffect(() => {
    if (isOpen) {
      setTitle(task.title);
      setDescription(task.description || "");
      setStatus(task.status);
      setPriority(task.priority);
      setProjectId(task.project);
      setAssigneeId(task.assignee);
      setDeadline(task.deadline ? task.deadline.substring(0, 16) : "");
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
      deadline: deadline ? `${deadline}:00` : undefined
    });
    onClose();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
        const { uploadAttachment } = useTaskStore.getState();
        const newFiles = Array.from(e.target.files);
        for (const file of newFiles) {
            await uploadAttachment(task.id, file);
        }
    }
  };

  const handleDeleteAttachment = async (id: number) => {
      if (confirm("Ви впевнені, що хочете видалити цей файл?")) {
          await useTaskStore.getState().deleteAttachment(id);
      }
  };

  const handleDelete = async () => {
      if (confirm("Ви впевнені, що хочете видалити це завдання?")) {
          await deleteTask(task.id);
          onClose();
      }
  };

  return (
    <>
    <BottomSheet isOpen={isOpen} onClose={onClose} title="Редагувати завдання">
      <div className="flex flex-col gap-5 mt-2 max-h-[70vh] overflow-y-auto px-2 pb-4 no-scrollbar">
        <div className="flex flex-col gap-1.5">
          <label className="typography-label text-text-muted ml-1">Назва</label>
          <input
            type="text"
            className="w-full rounded-2xl border border-outline/30 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50 transition-colors"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="typography-label text-text-muted ml-1">Опис</label>
          <textarea
            className="min-h-[100px] w-full rounded-2xl border border-outline/30 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50 resize-none transition-colors"
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
          
          {/* Контейнер відносного позиціонування для всього блоку */}
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

            {/* Хрестик для швидкого очищення */}
            {deadline && (
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation(); // Щоб не відкривався календар при кліку на хрестик
                  setDeadline("");
                  setIsCalendarOpen(false);
                }}
                className="absolute right-4 top-1/2 -translate-y-1/2 p-1 hover:bg-white/10 rounded-full text-danger transition-colors"
              >
                <X size={16} />
              </button>
            )}

            {/* ПОПОВЕР ПОВЕРХ КОНТЕНТУ (Ефект iOS) */}
            {isCalendarOpen && (
                <>
                  {/* Невидима тапалка на весь екран із затемненням */}
                  <div 
                    className="fixed inset-0 z-40 bg-black/40 backdrop-blur-[2px] transition-opacity animate-in fade-in duration-200" 
                    onClick={() => setIsCalendarOpen(false)} 
                  />

                  {/* Календар, зафіксований точно по центру екрана */}
                  <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
                    <div className="pointer-events-auto w-full max-w-sm animate-in fade-in zoom-in-95 duration-200 dynamic-island-shadow">
                      <CustomCalendar 
                        mode="single"
                        showTime={true} 
                        initialStart={deadline || null}
                        onSelectDate={(selectedDate) => {
                          // Форматуємо в локальний час для Django
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
                <div className="flex flex-col gap-2">
                    {task.attachments?.map((att: any) => (
                        <div key={att.id} className="flex items-center justify-between gap-3 bg-surface-container-high px-4 py-3 rounded-2xl border border-outline/10">
                            <div className="flex items-center gap-3 overflow-hidden">
                                {att.mime_type?.startsWith('image/') ? (
                                    <div className="h-10 w-10 rounded-lg overflow-hidden shrink-0 border border-outline/20">
                                        <img src={att.file_url || att.file} className="h-full w-full object-cover" alt="" />
                                    </div>
                                ) : (
                                    <div className="h-10 w-10 rounded-lg bg-surface-container-highest flex items-center justify-center shrink-0 border border-outline/20">
                                        <FileText size={20} className="text-text-muted" />
                                    </div>
                                )}
                                <div className="flex flex-col overflow-hidden">
                                    <span className="text-sm font-medium truncate">{att.file_name}</span>
                                    <span className="text-[10px] text-text-muted uppercase">{(att.file_size / 1024 / 1024).toFixed(2)} MB</span>
                                </div>
                            </div>
                            <div className="flex items-center gap-1">
                                <a href={att.file_url || att.file} target="_blank" rel="noopener noreferrer" className="p-2 hover:bg-white/10 rounded-full text-primary">
                                    <Download size={18} />
                                </a>
                                <button onClick={() => handleDeleteAttachment(att.id)} className="p-2 hover:bg-white/10 rounded-full text-danger">
                                    <X size={18} />
                                </button>
                            </div>
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

        <div className="flex gap-3 mt-2 px-1">
            <Button variant="ghost" className="h-14 px-5 text-danger border border-danger/20 bg-danger/5 shrink-0" onClick={handleDelete}>
                <Trash2 size={20} />
            </Button>
            <Button className="flex-1 h-14 shadow-lg shadow-primary/20" onClick={handleSave}>
                Зберегти зміни
            </Button>
        </div>
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
              setProjectId(undefined);
              setAssigneeId(undefined);
              setIsProjectSheetOpen(false);
            }}
            className={cn(
              "flex items-center gap-4 w-full rounded-xl p-4 text-left transition-colors",
              projectId === undefined ? "bg-primary/10 border border-primary/20" : "hover:bg-surface-container-highest"
            )}
          >
            <FolderX size={24} className={projectId === undefined ? "text-primary" : "text-text-muted"} />
            <div className="flex flex-col">
                <span className={cn("font-medium", projectId === undefined ? "text-primary" : "text-text-main")}>
                    Особисте
                </span>
            </div>
          </button>

          {projects.map((p) => (
            <button
              key={p.id}
              onClick={() => {
                setProjectId(p.id);
                setAssigneeId(undefined);
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
              setAssigneeId(undefined);
              setIsAssigneeSheetOpen(false);
            }}
            className={cn(
              "flex items-center gap-4 w-full rounded-xl p-4 text-left transition-colors",
              assigneeId === undefined ? "bg-primary/10 border border-primary/20" : "hover:bg-surface-container-highest"
            )}
          >
            <div className="h-10 w-10 rounded-full bg-surface-container-highest border border-outline/20 flex items-center justify-center">
                <User size={20} className="text-text-muted" />
            </div>
            <div className="flex flex-col">
                <span className={cn("font-medium", assigneeId === undefined ? "text-primary" : "text-text-main")}>
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
