import { useState, useEffect, useMemo } from "react";
import { Pause, Play, ChevronDown } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { ProgressRing } from "@/shared/ui/progress-ring";
import { Button } from "@/shared/ui/button";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { cn } from "@/shared/lib/cn";
import { useSessionStore } from "@/entities/session/sessionStore";
import { useTaskStore } from "@/entities/task/taskStore";

export function HomeFocusHero() {
  const {
    currentSession,
    fetchActiveSession,
    startSession,
    pauseSession,
    resumeSession
  } = useSessionStore();

  const { tasks, fetchTasks } = useTaskStore();
  const [showTaskSelector, setShowTaskSelector] = useState(false);
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
      };

      update();
      interval = setInterval(update, 1000);
    } else if (currentSession && currentSession.status === "paused") {
        // Calculate elapsed time up to last_paused_at
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
  const activeTask = useMemo(() => {
    if (!currentSession?.task) return null;
    return tasks.find(t => t.id === currentSession.task);
  }, [currentSession, tasks]);

  const handleToggle = async () => {
    if (!currentSession) {
        if (tasks.length > 0) {
            setShowTaskSelector(true);
        } else {
            alert("Спочатку створіть завдання");
        }
        return;
    }

    if (isActive) {
      await pauseSession();
    } else {
      await resumeSession();
    }
  };

  const handleSelectTask = async (taskId: number) => {
    await startSession(taskId);
    setShowTaskSelector(false);
  };

  return (
    <section className="flex flex-col items-center justify-center">
      {/* Timer Container */}
      <div
        className="relative group cursor-pointer flex items-center justify-center"
        onClick={handleToggle}
      >
        <ProgressRing
          progress={isActive ? (elapsedTime % 3600) / 36 : 75}
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
            {formatTime(elapsedTime)}
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
          onClick={() => setShowTaskSelector(!showTaskSelector)}
        >
          {/* Left */}
          <div className="flex flex-col cursor-pointer">
            <span className="typography-label uppercase text-primary-soft flex items-center gap-1">
              {activeTask?.project_name || "Особисте"}
              <ChevronDown size={12} />
            </span>

            <span className="typography-body-lg font-semibold text-text-main">
              {activeTask?.title || "Оберіть завдання для фокусу"}
            </span>
          </div>

          {/* Action */}
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
        </SurfacePanel>

        {/* Task Selector Dropdown (Simplified Bottom Sheet for now) */}
        <AnimatePresence>
          {showTaskSelector && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="absolute left-0 right-0 top-full mt-2 z-40"
            >
              <SurfacePanel variant="glass" className="p-2 max-h-60 overflow-y-auto shadow-2xl border border-outline/30">
                {tasks.filter(t => t.status !== 'done').length === 0 && (
                    <div className="p-4 text-center text-text-muted">Немає доступних завдань</div>
                )}
                {tasks.filter(t => t.status !== 'done').map((task) => (
                  <div
                    key={task.id}
                    className="p-3 hover:bg-surface-container-highest rounded-lg cursor-pointer transition-colors"
                    onClick={() => handleSelectTask(task.id)}
                  >
                    <div className="typography-label text-primary-soft text-[10px]">{task.project_name || "Особисте"}</div>
                    <div className="typography-body-md text-text-main">{task.title}</div>
                  </div>
                ))}
              </SurfacePanel>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </section>
  );
}
