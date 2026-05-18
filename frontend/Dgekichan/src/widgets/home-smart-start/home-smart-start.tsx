import { Rocket } from "lucide-react";

import { SurfacePanel } from "@/shared/ui/surface-panel";

export function HomeSmartStart() {
  return (
    <SurfacePanel
      variant="glass"
      className="
        mt-stack-md

        flex
        flex-col

        gap-stack-sm

        p-4
      "
    >
      {/* Top */}
      <div
        className="
          flex
          items-start
          justify-between
        "
      >
        {/* Left */}
        <div>
          <h2
            className="
              typography-headline-sm

              text-primary-soft
            "
          >
            Розумний Старт
          </h2>

          <p
            className="
              typography-body-md

              text-text-muted
            "
          >
            Вчора 2.8г, Ціль 3г
          </p>
        </div>

        {/* Icon */}
        <div
          className="
            rounded-lg

            bg-surface-container-highest

            p-2

            text-primary
          "
        >
          <Rocket size={20} />
        </div>
      </div>

      {/* Progress */}
      <div
        className="
          mt-2

          h-2
          w-full

          overflow-hidden

          rounded-full

          bg-surface-container-highest
        "
      >
        <div
          className="
            h-full

            rounded-full

            bg-[linear-gradient(90deg,#4cd6ff_0%,#ddb7ff_100%)]
          "
          style={{
            width: "85%",
          }}
        />
      </div>

      {/* Bottom */}
      <p
        className="
          mt-1

          text-right

          typography-label

          text-text-main
        "
      >
        Залишилося 15 хв
      </p>
    </SurfacePanel>
  );
}