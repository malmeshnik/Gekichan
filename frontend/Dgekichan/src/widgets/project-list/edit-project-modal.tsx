import { useState, useEffect } from "react";
import { UserPlus, Shield, User, Trash2, X, ChevronDown, Check } from "lucide-react";
import { Modal } from "@/shared/ui/modal";
import { Button } from "@/shared/ui/button";
import { useProjectStore, Project } from "@/entities/project/projectStore";
import { cn } from "@/shared/lib/cn";
import { BottomSheet } from "@/shared/ui/bottom-sheet";

interface EditProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  project: Project;
}

export function EditProjectModal({ isOpen, onClose, project }: EditProjectModalProps) {
  const { updateProject } = useProjectStore();

  const [name, setName] = useState(project.name);
  const [description, setDescription] = useState(project.description || "");
  const [activeTab, setActiveTab] = useState<"details" | "team">("details");

  // Mocking members for UI demonstration as they are in project.members if serializer is correct
  const [members, setMembers] = useState<any[]>([]);
  const [isRoleSheetOpen, setIsRoleSheetOpen] = useState(false);
  const [selectedMember, setSelectedMember] = useState<any>(null);

  useEffect(() => {
    if (isOpen) {
      setName(project.name);
      setDescription(project.description || "");
      // @ts-ignore
      setMembers(project.members || []);
    }
  }, [isOpen, project]);

  const handleSave = async () => {
    await updateProject(project.id, { name, description });
    onClose();
  };

  const handleAddMember = () => {
      // Mock logic for adding by username
      const username = prompt("Введіть username користувача:");
      if (username) {
          console.log("Adding member:", username);
      }
  };

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose} title="Налаштування проєкту">
        <div className="flex flex-col gap-6">
          {/* Tabs */}
          <div className="flex border-b border-outline/20">
            <button
              onClick={() => setActiveTab("details")}
              className={cn(
                "flex-1 pb-3 typography-label transition-all",
                activeTab === "details" ? "border-b-2 border-primary text-primary" : "text-text-muted"
              )}
            >
              ДЕТАЛІ
            </button>
            <button
              onClick={() => setActiveTab("team")}
              className={cn(
                "flex-1 pb-3 typography-label transition-all",
                activeTab === "team" ? "border-b-2 border-primary text-primary" : "text-text-muted"
              )}
            >
              КОМАНДА
            </button>
          </div>

          {activeTab === "details" ? (
            <div className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Назва</label>
                <input
                  type="text"
                  className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-3 text-text-main outline-none focus:border-primary/50"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Опис</label>
                <textarea
                  className="min-h-[100px] w-full rounded-control border border-outline/50 bg-surface-container-highest p-3 text-text-main outline-none focus:border-primary/50"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
              </div>
              <Button fullWidth onClick={handleSave}>Зберегти зміни</Button>
            </div>
          ) : (
            <div className="flex flex-col gap-4">
              <Button variant="secondary" className="justify-center gap-2 border-dashed" onClick={handleAddMember}>
                <UserPlus size={18} />
                Додати учасника
              </Button>

              <div className="flex flex-col gap-2">
                {members.map((member: any) => (
                  <div key={member.id} className="flex items-center justify-between rounded-xl bg-surface-container-high/50 p-3">
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-full bg-surface-container-highest overflow-hidden">
                        <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${member.user}`} alt="avatar" />
                      </div>
                      <div className="flex flex-col">
                        <span className="typography-body font-medium">{member.user_detail?.first_name || "Користувач"}</span>
                        <div className="flex items-center gap-1.5">
                           <span className="text-[10px] uppercase text-text-muted bg-surface-container-highest px-1.5 rounded">
                             {member.role}
                           </span>
                           {member.label && (
                             <span className="text-[10px] uppercase text-primary bg-primary/10 px-1.5 rounded">
                               {member.label}
                             </span>
                           )}
                        </div>
                      </div>
                    </div>

                    <button
                        onClick={() => {
                            setSelectedMember(member);
                            setIsRoleSheetOpen(true);
                        }}
                        className="p-2 text-text-muted hover:text-text-main"
                    >
                      <ChevronDown size={18} />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </Modal>

      <BottomSheet
        isOpen={isRoleSheetOpen}
        onClose={() => setIsRoleSheetOpen(false)}
        title="Керування учасником"
      >
        <div className="flex flex-col gap-4 mt-4">
          <div className="flex flex-col gap-2">
            <span className="typography-label text-text-muted px-2">Роль</span>
            <div className="grid grid-cols-2 gap-2">
                {['admin', 'member'].map(role => (
                    <button
                        key={role}
                        className={cn(
                            "flex items-center justify-between rounded-xl p-4 transition-all border",
                            selectedMember?.role === role ? "bg-primary/10 border-primary/30 text-primary" : "bg-surface-container-high border-transparent"
                        )}
                        onClick={() => {
                            console.log("Changing role to:", role);
                            setIsRoleSheetOpen(false);
                        }}
                    >
                        <span className="capitalize">{role === 'admin' ? 'Адмін' : 'Учасник'}</span>
                        {selectedMember?.role === role && <Check size={16} />}
                    </button>
                ))}
            </div>
          </div>

          <div className="flex flex-col gap-2">
             <span className="typography-label text-text-muted px-2">Лейбл (наприклад, Програміст)</span>
             <input
                type="text"
                className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-3 text-text-main outline-none focus:border-primary/50"
                placeholder="Введіть лейбл..."
                defaultValue={selectedMember?.label}
                onBlur={(e) => console.log("Updating label:", e.target.value)}
             />
          </div>

          <Button variant="danger" className="justify-center gap-2 mt-4" onClick={() => setIsRoleSheetOpen(false)}>
            <Trash2 size={18} />
            Вилучити з проєкту
          </Button>
        </div>
      </BottomSheet>
    </>
  );
}
