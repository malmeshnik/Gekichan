import React, { useEffect, useRef } from 'react';
import { Header } from '../shared/ui/Header';
import { ProgressRing } from '../shared/ui/ProgressRing';
import { TimerDisplay } from '../shared/ui/TimerDisplay';
import { TimerControls } from '../features/timer/TimerControls';
import { Badge } from '../shared/ui/Badge';
import { Flame, Hourglass } from 'lucide-react';
import { useSessionStore } from '../entities/model';

export const TimerPage: React.FC = () => {
  const { remainingSeconds, isActive, setIsActive, setRemainingSeconds } = useSessionStore();
  const requestRef = useRef<number>();
  const startTimeRef = useRef<number>();

  const animate = (time: number) => {
    if (startTimeRef.current === undefined) {
      startTimeRef.current = time;
    }

    const deltaTime = time - startTimeRef.current;
    if (deltaTime >= 1000) {
      setRemainingSeconds(Math.max(0, remainingSeconds - 1));
      startTimeRef.current = time;
    }

    if (isActive && remainingSeconds > 0) {
      requestRef.current = requestAnimationFrame(animate);
    }
  };

  useEffect(() => {
    if (isActive && remainingSeconds > 0) {
      requestRef.current = requestAnimationFrame(animate);
    } else {
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
      startTimeRef.current = undefined;
    }
    return () => {
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
    };
  }, [isActive, remainingSeconds]);

  const progress = (remainingSeconds / (25 * 60)) * 100;

  return (
    <div className="pb-32 min-h-screen flex flex-col">
      <Header title="Productivity" />

      <main className="flex-1 flex flex-col items-center justify-around px-md py-lg">
        {/* Indicators */}
        <div className="flex gap-md w-full max-w-xs">
          <div className="flex-1 bg-card border border-border rounded-2xl p-3 flex items-center justify-center gap-2">
            <Flame size={16} className="text-orange-500" />
            <span className="text-[10px] font-bold uppercase tracking-widest">5 Day Streak</span>
          </div>
          <div className="flex-1 bg-card border border-border rounded-2xl p-3 flex items-center justify-center gap-2">
            <div className="w-4 h-4 rounded-sm border-2 border-text-secondary flex items-center justify-center text-[8px]">2</div>
            <span className="text-[10px] font-bold uppercase tracking-widest text-text-secondary">Session 2 of 4</span>
          </div>
        </div>

        {/* Current Task */}
        <div className="text-center">
          <p className="text-[10px] font-bold text-text-secondary uppercase tracking-[0.2em] mb-2">Current Task</p>
          <h2 className="text-xl font-bold mb-3">Designing System Architecture</h2>
          <Badge variant="primary">Deep Work</Badge>
        </div>

        {/* Timer Ring */}
        <div className="relative">
           {/* Outer glow */}
           <div className="absolute inset-0 bg-primary-start/5 blur-[100px] rounded-full" />
           <ProgressRing progress={progress}>
             <TimerDisplay seconds={remainingSeconds} />
           </ProgressRing>
        </div>

        {/* Controls */}
        <TimerControls
          isActive={isActive}
          onStart={() => setIsActive(true)}
          onPause={() => setIsActive(false)}
          onStop={() => { setIsActive(false); setRemainingSeconds(25 * 60); }}
          onAdjust={(m) => setRemainingSeconds(Math.max(0, remainingSeconds + m * 60))}
        />
      </main>
    </div>
  );
};
