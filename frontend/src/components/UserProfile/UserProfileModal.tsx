import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  X,
  Download,
  LogOut,
  Check,
  Copy
} from 'lucide-react';
import { useAuth } from '../../auth/AuthProvider';
import type { UserProfile } from '../../auth/AuthProvider';
import { LogoutConfirmModal } from '../Auth/LogoutConfirmModal';
import './UserProfileModal.css';

interface UserProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const UserProfileModal: React.FC<UserProfileModalProps> = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  const { user, login, logout } = useAuth();
  const [copiedId, setCopiedId] = useState<boolean>(false);
  const [exportSuccess, setExportSuccess] = useState<boolean>(false);
  const [isConfirmLogoutOpen, setIsConfirmLogoutOpen] = useState<boolean>(false);

  if (!isOpen || !user) return null;

  const handleCopyUserId = () => {
    navigator.clipboard.writeText(user.id);
    setCopiedId(true);
    setTimeout(() => setCopiedId(false), 2000);
  };

  const handleRoleChange = (role: UserProfile['role']) => {
    login(user.email, role);
  };

  const handleExportData = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(user, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `finguard_user_export_${user.id}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();

    setExportSuccess(true);
    setTimeout(() => setExportSuccess(false), 2500);
  };

  const availableRoles: { role: UserProfile['role']; label: string; desc: string }[] = [
    { role: 'controller', label: 'Controller', desc: 'Policy manager, exception resolution & approvals' },
    { role: 'admin', label: 'Admin', desc: 'Full tenant & integration configuration authority' },
    { role: 'approver', label: 'Approver', desc: 'Department approval authority' },
    { role: 'ap_clerk', label: 'AP Clerk', desc: 'Upload, OCR review & extraction override' },
    { role: 'viewer', label: 'Auditor / Viewer', desc: 'Read-only financial and audit inspection' },
  ];

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="profile-modal-card" onClick={(e) => e.stopPropagation()}>
        {/* Modal Header */}
        <div className="modal-header">
          <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>User Identity & Security Profile</h3>
          <button type="button" onClick={onClose} className="modal-close-btn" title="Close profile">
            <X size={18} />
          </button>
        </div>

        {/* Modal Body */}
        <div className="modal-body">
          {/* Identity Hero */}
          <div className="profile-hero">
            <div className="profile-large-avatar">
              {user.name.slice(0, 2).toUpperCase()}
            </div>
            <div className="profile-hero-info">
              <div className="profile-name">
                {user.name}
                <span className="badge badge-success" style={{ fontSize: '11px', textTransform: 'capitalize' }}>
                  {user.role}
                </span>
              </div>
              <span className="profile-email">{user.email}</span>
              <div className="profile-meta-tags">
                <button
                  type="button"
                  onClick={handleCopyUserId}
                  style={{
                    background: 'transparent',
                    border: '1px solid var(--border-base)',
                    borderRadius: 'var(--radius-xs)',
                    padding: '2px 6px',
                    fontSize: '11px',
                    color: 'var(--text-muted)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    cursor: 'pointer',
                  }}
                >
                  <span style={{ fontFamily: 'var(--font-mono)' }}>ID: {user.id}</span>
                  {copiedId ? <Check size={11} style={{ color: 'var(--status-success)' }} /> : <Copy size={11} />}
                </button>
              </div>
            </div>
          </div>

          {/* Tenancy & Organization Info */}
          <div>
            <div className="profile-section-title">Organization & Tenancy Context</div>
            <div className="profile-info-grid">
              <div className="info-tile">
                <span className="info-tile-label">Organization</span>
                <span className="info-tile-val">{user.organizationName}</span>
              </div>
              <div className="info-tile">
                <span className="info-tile-label">Tenant ID</span>
                <span className="info-tile-val">{user.organizationId}</span>
              </div>
              <div className="info-tile">
                <span className="info-tile-label">Approval Limit</span>
                <span className="info-tile-val">Level 2 ($10k – $50k)</span>
              </div>
              <div className="info-tile">
                <span className="info-tile-label">Assigned Department</span>
                <span className="info-tile-val">Finance & Corporate</span>
              </div>
            </div>
          </div>

          {/* Role Preview Switcher (Interactive RBAC preview) */}
          <div>
            <div className="profile-section-title">Live RBAC Role Switcher</div>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
              Switch active role permissions to preview UI views under different security scopes:
            </p>
            <div className="role-pill-group">
              {availableRoles.map((r) => {
                const isActive = user.role === r.role;
                return (
                  <button
                    key={r.role}
                    type="button"
                    onClick={() => handleRoleChange(r.role)}
                    className={`role-switch-pill ${isActive ? 'active' : ''}`}
                    title={r.desc}
                  >
                    {r.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Security & Active Session Information */}
          <div>
            <div className="profile-section-title">Session Security (PRD §8.1)</div>
            <div
              style={{
                padding: '0.875rem',
                background: 'var(--bg-muted)',
                border: '1px solid var(--border-base)',
                borderRadius: 'var(--radius-md)',
                display: 'flex',
                flexDirection: 'column',
                gap: '6px',
                fontSize: '0.8125rem',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Access Token:</span>
                <span style={{ fontWeight: 600, color: 'var(--status-success)' }}>In-Memory (15m Short-Lived)</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Refresh Rotation:</span>
                <span style={{ fontWeight: 600 }}>HttpOnly Cookie (7 Days)</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Last Authenticated:</span>
                <span style={{ color: 'var(--text-secondary)' }}>Today, 18:32 UTC (Active Device)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Modal Footer Actions */}
        <div className="modal-footer">
          <button
            type="button"
            onClick={handleExportData}
            className="btn btn-secondary"
            style={{ fontSize: '12px', padding: '6px 12px' }}
          >
            {exportSuccess ? <Check size={14} style={{ color: 'var(--status-success)' }} /> : <Download size={14} />}
            {exportSuccess ? 'Data Exported!' : 'Export GDPR Profile (JSON)'}
          </button>

          <button
            type="button"
            onClick={() => setIsConfirmLogoutOpen(true)}
            className="btn btn-secondary"
            style={{ fontSize: '12px', padding: '6px 12px', color: 'var(--status-danger)', borderColor: 'var(--status-danger-border)' }}
          >
            <LogOut size={14} /> Sign Out
          </button>
        </div>
      </div>

      {/* ── Sign Out Confirmation Modal ────────────────────────────────────── */}
      <LogoutConfirmModal
        isOpen={isConfirmLogoutOpen}
        onClose={() => setIsConfirmLogoutOpen(false)}
        onConfirm={() => {
          setIsConfirmLogoutOpen(false);
          onClose();
          logout();
          navigate('/logout');
        }}
      />
    </div>
  );
};
