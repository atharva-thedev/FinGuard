import React from 'react';
import { Sun, Moon, Laptop } from 'lucide-react';
import { useTheme } from '../theme';
import type { ThemeMode } from '../theme';
import './ThemeToggle.css';

interface ThemeToggleProps {
  variant?: 'segmented' | 'compact' | 'dropdown';
  className?: string;
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({
  variant = 'segmented',
  className = '',
}) => {
  const { theme, resolvedTheme, setTheme, toggleTheme } = useTheme();

  if (variant === 'compact') {
    return (
      <button
        type="button"
        onClick={toggleTheme}
        className={`theme-toggle-compact ${className}`}
        aria-label={`Switch to ${resolvedTheme === 'dark' ? 'light' : 'dark'} mode`}
        title={`Currently in ${resolvedTheme} mode (click to toggle)`}
      >
        <span className="theme-toggle-compact-icon">
          {resolvedTheme === 'dark' ? (
            <Moon className="icon-moon" size={18} />
          ) : (
            <Sun className="icon-sun" size={18} />
          )}
        </span>
      </button>
    );
  }

  const options: { mode: ThemeMode; label: string; icon: React.ReactNode }[] = [
    { mode: 'light', label: 'Light', icon: <Sun size={15} /> },
    { mode: 'dark', label: 'Dark', icon: <Moon size={15} /> },
    { mode: 'system', label: 'Auto', icon: <Laptop size={15} /> },
  ];

  return (
    <div
      className={`theme-toggle-segmented ${className}`}
      role="radiogroup"
      aria-label="Color theme selector"
    >
      {options.map((opt) => {
        const isActive = theme === opt.mode;
        return (
          <button
            key={opt.mode}
            type="button"
            role="radio"
            aria-checked={isActive}
            onClick={() => setTheme(opt.mode)}
            className={`theme-toggle-option ${isActive ? 'active' : ''}`}
            title={`Switch to ${opt.label} theme`}
          >
            <span className="theme-toggle-icon">{opt.icon}</span>
            <span className="theme-toggle-label">{opt.label}</span>
          </button>
        );
      })}
    </div>
  );
};
