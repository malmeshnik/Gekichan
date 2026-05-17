import { TopAppBar } from "@/widgets/top-app-bar";
import { BottomNavigation } from "@/widgets/bottom-navigation";
import { HomeFocusHero } from "@/widgets/home-focus-hero";
import { HomeSmartStart } from "@/widgets/home-smart-start";
import { HomeDayGrid } from "@/widgets/home-day-grid";
import { HomeCompetition } from "@/widgets/home-competition";
import { HomeStyleCard } from "@/widgets/home-style-card";

export function HomePage() {
  return (
    <div className="min-h-screen bg-background pb-40 pt-20">
      <TopAppBar />

      <main className="section-padding stack-lg max-w-md mx-auto w-full">
        <HomeFocusHero />
        <HomeSmartStart />
        <HomeDayGrid />
        <HomeCompetition />
        <HomeStyleCard />
      </main>

      <BottomNavigation />
    </div>
  );
}
