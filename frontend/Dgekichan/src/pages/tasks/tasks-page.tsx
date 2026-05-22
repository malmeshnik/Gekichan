import { useSearchParams } from "react-router-dom";
import { TopAppBar } from "@/widgets/top-app-bar";
import { BottomNavigation } from "@/widgets/bottom-navigation";
import { TaskList } from "@/widgets/task-list/task-list";

export function TasksPage() {
  const [searchParams] = useSearchParams();
  const projectId = searchParams.get("projectId") || searchParams.get("project");

  return (
    <div className="relative min-h-screen overflow-x-hidden bg-background text-text-main">
      <div className="pointer-events-none absolute inset-0 z-0 opacity-40">
        <div className="absolute left-[-100px] top-[10%] h-[400px] w-[400px] rounded-full blur-3xl bg-primary/10" />
      </div>

      <div className="relative z-30">
        <TopAppBar />
      </div>

      <main className="relative z-10 mx-auto flex w-full max-w-md flex-col px-container-padding pt-24">
        <section className="animate-in fade-in slide-in-from-bottom-4 duration-700">
           <TaskList projectId={projectId ?? null} />
        </section>
      </main>

      <div className="relative z-30">
        <BottomNavigation />
      </div>
    </div>
  );
}
