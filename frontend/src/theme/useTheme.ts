import { useContext } from 'react';
import { ThemeContext } from './ThemeProvider';
import type { ThemeContextType } from './themeTypes';

export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
