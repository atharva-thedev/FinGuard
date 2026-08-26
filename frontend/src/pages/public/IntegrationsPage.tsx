import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ArrowRight,
  CheckCircle2,
  Share2
} from 'lucide-react';

export const IntegrationsPage: React.FC = () => {
  const navigate = useNavigate();

  const integrations = [
    {
      name: 'QuickBooks Online (QBO)',
      category: 'Accounting & Ledger',
      desc: 'Automatic two-way chart of accounts sync, vendor directory sync, and automated bill payment reconciliation.',
      status: 'Native Connector',
    },
    {
      name: 'Oracle NetSuite',
      category: 'Enterprise ERP',
      desc: '3-way PO & GRN line matching, multi-subsidiary currency translation, and dynamic GL account coding.',
      status: 'Native Connector',
    },
    {
      name: 'SAP S/4HANA',
      category: 'Enterprise ERP',
      desc: 'High-throughput enterprise batch matching, purchase order automation, and SAP IDoc integration.',
      status: 'Enterprise Certified',
    },
    {
      name: 'Xero Accounting',
      category: 'Accounting & Ledger',
      desc: 'Direct draft bill creation, tax rate alignment, and automated payment receipt attachment.',
      status: 'Native Connector',
    },
    {
      name: 'Stripe Billing & Payments',
      category: 'Payment Gateway',
      desc: 'Automated invoice fee ingestion, chargeback discrepancy detection, and subscription fee reconciliation.',
      status: 'Plug & Play',
    },
    {
      name: 'AWS / GCP Cloud Billing',
      category: 'Cloud Infrastructure',
      desc: 'Granular cost-center line item breakdown, compute usage analytics, and department budget alerting.',
      status: 'Automated Parser',
    },
    {
      name: 'Slack & Microsoft Teams',
      category: 'Notifications & Alerts',
      desc: 'Instant 1-click approval actions in Slack channels, duplicate fraud alerts, and daily AP digests.',
      status: 'Instant Webhook',
    },
    {
      name: 'FinGuard REST API & Webhooks',
      category: 'Developer Platform',
      desc: 'Full OpenAPI v3 compliant REST endpoints for custom ERPs, webhook event streams, and batch ingestion.',
      status: 'OpenAPI v3',
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
          <Share2 size={14} /> Unified Financial Ecosystem
        </div>
        <h1 style={{ fontSize: 'clamp(2.25rem, 4vw, 3.5rem)', fontWeight: 800, lineHeight: 1.15 }}>
          Connects Seamlessly With Your Existing Financial Stack
        </h1>
        <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          Sync vendors, purchase orders, general ledger codes, and approval workflows across all major ERPs and communication tools with zero disruption.
        </p>
      </div>

      {/* Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
        {integrations.map((item, i) => (
          <div key={i} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', padding: '1.75rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                {item.category}
              </span>
              <span className="badge badge-success" style={{ fontSize: '11px' }}>
                {item.status}
              </span>
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>{item.name}</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.5, flex: 1 }}>
              {item.desc}
            </p>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8125rem', color: 'var(--primary)', fontWeight: 600 }}>
              <CheckCircle2 size={14} /> Bidirectional Sync Supported
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
        <h2>Need a Custom ERP or Core Banking Connector?</h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '500px' }}>
          Explore our REST API documentation and Postman collections to connect custom proprietary workflows.
        </p>
        <button
          type="button"
          onClick={() => navigate('/signup')}
          className="btn btn-primary"
          style={{ padding: '0.875rem 2rem', fontSize: '1rem' }}
        >
          Explore Integration API <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
};
