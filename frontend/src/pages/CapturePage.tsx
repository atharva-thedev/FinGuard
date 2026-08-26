import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  UploadCloud,
  Mail,
  Copy,
  Check,
  FileText,
  Sparkles,
  ArrowRight,
  ShieldAlert,
  CheckCircle2
} from 'lucide-react';

interface UploadItem {
  id: string;
  name: string;
  size: string;
  progress: number;
  status: 'uploading' | 'extracting' | 'completed' | 'needs_review';
  vendor?: string;
  amount?: number;
  confidence?: number;
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function inferVendorFromFilename(filename: string): string {
  const clean = filename.toLowerCase().replace(/[._-]/g, ' ');
  if (clean.includes('aws') || clean.includes('amazon')) return 'AWS Cloud Services';
  if (clean.includes('stripe')) return 'Stripe Payments Inc';
  if (clean.includes('uber')) return 'Uber for Business';
  if (clean.includes('datadog')) return 'Datadog Enterprise';
  if (clean.includes('google') || clean.includes('gcp')) return 'Google Cloud Platform';
  if (clean.includes('workday')) return 'Workday HCM';
  if (clean.includes('apex')) return 'Apex Logistics Corp';
  if (clean.includes('delta')) return 'Delta Global Supplies';
  if (clean.includes('staples')) return 'Staples Office Supplies';
  if (clean.includes('salesforce')) return 'Salesforce.com';

  // Capitalize words from filename if no match
  return (
    filename
      .split('.')[0]
      .replace(/[_-]/g, ' ')
      .replace(/\b\w/g, (c) => c.toUpperCase()) || 'Extracted Vendor Record'
  );
}

export const CapturePage: React.FC = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [copied, setCopied] = useState<boolean>(false);
  const [dragActive, setDragActive] = useState<boolean>(false);

  const [uploads, setUploads] = useState<UploadItem[]>([
    {
      id: 'up-1',
      name: 'Datadog_Annual_Invoice_Q3.pdf',
      size: '2.4 MB',
      progress: 100,
      status: 'completed',
      vendor: 'Datadog Enterprise',
      amount: 18500.0,
      confidence: 98.6,
    },
    {
      id: 'up-2',
      name: 'Uber_Receipt_Trip_9981.png',
      size: '850 KB',
      progress: 100,
      status: 'needs_review',
      vendor: 'Uber Business',
      amount: 45.2,
      confidence: 72.4,
    },
  ]);

  const handleCopyEmail = () => {
    navigator.clipboard.writeText('invoices+acme-global@finguard.ai');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const processFiles = (files: FileList | File[]) => {
    Array.from(files).forEach((file) => {
      const newId = 'up-' + Date.now() + '-' + Math.random().toString(36).substring(2, 6);
      const inferredVendor = inferVendorFromFilename(file.name);
      const randomAmount = Math.floor(Math.random() * 8500) + 120 + 0.5;
      const isHighConfidence = Math.random() > 0.25;
      const confidence = isHighConfidence
        ? Number((Math.random() * 8 + 92).toFixed(1))
        : Number((Math.random() * 15 + 68).toFixed(1));

      const newItem: UploadItem = {
        id: newId,
        name: file.name,
        size: formatBytes(file.size),
        progress: 25,
        status: 'uploading',
      };

      setUploads((prev) => [newItem, ...prev]);

      // Step 1: Uploading progress
      setTimeout(() => {
        setUploads((prev) =>
          prev.map((item) =>
            item.id === newId ? { ...item, progress: 70, status: 'extracting' } : item
          )
        );
      }, 800);

      // Step 2: OCR Extraction Complete
      setTimeout(() => {
        setUploads((prev) =>
          prev.map((item) =>
            item.id === newId
              ? {
                  ...item,
                  progress: 100,
                  status: isHighConfidence ? 'completed' : 'needs_review',
                  vendor: inferredVendor,
                  amount: randomAmount,
                  confidence: confidence,
                }
              : item
          )
        );
      }, 2000);
    });
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      processFiles(e.target.files);
      // Reset input value so re-uploading the same file works
      e.target.value = '';
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      processFiles(e.dataTransfer.files);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* ── Hidden Native File Input ───────────────────────────────────────── */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".pdf,.png,.jpg,.jpeg"
        style={{ display: 'none' }}
        onChange={handleFileInputChange}
      />

      {/* ── Page Header ───────────────────────────────────────────────────── */}
      <div>
        <h2>Invoice Capture & Batch Ingestion</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          Multi-page PDF upload, high-speed OCR extraction, and automated email forwarding inbox.
        </p>
      </div>

      {/* ── Top Dual Capture Grid ─────────────────────────────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem' }}>
        {/* Left: Drag & Drop Dropzone */}
        <div
          className="card"
          onDragOver={(e) => {
            e.preventDefault();
            setDragActive(true);
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          style={{
            border: dragActive ? '2px dashed var(--primary)' : '2px dashed var(--border-strong)',
            background: dragActive ? 'var(--gradient-brand-subtle)' : 'var(--bg-surface)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '3rem 2rem',
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all var(--transition-base)',
          }}
        >
          <div
            style={{
              width: '56px',
              height: '56px',
              borderRadius: 'var(--radius-full)',
              background: 'var(--brand-teal-glow)',
              color: 'var(--primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '1rem',
            }}
          >
            <UploadCloud size={28} />
          </div>
          <h3 style={{ fontSize: '1.125rem', marginBottom: '0.25rem' }}>
            Click to upload or drag & drop invoices
          </h3>
          <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', maxWidth: '420px', marginBottom: '1.25rem' }}>
            Supports PDF, JPG, PNG up to 25MB per file. Batch processing handles up to 50 documents simultaneously.
          </p>
          <button
            className="btn btn-primary"
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              fileInputRef.current?.click();
            }}
          >
            <UploadCloud size={16} /> Choose Documents from Computer
          </button>
        </div>

        {/* Right: Email Forwarding Ingestion Pill */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary)', marginBottom: '0.5rem' }}>
              <Mail size={20} />
              <h3 style={{ fontSize: '1rem' }}>Dedicated Email Ingestion</h3>
            </div>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
              Forward vendor invoices directly from email. FinGuard automatically ingests and attaches PDF line items.
            </p>
          </div>

          <div
            style={{
              padding: '0.875rem',
              background: 'var(--bg-muted)',
              border: '1px solid var(--border-base)',
              borderRadius: 'var(--radius-md)',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.5rem',
            }}
          >
            <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
              Your Org Ingestion Address:
            </span>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.5rem' }}>
              <code style={{ fontSize: '0.75rem', color: 'var(--text-primary)', wordBreak: 'break-all' }}>
                invoices+acme-global@finguard.ai
              </code>
              <button
                type="button"
                onClick={handleCopyEmail}
                className="btn btn-secondary"
                style={{ padding: '4px 8px', fontSize: '11px', flexShrink: 0 }}
              >
                {copied ? <Check size={13} style={{ color: 'var(--status-success)' }} /> : <Copy size={13} />}
                {copied ? 'Copied' : 'Copy'}
              </button>
            </div>
          </div>

          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Sparkles size={14} style={{ color: 'var(--primary)' }} />
            <span>AI automatically deduplicates email threads</span>
          </div>
        </div>
      </div>

      {/* ── Active Ingestion & Batch Queue ────────────────────────────────── */}
      <div className="card table-card">
        <div className="table-header">
          <div className="table-title-group">
            <h2>Recent Batch Ingestion Queue</h2>
            <p>Real-time OCR extraction pipeline and field parsing confidence</p>
          </div>
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="btn btn-secondary"
            style={{ fontSize: '0.8125rem' }}
          >
            + Upload from File Manager
          </button>
        </div>

        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Document File</th>
                <th>Size</th>
                <th>Extracted Vendor</th>
                <th>Extracted Amount</th>
                <th>OCR Confidence</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {uploads.map((item) => (
                <tr key={item.id}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
                      <FileText size={18} style={{ color: 'var(--primary)' }} />
                      <span style={{ fontWeight: 600 }}>{item.name}</span>
                    </div>
                  </td>
                  <td>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.8125rem' }}>{item.size}</span>
                  </td>
                  <td>
                    {item.vendor ? (
                      <span style={{ fontWeight: 500 }}>{item.vendor}</span>
                    ) : (
                      <span style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Extracting...</span>
                    )}
                  </td>
                  <td>
                    {item.amount ? (
                      <span className="amount-cell">${item.amount.toFixed(2)}</span>
                    ) : (
                      <span style={{ color: 'var(--text-muted)' }}>—</span>
                    )}
                  </td>
                  <td>
                    {item.confidence ? (
                      <span
                        className="badge"
                        style={{
                          background: item.confidence >= 85 ? 'var(--status-success-bg)' : 'var(--status-warning-bg)',
                          color: item.confidence >= 85 ? 'var(--status-success-text)' : 'var(--status-warning-text)',
                          border: item.confidence >= 85 ? '1px solid var(--status-success-border)' : '1px solid var(--status-warning-border)',
                        }}
                      >
                        {item.confidence >= 85 ? <CheckCircle2 size={12} /> : <ShieldAlert size={12} />}
                        {item.confidence.toFixed(1)}%
                      </span>
                    ) : (
                      <div style={{ width: '80px', height: '6px', background: 'var(--bg-muted)', borderRadius: '999px', overflow: 'hidden' }}>
                        <div style={{ width: `${item.progress}%`, height: '100%', background: 'var(--primary)' }} />
                      </div>
                    )}
                  </td>
                  <td>
                    {item.status === 'completed' && (
                      <span className="badge badge-success">Ready</span>
                    )}
                    {item.status === 'needs_review' && (
                      <span className="badge badge-warning">Needs Review (&lt;85%)</span>
                    )}
                    {item.status === 'uploading' && (
                      <span className="badge badge-info">Uploading {item.progress}%</span>
                    )}
                    {item.status === 'extracting' && (
                      <span className="badge badge-info">OCR Parsing...</span>
                    )}
                  </td>
                  <td>
                    <button
                      type="button"
                      onClick={() => navigate('/invoices/inv-104/review')}
                      className="btn btn-secondary"
                      style={{ padding: '3px 8px', fontSize: '11px' }}
                    >
                      Review Studio <ArrowRight size={12} />
                    </button>
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
