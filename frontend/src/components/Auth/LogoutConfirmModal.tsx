import React, { useEffect } from 'react';
import { LogOut } from 'lucide-react';
import { useAuth } from '../../auth/AuthProvider';
import './LogoutConfirmModal.css';

interface LogoutConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
}

export const LogoutConfirmModal: React.FC<LogoutConfirmModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
}) => {
  const { user } = useAuth();

  // Close on Escape key press
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="logout-modal-backdrop"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="logout-title"
    >
      <div
        className="logout-modal-card"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="logout-modal-header">
          <div className="logout-icon-pill">
            <LogOut size={22} />
          </div>
          <div className="logout-modal-title-group">
            <h3 id="logout-title">Confirm Sign Out</h3>
            <p>
              Are you sure you want to end your current session? You will need to sign in again to access the workspace.
            </p>
          </div>
        </div>

        {/* Current Active Account Preview */}
        {user && (
          <div className="logout-account-preview">
            <div className="logout-account-avatar">
              {user.name.charAt(0)}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                {user.name}
              </span>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                {user.email} • {user.organizationId}
              </span>
            </div>
          </div>
        )}

        <div className="logout-modal-actions">
          <button
            type="button"
            onClick={onClose}
            className="logout-btn-cancel"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={onConfirm}
            className="logout-btn-confirm"
            autoFocus
          >
            <LogOut size={15} /> Yes, Sign Out
          </button>
        </div>
      </div>
    </div>
  );
};
