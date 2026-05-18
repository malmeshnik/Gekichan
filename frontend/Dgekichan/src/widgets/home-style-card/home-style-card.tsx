import { useState } from "react";
import { Shield, ChevronRight } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { Modal } from "@/shared/ui/modal";
import { useAuthStore } from "@/entities/auth/authStore";

export function HomeStyleCard() {
  const { user } = useAuthStore();
  const [showDetail, setShowDetail] = useState(false);

  const style = user?.style || {
      slug: "loading",
      title: "Завантаження...",
      description: "Аналізуємо твою активність",
      icon: "⏳"
  };

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
          cursor-pointer
          hover:bg-surface-container-highest/30
          transition-colors
        "
        onClick={() => setShowDetail(true)}
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
              text-2xl
            "
          >
            {style.icon || <Shield size={24} />}
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
              {style.title}
            </span>
          </div>
        </div>

        {/* Action */}
        <div
          className="
            text-text-muted
            transition-colors
          "
        >
          <ChevronRight size={20} />
        </div>
      </SurfacePanel>

      <Modal
        isOpen={showDetail}
        onClose={() => setShowDetail(false)}
        title="Твій стиль продуктивності"
      >
        <div className="flex flex-col items-center text-center py-4">
            <div className="text-6xl mb-4">{style.icon}</div>
            <h3 className="typography-headline-md text-secondary mb-2">{style.title}</h3>
            <p className="text-text-muted leading-relaxed">
                {style.description}
            </p>

            <div className="mt-8 p-4 bg-surface-container-highest/50 rounded-xl border border-outline/20 w-full">
                <p className="typography-label text-text-muted uppercase mb-2">Як це працює?</p>
                <p className="typography-body-sm text-text-secondary">
                    Ми аналізуємо твій час фокусу, кількість виконаних завдань та регулярність роботи, щоб визначити твій унікальний стиль. Продовжуй працювати, щоб відкрити нові досягнення!
                </p>
            </div>
        </div>
      </Modal>
    </div>
  );
}
