import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Cpu,
  CheckCircle2,
  AlertTriangle,
  FileCheck2
} from 'lucide-react';

export const FeaturesPage: React.FC = () => {
  const navigate = useNavigate();

  const corePillars = [
    {
      badge: 'Capture & Perception',
      icon: <Cpu size={28} />,
      title: 'Multimodal OCR & Visual Line Extraction',
      description:
        'FinGuard processes native PDFs, scanned TIFFs, and mobile camera receipts in under 1.2 seconds. Dynamic bounding boxes map line items, tax IDs, and remittance tables with 99.4% precision.',
      bullets: [
        '50-document simultaneous batch dropzone',
        'Automatic subtotal, tax rate, and math reconciliation',
        'Interactive 50/50 side-by-side human-in-the-loop studio',
        'Self-learning vendor template recollection',
      ],
    },
    {
      badge: 'Matching & Verification',
      icon: <FileCheck2 size={28} />,
      title: 'Autonomous 3-Way Reconciliation',
      description:
        'Line-by-line cross-matching against Purchase Orders and Goods Received Notes (GRN). Configurable price tolerances and quantity matching rules allow straight-through approval.',
      bullets: [
        'Real-time ERP PO synchronization (QBO, NetSuite)',
        'Automatic partial delivery & backorder tracking',
        'Configurable zero-touch tolerance thresholds',
        'Automated line-item categorization & GL code suggestions',
      ],
    },
    {
      badge: 'Fraud & Policy Guard',
      icon: <AlertTriangle size={28} />,
      title: 'Real-Time Duplicate & Spend Overrun Defense',
      description:
        'Advanced fuzzy string matching and multi-variable similarity scoring detect duplicate invoices before payment execution, preventing rogue spend and vendor bank tampering.',
      bullets: [
        'Multi-vector duplicate similarity scoring',
        'Live department budget cap warnings',
        'Vendor bank IBAN / routing number anomaly alerts',
        'Audit-mandatory exception resolution drawer',
      ],
    },
    {
      badge: 'Governance & Execution',
      icon: <ShieldCheck size={28} />,
      title: 'Multi-Tier Approval Authority Matrix',
      description:
        'Route invoices dynamically according to department budget owners and dollar thresholds (Level 1 AP Clerk $\\rightarrow$ Level 2 Dept Manager $\\rightarrow$ Level 3 CFO).',
      bullets: [
        '1-click batch authorization queues',
        'Transparent visual authority timelines',
        'Mandatory rejection reason audit trail',
        'Live Slack and Email notification triggers',
      ],
    },
  ];

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '4rem 2rem', display: 'flex', flexDirection: 'column', gap: '4rem' }}>
      {/* Hero Header */}
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
          <Sparkles size={14} /> FinGuard Autonomous Feature Architecture
        </div>
        <h1 style={{ fontSize: 'clamp(2.25rem, 4vw, 3.5rem)', fontWeight: 800, lineHeight: 1.15 }}>
          The Complete Intelligent AP Automation Stack
        </h1>
        <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          Explore the cutting-edge AI capabilities engineered to eliminate manual data entry, prevent duplicate fraud, and guarantee continuous audit compliance.
        </p>
      </div>

      {/* Deep Dive Pillars */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem' }}>
        {corePillars.map((pillar, idx) => (
          <div
            key={idx}
            className="card"
            style={{
              padding: '2.5rem',
              display: 'grid',
              gridTemplateColumns: '1fr 1.2fr',
              gap: '2.5rem',
              alignItems: 'center',
            }}
          >
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  textTransform: 'uppercase',
                  color: 'var(--primary)',
                  letterSpacing: '0.05em',
                }}
              >
                {pillar.badge}
              </div>
              <h2 style={{ fontSize: '1.625rem', fontWeight: 800 }}>{pillar.title}</h2>
              <p style={{ color: 'var(--text-secondary)', lineHeight: 1.6, fontSize: '0.9375rem' }}>
                {pillar.description}
              </p>
            </div>

            <div
              className="inner-box"
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '0.875rem',
              }}
            >
              <div style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--text-primary)', marginBottom: '4px' }}>
                Key Capabilities:
              </div>
              {pillar.bullets.map((b, bIdx) => (
                <div key={bIdx} style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.875rem' }}>
                  <CheckCircle2 size={16} style={{ color: 'var(--status-success)', flexShrink: 0 }} />
                  <span>{b}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
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
        <h2>Experience FinGuard in Action</h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '500px' }}>
          Test the OCR Review Studio and 3-Way matching engine on your own invoices.
        </p>
        <button
          type="button"
          onClick={() => navigate('/signup')}
          className="btn btn-primary"
          style={{ padding: '0.875rem 2rem', fontSize: '1rem' }}
        >
          Start 14-Day Free Trial <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
};
