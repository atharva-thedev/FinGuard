# FinGuard Design System & Theme Guidelines

This document provides a comprehensive guide for managing and utilizing the Light and Dark Theme architecture across all FinGuard web applications and UI components.

---

## 1. Overview & Architecture

FinGuard uses a **CSS Custom Properties (Design Tokens)** foundation paired with a React context provider (`ThemeProvider`).

```
frontend/src/
├── theme/
│   ├── theme.css           # CSS custom properties for :root (light) and [data-theme="dark"]
│   ├── themeTypes.ts       # ThemeMode ('light'|'dark'|'system'), ResolvedTheme ('light'|'dark')
│   ├── ThemeProvider.tsx   # Context provider, OS media query sync, localStorage persistence
│   ├── useTheme.ts         # Hook to access { theme, resolvedTheme, setTheme, toggleTheme }
│   └── index.ts            # Barrel export
├── components/
│   ├── ThemeToggle.tsx     # Segmented and compact switcher components
│   └── ThemeToggle.css
```

### Key Features
1. **Anti-FOUC (Flash of Unstyled Content)**: An inline script in `index.html` evaluates the saved theme or OS preference *before* the first render and sets `data-theme` immediately on the `<html>` root.
2. **System Preference Awareness**: When set to `'system'`, the app automatically reacts to OS/browser dark mode changes in real-time via `window.matchMedia('(prefers-color-scheme: dark)')`.
3. **Automatic Persistence**: User choices are saved under the `localStorage` key `'finguard-theme'`.

---

## 2. CSS Design Tokens Master Reference

Always use CSS variables instead of hardcoded hex codes.

### Brand & Accents
| Token | Light Mode | Dark Mode | Usage |
| :--- | :--- | :--- | :--- |
| `--primary` | `#0d9488` | `#14b8a6` | Primary action buttons, active highlights |
| `--primary-hover` | `#0f766e` | `#2dd4bf` | Button hover states |
| `--primary-fg` | `#ffffff` | `#050a14` | Foreground text on primary buttons |
| `--brand-navy-900` | `#0a192f` | `#050a14` | Deep brand navy background elements |
| `--brand-teal-500` | `#0d9488` | `#14b8a6` | Brand teal accent |
| `--brand-teal-glow`| `rgba(13, 148, 136, 0.25)` | `rgba(20, 184, 166, 0.35)` | Subtle glowing borders / badges |
| `--gradient-brand` | Navy → Teal gradient | Teal → Sky gradient | Badges, hero cards, logo shields |

### Surfaces & Backgrounds
| Token | Light Mode | Dark Mode | Usage |
| :--- | :--- | :--- | :--- |
| `--bg-app` | `#f8fafc` (Slate 50) | `#080d1a` (Space Navy) | Overall page background |
| `--bg-surface` | `#ffffff` (White) | `#0f172a` (Slate 900) | Standard cards, panels, modals |
| `--bg-surface-elevated` | `#ffffff` | `#1e293b` (Slate 800) | Dropdowns, tooltips, popovers |
| `--bg-surface-hover` | `#f1f5f9` (Slate 100) | `#1e293b` | List item / row hover states |
| `--bg-muted` | `#f1f5f9` | `#111c33` | Badges, table headers, inactive pills |
| `--bg-glass` | `rgba(255, 255, 255, 0.85)` | `rgba(15, 23, 42, 0.75)` | Frosted glass navigation & headers |

### Typography
| Token | Light Mode | Dark Mode | Usage |
| :--- | :--- | :--- | :--- |
| `--text-primary` | `#0f172a` (Slate 900) | `#f8fafc` (Slate 50) | Headings, primary labels, table values |
| `--text-secondary` | `#475569` (Slate 600) | `#94a3b8` (Slate 400) | Descriptions, subtitles, metadata |
| `--text-muted` | `#94a3b8` (Slate 400) | `#64748b` (Slate 500) | Placeholder text, timestamps, captions |
| `--text-brand` | `#0d9488` | `#2dd4bf` | Brand highlighted text |

### Status & Risk Indicators
| Token | Description |
| :--- | :--- |
| `--status-success`, `--status-success-bg`, `--status-success-border` | Approved invoices, healthy systems |
| `--status-warning`, `--status-warning-bg`, `--status-warning-border` | Pending approvals, manual review items |
| `--status-danger`, `--status-danger-bg`, `--status-danger-border` | Fraud anomalies, blocked payments, policy breaches |
| `--status-info`, `--status-info-bg`, `--status-info-border` | Processing items, informational notices |
| `--risk-low`, `--risk-medium`, `--risk-high` | AI Risk Scoring indicators (0–100) |

---

## 3. How to Use in Components

### Accessing Theme in React Components
```tsx
import React from 'react';
import { useTheme } from '@/theme';

export const MyComponent: React.FC = () => {
  const { theme, resolvedTheme, setTheme, toggleTheme } = useTheme();

  return (
    <div>
      <p>Current theme: {resolvedTheme}</p>
      <button onClick={toggleTheme}>Toggle Theme</button>
      <button onClick={() => setTheme('system')}>Reset to System</button>
    </div>
  );
};
```

### Writing Component CSS
```css
.custom-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-base);
  color: var(--text-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.custom-card:hover {
  background: var(--bg-surface-hover);
  border-color: var(--border-strong);
}

.custom-card-title {
  color: var(--text-primary);
  font-family: var(--font-heading);
}

.custom-card-desc {
  color: var(--text-secondary);
}
```

### Adding the Theme Toggle Button
```tsx
import { ThemeToggle } from '@/components/ThemeToggle';

// Segmented Pill (Light | Dark | Auto)
<ThemeToggle variant="segmented" />

// Compact Button (Single icon toggle)
<ThemeToggle variant="compact" />
```
