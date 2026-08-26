import React, { useState } from 'react';
import {
  CheckCircle2,
  XCircle,
  Clock,
  ArrowRight,
  AlertCircle
} from 'lucide-react';
import { initialApprovals } from '../lib/mockData';
import type { ApprovalItem } from '../lib/mockData';

export const ApprovalsPage: React.FC = () => {
  const [approvals, setApprovals] = useState<ApprovalItem[]>(initialApprovals);
  const [rejectingId, setRejectingId] = useState<string | null>(null);
  const [rejectionReason, setRejectionReason] = useState<string>('');
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);

  const handleApprove = (id: string, vendor: string) => {
    setApprovals((prev) =>
      prev.map((item) => (item.id === id ? { ...item, status: 'approved' } : item))
    );
    setActionSuccess(`Successfully approved invoice from ${vendor}. Logged in audit trail.`);
    setTimeout(() => setActionSuccess(null), 3000);
  };

  const handleConfirmReject = () => {
    if (!rejectingId) return;
    setApprovals((prev) =>
      prev.map((item) => (item.id === rejectingId ? { ...item, status: 'rejected' } : item))
    );
    setActionSuccess(`Invoice rejected. Reason logged in compliance audit trail.`);
    setRejectingId(null);
    setRejectionReason('');
    setTimeout(() => setActionSuccess(null), 3000);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* ── Header ────────────────────────────────────────────────────────── */}
      <div>
        <h2>Approvals Decision Hub</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          Role-scoped approval queue, multi-tier chain visualizers, and 1-click decision authorization.
        </p>
      </div>

      {actionSuccess && (
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
          <CheckCircle2 size={16} /> {actionSuccess}
        </div>
      )}

      {/* ── Approvals Feed ─────────────────────────────────────────────────── */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        {approvals.map((item) => {
          const isPending = item.status === 'pending';
          return (
            <div
              key={item.id}
              className="card"
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '1.25rem',
                opacity: isPending ? 1 : 0.65,
                borderLeft: isPending ? '4px solid var(--primary)' : '4px solid var(--border-base)',
              }}
            >
              {/* Card Top Row */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                  <div
                    style={{
                      width: '44px',
                      height: '44px',
                      borderRadius: 'var(--radius-md)',
                      background: 'var(--bg-muted)',
                      border: '1px solid var(--border-base)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 800,
                      fontSize: '14px',
                      color: 'var(--text-primary)',
                    }}
                  >
                    {item.vendor.slice(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <h3 style={{ fontSize: '1.125rem' }}>{item.vendor}</h3>
                      <span className="invoice-number" style={{ fontSize: '0.8125rem' }}>
                        {item.invoiceNo}
                      </span>
                    </div>
                    <span style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
                      Requested by {item.requestedBy} • {item.department} ({item.category})
                    </span>
                  </div>
                </div>

                <div style={{ textAlign: 'right' }}>
                  <div className="amount-cell" style={{ fontSize: '1.5rem', fontWeight: 800 }}>
                    ${item.amount.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                  </div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    Payment Due: {item.dueDate}
                  </span>
                </div>
              </div>

              {/* Approval Sequence Chain Timeline */}
              <div
                style={{
                  padding: '0.875rem 1.25rem',
                  background: 'var(--bg-muted)',
                  border: '1px solid var(--border-base)',
                  borderRadius: 'var(--radius-md)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  flexWrap: 'wrap',
                  gap: '1rem',
                }}
              >
                <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                  Approval Authority Chain:
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
                  {item.approvalChain.map((step, idx) => (
                    <React.Fragment key={step.role}>
                      <div
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '6px',
                          fontSize: '0.8125rem',
                          fontWeight: step.status === 'current' ? 700 : 500,
                          color:
                            step.status === 'approved'
                              ? 'var(--status-success-text)'
                              : step.status === 'current'
                              ? 'var(--primary)'
                              : 'var(--text-muted)',
                        }}
                      >
                        {step.status === 'approved' ? (
                          <CheckCircle2 size={15} style={{ color: 'var(--status-success)' }} />
                        ) : step.status === 'current' ? (
                          <Clock size={15} style={{ color: 'var(--primary)' }} />
                        ) : (
                          <div
                            style={{
                              width: '12px',
                              height: '12px',
                              borderRadius: '50%',
                              border: '1px solid var(--border-strong)',
                            }}
                          />
                        )}
                        <span>
                          {step.role} ({step.name})
                        </span>
                      </div>
                      {idx < item.approvalChain.length - 1 && (
                        <ArrowRight size={14} style={{ color: 'var(--border-strong)' }} />
                      )}
                    </React.Fragment>
                  ))}
                </div>
              </div>

              {/* Card Actions Footer */}
              {isPending ? (
                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
                  <button
                    type="button"
                    onClick={() => setRejectingId(item.id)}
                    className="btn btn-secondary"
                    style={{ color: 'var(--status-danger)', borderColor: 'var(--status-danger-border)' }}
                  >
                    <XCircle size={16} /> Reject with Reason
                  </button>
                  <button
                    type="button"
                    onClick={() => handleApprove(item.id, item.vendor)}
                    className="btn btn-primary"
                    style={{ padding: '0.5rem 1.5rem' }}
                  >
                    <CheckCircle2 size={16} /> 1-Click Authorize Approval
                  </button>
                </div>
              ) : (
                <div style={{ textAlign: 'right' }}>
                  <span
                    className={`badge ${item.status === 'approved' ? 'badge-success' : 'badge-danger'}`}
                    style={{ fontSize: '13px', padding: '5px 12px' }}
                  >
                    {item.status === 'approved' ? 'Authorized & Scheduled' : 'Rejected'}
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* ── Rejection Reason Modal ─────────────────────────────────────────── */}
      {rejectingId && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0, 0, 0, 0.7)',
            backdropFilter: 'blur(8px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 100,
            padding: '1rem',
          }}
        >
          <div className="card" style={{ maxWidth: '520px', width: '100%', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--status-danger)' }}>
              <AlertCircle size={22} />
              <h3 style={{ fontSize: '1.25rem' }}>Reject Invoice Authorization</h3>
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Rejection requires a mandatory audit comment explaining policy violations or discrepancies. This note will be immutably recorded.
            </p>

            <textarea
              rows={4}
              placeholder="e.g. Price exceeds contractual SLA or personal expense not covered under policy..."
              value={rejectionReason}
              onChange={(e) => setRejectionReason(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 14px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-base)',
                background: 'var(--bg-muted)',
                color: 'var(--text-primary)',
                fontSize: '0.875rem',
                outline: 'none',
              }}
            />

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
              <button
                type="button"
                onClick={() => setRejectingId(null)}
                className="btn btn-secondary"
              >
                Cancel
              </button>
              <button
                type="button"
                disabled={!rejectionReason.trim()}
                onClick={handleConfirmReject}
                className="btn btn-primary"
                style={{ background: 'var(--status-danger)', opacity: !rejectionReason.trim() ? 0.5 : 1 }}
              >
                Confirm Rejection
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
