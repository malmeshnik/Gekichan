import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ children, className = '', onClick }) => {
  return (
    <div
      onClick={onClick}
      className={`glass-card p-md ${onClick ? 'cursor-pointer active:opacity-80 transition-opacity' : ''} ${className}`}
    >
      {children}
    </div>
  );
};
