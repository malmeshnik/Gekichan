import { useState, useEffect, useRef, useMemo } from "react";
import { ChevronLeft, ChevronRight, Check, Clock, ArrowLeft } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { Button } from "@/shared/ui/button";
import { cn } from "@/shared/lib/cn";

interface CustomCalendarProps {
  mode?: "single" | "range";
  showTime?: boolean;
  initialStart?: Date | string | null;
  initialEnd?: Date | string | null;
  onSelectDate?: (date: Date) => void;
  onSelectRange?: (start: Date, end: Date) => void;
}

export function CustomCalendar({
  mode = "single",
  showTime = false,
  initialStart,
  initialEnd,
  onSelectDate,
  onSelectRange,
}: CustomCalendarProps) {
  // Керування кроками: 'date' або 'time'
  const [step, setStep] = useState<"date" | "time">("date");

  const [currentDate, setCurrentDate] = useState(new Date());
  const [startDate, setStartDate] = useState<Date | null>(initialStart ? new Date(initialStart) : null);
  const [endDate, setEndDate] = useState<Date | null>(initialEnd ? new Date(initialEnd) : null);

  const [selectedHours, setSelectedHours] = useState(() => {
    if (initialStart) return new Date(initialStart).getHours();
    return 12;
  });
  const [selectedMinutes, setSelectedMinutes] = useState(() => {
    if (initialStart) return new Date(initialStart).getMinutes();
    return 0;
  });

  const hoursScrollRef = useRef<HTMLDivElement>(null);
  const minutesScrollRef = useRef<HTMLDivElement>(null);

  const hoursArray = useMemo(() => Array.from({ length: 24 }, (_, i) => i), []);
  const minutesArray = useMemo(() => Array.from({ length: 60 }, (_, i) => i), []);

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const daysInMonth = (year: number, month: number) => new Date(year, month + 1, 0).getDate();
  const firstDayOfMonth = (year: number, month: number) => new Date(year, month, 1).getDay();

  const monthNames = [
    "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
    "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"
  ];

  const prevMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const nextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  // Скрол коліщаток запускаємо тільки тоді, коли переходимо на крок 'time'
  useEffect(() => {
    if (step === "time") {
      setTimeout(() => {
        scrollToValue(hoursScrollRef, selectedHours);
        scrollToValue(minutesScrollRef, selectedMinutes);
      }, 60);
    }
  }, [step]);

  const scrollToValue = (ref: React.RefObject<HTMLDivElement | null>, value: number) => {
    if (ref.current) {
      const itemHeight = 36;
      ref.current.scrollTop = value * itemHeight;
    }
  };

  const handleScroll = (
    ref: React.RefObject<HTMLDivElement | null>,
    setVal: (v: number) => void
  ) => {
    if (!ref.current) return;
    const itemHeight = 36;
    const index = Math.round(ref.current.scrollTop / itemHeight);
    if (index >= 0 && index < (ref.current === hoursScrollRef.current ? 24 : 60)) {
      setVal(index);
    }
  };

  const handleDateClick = (day: number) => {
    const clickedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
    clickedDate.setHours(0, 0, 0, 0);

    if (mode === "single") {
      setStartDate(clickedDate);
      setEndDate(null);
      
      // Якщо час потрібен — ведемо на крок часу, якщо ні — просто тримаємо виділення
      if (showTime) {
        setStep("time");
      }
    } else {
      // Режим діапазону (Range)
      if (!startDate || (startDate && endDate)) {
        setStartDate(clickedDate);
        setEndDate(null);
      } else {
        if (clickedDate.getTime() === startDate.getTime()) {
          setEndDate(clickedDate);
        } else if (clickedDate < startDate) {
          setStartDate(clickedDate);
        } else {
          setEndDate(clickedDate);
        }
        // ЖОДНИХ авто-відправок тут немає. Юзер просто бачить виділений період на екрані.
      }
    }
  };

  const handleConfirmTime = () => {
    if (!startDate) return;

    const finalStartDate = new Date(startDate);
    finalStartDate.setHours(selectedHours, selectedMinutes, 0, 0);

    if (mode === "single") {
      onSelectDate?.(finalStartDate);
    } else {
      const finalEndDate = endDate ? new Date(endDate) : new Date(startDate);
      finalEndDate.setHours(selectedHours, selectedMinutes, 0, 0);

      if (finalStartDate.getTime() === finalEndDate.getTime()) {
        onSelectDate?.(finalStartDate);
      } else {
        onSelectRange?.(finalStartDate, finalEndDate);
      }
    }
    // Скидаємо крок на дефолтний для наступного відкриття
    setStep("date");
  };

  const isSelected = (d: number) => {
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), d);
    date.setHours(0, 0, 0, 0);
    if (startDate && date.getTime() === startDate.getTime()) return true;
    if (endDate && date.getTime() === endDate.getTime()) return true;
    return false;
  };

  const isToday = (d: number) => {
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), d);
    date.setHours(0, 0, 0, 0);
    return date.getTime() === today.getTime();
  };

  const isInRange = (d: number) => {
    if (mode === "single" || !startDate || !endDate) return false;
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), d);
    date.setHours(0, 0, 0, 0);
    return date > startDate && date < endDate;
  };

  const renderDays = () => {
    const totalDays = daysInMonth(currentDate.getFullYear(), currentDate.getMonth());
    const startDay = (firstDayOfMonth(currentDate.getFullYear(), currentDate.getMonth()) + 6) % 7;
    const days = [];

    for (let i = 0; i < startDay; i++) {
      days.push(<div key={`empty-${i}`} className="h-10 w-10" />);
    }

    for (let d = 1; d <= totalDays; d++) {
      const selected = isSelected(d);
      const range = isInRange(d);
      const todayMarker = isToday(d);

      days.push(
        <button
          key={d}
          type="button"
          onClick={() => handleDateClick(d)}
          className={cn(
            "h-10 w-10 flex items-center justify-center rounded-lg transition-all relative text-sm",
            selected ? "bg-primary text-white font-semibold z-10" : "text-white/60 hover:bg-white/5",
            range && "bg-primary/20 text-white rounded-none",
            todayMarker && !selected && "border border-primary/40 text-primary"
          )}
        >
          {d}
          {todayMarker && (
            <div className={cn("absolute bottom-1 w-1 h-1 rounded-full", selected ? "bg-white" : "bg-primary")} />
          )}
        </button>
      );
    }

    return days;
  };

  return (
    <SurfacePanel className="p-4 flex flex-col gap-4 bg-surface-container-high border border-outline/10 rounded-2xl w-full max-w-sm mx-auto select-none overflow-hidden min-h-[310px] justify-between">
      
      <style dangerouslySetInnerHTML={{__html: `
        .ios-scroll-wheel {
          scrollbar-width: none;
          -ms-overflow-style: none;
        }
        .ios-scroll-wheel::-webkit-scrollbar {
          display: none;
          width: 0;
          height: 0;
        }
      `}} />

      {/* КРОК 1: ВИБІР ДАТИ */}
      {step === "date" && (
        <div className="flex flex-col gap-4 animate-in fade-in slide-in-from-left-4 duration-200">
          {/* Шапка календаря */}
          <div className="flex justify-between items-center">
            <h4 className="text-sm font-medium text-text-main">
              {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
            </h4>
            <div className="flex gap-1">
              <button type="button" onClick={prevMonth} className="p-2 hover:bg-white/5 rounded-xl text-text-muted transition-colors"><ChevronLeft size={18}/></button>
              <button type="button" onClick={nextMonth} className="p-2 hover:bg-white/5 rounded-xl text-text-muted transition-colors"><ChevronRight size={18}/></button>
            </div>
          </div>

          {/* Дні тижня */}
          <div className="grid grid-cols-7 gap-1 text-center">
            {["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"].map(d => (
              <div key={d} className="text-[11px] text-text-muted uppercase font-bold tracking-wider">{d}</div>
            ))}
          </div>

          {/* Сітка днів */}
          <div className="grid grid-cols-7 gap-1">
            {renderDays()}
          </div>

          {/* Нижній підвал для режиму діапазону дат (якщо підтвердження потрібне руками) */}
          {mode === "range" && (
            <div className="pt-2 border-t border-outline/10 flex items-center justify-between">
              <span className="text-[11px] text-text-muted uppercase font-bold tracking-wider">
                Діапазон: {startDate ? startDate.toLocaleDateString('uk-UA', { day: 'numeric', month: 'short' }) : '—'}
              </span>
              <Button disabled={!endDate} onClick={() => showTime ? setStep("time") : onSelectRange?.(startDate!, endDate!)} className="h-10 px-4 rounded-xl text-xs font-semibold" variant="active">
                Далі
              </Button>
            </div>
          )}
        </div>
      )}

      {/* КРОК 2: ВИБІР ЧАСУ */}
      {step === "time" && (
        <div className="flex flex-col gap-4 flex-1 justify-between animate-in fade-in slide-in-from-right-4 duration-200">
          
          {/* Кастомна навігація кроку часу */}
          <div className="flex items-center gap-2 border-b border-outline/5 pb-2">
            <button 
              type="button" 
              onClick={() => setStep("date")} 
              className="p-1.5 hover:bg-white/5 rounded-lg text-text-muted hover:text-text-main transition-colors"
            >
              <ArrowLeft size={16} />
            </button>
            <div className="flex flex-col">
              <span className="text-xs font-semibold text-text-main">Встановіть точний час</span>
              <span className="text-[10px] text-primary font-medium">
                Обрано: {startDate?.toLocaleDateString('uk-UA', { day: 'numeric', month: 'long' })}
              </span>
            </div>
          </div>

          {/* iOS Коліщатка */}
          <div className="relative h-[116px] bg-surface-container-highest/50 rounded-2xl border border-outline/5 overflow-hidden flex justify-center items-center touch-none my-auto">
            <div className="absolute inset-x-4 h-9 border-y border-primary/20 pointer-events-none bg-primary/5 rounded-lg" />
            
            <div className="flex items-center justify-center w-full max-w-[180px] h-full relative z-10 overflow-hidden">
              {/* Години */}
              <div 
                ref={hoursScrollRef}
                onScroll={() => handleScroll(hoursScrollRef, setSelectedHours)}
                className="ios-scroll-wheel w-14 h-full overflow-y-scroll overflow-x-hidden snap-y snap-mandatory scroll-smooth py-[40px]"
              >
                {hoursArray.map((h) => (
                  <div 
                    key={h} 
                    className={cn(
                      "h-9 flex items-center justify-center text-base font-semibold snap-center transition-all duration-100",
                      selectedHours === h ? "text-text-main text-lg font-bold scale-110" : "text-text-muted/30 text-sm"
                    )}
                  >
                    {h.toString().padStart(2, "0")}
                  </div>
                ))}
              </div>

              <div className="text-primary font-bold text-lg px-3 pb-0.5 pointer-events-none">:</div>

              {/* Хвилини */}
              <div 
                ref={minutesScrollRef}
                onScroll={() => handleScroll(minutesScrollRef, setSelectedMinutes)}
                className="ios-scroll-wheel w-14 h-full overflow-y-scroll overflow-x-hidden snap-y snap-mandatory scroll-smooth py-[40px]"
              >
                {minutesArray.map((m) => (
                  <div 
                    key={m} 
                    className={cn(
                      "h-9 flex items-center justify-center text-base font-semibold snap-center transition-all duration-100",
                      selectedMinutes === m ? "text-text-main text-lg font-bold scale-110" : "text-text-muted/30 text-sm"
                    )}
                  >
                    {m.toString().padStart(2, "0")}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Кнопка фінального збереження дедлайну */}
          <div className="pt-2 border-t border-outline/10 flex flex-col gap-2">
            <div className="flex justify-between items-center text-[10px] text-text-muted uppercase font-bold tracking-wider">
              <span>Підсумковий дедлайн:</span>
              <span className="text-primary font-bold">
                {selectedHours.toString().padStart(2, "0")}:{selectedMinutes.toString().padStart(2, "0")}
              </span>
            </div>
            <Button
              onClick={handleConfirmTime}
              className="w-full h-12 gap-2 rounded-xl text-sm font-semibold shadow-lg shadow-primary/10"
              variant="active"
            >
              <Check size={16} /> Підтвердити дедлайн
            </Button>
          </div>

        </div>
      )}

    </SurfacePanel>
  );
}