import React, { useState } from 'react';
import { Search, ShieldCheck } from 'lucide-react';
import { initialVendors } from '../lib/mockData';
import type { Vendor } from '../lib/mockData';

export const VendorsPage: React.FC = () => {
  const [vendors] = useState<Vendor[]>(initialVendors);
  const [search, setSearch] = useState<string>('');

  const filtered = vendors.filter(
    (v) =>
      v.name.toLowerCase().includes(search.toLowerCase()) ||
      v.category.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2>Vendors Directory & Risk Index</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Unified vendor directory, spend concentration, payment terms, and automated fraud risk scores.
          </p>
        </div>
        <button className="btn btn-primary">+ Add New Vendor</button>
      </div>

      {/* Search Bar */}
      <div className="card" style={{ padding: '0.75rem 1.25rem' }}>
        <div className="search-container" style={{ maxWidth: '400px' }}>
          <Search size={14} style={{ color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search vendor by name or category..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />
        </div>
      </div>

      {/* Vendor Table */}
      <div className="card table-card">
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Vendor Name</th>
                <th>Category</th>
                <th>Cumulative Spend</th>
                <th>Invoice Volume</th>
                <th>Payment Terms</th>
                <th>Risk Profile</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((v) => (
                <tr key={v.id}>
                  <td>
                    <div className="vendor-cell">
                      <div className="vendor-avatar">{v.name.slice(0, 2).toUpperCase()}</div>
                      <span className="vendor-name">{v.name}</span>
                    </div>
                  </td>
                  <td>
                    <span style={{ color: 'var(--text-secondary)' }}>{v.category}</span>
                  </td>
                  <td>
                    <span className="amount-cell">${v.totalSpend.toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
                  </td>
                  <td>
                    <span style={{ fontWeight: 600 }}>{v.invoiceCount} invoices</span>
                  </td>
                  <td>
                    <span style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>{v.paymentTerms}</span>
                  </td>
                  <td>
                    <span
                      className={`badge ${
                        v.riskRating === 'low'
                          ? 'badge-success'
                          : v.riskRating === 'medium'
                          ? 'badge-warning'
                          : 'badge-danger'
                      }`}
                      style={{ textTransform: 'uppercase', fontSize: '10px' }}
                    >
                      {v.riskRating} Risk
                    </span>
                  </td>
                  <td>
                    <span className="badge badge-success">
                      <ShieldCheck size={12} /> {v.status}
                    </span>
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
