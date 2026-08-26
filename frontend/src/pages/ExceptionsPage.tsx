import React, { useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  XCircle
} from 'lucide-react';
import { initialExceptions } from '../lib/mockData';
import type { ExceptionItem } from '../lib/mockData';

export const ExceptionsPage: React.FC = () => {
  const [exceptions, setExceptions] = useState<ExceptionItem[]>(initialExceptions);
  const [activeFilter, setActiveFilter] = useState<string>('all');
  const [selectedException, setSelectedException] = useState<ExceptionItem | null>(initialExceptions[0]);
  const [auditComment, setAuditComment] = useState<string>('');
  const [resolvedMsg, setResolvedMsg] = useState<string | null>(null);

  const filtered = exceptions.filter((exc) => {
    if (activeFilter === 'all') return true;
    return exc.type === activeFilter;
  });

  const handleResolve = (action: 'dismiss' | 'override') => {
    if (!selectedException) return;
    setExceptions((prev) =>
      prev.map((e) =>
        e.id === selectedException.id
          ? { ...e, status: action === 'dismiss' ? 'dismissed' : 'resolved' }
          : e
      )
    );
    setResolvedMsg(
      action === 'dismiss'
        ? `Exception on ${selectedException.invoiceNo} was voided/dismissed.`
        : `Exception on ${selectedException.invoiceNo} was overridden with audit note logged.`
    );
    setAuditComment('');
    setTimeout(() => setResolvedMsg(null), 3000);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* ── Header ────────────────────────────────────────────────────────── */}
      <div>
        <h2>Unified Exceptions & Risk Queue</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          Triaged fraud anomalies, exact/fuzzy duplicate matches, price variances, and budget policy overruns.
        </p>
      </div>

      {resolvedMsg && (
        <div
          style={{
            padding: '0.875rem 1.25rem',
            background: 'var(--status-success-bg)',
            border: '1px solid var(--status-success-border)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--status-success-text)',
            fontSize: '0.875rem',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}
        >
          <CheckCircle2 size={16} /> {resolvedMsg}
        </div>
      )}

      {/* ── Filter Tabs ───────────────────────────────────────────────────── */}
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        {[
          { id: 'all', label: 'All Active Exceptions' },
          { id: 'duplicate', label: 'Duplicates (Exact & Fuzzy)' },
          { id: 'budget_exceeded', label: 'Budget Policy Overruns' },
          { id: 'price_mismatch', label: 'Price / Quantity Mismatches' },
        ].map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setActiveFilter(tab.id)}
            className={`btn ${activeFilter === tab.id ? 'btn-primary' : 'btn-secondary'}`}
            style={{ padding: '6px 14px', fontSize: '13px' }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* ── Main Two Column Workspace ─────────────────────────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.6fr 1.2fr', gap: '1.5rem' }}>
        {/* Left: Exception List Table */}
        <div className="card table-card">
          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Exception Type</th>
                  <th>Invoice / Vendor</th>
                  <th>Amount</th>
                  <th>Severity</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((exc) => {
                  const isSelected = selectedException?.id === exc.id;
                  return (
                    <tr
                      key={exc.id}
                      onClick={() => setSelectedException(exc)}
                      style={{
                        cursor: 'pointer',
                        background: isSelected ? 'var(--bg-surface-hover)' : undefined,
                        borderLeft: isSelected ? '3px solid var(--primary)' : undefined,
                      }}
                    >
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <AlertTriangle
                            size={16}
                            style={{
                              color:
                                exc.severity === 'critical'
                                  ? 'var(--status-danger)'
                                  : exc.severity === 'high'
                                  ? 'var(--status-warning)'
                                  : 'var(--status-info)',
                            }}
                          />
                          <span style={{ fontWeight: 600, fontSize: '0.8125rem', textTransform: 'capitalize' }}>
                            {exc.type.replace('_', ' ')}
                          </span>
                        </div>
                      </td>
                      <td>
                        <div style={{ display: 'flex', flexDirection: 'column' }}>
                          <span style={{ fontWeight: 600 }}>{exc.vendor}</span>
                          <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                            {exc.invoiceNo}
                          </span>
                        </div>
                      </td>
                      <td>
                        <span className="amount-cell">${exc.amount.toFixed(2)}</span>
                      </td>
                      <td>
                        <span
                          className={`badge ${
                            exc.severity === 'critical'
                              ? 'badge-danger'
                              : exc.severity === 'high'
                              ? 'badge-warning'
                              : 'badge-info'
                          }`}
                          style={{ textTransform: 'uppercase', fontSize: '10px' }}
                        >
                          {exc.severity}
                        </span>
                      </td>
                      <td style={{ whiteSpace: 'nowrap' }}>
                        {exc.status === 'open' && (
                          <span className="badge badge-warning" style={{ whiteSpace: 'nowrap' }}>Action Required</span>
                        )}
                        {exc.status === 'resolved' && (
                          <span className="badge badge-success" style={{ whiteSpace: 'nowrap' }}>Resolved</span>
                        )}
                        {exc.status === 'dismissed' && (
                          <span className="badge badge-danger" style={{ whiteSpace: 'nowrap' }}>Voided</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right: Resolution Drawer & Audit Box */}
        {selectedException && (
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <span className="badge badge-danger" style={{ textTransform: 'uppercase', marginBottom: '6px' }}>
                  {selectedException.severity} Severity
                </span>
                <h3 style={{ fontSize: '1.125rem' }}>Exception Diagnostic</h3>
                <span style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
                  Triggered: {selectedException.triggeredAt}
                </span>
              </div>
              <span className="amount-cell" style={{ fontSize: '1.25rem' }}>
                ${selectedException.amount.toFixed(2)}
              </span>
            </div>

            {/* Explanation Callout */}
            <div
              style={{
                padding: '1rem',
                background: 'var(--status-danger-bg)',
                border: '1px solid var(--status-danger-border)',
                borderRadius: 'var(--radius-md)',
                color: 'var(--status-danger-text)',
                fontSize: '0.875rem',
                lineHeight: 1.4,
              }}
            >
              <strong>Detected Conflict:</strong> {selectedException.message}
            </div>

            {/* Side by Side Conflict Diagnostic Preview */}
            <div
              style={{
                padding: '1rem',
                background: 'var(--bg-muted)',
                border: '1px solid var(--border-base)',
                borderRadius: 'var(--radius-md)',
                fontSize: '0.8125rem',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.5rem',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Target Invoice:</span>
                <span style={{ fontWeight: 600, fontFamily: 'var(--font-mono)' }}>{selectedException.invoiceNo}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Vendor Record:</span>
                <span style={{ fontWeight: 600 }}>{selectedException.vendor}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Assigned Resolution Role:</span>
                <span style={{ fontWeight: 600, textTransform: 'capitalize', color: 'var(--primary)' }}>
                  {selectedException.assignedRole}
                </span>
              </div>
            </div>

            {/* Audit Justification Input */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                Resolution Reason / Audit Note *
              </label>
              <textarea
                rows={3}
                placeholder="Document reason for override or dismissal (recorded in SOC 2 compliance log)..."
                value={auditComment}
                onChange={(e) => setAuditComment(e.target.value)}
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-base)',
                  background: 'var(--bg-surface)',
                  color: 'var(--text-primary)',
                  fontSize: '0.8125rem',
                  outline: 'none',
                  resize: 'vertical',
                }}
              />
            </div>

            {/* Resolution Actions */}
            <div style={{ display: 'flex', gap: '0.75rem', marginTop: 'auto', paddingTop: '0.5rem' }}>
              <button
                type="button"
                onClick={() => handleResolve('dismiss')}
                className="btn btn-secondary"
                style={{ flex: 1, color: 'var(--status-danger)' }}
              >
                <XCircle size={15} /> Void / Dismiss Duplicate
              </button>
              <button
                type="button"
                onClick={() => handleResolve('override')}
                className="btn btn-primary"
                style={{ flex: 1 }}
              >
                <CheckCircle2 size={15} /> Override & Clear
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
