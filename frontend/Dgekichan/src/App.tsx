import { Button } from "@/shared/ui/button";

import { SurfacePanel } from "@/shared/ui/surface-panel";

export default function App() {
  return (
    <div className="min-h-dvh bg-background section-padding stack-md">
      <h1 className="typography-display-mobile text-text-main">
        TaskCommand
      </h1>

      <SurfacePanel
        variant="glass"
        glow="primary"
        className="section-padding stack-sm"
      >
        <h2 className="typography-headline-sm text-text-main">
          Active Session
        </h2>

        <p className="typography-body text-text-muted">
          Deep work in progress
        </p>

        <Button>
          Start Focus
        </Button>
      </SurfacePanel>
    </div>
  );
}