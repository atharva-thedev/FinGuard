import React, { useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { LogOut, ArrowRight } from 'lucide-react';
import { useAuth } from '../auth/AuthProvider';
import { ThemeToggle } from '../components/ThemeToggle';

export const LogoutPage: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  useEffect(() => {
    // Ensure auth state is cleared upon hitting logout route
    logout();
  }, [logout]);

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

      <div
        className="card"
        style={{
          maxWidth: '460px',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          gap: '1.5rem',
          padding: '3rem 2rem',
          boxShadow: 'var(--shadow-xl)',
        }}
      >
        <Link to="/">
          <img
            src="/logo.png"
            alt="FinGuard"
            style={{ height: '54px', width: 'auto', objectFit: 'contain' }}
          />
        </Link>

        <div
          style={{
            width: '52px',
            height: '52px',
            borderRadius: 'var(--radius-full)',
            background: 'var(--brand-teal-glow)',
            color: 'var(--primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <LogOut size={24} />
        </div>

        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800 }}>Signed Out Successfully</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
            Your in-memory credentials and tenant sessions have been securely terminated.
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', width: '100%' }}>
          <button
            type="button"
            onClick={() => navigate('/login')}
            className="btn btn-primary"
            style={{ padding: '0.75rem', width: '100%' }}
          >
            Sign Back In <ArrowRight size={16} />
          </button>
          <button
            type="button"
            onClick={() => navigate('/')}
            className="btn btn-secondary"
            style={{ padding: '0.75rem', width: '100%' }}
          >
            Return to Public Home
          </button>
        </div>
      </div>
    </div>
  );
};
