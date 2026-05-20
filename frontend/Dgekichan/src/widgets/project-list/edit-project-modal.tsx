import { useState, useEffect } from "react";
import { UserPlus, Trash2, ChevronDown, Check } from "lucide-react";
import { Modal } from "@/shared/ui/modal";
import { Button } from "@/shared/ui/button";
import { useProjectStore } from "@/entities/project/projectStore";
import type { Project, ProjectMember } from "@/entities/project/projectStore";
import { cn } from "@/shared/lib/cn";
import { BottomSheet } from "@/shared/ui/bottom-sheet";

interface EditProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  project: Project;
}

export function EditProjectModal({ isOpen, onClose, project }: EditProjectModalProps) {
  const { updateProject, addMember, updateMember, removeMember } = useProjectStore();

  const [name, setName] = useState(project.name);
  const [description, setDescription] = useState(project.description || "");
  const [activeTab, setActiveTab] = useState<"details" | "team">("details");

  const [isAddMemberModalOpen, setIsAddMemberModalOpen] = useState(false);
  const [newMemberUsername, setNewMemberUsername] = useState("");

  const [isMemberActionSheetOpen, setIsMemberActionSheetOpen] = useState(false);
  const [selectedMember, setSelectedMember] = useState<ProjectMember | null>(null);
  const [memberLabel, setMemberLabel] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      setName(project.name);
      setDescription(project.description || "");
      setActiveTab("details");
    }
  }, [isOpen, project]);

  const handleSaveDetails = async () => {
    try {
        await updateProject(project.id, { name, description });
        setSuccess("Зміни збережено!");
        setTimeout(() => setSuccess(null), 3000);
        onClose();
    } catch (e) {
        setError("Помилка при збереженні деталей");
        setTimeout(() => setError(null), 3000);
    }
  };

  const handleAddMember = async () => {
    const username = newMemberUsername.trim().replace(/^@/, '');
    if (username) {
      try {
          await addMember(project.id, username);
          setSuccess("Учасника додано!");
          setNewMemberUsername("");
          setIsAddMemberModalOpen(false);
          setTimeout(() => setSuccess(null), 3000);
      } catch (e: any) {
          setError(e.response?.data?.error || "Користувача не знайдено в боті.");
          // If user not found, we show invitation link (handled in modal)
      }
    }
  };

  const handleUpdateMember = async () => {
      if (selectedMember) {
          try {
              await updateMember(project.id, selectedMember.id, {
                  role: selectedMember.role,
                  label: memberLabel
              });
              setSuccess("Учасника оновлено!");
              setIsMemberActionSheetOpen(false);
              setTimeout(() => setSuccess(null), 3000);
          } catch (e) {
              setError("Помилка при оновленні учасника");
              setTimeout(() => setError(null), 3000);
          }
      }
  };

  const handleRemoveMember = async () => {
      if (selectedMember) {
          if (confirm("Ви впевнені, що хочете видалити цього учасника?")) {
              try {
                  await removeMember(project.id, selectedMember.id);
                  setSuccess("Учасника видалено!");
                  setIsMemberActionSheetOpen(false);
                  setTimeout(() => setSuccess(null), 3000);
              } catch (e) {
                  setError("Помилка при видаленні учасника");
                  setTimeout(() => setError(null), 3000);
              }
          }
      }
  };

  return (
    <>
      {/* Toast notifications */}
      <div className="fixed top-4 left-1/2 -translate-x-1/2 z-[100] flex flex-col gap-2 w-full max-w-[320px] pointer-events-none">
        {error && (
            <div className="bg-danger text-white px-4 py-3 rounded-xl shadow-lg animate-in fade-in slide-in-from-top-2 text-center typography-label">
                {error}
            </div>
        )}
        {success && (
            <div className="bg-secondary text-white px-4 py-3 rounded-xl shadow-lg animate-in fade-in slide-in-from-top-2 text-center typography-label">
                {success}
            </div>
        )}
      </div>

      <Modal isOpen={isOpen} onClose={onClose} title="Налаштування проєкту">
        <div className="flex flex-col gap-6">
          <div className="flex border-b border-outline/20">
            {["details", "team"].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab as any)}
                className={cn(
                  "flex-1 pb-3 typography-label transition-all uppercase tracking-wider",
                  activeTab === tab ? "border-b-2 border-primary text-primary" : "text-text-muted"
                )}
              >
                {tab === "details" ? "ДЕТАЛІ" : "КОМАНДА"}
              </button>
            ))}
          </div>

          {activeTab === "details" ? (
            <div className="flex flex-col gap-5">
              <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Назва</label>
                <input
                  type="text"
                  className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="typography-label text-text-muted ml-1">Опис</label>
                <textarea
                  className="min-h-[120px] w-full rounded-control border border-outline/50 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50 resize-none"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
              </div>
              <Button fullWidth className="h-14 mt-2" onClick={handleSaveDetails}>Зберегти зміни</Button>
            </div>
          ) : (
            <div className="flex flex-col gap-4">
              <Button variant="secondary" className="justify-center gap-2 border-dashed h-12" onClick={() => setIsAddMemberModalOpen(true)}>
                <UserPlus size={18} />
                Додати учасника
              </Button>

              <div className="flex flex-col gap-2 max-h-[300px] overflow-y-auto pr-1">
                {project.members?.map((member) => (
                  <div key={member.id} className="flex items-center justify-between rounded-xl bg-surface-container-high/40 p-3 border border-outline/10">
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-full bg-surface-container-highest border border-outline/20 overflow-hidden shrink-0">
                        <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${member.user}`} alt="avatar" />
                      </div>
                      <div className="flex flex-col leading-tight flex-1">
                        <div className="flex items-center gap-2">
                            <span className="typography-body font-medium line-clamp-1">{member.user_detail?.first_name || "Користувач"}</span>
                            {member.label && (
                                <span className="text-[9px] font-bold uppercase text-primary bg-primary/20 px-2 py-0.5 rounded-full border border-primary/30 shadow-[0_0_10px_rgba(59,130,246,0.2)]">
                                    {member.label}
                                </span>
                            )}
                        </div>
                        <div className="flex items-center gap-1.5 mt-0.5">
                           <span className="text-[9px] font-bold uppercase text-text-muted bg-surface-container-highest px-1.5 py-0.5 rounded border border-outline/20">
                             {member.role}
                           </span>
                        </div>
                      </div>
                    </div>

                    <button
                        onClick={() => {
                            setSelectedMember(member);
                            setMemberLabel(member.label || "");
                            setIsMemberActionSheetOpen(true);
                        }}
                        className="p-2 text-text-muted hover:text-text-main transition-colors"
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

      {/* Add Member Modal */}
      <Modal
        isOpen={isAddMemberModalOpen}
        onClose={() => {
            setIsAddMemberModalOpen(false);
            setError(null);
        }}
        title="Додати в команду"
      >
        <div className="flex flex-col gap-4">
          {error && error.includes("не знайдено") && (
              <div className="p-4 bg-primary/5 border border-primary/20 rounded-xl">
                  <p className="typography-body-sm text-primary mb-3">
                      Користувача не знайдено. Надішліть йому посилання для входу в проект:
                  </p>
                  <div className="bg-surface-container-highest p-3 rounded-lg text-[11px] font-mono break-all text-text-main select-all border border-outline/10">
                      https://t.me/dgekichan_bot?start=invite_{project.id}
                  </div>
              </div>
          )}
          <div className="flex flex-col gap-1.5">
             <label className="typography-label text-text-muted ml-1">Username в Telegram</label>
             <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted font-medium">@</span>
                <input
                    autoFocus
                    type="text"
                    className="w-full rounded-control border border-outline/50 bg-surface-container-highest p-4 pl-9 text-text-main outline-none focus:border-primary/50"
                    placeholder="username"
                    value={newMemberUsername}
                    onChange={(e) => {
                        setNewMemberUsername(e.target.value);
                        setError(null);
                    }}
                />
             </div>
          </div>
          <Button fullWidth onClick={handleAddMember} disabled={!newMemberUsername.trim()}>
            Запросити
          </Button>
        </div>
      </Modal>

      {/* Member Action Sheet */}
      <BottomSheet
        isOpen={isMemberActionSheetOpen}
        onClose={() => setIsMemberActionSheetOpen(false)}
        title={selectedMember?.user_detail?.first_name || "Учасник"}
      >
        <div className="flex flex-col gap-6 mt-4">
          <div className="flex flex-col gap-3">
            <span className="typography-label text-text-muted px-2 uppercase text-[10px] tracking-widest">Роль учасника</span>
            <div className="grid grid-cols-2 gap-3">
                {['admin', 'member'].map(role => (
                    <button
                        key={role}
                        className={cn(
                            "flex items-center justify-between rounded-2xl p-4 transition-all border-2",
                            selectedMember?.role === role ? "bg-primary/10 border-primary/40 text-primary" : "bg-surface-container-high border-transparent text-text-muted"
                        )}
                        onClick={() => setSelectedMember(selectedMember ? { ...selectedMember, role: role as any } : null)}
                    >
                        <span className="font-semibold">{role === 'admin' ? 'Адмін' : 'Учасник'}</span>
                        {selectedMember?.role === role && <Check size={18} />}
                    </button>
                ))}
            </div>
          </div>

          <div className="flex flex-col gap-3">
             <span className="typography-label text-text-muted px-2 uppercase text-[10px] tracking-widest">Лейбл (спеціалізація)</span>
             <input
                type="text"
                className="w-full rounded-2xl border border-outline/30 bg-surface-container-highest p-4 text-text-main outline-none focus:border-primary/50"
                placeholder="Наприклад: Програміст"
                value={memberLabel}
                onChange={(e) => setMemberLabel(e.target.value)}
             />
          </div>

          <div className="flex flex-col gap-3">
            <Button fullWidth onClick={handleUpdateMember}>Зберегти зміни учасника</Button>
            <Button variant="ghost" className="text-danger hover:bg-danger/10 gap-2 h-12" onClick={handleRemoveMember}>
                <Trash2 size={18} />
                Вилучити з проєкту
            </Button>
          </div>
        </div>
      </BottomSheet>
    </>
  );
}
