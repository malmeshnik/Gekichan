import { useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { cn } from "@/shared/lib/cn";
import { SurfacePanel } from "@/shared/ui/surface-panel/surface-panel";

interface CustomCalendarProps {
  onSelectRange: (start: Date, end: Date) => void;
  onSelectDate: (date: Date) => void;
}

export function CustomCalendar({ onSelectRange, onSelectDate }: CustomCalendarProps) {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);

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

    if (!startDate || (startDate && endDate)) {
        setStartDate(clickedDate);
        setEndDate(null);
        onSelectDate(clickedDate);
    } else {
        if (clickedDate < startDate) {
            setStartDate(clickedDate);
        } else {
            setEndDate(clickedDate);
            onSelectRange(startDate, clickedDate);
        }
    }
  };

  const isSelected = (d: number) => {
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), d);
    if (startDate && date.getTime() === startDate.getTime()) return true;
    if (endDate && date.getTime() === endDate.getTime()) return true;
    return false;
  };

  const isInRange = (d: number) => {
    if (!startDate || !endDate) return false;
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), d);
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

      days.push(
        <button
          key={d}
          onClick={() => handleDateClick(d)}
          className={cn(
            "h-10 w-10 flex items-center justify-center rounded-lg transition-all relative",
            selected ? "bg-primary text-white z-10" : "text-white/60 hover:bg-white/5",
            range && "bg-primary/20 text-white rounded-none"
          )}
        >
          {d}
        </button>
      );
    }

    return days;
  };

  return (
    <SurfacePanel className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h4 className="text-sm font-medium text-white">
          {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
        </h4>
        <div className="flex gap-2">
          <button onClick={prevMonth} className="p-1 hover:bg-white/5 rounded-md text-white/40"><ChevronLeft size={18}/></button>
          <button onClick={nextMonth} className="p-1 hover:bg-white/5 rounded-md text-white/40"><ChevronRight size={18}/></button>
        </div>
      </div>
      <div className="grid grid-cols-7 gap-1 text-center mb-2">
        {["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"].map(d => (
          <div key={d} className="text-[10px] text-white/20 uppercase font-bold">{d}</div>
        ))}
      </div>
      <div className="grid grid-cols-7 gap-1">
        {renderDays()}
      </div>
      <div className="mt-4 text-[10px] text-white/40 text-center italic">
          Виберіть одну дату або діапазон (початок та кінець)
      </div>
    </SurfacePanel>
  );
}
