export type ThemeMode = 'light' | 'dark' | 'system';
export type ResolvedTheme = 'light' | 'dark';

export interface ThemeContextType {
  /**
   * The explicitly selected theme setting ('light', 'dark', or 'system')
   */
  theme: ThemeMode;

  /**
   * The actual applied theme after resolving 'system' preference
   */
  resolvedTheme: ResolvedTheme;

  /**
   * Update the active theme mode
   */
  setTheme: (theme: ThemeMode) => void;

  /**
   * Quick toggle between light and dark modes
   */
  toggleTheme: () => void;
}
