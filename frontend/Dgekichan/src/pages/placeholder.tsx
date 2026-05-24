import { SurfacePanel } from "@/shared/ui/surface-panel";
import { BottomNavigation } from "@/widgets/bottom-navigation";

export function PlaceholderPage({ title }: { title: string }) {
  return (
    <div className="min-h-screen bg-background text-text-main flex flex-col">
      <main className="flex-1 flex items-center justify-center p-6">
        <SurfacePanel variant="glass" className="p-10 text-center">
            <h1 className="typography-headline-lg">{title}</h1>
            <p className="text-text-muted mt-2">Ця сторінка в розробці</p>
        </SurfacePanel>
      </main>
      <BottomNavigation />
    </div>
  );
}
