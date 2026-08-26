import React from 'react';
import { NavLink, Outlet, useNavigate, Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { ThemeToggle } from '../ThemeToggle';
import { useAuth } from '../../auth/AuthProvider';
import { useTheme } from '../../theme/ThemeProvider';
import './PublicLayout.css';

export const PublicLayout: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const { resolvedTheme } = useTheme();

  return (
    <div className="public-root">
      {/* ── Top Public Navigation ───────────────────────────────────────────── */}
      <header className="public-nav">
        <Link to="/" style={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }} title="FinGuard Home">
          <img
            src={resolvedTheme === 'dark' ? '/logo-dark.png' : '/logo.png'}
            alt="FinGuard"
            className="public-nav-logo"
          />
        </Link>

        <nav className="public-nav-links">
          <NavLink
            to="/features"
            className={({ isActive }) => `public-nav-link ${isActive ? 'active' : ''}`}
          >
            Features
          </NavLink>
          <NavLink
            to="/security"
            className={({ isActive }) => `public-nav-link ${isActive ? 'active' : ''}`}
          >
            Security & Trust
          </NavLink>
          <NavLink
            to="/integrations"
            className={({ isActive }) => `public-nav-link ${isActive ? 'active' : ''}`}
          >
            Integrations
          </NavLink>
          <NavLink
            to="/pricing"
            className={({ isActive }) => `public-nav-link ${isActive ? 'active' : ''}`}
          >
            Pricing
          </NavLink>
        </nav>

        <div className="public-nav-actions">
          <ThemeToggle variant="compact" />
          {isAuthenticated ? (
            <button
              type="button"
              onClick={() => navigate('/dashboard')}
              className="btn btn-primary"
            >
              Open Workspace <ArrowRight size={15} />
            </button>
          ) : (
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button
                type="button"
                onClick={() => navigate('/login')}
                className="btn btn-secondary"
              >
                Sign In
              </button>
              <button
                type="button"
                onClick={() => navigate('/signup')}
                className="btn btn-primary"
              >
                Get Started <ArrowRight size={15} />
              </button>
            </div>
          )}
        </div>
      </header>

      {/* ── Main Content Viewport ─────────────────────────────────────────── */}
      <main className="public-viewport">
        <Outlet />
      </main>

      {/* ── Compact Footer ────────────────────────────────────────────────── */}
      <footer className="public-footer">
        <div>
          <span>© 2026 FinGuard AI Technologies Inc. Enterprise Financial Intelligence.</span>
        </div>
        <div style={{ display: 'flex', gap: '1.25rem' }}>
          <Link to="/security" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>Security Center</Link>
          <Link to="/features" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>Platform</Link>
          <Link to="/pricing" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>Pricing</Link>
          <Link to="/integrations" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>Integrations</Link>
        </div>
      </footer>
    </div>
  );
};
