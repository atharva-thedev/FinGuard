import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FileSpreadsheet,
  CheckCircle2,
  AlertTriangle,
  DollarSign,
  Sparkles,
  Zap,
  ArrowRight,
  Clock,
  Send
} from 'lucide-react';
import { initialInvoices } from '../lib/mockData';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* ── Hero Status Banner ────────────────────────────────────────────── */}
      <section className="hero-banner">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <img
            src="/logo2.png"
            alt="FinGuard"
            style={{
              height: '56px',
              width: 'auto',
              objectFit: 'contain',
              flexShrink: 0,
            }}
          />
          <div className="hero-text">
            <h1>Autonomous Invoice & Expense Intelligence</h1>
            <p>
              Continuous 3-way matching, OCR confidence scoring, and real-time fraud mitigation
              protecting organization spend.
            </p>
          </div>
        </div>
        <div className="hero-metrics">
          <div className="hero-metric-item">
            <div className="hero-metric-icon">
              <Sparkles size={20} />
            </div>
            <div>
              <div className="hero-metric-title">AI Extraction</div>
              <div className="hero-metric-value">98.4% Acc.</div>
            </div>
          </div>
          <div className="hero-metric-item">
            <div className="hero-metric-icon">
              <Zap size={20} />
            </div>
            <div>
              <div className="hero-metric-title">Avg. Latency</div>
              <div className="hero-metric-value">1.8 sec</div>
            </div>
          </div>
        </div>
      </section>

      {/* ── KPI Metric Grid ───────────────────────────────────────────────── */}
      <section className="kpi-grid">
        <div className="card kpi-card">
          <div className="kpi-header">
            <span className="kpi-title">Invoices Processed</span>
            <div className="kpi-icon-wrap" style={{ background: 'var(--status-info-bg)', color: 'var(--status-info)' }}>
              <FileSpreadsheet size={18} />
            </div>
          </div>
          <div className="kpi-value">2,842</div>
          <div className="kpi-footer">
            <span className="trend-up">↑ 14.8%</span> vs previous month
          </div>
        </div>

        <div className="card kpi-card">
          <div className="kpi-header">
            <span className="kpi-title">Auto-Matched & Cleared</span>
            <div className="kpi-icon-wrap" style={{ background: 'var(--status-success-bg)', color: 'var(--status-success)' }}>
              <CheckCircle2 size={18} />
            </div>
          </div>
          <div className="kpi-value">94.2%</div>
          <div className="kpi-footer">
            <span className="trend-up">↑ 2.1%</span> OCR confidence
          </div>
        </div>

        <div className="card kpi-card">
          <div className="kpi-header">
            <span className="kpi-title">Risk Anomalies Intercepted</span>
            <div className="kpi-icon-wrap" style={{ background: 'var(--status-danger-bg)', color: 'var(--status-danger)' }}>
              <AlertTriangle size={18} />
            </div>
          </div>
          <div className="kpi-value">18</div>
          <div className="kpi-footer">
            <span className="trend-down">3 High Risk</span> holds active
          </div>
        </div>

        <div className="card kpi-card">
          <div className="kpi-header">
            <span className="kpi-title">Captured Early Discounts</span>
            <div className="kpi-icon-wrap" style={{ background: 'var(--brand-teal-glow)', color: 'var(--primary)' }}>
              <DollarSign size={18} />
            </div>
          </div>
          <div className="kpi-value">$46,290</div>
          <div className="kpi-footer">
            <span className="trend-up">↑ $8.4k</span> dynamic payment terms
          </div>
        </div>
      </section>

      {/* ── Content Grid ──────────────────────────────────────────────────── */}
      <div className="content-grid">
        {/* Live Ingestion Stream Table */}
        <div className="card table-card">
          <div className="table-header">
            <div className="table-title-group">
              <h2>Live Ingestion Stream</h2>
              <p>Real-time queue across PDF, scan, and email forwarding channels</p>
            </div>
            <button
              type="button"
              onClick={() => navigate('/invoices')}
              className="btn btn-secondary"
              style={{ fontSize: '0.8125rem' }}
            >
              View All Queue <ArrowRight size={14} />
            </button>
          </div>
          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Vendor / Invoice</th>
                  <th>Department</th>
                  <th>Amount</th>
                  <th>Status</th>
                  <th>Risk Score</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {initialInvoices.map((inv) => (
                  <tr key={inv.id}>
                    <td>
                      <div className="vendor-cell">
                        <div className="vendor-avatar">
                          {inv.vendor.slice(0, 2).toUpperCase()}
                        </div>
                        <div className="vendor-info">
                          <span className="vendor-name">{inv.vendor}</span>
                          <span className="invoice-number">{inv.invoiceNo}</span>
                        </div>
                      </div>
                    </td>
                    <td>
                      <span style={{ color: 'var(--text-secondary)' }}>{inv.department}</span>
                    </td>
                    <td>
                      <span className="amount-cell">
                        ${inv.totalAmount.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                      </span>
                    </td>
                    <td>
                      {inv.status === 'approved' && (
                        <span className="badge badge-success">
                          <CheckCircle2 size={12} /> Approved
                        </span>
                      )}
                      {inv.status === 'needs_review' && (
                        <span className="badge badge-warning">
                          <Clock size={12} /> Needs Review
                        </span>
                      )}
                      {inv.status === 'pending_approval' && (
                        <span className="badge badge-info">
                          <Clock size={12} /> Pending Approval
                        </span>
                      )}
                      {inv.status === 'exception' && (
                        <span className="badge badge-danger">
                          <AlertTriangle size={12} /> Exception Flag
                        </span>
                      )}
                      {inv.status === 'validated' && (
                        <span className="badge badge-success">
                          <CheckCircle2 size={12} /> Validated
                        </span>
                      )}
                    </td>
                    <td>
                      <span
                        className={`risk-pill ${
                          inv.riskScore < 30
                            ? 'risk-low'
                            : inv.riskScore < 70
                            ? 'risk-medium'
                            : 'risk-high'
                        }`}
                      >
                        {inv.riskScore}/100
                      </span>
                    </td>
                    <td>
                      <button
                        type="button"
                        onClick={() => navigate(`/invoices/${inv.id}/review`)}
                        className="btn btn-secondary"
                        style={{ padding: '3px 8px', fontSize: '11px' }}
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right Side: Budget Health & Copilot */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Department Budget Utilization */}
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <h3>Department Budget Velocity</h3>
              <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
                Q3 2026 Monthly Budget Burn Rate
              </p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8125rem', marginBottom: '4px' }}>
                  <span style={{ fontWeight: 600 }}>Engineering</span>
                  <span style={{ color: 'var(--text-muted)' }}>$82,400 / $100,000 (82.4%)</span>
                </div>
                <div style={{ width: '100%', height: '8px', background: 'var(--bg-muted)', borderRadius: '999px', overflow: 'hidden' }}>
                  <div style={{ width: '82.4%', height: '100%', background: 'var(--primary)', borderRadius: '999px' }} />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8125rem', marginBottom: '4px' }}>
                  <span style={{ fontWeight: 600 }}>Marketing</span>
                  <span style={{ color: 'var(--status-warning)', fontWeight: 600 }}>$47,200 / $50,000 (94.4%)</span>
                </div>
                <div style={{ width: '100%', height: '8px', background: 'var(--bg-muted)', borderRadius: '999px', overflow: 'hidden' }}>
                  <div style={{ width: '94.4%', height: '100%', background: 'var(--status-warning)', borderRadius: '999px' }} />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8125rem', marginBottom: '4px' }}>
                  <span style={{ fontWeight: 600 }}>Operations</span>
                  <span style={{ color: 'var(--text-muted)' }}>$31,000 / $70,000 (44.3%)</span>
                </div>
                <div style={{ width: '100%', height: '8px', background: 'var(--bg-muted)', borderRadius: '999px', overflow: 'hidden' }}>
                  <div style={{ width: '44.3%', height: '100%', background: 'var(--status-success)', borderRadius: '999px' }} />
                </div>
              </div>
            </div>
          </div>

          {/* AI Finance Copilot Quick Bar */}
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Sparkles size={18} style={{ color: 'var(--primary)' }} />
              <h3 style={{ fontSize: '1rem' }}>AI Finance Copilot</h3>
            </div>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
              Ask natural language queries across vendor pricing changes, fraud anomalies, and cash flow forecasts.
            </p>
            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.25rem' }}>
              <input
                type="text"
                placeholder="e.g. Find vendors with price spikes >10%..."
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-base)',
                  background: 'var(--bg-surface)',
                  color: 'var(--text-primary)',
                  fontSize: '0.8125rem',
                  outline: 'none',
                }}
              />
              <button className="btn btn-primary" style={{ padding: '8px 12px' }}>
                <Send size={14} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
