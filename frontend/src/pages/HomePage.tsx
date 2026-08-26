import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  AlertTriangle,
  Lock,
  Database,
  Cpu,
  Check
} from 'lucide-react';
import { useAuth } from '../auth/AuthProvider';
import './HomePage.css';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const features = [
    {
      icon: <Sparkles size={24} />,
      title: 'Autonomous 3-Way Matching',
      desc: 'Instant PO-to-Invoice line reconciliation and GRN validation with automated policy tolerance checks.',
    },
    {
      icon: <Cpu size={24} />,
      title: 'High-Speed OCR Studio',
      desc: '50/50 side-by-side visual bounding boxes, auto-tax recalculation, and continuous field learning.',
    },
    {
      icon: <AlertTriangle size={24} />,
      title: 'AI Fraud & Duplicate Shield',
      desc: 'Multi-variable similarity detection flags duplicate invoices, IBAN changes, and department budget overruns.',
    },
    {
      icon: <ShieldCheck size={24} />,
      title: 'Multi-Tier Approvals Chain',
      desc: 'Configurable approval authority matrix with 1-click approvals and transparent audit timelines.',
    },
    {
      icon: <Database size={24} />,
      title: 'Continuous ERP Connectors',
      desc: 'Seamless two-way integration with QuickBooks Online, NetSuite, SAP, and custom REST webhooks.',
    },
    {
      icon: <Lock size={24} />,
      title: 'SOC 2 Immutable Audit Trail',
      desc: 'Every upload, override, and authorization is cryptographically logged with tamper-proof tenant scoping.',
    },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      {/* ── Hero Section ──────────────────────────────────────────────────── */}
      <section className="home-hero">
        <div className="hero-pill-tag">
          <Sparkles size={14} /> Enterprise AI Finance & Autonomous AP Ingestion
        </div>

        <h1 className="home-hero-title">
          Protect, Analyze & <span>Optimize</span> Enterprise Cash Flow
        </h1>

        <p className="home-hero-subtitle">
          FinGuard empowers modern finance teams with continuous 3-way matching, AI invoice capture,
          real-time duplicate fraud defense, and immutable SOC 2 audit readiness.
        </p>

        <div className="home-hero-cta-group">
          <button
            type="button"
            onClick={() => navigate(isAuthenticated ? '/dashboard' : '/signup')}
            className="btn btn-primary"
            style={{ padding: '0.875rem 2rem', fontSize: '1rem' }}
          >
            {isAuthenticated ? 'Launch Workspace' : 'Start Free 14-Day Trial'} <ArrowRight size={18} />
          </button>
          <button
            type="button"
            onClick={() => navigate('/features')}
            className="btn btn-secondary"
            style={{ padding: '0.875rem 1.75rem', fontSize: '1rem' }}
          >
            Explore Platform Features
          </button>
        </div>

        {/* Interactive App Preview Banner */}
        <div className="home-preview-frame">
          <div className="preview-browser-bar">
            <span className="browser-dot red" />
            <span className="browser-dot yellow" />
            <span className="browser-dot green" />
            <div className="preview-browser-url">https://app.finguard.ai/dashboard</div>
          </div>

          <div
            style={{
              padding: '1.5rem',
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: '1rem',
              background: 'var(--bg-muted)',
              borderRadius: 'var(--radius-md)',
            }}
          >
            <div className="kpi-card" style={{ padding: '1rem' }}>
              <span className="kpi-label">Auto-Processed (Passes 3-Way)</span>
              <span className="kpi-value" style={{ fontSize: '1.5rem', color: 'var(--status-success)' }}>
                98.4%
              </span>
              <span className="kpi-subtext">Zero-touch matching</span>
            </div>
            <div className="kpi-card" style={{ padding: '1rem' }}>
              <span className="kpi-label">Exceptions Triaged</span>
              <span className="kpi-value" style={{ fontSize: '1.5rem', color: 'var(--status-danger)' }}>
                3 Flagged
              </span>
              <span className="kpi-subtext">$1,450 duplicate prevented</span>
            </div>
            <div className="kpi-card" style={{ padding: '1rem' }}>
              <span className="kpi-label">Avg. Ingestion Speed</span>
              <span className="kpi-value" style={{ fontSize: '1.5rem', color: 'var(--primary)' }}>
                1.2s / doc
              </span>
              <span className="kpi-subtext">Async OCR extraction</span>
            </div>
            <div className="kpi-card" style={{ padding: '1rem' }}>
              <span className="kpi-label">Month-to-Date Spend</span>
              <span className="kpi-value" style={{ fontSize: '1.5rem' }}>$482,900</span>
              <span className="kpi-subtext">Synced to QuickBooks</span>
            </div>
          </div>
        </div>
      </section>

      {/* ── Stats Strip ───────────────────────────────────────────────────── */}
      <section className="home-stats-strip">
        <div className="stat-item">
          <h3>99.4%</h3>
          <p>OCR Field Accuracy</p>
        </div>
        <div className="stat-item">
          <h3>10x</h3>
          <p>Faster AP Processing Cycle</p>
        </div>
        <div className="stat-item">
          <h3>$0</h3>
          <p>Duplicate Payment Leakage</p>
        </div>
        <div className="stat-item">
          <h3>SOC 2</h3>
          <p>Type II Certified Compliance</p>
        </div>
      </section>

      {/* ── 3-Box Feature Value Strip (Inspiration Design) ────────────────── */}
      <section style={{ maxWidth: '1200px', width: '100%', margin: '0 auto', padding: '0 2rem 3rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem' }}>
          <div className="feature-pill-box">
            <div className="feature-pill-check-icon">
              <Check size={16} strokeWidth={3} />
            </div>
            <div className="feature-pill-text">
              See what is due, what is blocked, and what needs attention next
            </div>
          </div>
          <div className="feature-pill-box">
            <div className="feature-pill-check-icon">
              <Check size={16} strokeWidth={3} />
            </div>
            <div className="feature-pill-text">
              Catch duplicate spend and unbilled work earlier, before it turns into write-downs
            </div>
          </div>
          <div className="feature-pill-box">
            <div className="feature-pill-check-icon">
              <Check size={16} strokeWidth={3} />
            </div>
            <div className="feature-pill-text">
              Keep the work, the client conversation, and the billing trail tied together
            </div>
          </div>
        </div>
      </section>

      {/* ── Features Section ──────────────────────────────────────────────── */}
      <section id="features" className="home-features-section">
        <div className="home-section-header">
          <h2>Engineered for High-Growth Finance Teams</h2>
          <p style={{ color: 'var(--text-secondary)' }}>
            Replace manual spreadsheets and brittle rule engines with autonomous AI document intelligence.
          </p>
        </div>

        <div className="home-features-grid">
          {features.map((f, i) => (
            <div key={i} className="feature-card">
              <div className="feature-icon-wrapper">{f.icon}</div>
              <h3 style={{ fontSize: '1.125rem' }}>{f.title}</h3>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                {f.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA Banner ────────────────────────────────────────────────────── */}
      <section className="home-cta-banner">
        <h2 style={{ fontSize: '2rem', fontWeight: 800 }}>Ready to automate your AP pipeline?</h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '540px', fontSize: '1rem' }}>
          Join leading finance leaders who trust FinGuard to safeguard their enterprise accounts payable.
        </p>
        <button
          type="button"
          onClick={() => navigate('/signup')}
          className="btn btn-primary"
          style={{ padding: '0.875rem 2rem', fontSize: '1rem' }}
        >
          Create Enterprise Workspace <ArrowRight size={18} />
        </button>
      </section>
    </div>
  );
};
