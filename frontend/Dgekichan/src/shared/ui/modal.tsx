import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

export function Modal({
  isOpen,
  onClose,
  title,
  children
}: ModalProps) {
  React.useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }

    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[100]">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="
              absolute
              inset-0
              bg-background/80
              backdrop-blur-sm
            "
          />

          <div
            className="
              absolute
              inset-0
              flex
              items-center
              justify-center
              p-4
            "
            onClick={onClose}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              transition={{
                duration: 0.2,
                ease: "easeOut"
              }}
              onClick={(e) => e.stopPropagation()}
              className="
                relative
                w-full
                max-w-md
                overflow-hidden
                rounded-card
                border
                border-outline/50
                bg-surface-container
                p-6
                shadow-2xl
              "
            >
              <div
                className="
                  mb-4
                  flex
                  items-center
                  justify-between
                "
              >
                {title && (
                  <h2
                    className="
                      typography-headline-sm
                      text-text-main
                    "
                  >
                    {title}
                  </h2>
                )}

                <button
                  onClick={onClose}
                  className="
                    rounded-full
                    p-1
                    text-text-muted
                    transition-colors
                    hover:bg-surface-container-highest
                  "
                >
                  <X size={20} />
                </button>
              </div>

              {children}
            </motion.div>
          </div>
        </div>
      )}
    </AnimatePresence>
  );
}