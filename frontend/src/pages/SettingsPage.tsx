import React, { useState } from 'react';
import { Sliders, Database, CheckCircle2 } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [qboConnected, setQboConnected] = useState<boolean>(true);
  const [netSuiteConnected, setNetSuiteConnected] = useState<boolean>(false);
  const [autoApproveThreshold, setAutoApproveThreshold] = useState<number>(1000);
  const [controllerThreshold, setControllerThreshold] = useState<number>(10000);
  const [saved, setSaved] = useState<boolean>(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '1000px' }}>
      {/* Header */}
      <div>
        <h2>Organization Policies & System Configuration</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          Configure approval thresholds, ERP connectors, department budget rules, and user roles.
        </p>
      </div>

      {saved && (
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
          <CheckCircle2 size={16} /> Configuration updated successfully!
        </div>
      )}

      {/* Approval Threshold Rules */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Sliders size={18} style={{ color: 'var(--primary)' }} />
          <h3>Approval Authority Thresholds</h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.25rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <label style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              Auto-Approve Limit (Passes 3-Way Match)
            </label>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontFamily: 'var(--font-mono)' }}>$</span>
              <input
                type="number"
                value={autoApproveThreshold}
                onChange={(e) => setAutoApproveThreshold(Number(e.target.value))}
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-base)',
                  background: 'var(--bg-muted)',
                  color: 'var(--text-primary)',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.875rem',
                }}
              />
            </div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Invoices under this amount skip manual review if PO matches 100%.
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <label style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              CFO / Executive Signoff Threshold
            </label>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontFamily: 'var(--font-mono)' }}>$</span>
              <input
                type="number"
                value={controllerThreshold}
                onChange={(e) => setControllerThreshold(Number(e.target.value))}
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-base)',
                  background: 'var(--bg-muted)',
                  color: 'var(--text-primary)',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.875rem',
                }}
              />
            </div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Invoices exceeding this amount require Controller and CFO signoff.
            </span>
          </div>
        </div>
      </div>

      {/* ERP Integrations */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Database size={18} style={{ color: 'var(--primary)' }} />
          <h3>ERP & Accounting System Connectors</h3>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '12px 16px',
              background: 'var(--bg-muted)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-base)',
            }}
          >
            <div>
              <div style={{ fontWeight: 600, fontSize: '0.875rem' }}>QuickBooks Online (QBO)</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                Syncs chart of accounts, vendors, and paid invoice receipts.
              </div>
            </div>
            <button
              type="button"
              onClick={() => setQboConnected(!qboConnected)}
              className={`btn ${qboConnected ? 'btn-primary' : 'btn-secondary'}`}
              style={{ fontSize: '12px' }}
            >
              {qboConnected ? 'Connected' : 'Connect'}
            </button>
          </div>

          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '12px 16px',
              background: 'var(--bg-muted)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-base)',
            }}
          >
            <div>
              <div style={{ fontWeight: 600, fontSize: '0.875rem' }}>Oracle NetSuite ERP</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                Two-way 3-way matching synchronization for purchase orders & GRNs.
              </div>
            </div>
            <button
              type="button"
              onClick={() => setNetSuiteConnected(!netSuiteConnected)}
              className={`btn ${netSuiteConnected ? 'btn-primary' : 'btn-secondary'}`}
              style={{ fontSize: '12px' }}
            >
              {netSuiteConnected ? 'Connected' : 'Connect'}
            </button>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <button
        type="button"
        onClick={handleSave}
        className="btn btn-primary"
        style={{ alignSelf: 'flex-start', padding: '0.625rem 1.75rem' }}
      >
        Save Policy Settings
      </button>
    </div>
  );
};
