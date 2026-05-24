import { TopAppBar } from "@/widgets/top-app-bar";
import { BottomNavigation } from "@/widgets/bottom-navigation";
import { ProjectList } from "@/widgets/project-list/project-list";

export function ProjectsPage() {
  return (
    <div
      className="
        relative
        min-h-screen
        overflow-x-hidden
        bg-background
        text-text-main
      "
    >
      {/* Ambient background glow */}
      <div
        className="
          pointer-events-none
          absolute
          inset-0
          z-0
          opacity-40
        "
      >
        <div
          className="
            absolute
            right-[-100px]
            top-[10%]
            h-[400px]
            w-[400px]
            rounded-full
            blur-3xl
            bg-secondary/10
          "
        />
        <div
          className="
            absolute
            left-[-150px]
            bottom-[20%]
            h-[500px]
            w-[500px]
            rounded-full
            blur-3xl
            bg-primary/5
          "
        />
      </div>

      {/* Top bar */}
      <div className="relative z-30">
        <TopAppBar />
      </div>

      {/* Main content */}
      <main
        className="
          relative
          z-10
          mx-auto
          flex
          w-full
          max-w-md
          flex-col
          px-container-padding
          pt-24
        "
      >
        <section className="animate-in fade-in slide-in-from-bottom-4 duration-700">
           <ProjectList />
        </section>
      </main>

      {/* Navigation */}
      <div className="relative z-30">
        <BottomNavigation />
      </div>
    </div>
  );
}
