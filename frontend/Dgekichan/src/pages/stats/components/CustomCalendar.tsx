import { useState } from "react";
import { ChevronLeft, ChevronRight, Check } from "lucide-react";
import { cn } from "@/shared/lib/cn";
import { SurfacePanel } from "@/shared/ui/surface-panel/surface-panel";
import { Button } from "@/shared/ui/button/button";

interface CustomCalendarProps {
  onSelectRange: (start: Date, end: Date) => void;
  onSelectDate: (date: Date) => void;
  initialStart?: string;
  initialEnd?: string;
}

export function CustomCalendar({ onSelectRange, onSelectDate, initialStart, initialEnd }: CustomCalendarProps) {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [startDate, setStartDate] = useState<Date | null>(initialStart ? new Date(initialStart) : null);
  const [endDate, setEndDate] = useState<Date | null>(initialEnd ? new Date(initialEnd) : null);

  const today = new Date();
  today.setHours(0,0,0,0);

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

  const handleDateClick = (day: number) => {
    const clickedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
    clickedDate.setHours(0,0,0,0);

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
    }
  };

  const handleConfirm = () => {
      if (startDate) {
          if (endDate) {
              if (startDate.getTime() === endDate.getTime()) {
                  onSelectDate(startDate);
              } else {
                  onSelectRange(startDate, endDate);
              }
          } else {
              // If only one click, we can either wait for second or treat as single day
              onSelectDate(startDate);
          }
      }
  };

  const isSelected = (d: number) => {
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), d);
    date.setHours(0,0,0,0);
    if (startDate && date.getTime() === startDate.getTime()) return true;
    if (endDate && date.getTime() === endDate.getTime()) return true;
    return false;
  };

  const isToday = (d: number) => {
      const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), d);
      date.setHours(0,0,0,0);
      return date.getTime() === today.getTime();
  }

  const isInRange = (d: number) => {
    if (!startDate || !endDate) return false;
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), d);
    date.setHours(0,0,0,0);
    return date > startDate && date < endDate;
  };

  const renderDays = () => {
    const totalDays = daysInMonth(currentDate.getFullYear(), currentDate.getMonth());
    const startDay = (firstDayOfMonth(currentDate.getFullYear(), currentDate.getMonth()) + 6) % 7; // Monday start
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
          onClick={() => handleDateClick(d)}
          className={cn(
            "h-10 w-10 flex items-center justify-center rounded-lg transition-all relative",
            selected ? "bg-primary text-white z-10" : "text-white/60 hover:bg-white/5",
            range && "bg-primary/20 text-white rounded-none",
            todayMarker && !selected && "border border-primary/40"
          )}
        >
          {d}
          {todayMarker && (
              <div className="absolute bottom-1.5 w-1 h-1 bg-primary rounded-full" />
          )}
        </button>
      );
    }

    return days;
  };

  return (
    <SurfacePanel className="p-4 flex flex-col gap-4">
      <div className="flex justify-between items-center">
        <h4 className="text-sm font-medium text-white">
          {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
        </h4>
        <div className="flex gap-2">
          <button onClick={prevMonth} className="p-1 hover:bg-white/5 rounded-md text-white/40"><ChevronLeft size={18}/></button>
          <button onClick={nextMonth} className="p-1 hover:bg-white/5 rounded-md text-white/40"><ChevronRight size={18}/></button>
        </div>
      </div>
      <div className="grid grid-cols-7 gap-1 text-center">
        {["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"].map(d => (
          <div key={d} className="text-[10px] text-white/20 uppercase font-bold">{d}</div>
        ))}
      </div>
      <div className="grid grid-cols-7 gap-1">
        {renderDays()}
      </div>

      <div className="flex flex-col gap-2 pt-2 border-t border-white/5">
          <div className="flex justify-between text-[10px] text-white/40 uppercase font-bold">
              <span>Вибрано:</span>
              <span className="text-white">
                  {startDate ? startDate.toLocaleDateString('uk-UA') : '—'}
                  {endDate && endDate.getTime() !== startDate?.getTime() ? ` — ${endDate.toLocaleDateString('uk-UA')}` : ''}
              </span>
          </div>
          <Button
            disabled={!startDate}
            onClick={handleConfirm}
            className="w-full gap-2"
            variant="active"
          >
              <Check size={16} /> Підтвердити
          </Button>
      </div>
    </SurfacePanel>
  );
}
