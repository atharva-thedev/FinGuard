export interface LineItem {
  id: string;
  description: string;
  quantity: number;
  unitPrice: number;
  taxAmount: number;
  total: number;
}

export interface Invoice {
  id: string;
  invoiceNo: string;
  vendor: string;
  vendorCategory: string;
  department: string;
  issueDate: string;
  dueDate: string;
  subtotal: number;
  taxAmount: number;
  totalAmount: number;
  status: 'captured' | 'extracting' | 'needs_review' | 'validated' | 'pending_approval' | 'approved' | 'rejected' | 'exception';
  confidenceScore: number; // 0 - 100
  lowConfidenceFields?: string[];
  riskScore: number; // 0 - 100
  lineItems: LineItem[];
  fileUrl?: string;
  poNumber?: string;
  paymentTerms: string;
}

export interface ExceptionItem {
  id: string;
  invoiceId: string;
  invoiceNo: string;
  vendor: string;
  amount: number;
  type: 'duplicate' | 'budget_exceeded' | 'price_mismatch' | 'unregistered_vendor';
  severity: 'critical' | 'high' | 'medium';
  message: string;
  triggeredAt: string;
  assignedRole: string;
  status: 'open' | 'resolved' | 'dismissed';
}

export interface ApprovalItem {
  id: string;
  invoiceId: string;
  invoiceNo: string;
  vendor: string;
  department: string;
  amount: number;
  category: string;
  requestedBy: string;
  date: string;
  dueDate: string;
  riskScore: number;
  status: 'pending' | 'approved' | 'rejected';
  approvalChain: {
    role: string;
    name: string;
    status: 'approved' | 'current' | 'pending';
  }[];
}

export interface Vendor {
  id: string;
  name: string;
  category: string;
  totalSpend: number;
  invoiceCount: number;
  riskRating: 'low' | 'medium' | 'high';
  paymentTerms: string;
  status: 'verified' | 'pending';
}

export interface AuditLog {
  id: string;
  timestamp: string;
  actor: string;
  role: string;
  action: string;
  resourceType: string;
  resourceId: string;
  details: string;
}

// ── Initial Mock Dataset ───────────────────────────────────────────────────

export const initialInvoices: Invoice[] = [
  {
    id: 'inv-101',
    invoiceNo: 'INV-2026-8891',
    vendor: 'AWS Cloud Services',
    vendorCategory: 'Software & Infrastructure',
    department: 'Engineering',
    issueDate: '2026-08-20',
    dueDate: '2026-09-19',
    subtotal: 13500.0,
    taxAmount: 1350.0,
    totalAmount: 14850.0,
    status: 'approved',
    confidenceScore: 99,
    riskScore: 12,
    paymentTerms: 'Net 30',
    poNumber: 'PO-ENG-4421',
    lineItems: [
      { id: 'li-1', description: 'EC2 Elastic Compute Tier 3', quantity: 1, unitPrice: 8500.0, taxAmount: 850.0, total: 9350.0 },
      { id: 'li-2', description: 'Amazon S3 High Performance Storage', quantity: 1, unitPrice: 5000.0, taxAmount: 500.0, total: 5500.0 },
    ],
  },
  {
    id: 'inv-102',
    invoiceNo: 'INV-7734-X',
    vendor: 'Apex Logistics Corp',
    vendorCategory: 'Supply Chain',
    department: 'Operations',
    issueDate: '2026-08-25',
    dueDate: '2026-09-24',
    subtotal: 30000.0,
    taxAmount: 2400.75,
    totalAmount: 32400.75,
    status: 'exception',
    confidenceScore: 84,
    lowConfidenceFields: ['taxAmount'],
    riskScore: 88,
    paymentTerms: 'Net 30',
    lineItems: [
      { id: 'li-3', description: 'Intermodal Freight Shipment Route A', quantity: 3, unitPrice: 10000.0, taxAmount: 2400.75, total: 32400.75 },
    ],
  },
  {
    id: 'inv-103',
    invoiceNo: 'INV-9011-W',
    vendor: 'Workday Enterprise',
    vendorCategory: 'HR & Systems',
    department: 'People & HR',
    issueDate: '2026-08-22',
    dueDate: '2026-09-21',
    subtotal: 8000.0,
    taxAmount: 900.0,
    totalAmount: 8900.0,
    status: 'pending_approval',
    confidenceScore: 97,
    riskScore: 18,
    paymentTerms: 'Net 30',
    poNumber: 'PO-HR-1102',
    lineItems: [
      { id: 'li-4', description: 'Annual HCM License Seat Tier 2', quantity: 200, unitPrice: 40.0, taxAmount: 900.0, total: 8900.0 },
    ],
  },
  {
    id: 'inv-104',
    invoiceNo: 'INV-3329-B',
    vendor: 'Delta Global Supplies',
    vendorCategory: 'Office Equipment',
    department: 'Facilities',
    issueDate: '2026-08-26',
    dueDate: '2026-09-10',
    subtotal: 5800.0,
    taxAmount: 450.5,
    totalAmount: 6250.5,
    status: 'needs_review',
    confidenceScore: 71,
    lowConfidenceFields: ['vendor', 'taxAmount'],
    riskScore: 48,
    paymentTerms: 'Net 15',
    lineItems: [
      { id: 'li-5', description: 'Ergonomic Standing Workstations', quantity: 10, unitPrice: 580.0, taxAmount: 450.5, total: 6250.5 },
    ],
  },
  {
    id: 'inv-105',
    invoiceNo: 'INV-4019-S',
    vendor: 'Stripe Payments Inc',
    vendorCategory: 'Financial Services',
    department: 'Finance',
    issueDate: '2026-08-24',
    dueDate: '2026-09-23',
    subtotal: 3200.0,
    taxAmount: 0.0,
    totalAmount: 3200.0,
    status: 'validated',
    confidenceScore: 98,
    riskScore: 8,
    paymentTerms: 'Due on Receipt',
    lineItems: [
      { id: 'li-6', description: 'Merchant Interchange Processing', quantity: 1, unitPrice: 3200.0, taxAmount: 0.0, total: 3200.0 },
    ],
  },
];

export const initialExceptions: ExceptionItem[] = [
  {
    id: 'exc-1',
    invoiceId: 'inv-102',
    invoiceNo: 'INV-7734-X',
    vendor: 'Apex Logistics Corp',
    amount: 32400.75,
    type: 'duplicate',
    severity: 'critical',
    message: 'Identical invoice amount & vendor detected matching INV-7734 paid on 2026-08-10.',
    triggeredAt: '2026-08-26 14:32 UTC',
    assignedRole: 'controller',
    status: 'open',
  },
  {
    id: 'exc-2',
    invoiceId: 'inv-106',
    invoiceNo: 'INV-5510-M',
    vendor: 'GrowthWave Marketing',
    amount: 14200.0,
    type: 'budget_exceeded',
    severity: 'high',
    message: 'Invoice exceeds Marketing Q3 remaining budget by $4,200.00.',
    triggeredAt: '2026-08-26 11:15 UTC',
    assignedRole: 'controller',
    status: 'open',
  },
  {
    id: 'exc-3',
    invoiceId: 'inv-107',
    invoiceNo: 'INV-8812-V',
    vendor: 'Global Soft Ltd',
    amount: 9800.0,
    type: 'price_mismatch',
    severity: 'medium',
    message: 'Line item unit price variance >12% vs purchase order PO-ENG-9011.',
    triggeredAt: '2026-08-25 18:40 UTC',
    assignedRole: 'ap_clerk',
    status: 'open',
  },
];

export const initialApprovals: ApprovalItem[] = [
  {
    id: 'appr-1',
    invoiceId: 'inv-103',
    invoiceNo: 'INV-9011-W',
    vendor: 'Workday Enterprise',
    department: 'People & HR',
    amount: 8900.0,
    category: 'HR & Systems',
    requestedBy: 'Sarah Jenkins (HR Lead)',
    date: '2026-08-22',
    dueDate: '2026-09-21',
    riskScore: 18,
    status: 'pending',
    approvalChain: [
      { role: 'AP Clerk', name: 'James Doe', status: 'approved' },
      { role: 'Department Manager', name: 'Sarah Jenkins', status: 'current' },
      { role: 'Controller', name: 'Alex Vance', status: 'pending' },
    ],
  },
  {
    id: 'appr-2',
    invoiceId: 'inv-108',
    invoiceNo: 'INV-6612-G',
    vendor: 'Google Cloud Platform',
    department: 'Engineering',
    amount: 12350.0,
    category: 'Software & Infrastructure',
    requestedBy: 'David Kim (VP Eng)',
    date: '2026-08-24',
    dueDate: '2026-09-15',
    riskScore: 14,
    status: 'pending',
    approvalChain: [
      { role: 'AP Clerk', name: 'James Doe', status: 'approved' },
      { role: 'VP Engineering', name: 'David Kim', status: 'current' },
      { role: 'CFO', name: 'Marcus Sterling', status: 'pending' },
    ],
  },
  {
    id: 'appr-3',
    invoiceId: 'inv-109',
    invoiceNo: 'INV-1102-O',
    vendor: 'Zoom Video Communications',
    department: 'Operations',
    amount: 2400.0,
    category: 'SaaS Subscriptions',
    requestedBy: 'Elena Rostova',
    date: '2026-08-25',
    dueDate: '2026-09-25',
    riskScore: 8,
    status: 'pending',
    approvalChain: [
      { role: 'AP Clerk', name: 'James Doe', status: 'approved' },
      { role: 'Operations Lead', name: 'Elena Rostova', status: 'current' },
    ],
  },
];

export const initialVendors: Vendor[] = [
  { id: 'v-1', name: 'AWS Cloud Services', category: 'Infrastructure', totalSpend: 142500.0, invoiceCount: 14, riskRating: 'low', paymentTerms: 'Net 30', status: 'verified' },
  { id: 'v-2', name: 'Apex Logistics Corp', category: 'Supply Chain', totalSpend: 89400.0, invoiceCount: 6, riskRating: 'high', paymentTerms: 'Net 30', status: 'verified' },
  { id: 'v-3', name: 'Workday Enterprise', category: 'HR Systems', totalSpend: 54000.0, invoiceCount: 4, riskRating: 'low', paymentTerms: 'Net 30', status: 'verified' },
  { id: 'v-4', name: 'Delta Global Supplies', category: 'Office Equipment', totalSpend: 31200.0, invoiceCount: 8, riskRating: 'medium', paymentTerms: 'Net 15', status: 'verified' },
  { id: 'v-5', name: 'Stripe Payments Inc', category: 'Financial Services', totalSpend: 28900.0, invoiceCount: 12, riskRating: 'low', paymentTerms: 'Due on Receipt', status: 'verified' },
  { id: 'v-6', name: 'Google Cloud Platform', category: 'Infrastructure', totalSpend: 96400.0, invoiceCount: 9, riskRating: 'low', paymentTerms: 'Net 30', status: 'verified' },
];

export const initialAuditLogs: AuditLog[] = [
  {
    id: 'aud-1',
    timestamp: '2026-08-26 15:12:04 UTC',
    actor: 'Alex Vance',
    role: 'Controller',
    action: 'invoice_approved',
    resourceType: 'Invoice',
    resourceId: 'inv-101',
    details: 'Approved invoice INV-2026-8891 ($14,850.00) from AWS Cloud Services.',
  },
  {
    id: 'aud-2',
    timestamp: '2026-08-26 14:32:10 UTC',
    actor: 'System AI Anomaly Guard',
    role: 'Automated Engine',
    action: 'exception_created',
    resourceType: 'Exception',
    resourceId: 'exc-1',
    details: 'Flagged critical duplicate exception on invoice INV-7734-X ($32,400.75).',
  },
  {
    id: 'aud-3',
    timestamp: '2026-08-26 12:45:00 UTC',
    actor: 'James Doe',
    role: 'AP Clerk',
    action: 'extraction_overridden',
    resourceType: 'Invoice',
    resourceId: 'inv-104',
    details: 'Overrode low-confidence field tax_amount from 410.00 to 450.50.',
  },
  {
    id: 'aud-4',
    timestamp: '2026-08-26 10:18:22 UTC',
    actor: 'Sarah Jenkins',
    role: 'Department Lead',
    action: 'approval_granted',
    resourceType: 'Approval',
    resourceId: 'appr-1',
    details: 'Approved Level 1 threshold for Workday HCM ($8,900.00).',
  },
];
