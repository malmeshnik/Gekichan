import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";

interface BottomSheetProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

export function BottomSheet({
  isOpen,
  onClose,
  title,
  children
}: BottomSheetProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="
              fixed
              inset-0
              z-[100]
              bg-background/80
              backdrop-blur-sm
            "
          />

          {/* Sheet */}
          <motion.div
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            transition={{
              type: "spring",
              damping: 30,
              stiffness: 260
            }}
            drag="y"
            dragConstraints={{ top: 0, bottom: 0 }}
            dragElastic={0.15}
            onDragEnd={(_, info) => {
              if (info.offset.y > 120) {
                onClose();
              }
            }}
            className="
              fixed
              inset-x-0
              bottom-0
              z-[101]
              mx-auto
              flex
              w-full
              max-w-md
              flex-col
              rounded-t-[28px]
              border-t
              border-outline/50
              bg-surface-container
              shadow-[0_-8px_40px_rgba(0,0,0,0.5)]

              max-h-[85vh]
            "
          >
            {/* Handle */}
            <div
              className="
                flex
                justify-center
                py-3
              "
            >
              <div
                className="
                  h-1.5
                  w-12
                  rounded-full
                  bg-outline/30
                "
              />
            </div>

            {/* Header */}
            {title && (
              <div className="px-6 pb-4">
                <h2
                  className="
                    text-center
                    typography-headline-sm
                    text-text-main
                  "
                >
                  {title}
                </h2>
              </div>
            )}

            {/* Scroll Content */}
            <div
              className="
                flex-1
                overflow-y-auto
                px-6
                pb-[120px]
              "
            >
              {children}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}