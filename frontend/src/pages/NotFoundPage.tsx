import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert, ArrowLeft } from 'lucide-react';

export const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh',
        textAlign: 'center',
        gap: '1rem',
      }}
    >
      <ShieldAlert size={48} style={{ color: 'var(--status-warning)' }} />
      <h1 style={{ fontSize: '2rem' }}>404 — Page Not Found</h1>
      <p style={{ color: 'var(--text-secondary)', maxWidth: '400px' }}>
        The requested financial resource, queue, or studio workspace does not exist or has been archived.
      </p>
      <button
        type="button"
        onClick={() => navigate('/dashboard')}
        className="btn btn-primary"
      >
        <ArrowLeft size={16} /> Return to Dashboard
      </button>
    </div>
  );
};
