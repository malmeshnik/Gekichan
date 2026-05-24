import { useState, useEffect, useMemo } from "react";
import { Pause, Play, ChevronDown, Timer } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { ProgressRing } from "@/shared/ui/progress-ring";
import { Button } from "@/shared/ui/button";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { BottomSheet } from "@/shared/ui/bottom-sheet";
import { Modal } from "@/shared/ui/modal";
import { cn } from "@/shared/lib/cn";
import { useSessionStore } from "@/entities/session/sessionStore";
import { useTaskStore } from "@/entities/task/taskStore";

export function HomeFocusHero() {
  const {
    currentSession,
    fetchActiveSession,
    startSession,
    pauseSession,
    resumeSession,
    stopSession
  } = useSessionStore();

  const { tasks, fetchTasks } = useTaskStore();

  const [showTaskSelector, setShowTaskSelector] = useState(false);
  const [showStopConfirm, setShowStopConfirm] = useState(false);
  const [showFinishedModal, setShowFinishedModal] = useState(false);
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);
  const [step, setStep] = useState<"task" | "time">("task");
  const [customMinutes, setCustomMinutes] = useState("");

  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    fetchActiveSession();
    fetchTasks();
  }, [fetchActiveSession, fetchTasks]);

  // Timer logic
  useEffect(() => {
    let interval: any;
    if (currentSession && currentSession.status === "active") {
      const startTime = new Date(currentSession.start_time).getTime();
      const pausedDuration = currentSession.total_paused_duration * 1000;

      const update = () => {
        const now = new Date().getTime();
        const diff = Math.floor((now - startTime - pausedDuration) / 1000);
        setElapsedTime(diff > 0 ? diff : 0);

        // Check if pomodoro finished
        if (currentSession?.target_duration && diff >= currentSession.target_duration) {
            setShowFinishedModal(true);
            clearInterval(interval);
        }
      };

      update();
      interval = setInterval(update, 1000);
    } else if (currentSession && currentSession.status === "paused") {
        const startTime = new Date(currentSession.start_time).getTime();
        const pausedDuration = currentSession.total_paused_duration * 1000;
        const lastPausedAt = currentSession.last_paused_at ? new Date(currentSession.last_paused_at).getTime() : new Date().getTime();
        const diff = Math.floor((lastPausedAt - startTime - pausedDuration) / 1000);
        setElapsedTime(diff > 0 ? diff : 0);
    } else {
      setElapsedTime(0);
    }

    return () => clearInterval(interval);
  }, [currentSession]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const isActive = currentSession?.status === "active";
  const isPomodoro = !!currentSession?.target_duration;

  const displayTime = useMemo(() => {
      if (isPomodoro && currentSession?.target_duration) {
          const remaining = currentSession.target_duration - elapsedTime;
          return formatTime(remaining > 0 ? remaining : 0);
      }
      return formatTime(elapsedTime);
  }, [isPomodoro, currentSession, elapsedTime]);

  const progress = useMemo(() => {
      if (isPomodoro && currentSession?.target_duration) {
          return Math.min((elapsedTime / currentSession.target_duration) * 100, 100);
      }
      return (isActive || currentSession?.status === 'paused') ? (elapsedTime % 3600) / 36 : 0;
  }, [isPomodoro, currentSession, elapsedTime, isActive]);

  const activeTask = useMemo(() => {
    if (!currentSession?.task) return null;
    return tasks.find(t => t.id === currentSession.task);
  }, [currentSession, tasks]);

  const handleToggle = async () => {
    if (!currentSession) {
        setShowTaskSelector(true);
        setStep("task");
        return;
    }

    if (isActive) {
      await pauseSession();
    } else {
      await resumeSession();
    }
  };

  const handleTaskClick = (taskId: number) => {
      setSelectedTaskId(taskId);
      setStep("time");
  };

  const handleStartTime = async (seconds?: number) => {
      if (selectedTaskId) {
          await startSession(selectedTaskId, seconds);
          setShowTaskSelector(false);
          setSelectedTaskId(null);
          setStep("task");
          setCustomMinutes("");
      }
  };

  const confirmStop = async () => {
      await stopSession();
      setShowStopConfirm(false);
      setShowFinishedModal(false);
  };

  const handleAddTime = async (minutes: number) => {
      if (activeTask) {
        await stopSession();
        await startSession(activeTask.id, minutes * 60);
        setShowFinishedModal(false);
      }
  };

  return (
    <section className="flex flex-col items-center justify-center">
      {/* Timer Container */}
      <div
        className="relative group cursor-pointer flex items-center justify-center"
        onClick={handleToggle}
      >
        <ProgressRing
          progress={progress || 0}
          size={200}
          strokeWidth={6}
          glow={isActive}
          className="transition-all duration-1000"
        />

        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <motion.span
            animate={{
              scale: isActive ? 1.02 : 1,
              opacity: isActive ? 1 : 0.8
            }}
            className="typography-display text-text-main"
          >
            {displayTime}
          </motion.span>
          <span className="typography-label text-text-muted mt-2 opacity-60">
            {!currentSession ? "готовий" : isActive ? "в процесі" : "пауза"}
          </span>
        </div>
      </div>

      {/* Active Task Card */}
      <div className="w-full mt-stack-md relative">
        <SurfacePanel
          variant="glass"
          className={cn(
            "flex w-full items-center justify-between border-l-4 p-4 transition-colors",
            activeTask ? "border-l-primary" : "border-l-outline/20"
          )}
          onClick={() => !currentSession && setShowTaskSelector(true)}
        >
          {/* Left */}
          <div className="flex flex-col cursor-pointer">
            <span className="typography-label uppercase text-primary-soft flex items-center gap-1">
              {activeTask ? (activeTask.project_name || "Особисте") : "Оберіть проект"}
              {!currentSession && <ChevronDown size={12} />}
            </span>

            <span className="typography-body-lg font-semibold text-text-main">
              {activeTask?.title || "Оберіть завдання для фокусу"}
            </span>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
              {currentSession && (
                  <Button
                    variant="ghost"
                    className="
                      flex
                      h-10
                      w-10
                      items-center
                      justify-center
                      rounded-full
                      border
                      border-outline/60
                      bg-surface-container-highest
                      text-danger
                      transition-colors
                      hover:bg-danger/10
                    "
                    onClick={(e) => {
                      e.stopPropagation();
                      setShowStopConfirm(true);
                    }}
                  >
                    <motion.div
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      transition={{ duration: 0.2 }}
                      className="flex items-center justify-center"
                    >
                      <div className="h-[18px] w-[18px] rounded-[3px] bg-current" />
                    </motion.div>
                  </Button>
              )}

              <Button
                variant="ghost"
                className={cn(
                  "flex h-10 w-10 items-center justify-center rounded-full border border-outline/60 bg-surface-container-highest text-primary transition-colors hover:bg-surface-container-high",
                  !isActive && currentSession && "text-primary-soft"
                )}
                onClick={(e) => {
                  e.stopPropagation();
                  handleToggle();
                }}
              >
                <AnimatePresence mode="wait">
                  <motion.div
                    key={isActive ? "pause" : "play"}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.8 }}
                    transition={{ duration: 0.2 }}
                  >
                    {isActive ? (
                      <Pause size={18} className="fill-current" />
                    ) : (
                      <Play size={18} className="ml-0.5 fill-current" />
                    )}
                  </motion.div>
                </AnimatePresence>
              </Button>
          </div>
        </SurfacePanel>
      </div>

      {/* Task Selector Bottom Sheet */}
      <BottomSheet
        isOpen={showTaskSelector}
        onClose={() => setShowTaskSelector(false)}
        title={step === "task" ? "Оберіть завдання" : "Налаштуйте час"}
      >
        {step === "task" ? (
            <div className="space-y-2">
                {tasks.filter(t => t.status !== 'done').map((task) => (
                  <div
                    key={task.id}
                    className="p-4 bg-surface-container-highest/50 hover:bg-surface-container-highest rounded-xl cursor-pointer transition-colors border border-outline/10"
                    onClick={() => handleTaskClick(task.id)}
                  >
                    <div className="typography-label text-primary-soft text-[10px] uppercase tracking-wider mb-1">{task.project_name || "Особисте"}</div>
                    <div className="typography-body-lg text-text-main font-medium">{task.title}</div>
                  </div>
                ))}
                {tasks.filter(t => t.status !== 'done').length === 0 && (
                    <p className="text-center text-text-muted py-8">Немає активних завдань</p>
                )}
            </div>
        ) : (
            <div className="space-y-6">
                <div className="grid grid-cols-3 gap-3">
                    {[25, 45, 60].map(mins => (
                        <Button
                            key={mins}
                            variant="secondary"
                            className="flex flex-col py-6 h-auto"
                            onClick={() => handleStartTime(mins * 60)}
                        >
                            <span className="typography-headline-sm">{mins}</span>
                            <span className="typography-label opacity-60">хв</span>
                        </Button>
                    ))}
                </div>

                <div className="flex gap-2">
                    <div className="relative flex-1">
                        <div className="absolute inset-y-0 left-4 flex items-center text-text-muted">
                            <Timer size={18} />
                        </div>
                        <input
                            type="number"
                            placeholder="Власний час (хв)"
                            className="w-full bg-surface-container-highest rounded-xl py-4 pl-12 pr-4 text-text-main outline-none border border-outline/20 focus:border-primary/50"
                            value={customMinutes}
                            onChange={(e) => setCustomMinutes(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                    const val = parseInt(customMinutes);
                                    if (val > 0) handleStartTime(val * 60);
                                }
                            }}
                        />
                    </div>
                    <Button
                        className="h-auto px-6 rounded-xl"
                        disabled={!customMinutes || parseInt(customMinutes) <= 0}
                        onClick={() => {
                            const val = parseInt(customMinutes);
                            if (val > 0) handleStartTime(val * 60);
                        }}
                    >
                        <Play size={20} fill="currentColor" />
                    </Button>
                </div>

                <Button
                    variant="ghost"
                    className="w-full py-4 text-primary-soft"
                    onClick={() => handleStartTime()}
                >
                    Без обмежень (секундомір)
                </Button>
            </div>
        )}
      </BottomSheet>

      {/* Stop Confirmation Modal */}
      <Modal
        isOpen={showStopConfirm}
        onClose={() => setShowStopConfirm(false)}
        title="Зупинити фокус?"
      >
          <p className="text-text-muted mb-6">
              Ви впевнені, що хочете зупинити сесію? Весь накопичений час буде збережено.
          </p>
          <div className="flex gap-3">
              <Button variant="ghost" className="flex-1" onClick={() => setShowStopConfirm(false)}>
                  Скасувати
              </Button>
              <Button variant="primary" className="flex-1 bg-danger text-white border-none" onClick={confirmStop}>
                  Зупинити
              </Button>
          </div>
      </Modal>

      {/* Session Finished Modal */}
      <Modal
        isOpen={showFinishedModal}
        onClose={() => setShowFinishedModal(false)}
        title="Час вичерпано!"
      >
          <div className="flex flex-col items-center text-center">
            <div className="h-20 w-20 rounded-full bg-primary/10 flex items-center justify-center text-primary mb-4">
                <Timer size={40} />
            </div>
            <p className="text-text-main font-medium mb-2">Фокус-сесія завершена</p>
            <p className="text-text-muted mb-8">
                Ви чудово попрацювали! Бажаєте продовжити чи завершити замовлення?
            </p>
          </div>

          <div className="flex flex-col gap-3">
              <div className="grid grid-cols-2 gap-3">
                <Button variant="secondary" onClick={() => handleAddTime(5)}>+5 хв</Button>
                <Button variant="secondary" onClick={() => handleAddTime(15)}>+15 хв</Button>
              </div>
              <Button variant="primary" className="h-14" onClick={confirmStop}>
                  Завершити фокус
              </Button>
          </div>
      </Modal>
    </section>
  );
}
