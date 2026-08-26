import React from 'react';
import { Download, BarChart2, PieChart, Calendar } from 'lucide-react';

export const ReportsPage: React.FC = () => {
  const categorySpend = [
    { category: 'Software & Infrastructure', amount: 142500, percentage: 48, color: 'var(--primary)' },
    { category: 'Supply Chain & Logistics', amount: 89400, percentage: 30, color: 'var(--status-info)' },
    { category: 'HR Systems & Recruiting', amount: 38200, percentage: 13, color: 'var(--status-success)' },
    { category: 'Office Equipment & Facilities', amount: 26800, percentage: 9, color: 'var(--status-warning)' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <img
            src="/logo.png"
            alt="FinGuard"
            style={{ width: '38px', height: '38px', objectFit: 'contain' }}
          />
          <div>
            <h2>Spend Intelligence & Financial Analytics</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              Interactive spend breakdowns, vendor concentration analysis, and budget variance heatmaps.
            </p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button className="btn btn-secondary" style={{ fontSize: '13px' }}>
            <Calendar size={14} /> Q3 2026 ▾
          </button>
          <button className="btn btn-primary" style={{ fontSize: '13px' }}>
            <Download size={14} /> Export CSV Audit Pack
          </button>
        </div>
      </div>

      {/* Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        {/* Category Breakdown Card */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <PieChart size={18} style={{ color: 'var(--primary)' }} />
            <h3>Spend Distribution by Category</h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {categorySpend.map((item) => (
              <div key={item.category} style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8125rem' }}>
                  <span style={{ fontWeight: 600 }}>{item.category}</span>
                  <span style={{ fontFamily: 'var(--font-mono)' }}>
                    ${item.amount.toLocaleString()} ({item.percentage}%)
                  </span>
                </div>
                <div style={{ width: '100%', height: '8px', background: 'var(--bg-muted)', borderRadius: '999px', overflow: 'hidden' }}>
                  <div style={{ width: `${item.percentage}%`, height: '100%', background: item.color, borderRadius: '999px' }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Department Budget vs Actual Variance */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <BarChart2 size={18} style={{ color: 'var(--primary)' }} />
            <h3>Department Budget vs. Actual</h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {[
              { dept: 'Engineering', budget: 100000, actual: 82400, status: 'On Track' },
              { dept: 'Marketing', budget: 50000, actual: 47200, status: 'Warning (94%)' },
              { dept: 'Operations', budget: 70000, actual: 31000, status: 'Healthy' },
              { dept: 'People & HR', budget: 40000, actual: 28900, status: 'On Track' },
            ].map((d) => (
              <div
                key={d.dept}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '10px 14px',
                  background: 'var(--bg-muted)',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-base)',
                }}
              >
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.875rem' }}>{d.dept}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    Budget: ${d.budget.toLocaleString()} • Incurred: ${d.actual.toLocaleString()}
                  </div>
                </div>
                <span
                  className={`badge ${
                    d.status.includes('Warning') ? 'badge-warning' : 'badge-success'
                  }`}
                >
                  {d.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
