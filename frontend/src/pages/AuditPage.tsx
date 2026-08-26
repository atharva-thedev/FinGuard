import React, { useState } from 'react';
import { Search, Lock } from 'lucide-react';
import { initialAuditLogs } from '../lib/mockData';
import type { AuditLog } from '../lib/mockData';

export const AuditPage: React.FC = () => {
  const [logs] = useState<AuditLog[]>(initialAuditLogs);
  const [search, setSearch] = useState<string>('');

  const filtered = logs.filter(
    (l) =>
      l.actor.toLowerCase().includes(search.toLowerCase()) ||
      l.action.toLowerCase().includes(search.toLowerCase()) ||
      l.details.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2>Compliance Audit Trail</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Immutable, append-only security logs for extraction overrides, approval decisions, and policy overrides.
          </p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8125rem', color: 'var(--status-success)' }}>
          <Lock size={14} />
          <span style={{ fontWeight: 600 }}>SOC 2 Type II Immutable Store</span>
        </div>
      </div>

      {/* Search */}
      <div className="card" style={{ padding: '0.75rem 1.25rem' }}>
        <div className="search-container" style={{ maxWidth: '400px' }}>
          <Search size={14} style={{ color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search audit trail by actor, action, or details..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />
        </div>
      </div>

      {/* Audit Table */}
      <div className="card table-card">
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Timestamp (UTC)</th>
                <th>Actor</th>
                <th>Role</th>
                <th>Action</th>
                <th>Resource ID</th>
                <th>Audit Details & State Diff</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((log) => (
                <tr key={log.id}>
                  <td>
                    <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-secondary)' }}>
                      {log.timestamp}
                    </span>
                  </td>
                  <td>
                    <span style={{ fontWeight: 600 }}>{log.actor}</span>
                  </td>
                  <td>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.8125rem' }}>{log.role}</span>
                  </td>
                  <td>
                    <code style={{ fontSize: '11px', padding: '2px 6px', background: 'var(--bg-muted)', borderRadius: '4px' }}>
                      {log.action}
                    </code>
                  </td>
                  <td>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--primary)' }}>
                      {log.resourceId}
                    </span>
                  </td>
                  <td>
                    <span style={{ fontSize: '0.8125rem', color: 'var(--text-primary)' }}>{log.details}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
