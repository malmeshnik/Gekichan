import { useState, useEffect, useMemo } from "react";
import { useTaskStore } from "@/entities/task/taskStore";
import { useProjectStore, Project } from "@/entities/project/projectStore";
import { Modal } from "@/shared/ui/modal";
import { BottomSheet } from "@/shared/ui/bottom-sheet";
import { Button } from "@/shared/ui/button";
import { ChevronRight, Folder, FolderX } from "lucide-react";
import { cn } from "@/shared/lib/cn";

interface CreateTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialProjectId?: number | null;
}

export function CreateTaskModal({ isOpen, onClose, initialProjectId }: CreateTaskModalProps) {
  const { fetchTasks } = useTaskStore(); // Ideally we'd have a createTask but useTaskStore is simple now
  const { projects, fetchProjects } = useProjectStore();

  const [title, setTitle] = useState("");
  const [projectId, setProjectId] = useState<number | null>(initialProjectId || null);
  const [isProjectSheetOpen, setIsProjectSheetOpen] = useState(false);

  useEffect(() => {
    if (isOpen && projects.length === 0) fetchProjects();
    if (isOpen) setProjectId(initialProjectId || null);
  }, [isOpen, initialProjectId, projects.length, fetchProjects]);

  const selectedProject = useMemo(() =>
    projectId ? projects.find(p => p.id === projectId) : null
  , [projectId, projects]);

  const handleCreate = async () => {
    // Mocking creation for now as taskStore doesn't have it yet
    console.log("Creating task:", { title, projectId });
    onClose();
    setTitle("");
  };

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose} title="Нове завдання">
        <div className="flex flex-col gap-5">
          <div className="flex flex-col gap-1.5">
            <label className="typography-label text-text-muted ml-1">Що потрібно зробити?</label>
            <textarea
              autoFocus
              className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50 min-h-[100px] resize-none"
              placeholder="Напишіть назву завдання..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="typography-label text-text-muted ml-1">Проєкт</label>
            <button
              onClick={() => setIsProjectSheetOpen(true)}
              className="flex items-center justify-between w-full rounded-control border border-outline/50 bg-surface-container-highest p-4 text-left transition-colors hover:bg-surface-container-high"
            >
              <div className="flex items-center gap-3">
                {selectedProject ? (
                    <Folder size={20} className="text-primary" />
                ) : (
                    <FolderX size={20} className="text-text-muted" />
                )}
                <span className={cn("typography-body", !selectedProject && "text-text-muted")}>
                  {selectedProject?.name || "Без проєкту"}
                </span>
              </div>
              <ChevronRight size={18} className="text-text-muted" />
            </button>
          </div>

          <Button
            fullWidth
            onClick={handleCreate}
            disabled={!title.trim()}
          >
            Створити завдання
          </Button>
        </div>
      </Modal>

      <BottomSheet
        isOpen={isProjectSheetOpen}
        onClose={() => setIsProjectSheetOpen(false)}
        title="Оберіть проєкт"
      >
        <div className="flex flex-col gap-2 mt-2">
          <button
            onClick={() => {
              setProjectId(null);
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
    </>
  );
}
