import { Shield, ChevronRight } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";

export function HomeStyleCard() {
  return (
    <div className="w-full">
      <SurfacePanel
        variant="glass"
        className="
          flex
          items-center
          justify-between

          border-l-4
          border-l-secondary

          p-4
        "
      >
        {/* Left */}
        <div
          className="
            flex
            items-center
            gap-3
          "
        >
          {/* Icon */}
          <div
            className="
              flex
              h-12
              w-12
              items-center
              justify-center

              rounded-full

              bg-secondary/15

              text-secondary
            "
          >
            <Shield size={24} />
          </div>

          {/* Content */}
          <div
            className="
              flex
              flex-col
            "
          >
            <span
              className="
                typography-label

                uppercase

                text-text-muted
              "
            >
              Твій Стиль
            </span>

            <span
              className="
                typography-body-lg

                font-semibold

                text-text-main
              "
            >
              Стабільний Виконавець
            </span>
          </div>
        </div>

        {/* Action */}
        <button
          className="
            text-text-muted

            transition-colors

            hover:text-primary
          "
        >
          <ChevronRight size={20} />
        </button>
      </SurfacePanel>
    </div>
  );
}
