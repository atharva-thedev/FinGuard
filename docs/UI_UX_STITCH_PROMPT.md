# FinGuard — Master UI/UX Design & Layout Prompt for Stitch / AI UI Generators

> **How to use this file:**  
> Copy the complete prompt block below and paste it directly into **Stitch**, **v0**, **Figma AI**, or your AI UI/UX generator of choice to generate the complete, high-fidelity, interactive frontend for the FinGuard platform.

---

```markdown
# MISSION: DESIGN & SCAFFOLD FINGUARD ENTERPRISE AI FINANCE PLATFORM

## 1. PROJECT & PRODUCT IDENTITY
- **Product Name:** FinGuard
- **Tagline:** Protect • Analyze • Optimize
- **Domain:** Enterprise AI-Powered Autonomous Invoice & Expense Management, Fraud Detection, and Spend Intelligence.
- **Audience:** Finance Leaders, Controllers, AP Clerks, Department Approvers, CFOs (High-density, professional, trust-inspiring SaaS aesthetic).
- **Core Value Proposition:** Automates the complete invoice lifecycle from multi-format capture (PDF/image/email) through AI OCR extraction, 3-way matching, duplicate/fraud anomaly detection, automated policy & budget checks, to 1-click approval routing and live analytics.

---

## 2. DESIGN SYSTEM & VISUAL LANGUAGE

### 2.1 Color Palette & Theme Tokens
Support seamless **Light Mode** and **Dark Mode** with CSS custom properties and instant switching:

#### Dark Mode (Default / Primary):
- **App Background (`--bg-app`):** Deep Space Navy `#080D1A`
- **Surface Cards (`--bg-surface`):** Obsidian Slate `#0F172A`
- **Elevated Surfaces (`--bg-surface-elevated`):** Slate `#1E293B`
- **Muted Elements (`--bg-muted`):** Navy Tint `#111C33`
- **Glass Surfaces (`--bg-glass`):** `rgba(15, 23, 42, 0.75)` with `backdrop-filter: blur(16px)`
- **Primary Brand Accent (`--primary`):** Electric Teal `#14B8A6` (Hover: `#2DD4BF`, Active: `#0D9488`)
- **Brand Glow (`--brand-teal-glow`):** `rgba(20, 184, 166, 0.35)`
- **Brand Gradient:** `linear-gradient(135deg, #14B8A6 0%, #38BDF8 100%)`
- **Text Primary (`--text-primary`):** Crisp Snow `#F8FAFC`
- **Text Secondary (`--text-secondary`):** Slate `#94A3B8`
- **Text Muted (`--text-muted`):** Cool Slate `#64748B`
- **Borders (`--border-base`):** `rgba(255, 255, 255, 0.08)` (Strong: `rgba(255, 255, 255, 0.16)`)

#### Light Mode:
- **App Background (`--bg-app`):** Porcelain Mist `#F8FAFC`
- **Surface Cards (`--bg-surface`):** Pure White `#FFFFFF`
- **Elevated Surfaces (`--bg-surface-elevated`):** `#FFFFFF` with drop-shadow
- **Muted Elements (`--bg-muted`):** Soft Cool Gray `#F1F5F9`
- **Glass Surfaces (`--bg-glass`):** `rgba(255, 255, 255, 0.85)` with `backdrop-filter: blur(16px)`
- **Primary Brand Accent (`--primary`):** Deep Pine Teal `#0D9488` (Hover: `#0F766E`)
- **Brand Gradient:** `linear-gradient(135deg, #0F2744 0%, #0D9488 100%)`
- **Text Primary (`--text-primary`):** Deep Midnight Navy `#0F172A`
- **Text Secondary (`--text-secondary`):** Slate `#475569`
- **Text Muted (`--text-muted`):** Muted Slate `#94A3B8`
- **Borders (`--border-base`):** `#E2E8F0` (Strong: `#CBD5E1`)

#### Functional & Semantic Status Tokens:
- **Success / Validated / Approved:** Emerald `#10B981` (Bg: `rgba(16, 185, 129, 0.15)`, Border: `rgba(16, 185, 129, 0.3)`)
- **Warning / Review Needed:** Amber `#F59E0B` (Bg: `rgba(245, 158, 11, 0.15)`, Border: `rgba(245, 158, 11, 0.3)`)
- **Danger / Exception / Fraud Flag:** Rose `#EF4444` (Bg: `rgba(239, 68, 68, 0.15)`, Border: `rgba(239, 68, 68, 0.3)`)
- **Info / Ingesting / Extracting:** Sky Blue `#3B82F6` (Bg: `rgba(59, 130, 246, 0.15)`, Border: `rgba(59, 130, 246, 0.3)`)
- **AI Risk Score Gradient (0–100):**
  - Low Risk (0–29): Emerald `#10B981`
  - Medium Risk (30–69): Amber `#F59E0B`
  - High Risk (70–100): Crimson Rose `#EF4444`

### 2.2 Typography & Density
- **Headings Font:** `'Outfit', sans-serif` (Bold, geometric, modern)
- **UI & Body Font:** `'Inter', -apple-system, sans-serif` (Clean, highly readable)
- **Monospace Font:** `'JetBrains Mono', monospace` (For currency amounts `$12,450.00`, invoice numbers `INV-9021`, timestamps, and hash IDs)
- **Visual Feel:** Data-dense enterprise grid, 10–14px border radii, subtle 1px translucent borders, elegant hover transitions (`200ms ease`), micro-glows on active states.

---

## 3. GLOBAL APPLICATION SHELL & LAYOUT

### 3.1 Collapsible Enterprise Sidebar Navigation:
- **Header:** FinGuard Shield Logo (Navy-to-Teal gradient) + Bold "FinGuard" monogram + Organization Switcher dropdown (e.g. "Acme Global Inc. ▾").
- **Navigation Links (with active indicator & notification pill counters):**
  1. 📊 **Dashboard** (`/dashboard`)
  2. 📤 **Capture & Upload** (`/invoices/capture`) — with badge `+Batch`
  3. 📑 **Invoices Queue** (`/invoices`) — with live count badge
  4. ⚠️ **Exception Queue** (`/exceptions`) — with alert pill `3 Action Req.`
  5. ✅ **Approvals** (`/approvals`) — with badge `5 Pending`
  6. 🏢 **Vendors Directory** (`/vendors`)
  7. 📈 **Reports & Spend Analytics** (`/reports`)
  8. 🛡️ **Audit Logs** (`/audit`)
  9. ⚙️ **Settings & Policies** (`/settings`)
- **Sidebar Footer:**
  - System Status: Live WebSocket pulse ("⚡ Connected • 14ms")
  - User Profile snippet (Avatar, Name "Alex Vance", Role "Controller", Logout icon).

### 3.2 Sticky Frosted Top Header:
- **Global Search Bar (`Cmd+K` / `Ctrl+K`):** "Search invoices, vendors, amounts, or audit logs..."
- **Real-Time Ingestion Activity Pill:** Animated pulsing dot showing active background jobs (e.g. "3 Invoices Extracting...").
- **Theme Selector (`ThemeToggle`):** Segmented pill switcher (`Light` | `Dark` | `Auto`) with smooth sliding highlight.
- **Notification Bell Center:** Slide-over drawer with real-time WebSocket alerts (e.g. "Duplicate invoice intercepted", "Approval granted by Department Lead").
- **Quick Action Button:** Primary Teal "+ Upload Invoice" button opening modal.

---

## 4. DETAILED SCREEN SPECIFICATIONS

### SCREEN 1: Real-Time Executive Dashboard (`/dashboard`)
- **Hero Metrics Banner:**
  - AI Extraction Accuracy (e.g. `98.4%`), Average Ingestion Latency (`1.8 sec`), Fraud Protection Shield Active.
- **4 Key KPI Stat Cards:**
  1. *Total Invoices Processed:* `2,842` (`↑ 14.8% MoM`, mini bar chart).
  2. *Auto-Matched & Cleared:* `94.2%` (`↑ 2.1%` OCR confidence, green badge).
  3. *Risk Anomalies Intercepted:* `18` (`3 High Risk` holds active, red badge).
  4. *Captured Early Discounts:* `$46,290` (`↑ $8.4k` saved, teal glow).
- **Two-Column Analytics Section:**
  - **Left (2/3 width):** Live Invoice Ingestion Stream — Data-dense table showing latest incoming invoices, vendor logo initials, amount, status pill (`extracting`, `needs_review`, `validated`, `pending_approval`, `approved`, `exception`), and Risk Score indicator (0–100).
  - **Right (1/3 width):** Spend Velocity Chart & Department Budget Utilization Gauges (Engineering: 82%, Marketing: 94% [Warning], Operations: 45%).
- **Bottom Section:** Quick Actions & AI Finance Copilot preview query bar: *"Which vendors increased prices by >10% this quarter?"*

---

### SCREEN 2: Invoice Capture & Ingestion Studio (`/invoices/capture`)
- **Dual-Ingestion View:**
  - **Option A: Drag & Drop Ingestion Zone:**
    - Large dashed dropzone supporting PDF, PNG, JPG up to 25MB.
    - Batch upload capability (up to 50 files simultaneously).
    - Auto-tagging & camera capture button for mobile receipts.
  - **Option B: Dedicated Email Ingestion Box:**
    - Display organization-specific email forwarding address (e.g., `invoices+acme@finguard.ai`) with 1-click "Copy Address" pill.
- **Active Uploads Queue Table:**
  - Per-file progress bar, thumbnail preview, file size, auto-detected page count, and dynamic status:
    `Uploading (100%)` → `OCR Extracting...` → `Confidence: 96% (Validated)` or `Confidence: 71% (Needs Review)`.
  - Instant button: "Open Review Studio ➔".

---

### SCREEN 3: AI Extraction & Side-by-Side Review Studio (`/invoices/:id/review`)
*The flagship human-in-the-loop validation workspace.*
- **Split-Screen Workspace (50% / 50%):**
  - **Left Pane — Interactive Document Viewer:**
    - High-resolution PDF/image viewer with zoom, pan, rotate, and page pagination.
    - **OCR Bounding Box Overlays:** Interactive colored highlight rectangles over detected fields (Vendor Name, Total Amount, Due Date, Line Items). Clicking a bounding box scrolls directly to the field on the right.
  - **Right Pane — Structured Extraction Form & Validation Engine:**
    - **Header:** Invoice Status pill, Overall Confidence Score Gauge (e.g. `74% - Low Confidence`), and Risk Score Pill (`48/100`).
    - **Extracted Fields Form (with Confidence Highlighting):**
      - *Vendor:* Text input with auto-complete + registered vendor badge.
      - *Invoice Number:* Text input (checks duplicate detection in real-time).
      - *Invoice Date & Due Date:* Date pickers with payment term detector (`Net 30`).
      - *Line Items Table:* Editable grid (Description, Quantity, Unit Price, Tax, Subtotal) with 1-click "Add Line Item".
      - *Subtotal, Tax & Total Amount:* Auto-recalculating calculator; highlights discrepancy in red if subtotals + tax != total amount.
      - *Category Taxonomy:* Dropdown (`Software`, `Travel`, `Office Supplies`, `Supply Chain`) with an indicator *"User correction will update auto-learning model for future invoices."*
    - **Confidence Score Pill next to each field:**
      - Green badge `98%` for high confidence.
      - Pulsing Amber badge `65% (Check Required)` for low-confidence fields.
  - **Bottom Floating Action Bar:**
    - `Discard / Reject` (Opens reason modal)
    - `Flag as Exception` (Routes to controller)
    - `Save & Route to Approvals` (Primary Teal button)

---

### SCREEN 4: Unified Exceptions & Risk Resolution Queue (`/exceptions`)
- **Triaging Filter Tabs:**
  - `All Exceptions (12)` | `Duplicate Invoices (3)` | `Budget Overruns (4)` | `Price Variance (3)` | `Unregistered Vendors (2)`
- **Exceptions Data Table:**
  - Columns: Exception Type badge, Invoice Ref, Vendor, Amount, Triggered Rule (e.g., *"Invoice exceeds Marketing Q3 budget by $4,200"* or *"Exact duplicate invoice number INV-8821 already paid on 2026-08-10"*), Severity (`Critical`, `High`, `Medium`), Assigned SLA Countdown (e.g. `4 hrs left`), Actions.
- **Interactive Resolution Drawer:**
  - Clicking an exception opens a slide-over panel comparing the conflict side-by-side (e.g., Original Invoice vs. New Duplicate Invoice, or Department Monthly Budget Bar vs. Incurred Expense).
  - One-click resolution actions:
    - **Path 1: Void / Discard Duplicate**
    - **Path 2: Override & Approve with Audit Note** (Mandatory comment box for controller compliance).
    - **Path 3: Request Vendor Clarification** (Pre-drafted email template).

---

### SCREEN 5: Approvals Inbox & Multi-Level Decision Hub (`/approvals`)
- **Role-Aware Approval Feed (Desktop & Mobile Optimized):**
  - **Quick-Action Cards:** Clean list of pending invoices requiring user's signature/authority.
  - Card displays: Vendor, Amount, Department, Attached PO match status, AI Risk Score, and Due Date urgency timer.
  - **Approval Chain Timeline Visualizer:**
    - Step 1: AP Clerk Verified ✅
    - Step 2: Department Manager (Current - Pending) ⏳
    - Step 3: Controller / CFO (Triggered if amount > $10,000) 🔒
- **Invoice Quick-Inspect Drawer:**
  - Preview full invoice breakdown without leaving the approvals list.
  - Department budget impact visualizer: shows department budget *before* vs. *after* this invoice approval.
- **Action Buttons:**
  - 1-Click `Approve` (Green button with optimistic UI transition).
  - `Reject` (Prompts mandatory reason modal: *"Reason for rejection is logged in immutable audit trail"*).

---

### SCREEN 6: Spend Analytics, Reports & Compliance Audit Trail (`/reports`, `/audit`)
- **Analytics View (`/reports`):**
  - Date range filter (`This Month`, `Q3 2026`, `Year to Date`, `Custom Range`).
  - Interactive Spend by Category Donut Chart.
  - Spend by Vendor Top 10 Horizontal Bar Chart with YoY variance indicators.
  - Budget vs. Actual Department Variance Heatmap.
  - Export Options: `Export CSV`, `Export Excel`, `Export Audit Pack (PDF)`.
- **Compliance Audit Trail (`/audit`):**
  - Immutable chronological log table: Timestamp (UTC), Actor (Avatar, Name, Email, IP), Action (`invoice_created`, `extraction_overridden`, `budget_overridden`, `approval_granted`, `exception_dismissed`), Resource ID, State Diff (`before_value` vs `after_value` in side-by-side JSON diff viewer).

---

### SCREEN 7: Organization & Policy Rules Configuration (`/settings`)
- **Department Budget Allocations:**
  - Monthly budget limit inputs with real-time spend progress bars.
- **Approval Threshold Rules Matrix:**
  - Configurable tiers: e.g., `< $1,000` (Auto-approve if 3-way match passes), `$1,000 – $10,000` (Department Manager), `> $10,000` (Controller + CFO required).
- **ERP Integration Connectors:**
  - QuickBooks Online (Status: `Connected • Last Synced 5m ago`).
  - NetSuite (Status: `Configured`).
- **User Management & RBAC Matrix:**
  - Table of organization members with roles (`Admin`, `Controller`, `Approver`, `AP Clerk`, `Viewer`).
  - Invite user button with role selector.

---

## 5. INTERACTIVE COMPONENT LIBRARY & MICRO-INTERACTIONS

1. **Theme Toggle Component (`ThemeToggle.tsx`):**
   - Segmented 3-state control (`Light`, `Dark`, `Auto`) with smooth active pill sliding animation.
2. **AI Risk Score Badge (`<RiskBadge score={number} />`):**
   - Circular gauge / pill with color gradient: 0–29 Green, 30–69 Yellow, 70–100 Red.
3. **OCR Confidence Score Chip (`<ConfidenceChip score={number} />`):**
   - Visual percentage with indicator dot; pulsing animation if below 85%.
4. **WebSocket Pulse Indicator (`<RealtimeStatus connected={boolean} />`):**
   - Green pulsing dot in header with tooltip showing socket latency and tenant channel ID.
5. **Interactive Data Tables:**
   - Sortable columns, sticky headers, pagination, row hover states, and batch action toolbar.
6. **Toast & Alert Notification Banners:**
   - Matches standard API error envelope: `{ success: false, error: { code, message, fields } }`.

---

## 6. DESIGN INSTRUCTIONS & DELIVERABLES EXPECTATION
- Generate complete, interactive, pixel-perfect pages with fully realized components.
- Ensure every button, dropdown, modal, drawer, and tab is functional and interactive.
- Use zero generic placeholder text; populate with realistic enterprise finance data (AWS, NetSuite, Salesforce, Apex Logistics, Workday).
- Ensure mobile responsiveness for all approval flows and capture screens.
- Maintain strict adherence to the FinGuard Navy/Teal brand aesthetic and design token system in both Light and Dark themes.
```
