import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Edit2, Trash2 } from "lucide-react";
import { useProjectStore } from "@/entities/project/projectStore";
import type { Project } from "@/entities/project/projectStore";
import { ProjectCard } from "./project-card";
import { CreateProjectCard } from "./create-project-card";
import { Modal } from "@/shared/ui/modal";
import { Button } from "@/shared/ui/button";
import { cn } from "@/shared/lib/cn";
import { EditProjectModal } from "./edit-project-modal";

export function ProjectList() {
  const { projects, fetchProjects, createProject, deleteProject, isLoading } = useProjectStore();
  const [activeTab, setActiveTab] = useState<"active" | "completed">("active");

  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [isActionModalOpen, setIsActionModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [newProjectName, setNewProjectName] = useState("");
  const [newProjectDesc, setNewProjectDesc] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const filteredProjects = projects.filter((project) => {
    const isCompleted = project.done_tasks_count > 0 && project.done_tasks_count === project.tasks_count;
    return activeTab === "active" ? !isCompleted : isCompleted;
  });

  const handleAction = (e: React.MouseEvent, project: Project) => {
    e.stopPropagation();
    setSelectedProject(project);
    setIsActionModalOpen(true);
  };

  const handleDelete = async () => {
    if (selectedProject) {
      await deleteProject(selectedProject.id);
      setIsActionModalOpen(false);
      setSelectedProject(null);
    }
  };

  const handleCreate = async () => {
    if (newProjectName.trim()) {
      await createProject({ name: newProjectName, description: newProjectDesc });
      setIsCreateModalOpen(false);
      setNewProjectName("");
      setNewProjectDesc("");
    }
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Page Title */}
      <h1 className="typography-headline-lg px-2">Проєкти</h1>

      {/* Tabs */}
      <div className="flex rounded-xl bg-surface-container-low p-1 mx-2">
        <button
          onClick={() => setActiveTab("active")}
          className={cn(
            "flex-1 rounded-lg py-2.5 typography-label transition-all",
            activeTab === "active"
              ? "bg-surface-container-highest text-text-main shadow-sm"
              : "text-text-muted hover:text-text-main"
          )}
        >
          АКТИВНІ
        </button>
        <button
          onClick={() => setActiveTab("completed")}
          className={cn(
            "flex-1 rounded-lg py-2.5 typography-label transition-all",
            activeTab === "completed"
              ? "bg-surface-container-highest text-text-main shadow-sm"
              : "text-text-muted hover:text-text-main"
          )}
        >
          ЗАВЕРШЕНІ
        </button>
      </div>

      {/* Grid */}
      <div className="flex flex-col gap-4 pb-24">
        {activeTab === "active" && (
           <CreateProjectCard onClick={() => setIsCreateModalOpen(true)} />
        )}

        {isLoading ? (
          <div className="flex justify-center py-10 text-text-muted">Завантаження...</div>
        ) : filteredProjects.length > 0 ? (
          filteredProjects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onClick={() => navigate(`/tasks?project=${project.id}`)}
              onAction={(e) => handleAction(e, project)}
            />
          ))
        ) : (
          <div className="flex flex-col items-center justify-center py-12 text-center text-text-muted">
            <p>Проєктів не знайдено</p>
          </div>
        )}
      </div>

      {/* Create Modal */}
      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Новий проєкт"
      >
        <div className="flex flex-col gap-5">
          <div className="flex flex-col gap-1.5">
            <label className="typography-label text-text-muted ml-1">Назва проєкту</label>
            <input
              autoFocus
              type="text"
              className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50"
              placeholder="Наприклад: Obsidian App"
              value={newProjectName}
              onChange={(e) => setNewProjectName(e.target.value)}
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="typography-label text-text-muted ml-1">Опис (опціонально)</label>
            <textarea
              className="min-h-[120px] w-full rounded-control border border-outline/50 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50 resize-none"
              placeholder="Коротко про цілі проєкту..."
              value={newProjectDesc}
              onChange={(e) => setNewProjectDesc(e.target.value)}
            />
          </div>
          <Button
            className="mt-2 h-14"
            fullWidth
            onClick={handleCreate}
            disabled={!newProjectName.trim()}
          >
            Створити проєкт
          </Button>
        </div>
      </Modal>

      {/* Action Modal */}
      <Modal
        isOpen={isActionModalOpen}
        onClose={() => setIsActionModalOpen(false)}
        title={selectedProject?.name}
      >
        <div className="flex flex-col gap-3">
          <Button
            variant="secondary"
            className="justify-start gap-3 h-14"
            onClick={() => {
                setIsActionModalOpen(false);
                setIsEditModalOpen(true);
            }}
          >
            <Edit2 size={20} className="text-primary" />
            Редагувати проєкт
          </Button>
          <Button
            variant="danger"
            className="justify-start gap-3 h-14"
            onClick={handleDelete}
          >
            <Trash2 size={20} />
            Видалити проєкт
          </Button>
        </div>
      </Modal>

      {selectedProject && (
          <EditProjectModal
            isOpen={isEditModalOpen}
            onClose={() => setIsEditModalOpen(false)}
            project={selectedProject}
          />
      )}
    </div>
  );
}
