import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";

interface BottomSheetProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

export function BottomSheet({ isOpen, onClose, title, children }: BottomSheetProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-[100] bg-background/80 backdrop-blur-sm"
          />
          <motion.div
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="fixed inset-x-0 bottom-0 z-[101] mx-auto w-full max-w-md rounded-t-[24px] border-t border-outline/50 bg-surface-container p-6 pb-10 shadow-[0_-8px_40px_rgba(0,0,0,0.5)]"
          >
            {/* Handle */}
            <div className="mx-auto mb-6 h-1.5 w-12 rounded-full bg-outline/30" />

            {title && (
              <h2 className="mb-4 typography-headline-sm text-text-main text-center">
                {title}
              </h2>
            )}

            <div className="max-h-[70vh] overflow-y-auto">
              {children}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
