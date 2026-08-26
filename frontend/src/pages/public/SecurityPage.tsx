import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ShieldCheck,
  Lock,
  KeyRound,
  FileKey2,
  Database,
  ArrowRight,
  EyeOff,
  History
} from 'lucide-react';

export const SecurityPage: React.FC = () => {
  const navigate = useNavigate();

  const securityFeatures = [
    {
      icon: <Database size={24} />,
      title: 'Tenant Isolation & Zero Leakage',
      desc: 'Every query is strictly scoped by organization_id. Cross-tenant queries return 404 NOT FOUND (never 403) to prevent resource existence disclosure.',
    },
    {
      icon: <Lock size={24} />,
      title: 'Short-Lived In-Memory JWT',
      desc: 'Access tokens are maintained in-memory only (never stored in localStorage) and rotate every 15 minutes via secure HttpOnly SameSite cookies.',
    },
    {
      icon: <FileKey2 size={24} />,
      title: 'AES-256-GCM & Bcrypt-12',
      desc: 'Sensitive ERP OAuth credentials and bank details are encrypted using authenticated AES-256-GCM. Passwords use 12-round salted bcrypt hashing.',
    },
    {
      icon: <History size={24} />,
      title: 'Immutable SOC 2 Audit Trail',
      desc: 'All approvals, OCR overrides, and configuration changes are timestamped with IP attribution and cryptographically signed log records.',
    },
    {
      icon: <EyeOff size={24} />,
      title: 'GDPR & CCPA Data Rights',
      desc: 'Native data export and right-to-erasure endpoints ensure full compliance with global privacy regulations.',
    },
    {
      icon: <KeyRound size={24} />,
      title: 'Enterprise SSO & SAML 2.0',
      desc: 'Direct integration with Okta, Google Workspace, Azure AD, and custom SAML identity providers.',
    },
  ];

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '4rem 2rem', display: 'flex', flexDirection: 'column', gap: '4rem' }}>
      {/* Hero */}
      <div style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            alignSelf: 'center',
            padding: '6px 14px',
            borderRadius: 'var(--radius-full)',
            background: 'var(--brand-teal-glow)',
            color: 'var(--primary)',
            fontSize: '0.8125rem',
            fontWeight: 600,
          }}
        >
          <ShieldCheck size={14} /> Bank-Grade Financial Security
        </div>
        <h1 style={{ fontSize: 'clamp(2.25rem, 4vw, 3.5rem)', fontWeight: 800, lineHeight: 1.15 }}>
          Enterprise Security & Trust Architecture
        </h1>
        <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          FinGuard is built from the ground up for strict multi-tenant isolation, cryptographic auditability, and SOC 2 Type II compliance.
        </p>
      </div>

      {/* Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2rem' }}>
        {securityFeatures.map((f, i) => (
          <div key={i} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', padding: '2rem' }}>
            <div
              style={{
                width: '48px',
                height: '48px',
                borderRadius: 'var(--radius-md)',
                background: 'var(--brand-teal-glow)',
                color: 'var(--primary)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              {f.icon}
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>{f.title}</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6 }}>
              {f.desc}
            </p>
          </div>
        ))}
      </div>

      {/* Compliance Matrix Card */}
      <div className="card" style={{ padding: '2.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem' }}>Security Standards & Certifications</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.5rem' }}>
          <div className="feature-pill-box" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '6px' }}>
            <div style={{ fontWeight: 700, fontSize: '1.125rem', color: 'var(--primary)' }}>SOC 2 Type II</div>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>Continuous automated security controls & independent third-party audits.</p>
          </div>
          <div className="feature-pill-box" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '6px' }}>
            <div style={{ fontWeight: 700, fontSize: '1.125rem', color: 'var(--primary)' }}>GDPR Compliant</div>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>Complete data residency controls, encrypted exports, and right to be forgotten.</p>
          </div>
          <div className="feature-pill-box" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '6px' }}>
            <div style={{ fontWeight: 700, fontSize: '1.125rem', color: 'var(--primary)' }}>TLS 1.3 & AES-256</div>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>End-to-end encryption in transit and at rest with hardware security modules.</p>
          </div>
        </div>
      </div>

      {/* Bottom CTA */}
      <div
        className="card"
        style={{
          textAlign: 'center',
          padding: '4rem 2rem',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '1.25rem',
        }}
      >
        <h2>Request Our Full Security Audit Whitepaper</h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '540px', lineHeight: 1.6 }}>
          Speak with our compliance engineers to review our penetration test reports and architecture.
        </p>
        <button
          type="button"
          onClick={() => navigate('/signup')}
          className="btn btn-primary"
          style={{ padding: '0.875rem 2rem', fontSize: '1rem', marginTop: '0.5rem' }}
        >
          Get Started Securely <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
};
