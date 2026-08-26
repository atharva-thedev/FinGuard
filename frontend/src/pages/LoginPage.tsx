import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Lock, Mail, ArrowRight, Building, User } from 'lucide-react';
import { useAuth } from '../auth/AuthProvider';
import type { UserProfile } from '../auth/AuthProvider';
import { useTheme } from '../theme/ThemeProvider';
import { ThemeToggle } from '../components/ThemeToggle';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const { resolvedTheme } = useTheme();
  const [tab, setTab] = useState<'login' | 'signup'>('login');

  // Form states
  const [email, setEmail] = useState<string>('alex.vance@finguard.com');
  const [password, setPassword] = useState<string>('password123');
  const [orgName, setOrgName] = useState<string>('Acme Global Corp');
  const [fullName, setFullName] = useState<string>('Alex Vance');
  const [role, setRole] = useState<UserProfile['role']>('controller');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(email, role);
    navigate('/dashboard');
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'var(--bg-app)',
        padding: '2rem 1.5rem',
        position: 'relative',
      }}
    >
      <div style={{ position: 'absolute', top: '1.5rem', right: '1.5rem' }}>
        <ThemeToggle variant="segmented" />
      </div>

      <div style={{ position: 'absolute', top: '1.5rem', left: '1.5rem' }}>
        <Link to="/" style={{ textDecoration: 'none', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          ← Back to Home
        </Link>
      </div>

      <div
        className="card"
        style={{
          maxWidth: '460px',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          gap: '1.5rem',
          padding: '2.5rem 2rem',
          boxShadow: 'var(--shadow-xl)',
        }}
      >
        {/* Brand Header */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', gap: '0.75rem' }}>
          <Link to="/">
            <img
              src={resolvedTheme === 'dark' ? '/logo-dark.png' : '/logo.png'}
              alt="FinGuard"
              style={{ height: '56px', width: 'auto', objectFit: 'contain' }}
            />
          </Link>
          <span style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
            Autonomous Invoice & Expense Intelligence
          </span>
        </div>

        {/* Tab Switcher */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            background: 'var(--bg-muted)',
            padding: '4px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border-base)',
          }}
        >
          <button
            type="button"
            onClick={() => setTab('login')}
            style={{
              padding: '8px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: tab === 'login' ? 'var(--bg-surface)' : 'transparent',
              color: tab === 'login' ? 'var(--text-primary)' : 'var(--text-muted)',
              fontWeight: 600,
              fontSize: '0.875rem',
              cursor: 'pointer',
              boxShadow: tab === 'login' ? 'var(--shadow-sm)' : 'none',
              transition: 'all var(--transition-fast)',
            }}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => setTab('signup')}
            style={{
              padding: '8px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: tab === 'signup' ? 'var(--bg-surface)' : 'transparent',
              color: tab === 'signup' ? 'var(--text-primary)' : 'var(--text-muted)',
              fontWeight: 600,
              fontSize: '0.875rem',
              cursor: 'pointer',
              boxShadow: tab === 'signup' ? 'var(--shadow-sm)' : 'none',
              transition: 'all var(--transition-fast)',
            }}
          >
            Create Org
          </button>
        </div>

        {/* Auth Form */}
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {tab === 'signup' && (
            <>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
                  Full Name
                </label>
                <div className="search-container" style={{ width: '100%', borderRadius: 'var(--radius-md)' }}>
                  <User size={15} style={{ color: 'var(--text-muted)' }} />
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="search-input"
                    placeholder="e.g. Alex Vance"
                  />
                </div>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
                  Organization Name
                </label>
                <div className="search-container" style={{ width: '100%', borderRadius: 'var(--radius-md)' }}>
                  <Building size={15} style={{ color: 'var(--text-muted)' }} />
                  <input
                    type="text"
                    required
                    value={orgName}
                    onChange={(e) => setOrgName(e.target.value)}
                    className="search-input"
                    placeholder="e.g. Acme Global Corp"
                  />
                </div>
              </div>
            </>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              Work Email Address
            </label>
            <div className="search-container" style={{ width: '100%', borderRadius: 'var(--radius-md)' }}>
              <Mail size={15} style={{ color: 'var(--text-muted)' }} />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="search-input"
                placeholder="name@company.com"
              />
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              Password
            </label>
            <div className="search-container" style={{ width: '100%', borderRadius: 'var(--radius-md)' }}>
              <Lock size={15} style={{ color: 'var(--text-muted)' }} />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="search-input"
                placeholder="••••••••••••"
              />
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              Sign In Role
            </label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value as UserProfile['role'])}
              style={{
                padding: '8px 12px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-base)',
                background: 'var(--bg-muted)',
                color: 'var(--text-primary)',
                fontSize: '0.875rem',
              }}
            >
              <option value="controller">Controller (Policy & Approvals)</option>
              <option value="ap_clerk">AP Clerk (Capture & OCR Review)</option>
              <option value="approver">Department Approver</option>
              <option value="admin">Tenant Administrator</option>
              <option value="viewer">Auditor (Read-Only)</option>
            </select>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ marginTop: '0.5rem', padding: '0.75rem' }}
          >
            {tab === 'login' ? 'Sign In to Workspace' : 'Create Enterprise Account'} <ArrowRight size={16} />
          </button>
        </form>

        <div style={{ textAlign: 'center', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          Enterprise SSO & Multi-Tenant Scoped Environment
        </div>
      </div>
    </div>
  );
};
