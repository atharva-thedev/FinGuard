import React, { useState } from 'react';
import { NavLink, Outlet, useNavigate, Link } from 'react-router-dom';
import {
  LayoutDashboard,
  UploadCloud,
  FileSpreadsheet,
  AlertTriangle,
  CheckSquare,
  Building2,
  BarChart3,
  ShieldCheck,
  Settings,
  Search,
  Plus,
  PanelLeftClose,
  PanelLeft,
  LogOut,
  ChevronDown
} from 'lucide-react';
import { ThemeToggle } from '../ThemeToggle';
import { UserProfileModal } from '../UserProfile/UserProfileModal';
import { LogoutConfirmModal } from '../Auth/LogoutConfirmModal';
import { useAuth } from '../../auth/AuthProvider';
import { useTheme } from '../../theme/ThemeProvider';
import './AppLayout.css';

export const AppLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState<boolean>(false);
  const [isProfileOpen, setIsProfileOpen] = useState<boolean>(false);
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState<boolean>(false);
  const { user, logout } = useAuth();
  const { resolvedTheme } = useTheme();
  const navigate = useNavigate();

  const navItems = [
    { to: '/dashboard', label: 'Dashboard', icon: <LayoutDashboard size={18} /> },
    { to: '/capture', label: 'Capture & Ingest', icon: <UploadCloud size={18} />, pill: '+Batch', pillClass: 'nav-pill-info' },
    { to: '/invoices', label: 'Invoices Queue', icon: <FileSpreadsheet size={18} />, pill: '5', pillClass: 'nav-pill-info' },
    { to: '/exceptions', label: 'Exceptions Queue', icon: <AlertTriangle size={18} />, pill: '3', pillClass: 'nav-pill-danger' },
    { to: '/approvals', label: 'Approvals Hub', icon: <CheckSquare size={18} />, pill: '3', pillClass: 'nav-pill-warning' },
    { to: '/vendors', label: 'Vendors Directory', icon: <Building2 size={18} /> },
    { to: '/reports', label: 'Spend & Analytics', icon: <BarChart3 size={18} /> },
    { to: '/audit', label: 'Audit Logs', icon: <ShieldCheck size={18} /> },
    { to: '/settings', label: 'Settings & Policy', icon: <Settings size={18} /> },
  ];

  return (
    <div className="layout-root">
      {/* ── Collapsible Sidebar ───────────────────────────────────────────── */}
      <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
        {/* Brand Header with Logo */}
        <div className="sidebar-header">
          <Link to="/dashboard" title="Go to Dashboard" style={{ display: 'inline-block', textDecoration: 'none' }}>
            <img
              src={resolvedTheme === 'dark' ? '/logo-dark.png' : '/logo.png'}
              alt="FinGuard — Go to Dashboard"
              className="sidebar-brand-logo"
            />
          </Link>
          {!collapsed && (
            <div className="sidebar-org-select-pill">
              <span>Acme Global Corp</span>
              <ChevronDown size={13} style={{ color: 'var(--text-muted)' }} />
            </div>
          )}
        </div>

        {/* Navigation Items */}
        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `nav-link-item ${isActive ? 'active' : ''}`}
              title={collapsed ? item.label : undefined}
            >
              <span className="nav-icon">{item.icon}</span>
              {!collapsed && (
                <>
                  <span className="nav-text">{item.label}</span>
                  {item.pill && (
                    <span className={`nav-pill ${item.pillClass}`}>{item.pill}</span>
                  )}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        {/* Sidebar Footer */}
        <div className="sidebar-footer">
          <div
            className="sidebar-user"
            onClick={() => setIsProfileOpen(true)}
            title="Click to view profile & security details"
          >
            <div className="user-info-group">
              <div className="user-avatar-badge">
                {user?.name ? user.name.slice(0, 2).toUpperCase() : 'AV'}
              </div>
              {!collapsed && (
                <div className="user-details">
                  <span className="user-name-text">{user?.name || 'Alex Vance'}</span>
                  <span className="user-role-text">{user?.role || 'Controller'}</span>
                </div>
              )}
            </div>

            {!collapsed && (
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  setIsLogoutModalOpen(true);
                }}
                title="Sign out"
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-muted)',
                  cursor: 'pointer',
                  padding: '4px',
                  display: 'flex',
                }}
              >
                <LogOut size={16} />
              </button>
            )}
          </div>
        </div>
      </aside>

      {/* ── User Profile & Security Details Modal ──────────────────────────── */}
      <UserProfileModal
        isOpen={isProfileOpen}
        onClose={() => setIsProfileOpen(false)}
      />

      {/* ── Sign Out Confirmation Modal ────────────────────────────────────── */}
      <LogoutConfirmModal
        isOpen={isLogoutModalOpen}
        onClose={() => setIsLogoutModalOpen(false)}
        onConfirm={() => {
          setIsLogoutModalOpen(false);
          logout();
          navigate('/logout');
        }}
      />

      {/* ── Main Viewport Area ────────────────────────────────────────────── */}
      <div className="main-wrapper">
        {/* Sticky Top Navigation Bar */}
        <header className="top-header">
          <div className="header-left">
            <button
              type="button"
              onClick={() => setCollapsed(!collapsed)}
              className="toggle-sidebar-btn"
              title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            >
              {collapsed ? <PanelLeft size={18} /> : <PanelLeftClose size={18} />}
            </button>

            <div className="search-container">
              <Search size={15} style={{ color: 'var(--text-muted)' }} />
              <input
                type="text"
                placeholder="Search invoices, vendors, PO numbers..."
                className="search-input"
              />
              <span className="search-kbd">⌘K</span>
            </div>
          </div>

          <div className="header-right">
            {/* Theme Toggle Selector */}
            <ThemeToggle variant="segmented" />

            {/* Quick Upload Action */}
            <button
              type="button"
              onClick={() => navigate('/capture')}
              className="btn btn-primary"
              style={{ padding: '0.45rem 0.875rem', fontSize: '0.8125rem' }}
            >
              <Plus size={15} /> Upload Invoice
            </button>
          </div>
        </header>

        {/* Dynamic Nested Route Content */}
        <main className="page-viewport">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
