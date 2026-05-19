import { TopAppBar } from "@/widgets/top-app-bar";
import { BottomNavigation } from "@/widgets/bottom-navigation";

import { HomeFocusHero } from "@/widgets/home-focus-hero";
import { HomeSmartStart } from "@/widgets/home-smart-start";
import { HomeStyleCard } from "@/widgets/home-style-card";

export function HomePage() {
  return (
    <div
      className="
        relative
        min-h-screen
        overflow-hidden
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
          opacity-60
        "
      >
        <div
          className="
            absolute
            left-[-120px]
            top-[-120px]
            h-[320px]
            w-[320px]
            rounded-full
            blur-3xl
            bg-primary/10
          "
        />

        <div
          className="
            absolute
            bottom-[-180px]
            right-[-100px]
            h-[360px]
            w-[360px]
            rounded-full
            blur-3xl
            bg-secondary/10
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
          gap-stack-md
          px-container-padding
          pb-24
          pt-20
        "
      >
        {/* Smart Start */}
        <section className="animate-in fade-in slide-in-from-top-2 duration-500">
          <HomeSmartStart />
        </section>

        {/* Focus Hero */}
        <section className="animate-in fade-in slide-in-from-bottom-4 duration-700">
          <HomeFocusHero />
        </section>

        {/* Bottom Blocks */}
        <section
          className="
            flex
            flex-col
            gap-stack-md
            animate-in
            fade-in
            slide-in-from-bottom-6
            duration-1000
          "
        >
          <HomeStyleCard />
        </section>
      </main>

      {/* Navigation */}
      <div className="relative z-30">
        <BottomNavigation />
      </div>
    </div>
  );
}