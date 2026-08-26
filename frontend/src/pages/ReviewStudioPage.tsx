import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  ZoomIn,
  ZoomOut,
  RotateCw,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  Plus,
  Trash2,
  Send
} from 'lucide-react';
import { initialInvoices } from '../lib/mockData';
import type { Invoice, LineItem } from '../lib/mockData';

export const ReviewStudioPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  // Find target invoice or fallback to sample
  const targetInvoice: Invoice =
    initialInvoices.find((i) => i.id === id) || initialInvoices[3];

  const [zoomLevel, setZoomLevel] = useState<number>(100);
  const [vendorName, setVendorName] = useState<string>(targetInvoice.vendor);
  const [invoiceNo, setInvoiceNo] = useState<string>(targetInvoice.invoiceNo);
  const [issueDate, setIssueDate] = useState<string>(targetInvoice.issueDate);
  const [dueDate, setDueDate] = useState<string>(targetInvoice.dueDate);
  const [category, setCategory] = useState<string>(targetInvoice.vendorCategory);
  const [lineItems, setLineItems] = useState<LineItem[]>(targetInvoice.lineItems);
  const [taxAmount, setTaxAmount] = useState<number>(targetInvoice.taxAmount);
  const [isSaved, setIsSaved] = useState<boolean>(false);

  // Recalculate subtotal
  const subtotal = lineItems.reduce((acc, item) => acc + item.total, 0);
  const calculatedTotal = subtotal + Number(taxAmount || 0);

  const handleUpdateLineItem = (itemId: string, field: keyof LineItem, value: any) => {
    setLineItems((prev) =>
      prev.map((item) => {
        if (item.id !== itemId) return item;
        const updated = { ...item, [field]: value };
        if (field === 'quantity' || field === 'unitPrice') {
          updated.total = Number(updated.quantity || 0) * Number(updated.unitPrice || 0);
        }
        return updated;
      })
    );
  };

  const handleAddLineItem = () => {
    const newItem: LineItem = {
      id: 'li-' + Date.now(),
      description: 'New Line Item Description',
      quantity: 1,
      unitPrice: 100.0,
      taxAmount: 10.0,
      total: 100.0,
    };
    setLineItems([...lineItems, newItem]);
  };

  const handleDeleteLineItem = (itemId: string) => {
    setLineItems(lineItems.filter((i) => i.id !== itemId));
  };

  const handleSaveAndRoute = () => {
    setIsSaved(true);
    setTimeout(() => {
      navigate('/invoices');
    }, 1200);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* ── Top Action Bar ────────────────────────────────────────────────── */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <button
            type="button"
            onClick={() => navigate('/invoices')}
            className="btn btn-secondary"
            style={{ padding: '6px 10px', fontSize: '13px' }}
          >
            <ArrowLeft size={16} /> Back to Invoices
          </button>
          <div>
            <h2 style={{ fontSize: '1.25rem' }}>
              Review Studio: <span style={{ fontFamily: 'var(--font-mono)' }}>{invoiceNo}</span>
            </h2>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Human-in-the-Loop AI Extraction Validation & Field Editor
            </span>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <span
            className="badge"
            style={{
              background: targetInvoice.confidenceScore >= 85 ? 'var(--status-success-bg)' : 'var(--status-warning-bg)',
              color: targetInvoice.confidenceScore >= 85 ? 'var(--status-success-text)' : 'var(--status-warning-text)',
              border: targetInvoice.confidenceScore >= 85 ? '1px solid var(--status-success-border)' : '1px solid var(--status-warning-border)',
              padding: '6px 12px',
              fontSize: '13px',
            }}
          >
            <Sparkles size={14} /> OCR Confidence: {targetInvoice.confidenceScore}%
          </span>

          <span
            className={`risk-pill ${
              targetInvoice.riskScore < 30
                ? 'risk-low'
                : targetInvoice.riskScore < 70
                ? 'risk-medium'
                : 'risk-high'
            }`}
            style={{ padding: '6px 12px', fontSize: '13px' }}
          >
            Risk Score: {targetInvoice.riskScore}/100
          </span>
        </div>
      </div>

      {/* ── 50/50 Split Studio Workspace ─────────────────────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', minHeight: '680px' }}>
        {/* Left Pane: Interactive Document Viewer */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', padding: 0, overflow: 'hidden' }}>
          {/* Document Toolbar */}
          <div
            style={{
              padding: '0.75rem 1rem',
              borderBottom: '1px solid var(--border-base)',
              background: 'var(--bg-muted)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <span style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              Source Document: {invoiceNo}.pdf (Page 1 of 1)
            </span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <button
                type="button"
                onClick={() => setZoomLevel((z) => Math.max(z - 15, 60))}
                className="btn btn-secondary"
                style={{ padding: '4px 8px' }}
                title="Zoom Out"
              >
                <ZoomOut size={14} />
              </button>
              <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', minWidth: '40px', textAlign: 'center' }}>
                {zoomLevel}%
              </span>
              <button
                type="button"
                onClick={() => setZoomLevel((z) => Math.min(z + 15, 160))}
                className="btn btn-secondary"
                style={{ padding: '4px 8px' }}
                title="Zoom In"
              >
                <ZoomIn size={14} />
              </button>
              <button
                type="button"
                onClick={() => setZoomLevel(100)}
                className="btn btn-secondary"
                style={{ padding: '4px 8px' }}
                title="Reset Zoom"
              >
                <RotateCw size={14} />
              </button>
            </div>
          </div>

          {/* Document Canvas Preview with OCR Bounding Boxes */}
          <div
            style={{
              flex: 1,
              background: 'var(--bg-app)',
              padding: '2rem',
              overflow: 'auto',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'flex-start',
            }}
          >
            <div
              style={{
                width: `${480 * (zoomLevel / 100)}px`,
                minHeight: `${620 * (zoomLevel / 100)}px`,
                background: '#ffffff',
                color: '#0f172a',
                borderRadius: 'var(--radius-sm)',
                boxShadow: 'var(--shadow-lg)',
                padding: '2rem',
                position: 'relative',
                fontSize: `${13 * (zoomLevel / 100)}px`,
                fontFamily: 'var(--font-sans)',
                border: '1px solid #cbd5e1',
              }}
            >
              {/* Simulated PDF Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '2px solid #0f172a', paddingBottom: '1rem', marginBottom: '1.5rem' }}>
                <div>
                  <div
                    style={{
                      border: '2px solid #0d9488',
                      background: 'rgba(13, 148, 136, 0.1)',
                      padding: '2px 6px',
                      borderRadius: '4px',
                      fontWeight: 800,
                      fontSize: '1.1em',
                    }}
                  >
                    {vendorName}
                  </div>
                  <div style={{ fontSize: '0.85em', color: '#64748b', marginTop: '4px' }}>
                    100 Innovation Way, Suite 400<br />San Francisco, CA 94107
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '1.4em', fontWeight: 800, letterSpacing: '-0.02em' }}>INVOICE</div>
                  <div
                    style={{
                      border: '2px solid #0d9488',
                      background: 'rgba(13, 148, 136, 0.1)',
                      padding: '2px 6px',
                      borderRadius: '4px',
                      fontFamily: 'var(--font-mono)',
                      fontWeight: 600,
                    }}
                  >
                    #{invoiceNo}
                  </div>
                </div>
              </div>

              {/* Simulated Dates */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem', fontSize: '0.9em' }}>
                <div>
                  <span style={{ color: '#64748b' }}>Date: </span>
                  <span style={{ fontWeight: 600 }}>{issueDate}</span>
                </div>
                <div>
                  <span style={{ color: '#64748b' }}>Due Date: </span>
                  <span style={{ fontWeight: 600 }}>{dueDate}</span>
                </div>
              </div>

              {/* Simulated Line Items Grid */}
              <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '1.5rem', fontSize: '0.85em' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid #cbd5e1', textAlign: 'left', color: '#64748b' }}>
                    <th style={{ padding: '6px 0' }}>Item Description</th>
                    <th style={{ padding: '6px 0', textAlign: 'right' }}>Qty</th>
                    <th style={{ padding: '6px 0', textAlign: 'right' }}>Price</th>
                    <th style={{ padding: '6px 0', textAlign: 'right' }}>Total</th>
                  </tr>
                </thead>
                <tbody>
                  {lineItems.map((li) => (
                    <tr key={li.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                      <td style={{ padding: '6px 0' }}>{li.description}</td>
                      <td style={{ padding: '6px 0', textAlign: 'right' }}>{li.quantity}</td>
                      <td style={{ padding: '6px 0', textAlign: 'right' }}>${li.unitPrice.toFixed(2)}</td>
                      <td style={{ padding: '6px 0', textAlign: 'right', fontWeight: 600 }}>${li.total.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Total Calculation Box */}
              <div style={{ marginLeft: 'auto', width: '200px', fontSize: '0.9em', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748b' }}>
                  <span>Subtotal:</span>
                  <span>${subtotal.toFixed(2)}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748b' }}>
                  <span>Tax Amount:</span>
                  <span>${Number(taxAmount || 0).toFixed(2)}</span>
                </div>
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    fontWeight: 800,
                    fontSize: '1.1em',
                    borderTop: '2px solid #0f172a',
                    paddingTop: '6px',
                    border: '2px solid #0d9488',
                    background: 'rgba(13, 148, 136, 0.1)',
                    padding: '4px 8px',
                    borderRadius: '4px',
                  }}
                >
                  <span>Total Due:</span>
                  <span>${calculatedTotal.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Pane: Structured Extraction Form & Validation */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', overflowY: 'auto' }}>
          <div>
            <h3 style={{ fontSize: '1.125rem' }}>Extracted Fields & Overrides</h3>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
              Validate fields extracted by AI. Low-confidence fields are highlighted in amber.
            </p>
          </div>

          {/* Form Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            {/* Vendor Name */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
                  Vendor Name *
                </label>
                <span className="badge badge-warning" style={{ fontSize: '10px' }}>74% OCR</span>
              </div>
              <input
                type="text"
                value={vendorName}
                onChange={(e) => setVendorName(e.target.value)}
                style={{
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-base)',
                  background: 'var(--bg-muted)',
                  color: 'var(--text-primary)',
                  fontSize: '0.875rem',
                  outline: 'none',
                }}
              />
            </div>

            {/* Invoice Number */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
                  Invoice Number *
                </label>
                <span className="badge badge-success" style={{ fontSize: '10px' }}>99% OCR</span>
              </div>
              <input
                type="text"
                value={invoiceNo}
                onChange={(e) => setInvoiceNo(e.target.value)}
                style={{
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-base)',
                  background: 'var(--bg-muted)',
                  color: 'var(--text-primary)',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.875rem',
                  outline: 'none',
                }}
              />
            </div>

            {/* Issue Date */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
                Issue Date *
              </label>
              <input
                type="date"
                value={issueDate}
                onChange={(e) => setIssueDate(e.target.value)}
                style={{
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-base)',
                  background: 'var(--bg-muted)',
                  color: 'var(--text-primary)',
                  fontSize: '0.875rem',
                  outline: 'none',
                }}
              />
            </div>

            {/* Due Date */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
                Due Date *
              </label>
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                style={{
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-base)',
                  background: 'var(--bg-muted)',
                  color: 'var(--text-primary)',
                  fontSize: '0.875rem',
                  outline: 'none',
                }}
              />
            </div>
          </div>

          {/* Category Taxonomy Feedback */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              Expense Category (Auto-Categorized)
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              style={{
                padding: '8px 12px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-base)',
                background: 'var(--bg-muted)',
                color: 'var(--text-primary)',
                fontSize: '0.875rem',
                outline: 'none',
              }}
            >
              <option value="Software & Infrastructure">Software & Infrastructure</option>
              <option value="Office Equipment">Office Equipment</option>
              <option value="Supply Chain">Supply Chain</option>
              <option value="HR & Systems">HR & Systems</option>
              <option value="Travel & Entertainment">Travel & Entertainment</option>
              <option value="Professional Services">Professional Services</option>
            </select>
            <span style={{ fontSize: '0.75rem', color: 'var(--primary)', display: 'flex', alignItems: 'center', gap: '4px', marginTop: '2px' }}>
              <Sparkles size={12} /> Auto-learning: Overrides will retrain categorization prompts for this vendor.
            </span>
          </div>

          {/* Line Items Editor */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <label style={{ fontSize: '0.8125rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                Line Items
              </label>
              <button
                type="button"
                onClick={handleAddLineItem}
                className="btn btn-secondary"
                style={{ padding: '3px 8px', fontSize: '11px' }}
              >
                <Plus size={12} /> Add Item
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {lineItems.map((li) => (
                <div
                  key={li.id}
                  style={{
                    display: 'grid',
                    gridTemplateColumns: '3fr 1fr 1fr 1fr auto',
                    gap: '6px',
                    alignItems: 'center',
                    padding: '6px',
                    background: 'var(--bg-muted)',
                    borderRadius: 'var(--radius-sm)',
                  }}
                >
                  <input
                    type="text"
                    value={li.description}
                    onChange={(e) => handleUpdateLineItem(li.id, 'description', e.target.value)}
                    style={{
                      padding: '4px 8px',
                      borderRadius: 'var(--radius-xs)',
                      border: '1px solid var(--border-base)',
                      background: 'var(--bg-surface)',
                      color: 'var(--text-primary)',
                      fontSize: '12px',
                    }}
                  />
                  <input
                    type="number"
                    value={li.quantity}
                    onChange={(e) => handleUpdateLineItem(li.id, 'quantity', parseFloat(e.target.value))}
                    style={{
                      padding: '4px 8px',
                      borderRadius: 'var(--radius-xs)',
                      border: '1px solid var(--border-base)',
                      background: 'var(--bg-surface)',
                      color: 'var(--text-primary)',
                      fontSize: '12px',
                    }}
                  />
                  <input
                    type="number"
                    value={li.unitPrice}
                    onChange={(e) => handleUpdateLineItem(li.id, 'unitPrice', parseFloat(e.target.value))}
                    style={{
                      padding: '4px 8px',
                      borderRadius: 'var(--radius-xs)',
                      border: '1px solid var(--border-base)',
                      background: 'var(--bg-surface)',
                      color: 'var(--text-primary)',
                      fontSize: '12px',
                    }}
                  />
                  <span style={{ fontSize: '12px', fontFamily: 'var(--font-mono)', fontWeight: 600, textAlign: 'right' }}>
                    ${li.total.toFixed(2)}
                  </span>
                  <button
                    type="button"
                    onClick={() => handleDeleteLineItem(li.id)}
                    style={{ background: 'transparent', border: 'none', color: 'var(--status-danger)', cursor: 'pointer' }}
                  >
                    <Trash2 size={13} />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Tax & Total Summary Box */}
          <div
            style={{
              padding: '1rem',
              background: 'var(--bg-muted)',
              border: '1px solid var(--border-base)',
              borderRadius: 'var(--radius-md)',
              display: 'flex',
              flexDirection: 'column',
              gap: '6px',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8125rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Subtotal:</span>
              <span style={{ fontWeight: 600 }}>${subtotal.toFixed(2)}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.8125rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Tax Amount:</span>
              <input
                type="number"
                value={taxAmount}
                onChange={(e) => setTaxAmount(parseFloat(e.target.value) || 0)}
                style={{
                  width: '90px',
                  textAlign: 'right',
                  padding: '2px 6px',
                  borderRadius: 'var(--radius-xs)',
                  border: '1px solid var(--border-base)',
                  background: 'var(--bg-surface)',
                  color: 'var(--text-primary)',
                  fontSize: '12px',
                }}
              />
            </div>
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                fontSize: '1rem',
                fontWeight: 800,
                borderTop: '1px solid var(--border-base)',
                paddingTop: '6px',
                color: 'var(--primary)',
              }}
            >
              <span>Calculated Total:</span>
              <span style={{ fontFamily: 'var(--font-mono)' }}>${calculatedTotal.toFixed(2)}</span>
            </div>
          </div>

          {/* Bottom Actions Bar */}
          <div style={{ display: 'flex', gap: '0.75rem', marginTop: 'auto', paddingTop: '1rem' }}>
            <button
              type="button"
              onClick={() => navigate('/exceptions')}
              className="btn btn-secondary"
              style={{ color: 'var(--status-danger)', borderColor: 'var(--status-danger-border)' }}
            >
              <AlertTriangle size={15} /> Flag Exception
            </button>
            <button
              type="button"
              onClick={handleSaveAndRoute}
              className="btn btn-primary"
              style={{ flex: 1 }}
            >
              {isSaved ? <CheckCircle2 size={16} /> : <Send size={16} />}
              {isSaved ? 'Validated & Routed!' : 'Save & Route to Approval'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
