import { TopAppBar } from "@/widgets/top-app-bar";
import { BottomNavigation } from "@/widgets/bottom-navigation";
import { HomeFocusHero } from "@/widgets/home-focus-hero";
import { HomeSmartStart } from "@/widgets/home-smart-start";
import { HomeDayGrid } from "@/widgets/home-day-grid";
import { HomeCompetition } from "@/widgets/home-competition";
import { HomeStyleCard } from "@/widgets/home-style-card";

export function HomePage() {
  return (
    <div className="min-h-screen bg-background pb-44 pt-24">
      <TopAppBar />

      <main className="px-6 flex flex-col gap-12 max-w-md mx-auto w-full">
        <HomeFocusHero />

        <div className="flex flex-col gap-10">
          <HomeSmartStart />
          <HomeDayGrid />
          <HomeCompetition />
          <HomeStyleCard />
        </div>
      </main>

      <BottomNavigation />
    </div>
  );
}
