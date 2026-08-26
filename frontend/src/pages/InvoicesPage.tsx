import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Search,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Eye
} from 'lucide-react';
import { initialInvoices } from '../lib/mockData';
import type { Invoice } from '../lib/mockData';

export const InvoicesPage: React.FC = () => {
  const navigate = useNavigate();
  const [activeFilter, setActiveFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const filteredInvoices = initialInvoices.filter((inv) => {
    const matchesFilter =
      activeFilter === 'all' ||
      (activeFilter === 'needs_review' && inv.status === 'needs_review') ||
      (activeFilter === 'pending_approval' && inv.status === 'pending_approval') ||
      (activeFilter === 'approved' && inv.status === 'approved') ||
      (activeFilter === 'exception' && inv.status === 'exception');

    const matchesSearch =
      inv.vendor.toLowerCase().includes(searchQuery.toLowerCase()) ||
      inv.invoiceNo.toLowerCase().includes(searchQuery.toLowerCase()) ||
      inv.department.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesFilter && matchesSearch;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* ── Header ────────────────────────────────────────────────────────── */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <h2>Invoices Management Queue</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Unified processing queue for all ingested invoices, policy validations, and review states.
          </p>
        </div>
        <button
          type="button"
          onClick={() => navigate('/capture')}
          className="btn btn-primary"
        >
          + Upload Invoices
        </button>
      </div>

      {/* ── Filter Bar & Search ───────────────────────────────────────────── */}
      <div className="card" style={{ padding: '0.875rem 1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        {/* Status Filter Tabs */}
        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
          {[
            { id: 'all', label: 'All Invoices', count: initialInvoices.length },
            { id: 'needs_review', label: 'Needs Review', count: initialInvoices.filter(i => i.status === 'needs_review').length },
            { id: 'pending_approval', label: 'Pending Approval', count: initialInvoices.filter(i => i.status === 'pending_approval').length },
            { id: 'approved', label: 'Approved', count: initialInvoices.filter(i => i.status === 'approved').length },
            { id: 'exception', label: 'Exceptions', count: initialInvoices.filter(i => i.status === 'exception').length },
          ].map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveFilter(tab.id)}
              className={`btn ${activeFilter === tab.id ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '5px 12px', fontSize: '13px' }}
            >
              {tab.label}
              <span style={{
                fontSize: '11px',
                padding: '1px 5px',
                borderRadius: '999px',
                background: activeFilter === tab.id ? 'rgba(255,255,255,0.2)' : 'var(--bg-muted)',
                marginLeft: '4px'
              }}>
                {tab.count}
              </span>
            </button>
          ))}
        </div>

        {/* Search Bar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', minWidth: '260px' }}>
          <div className="search-container" style={{ width: '100%' }}>
            <Search size={14} style={{ color: 'var(--text-muted)' }} />
            <input
              type="text"
              placeholder="Filter by vendor, invoice #..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
          </div>
        </div>
      </div>

      {/* ── Main Invoices Table ───────────────────────────────────────────── */}
      <div className="card table-card">
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Vendor / Invoice #</th>
                <th>Category / Dept</th>
                <th>Issue Date</th>
                <th>Due Date</th>
                <th>Total Amount</th>
                <th>Status</th>
                <th>Confidence</th>
                <th>Risk Score</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredInvoices.length > 0 ? (
                filteredInvoices.map((inv: Invoice) => (
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
                      <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <span style={{ fontWeight: 500, fontSize: '0.8125rem' }}>{inv.vendorCategory}</span>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{inv.department}</span>
                      </div>
                    </td>
                    <td>
                      <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>{inv.issueDate}</span>
                    </td>
                    <td>
                      <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>{inv.dueDate}</span>
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
                          <AlertTriangle size={12} /> Exception
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
                        className="badge"
                        style={{
                          background: inv.confidenceScore >= 85 ? 'var(--status-success-bg)' : 'var(--status-warning-bg)',
                          color: inv.confidenceScore >= 85 ? 'var(--status-success-text)' : 'var(--status-warning-text)',
                          border: inv.confidenceScore >= 85 ? '1px solid var(--status-success-border)' : '1px solid var(--status-warning-border)',
                        }}
                      >
                        {inv.confidenceScore}%
                      </span>
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
                        style={{ padding: '4px 10px', fontSize: '12px' }}
                      >
                        <Eye size={13} /> Open Studio
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={9} style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                    No invoices match the selected filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
