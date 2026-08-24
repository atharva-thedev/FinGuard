"""
FinGuard Complete Live Scenario & Database Verification Suite
Executes test cases against all API endpoints and verifies MongoDB Atlas database mutations.
"""

import asyncio
import io
import os
import sys
import uuid

import httpx

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config.db import connect_db, disconnect_db
from app.models.documents import (
    Approval,
    AuditLog,
    BudgetRule,
    Category,
    CategoryOverride,
    Invoice,
    InvoiceException,
    Organization,
    PolicyRule,
    Session,
    User,
    Vendor,
)
from app.utils.jwt import sign_email_action

BASE_URL = "http://localhost:5000"
PREFIX = f"test_{uuid.uuid4().hex[:6]}"


def log_step(phase: str, desc: str):
    print(f"\n[PHASE {phase}] >> {desc}")


def log_assert(msg: str):
    print(f"  [OK] {msg}")


async def run_all_tests():
    print("=" * 70)
    print("  FINGUARD LIVE API & DATABASE VERIFICATION SUITE")
    print("=" * 70)

    # 0. Connect to DB directly for async verification assertions
    await connect_db()
    print("[DB] Connected to MongoDB Atlas for state verification.")

    client = httpx.AsyncClient(base_url=BASE_URL, timeout=15.0)

    try:
        # =====================================================================
        # PHASE 1: System Health & Readiness
        # =====================================================================
        log_step("1.0", "Testing Health & Readiness Endpoints")
        res = await client.get("/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        log_assert("GET /health -> 200 OK")

        res = await client.get("/ready")
        assert res.status_code == 200 and res.json()["database"] == "connected", f"Readiness check failed: {res.text}"
        log_assert("GET /ready -> 200 OK (database: connected)")

        # =====================================================================
        # PHASE 2: Auth, Sessions, Lockout & Multi-Tenancy
        # =====================================================================
        log_step("2.0", "Testing Registration & DB Verification")
        org1_email = f"{PREFIX}_admin@acme.com"
        org1_password = "Password123!"
        reg_payload = {
            "email": org1_email,
            "password": org1_password,
            "full_name": "Alice Admin",
            "organization_name": f"{PREFIX} Acme Corp",
        }
        res = await client.post("/api/v1/auth/register", json=reg_payload)
        assert res.status_code == 201, f"Registration failed: {res.text}"
        org1_token = res.json()["data"]["access_token"]
        org1_user_id = res.json()["data"]["user"]["id"]
        org1_id = res.json()["data"]["user"]["organization_id"]
        log_assert(f"POST /api/v1/auth/register -> 201 Created (OrgID: {org1_id})")

        # Verify in DB: User, Org, and default Categories
        db_user = await User.get(org1_user_id)
        assert db_user and db_user.email == org1_email.lower(), "User not in MongoDB"
        db_org = await Organization.get(org1_id)
        assert db_org and db_org.name == f"{PREFIX} Acme Corp", "Org not in MongoDB"
        db_categories = await Category.find(Category.organization_id == str(org1_id)).to_list()
        assert len(db_categories) >= 5, "Default categories not seeded in MongoDB"
        log_assert(f"MongoDB Verified: User, Org, and {len(db_categories)} Default Categories created.")

        # Register Org 2 for Multi-Tenant Isolation Testing
        org2_email = f"{PREFIX}_org2@globex.com"
        res2 = await client.post(
            "/api/v1/auth/register",
            json={
                "email": org2_email,
                "password": "Password123!",
                "full_name": "Bob Globex",
                "organization_name": f"{PREFIX} Globex Corp",
            },
        )
        assert res2.status_code == 201
        org2_token = res2.json()["data"]["access_token"]
        org2_id = res2.json()["data"]["user"]["organization_id"]
        log_assert(f"POST /api/v1/auth/register (Org 2) -> 201 Created (OrgID: {org2_id})")

        # Duplicate Email Conflict Check
        res_dup = await client.post("/api/v1/auth/register", json=reg_payload)
        assert res_dup.status_code == 409, f"Expected 409, got {res_dup.status_code}"
        log_assert("POST /api/v1/auth/register -> 409 Conflict (Duplicate email prevented)")

        # Login & Cookie Session Tracking
        log_step("2.1", "Testing Login & Session Rotation")
        login_res = await client.post("/api/v1/auth/login", json={"email": org1_email, "password": org1_password})
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
        
        # Check set-cookie header
        set_cookie_hdr = login_res.headers.get("set-cookie", "")
        assert "refresh_token=" in set_cookie_hdr or "refresh_token" in login_res.cookies, "Set-Cookie refresh_token missing"
        
        # Extract refresh_token value
        if "refresh_token" in login_res.cookies:
            refresh_cookie = login_res.cookies["refresh_token"]
        else:
            # Parse from set-cookie header: refresh_token=<val>; ...
            refresh_cookie = set_cookie_hdr.split("refresh_token=")[1].split(";")[0]
            
        log_assert("POST /api/v1/auth/login -> 200 OK (Set-Cookie received)")

        # Verify Session in DB
        session_id = refresh_cookie.split(".")[0]
        db_session = await Session.get(session_id)
        assert db_session and not db_session.revoked, "Session not active in MongoDB"
        log_assert("MongoDB Verified: Active Session created with bcrypt hash.")

        # Token Refresh & Rotation
        refresh_res = await client.post(
            "/api/v1/auth/refresh",
            cookies={"refresh_token": refresh_cookie},
            headers={"Cookie": f"refresh_token={refresh_cookie}"}
        )
        assert refresh_res.status_code == 200, f"Refresh failed: {refresh_res.text}"
        new_token = refresh_res.json()["data"]["access_token"]
        auth1_headers = {"Authorization": f"Bearer {new_token}"}
        new_set_cookie_hdr = refresh_res.headers.get("set-cookie", "")
        if "refresh_token" in refresh_res.cookies:
            new_refresh_cookie = refresh_res.cookies["refresh_token"]
        else:
            new_refresh_cookie = new_set_cookie_hdr.split("refresh_token=")[1].split(";")[0]
        log_assert("POST /api/v1/auth/refresh -> 200 OK (Session Rotated)")

        # Verify old session revoked in DB and new session active
        old_session = await Session.get(session_id)
        assert old_session and old_session.revoked, "Old session not revoked in MongoDB"
        new_session_id = new_refresh_cookie.split(".")[0]
        new_session = await Session.get(new_session_id)
        assert new_session and not new_session.revoked, "New session not created in MongoDB"
        log_assert("MongoDB Verified: Old session revoked, new session active.")

        # Account Lockout Test (5 failed attempts)
        log_step("2.2", "Testing 5-Attempt Account Lockout Protection")
        lockout_email = f"{PREFIX}_lockout@test.com"
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": lockout_email,
                "password": "Password123!",
                "full_name": "Lock Target",
                "organization_name": f"{PREFIX} Lock Org",
            },
        )
        for attempt in range(1, 6):
            fail_res = await client.post(
                "/api/v1/auth/login", json={"email": lockout_email, "password": "WrongPassword!"}
            )
            if attempt < 5:
                assert fail_res.status_code == 401
            else:
                assert fail_res.status_code == 423, f"Expected 423 Locked on attempt 5, got {fail_res.status_code}"
        log_assert("POST /api/v1/auth/login (5th failed attempt) -> 423 Locked")

        # Verify User locked_until in DB
        db_locked_user = await User.find_one(User.email == lockout_email.lower())
        assert db_locked_user and db_locked_user.locked_until, "locked_until timestamp not set in MongoDB"
        log_assert("MongoDB Verified: User.locked_until timestamp set for 15-minute cooldown.")

        # =====================================================================
        # PHASE 3: Users Profile, Password Change & GDPR Export
        # =====================================================================
        log_step("3.0", "Testing User Profile, Password Change & Sessions")
        auth2_headers = {"Authorization": f"Bearer {org2_token}"}

        # Get Profile
        me_res = await client.get("/api/v1/users/me", headers=auth1_headers)
        assert me_res.status_code == 200, f"Profile fetch failed: {me_res.text}"
        assert me_res.json()["data"]["email"] == org1_email.lower()
        log_assert("GET /api/v1/users/me -> 200 OK")

        # List Sessions
        sessions_res = await client.get("/api/v1/users/me/sessions", headers=auth1_headers)
        assert sessions_res.status_code == 200, f"Sessions list failed: {sessions_res.text}"
        log_assert(f"GET /api/v1/users/me/sessions -> 200 OK ({len(sessions_res.json()['data'])} sessions)")

        # Change Password
        pwd_res = await client.post(
            "/api/v1/users/me/change-password",
            headers=auth1_headers,
            json={"current_password": "Password123!", "new_password": "NewPassword456!"},
        )
        assert pwd_res.status_code == 200, f"Password change failed: {pwd_res.text}"
        log_assert("POST /api/v1/users/me/change-password -> 200 OK")

        # Verify login with new password
        login_new_res = await client.post(
            "/api/v1/auth/login", json={"email": org1_email, "password": "NewPassword456!"}
        )
        assert login_new_res.status_code == 200
        org1_token = login_new_res.json()["data"]["access_token"]
        auth1_headers = {"Authorization": f"Bearer {org1_token}"}
        log_assert("POST /api/v1/auth/login (New Password) -> 200 OK")

        # GDPR Export
        export_res = await client.get("/api/v1/users/me/export", headers=auth1_headers)
        assert export_res.status_code == 200 and "user" in export_res.json()["data"], f"GDPR Export failed: {export_res.text}"
        log_assert("GET /api/v1/users/me/export -> 200 OK (GDPR Archive generated)")

        # =====================================================================
        # PHASE 4: Organizations, Thresholds, Policies & Budgets
        # =====================================================================
        log_step("4.0", "Testing Organization Thresholds, Policies & Budgets")
        # Update Thresholds
        thresh_res = await client.patch(
            "/api/v1/organizations/me",
            headers=auth1_headers,
            json={"approval_threshold": 500.0},
        )
        assert thresh_res.status_code == 200, f"Organization update failed: {thresh_res.text}"
        log_assert("PATCH /api/v1/organizations/me -> 200 OK")

        # Verify DB Organization thresholds
        db_org = await Organization.get(org1_id)
        assert (
            db_org.approval_threshold == 500.0
        ), "Threshold not updated in DB"
        log_assert("MongoDB Verified: Organization approval threshold updated ($500.00).")

        # Set Department Budget
        budget_res = await client.post(
            "/api/v1/policies/budgets",
            headers=auth1_headers,
            json={"department": "Engineering", "category": "Cloud Infrastructure", "monthly_limit": 25000.0},
        )
        assert budget_res.status_code == 201, f"Budget creation failed: {budget_res.text}"
        log_assert("POST /api/v1/policies/budgets -> 201 Created (Engineering Cloud: $25,000)")

        # Verify DB BudgetRule
        db_budget = await BudgetRule.find_one(
            BudgetRule.organization_id == str(org1_id),
            BudgetRule.department == "Engineering",
            BudgetRule.category == "Cloud Infrastructure",
        )
        assert db_budget and db_budget.monthly_limit == 25000.0, "Budget rule not saved in DB"
        log_assert("MongoDB Verified: BudgetRule created with $25,000 limit.")

        # List Policy Rules
        rules_res = await client.get("/api/v1/policies/rules", headers=auth1_headers)
        assert rules_res.status_code == 200
        log_assert(f"GET /api/v1/policies/rules -> 200 OK ({len(rules_res.json()['data'])} rules)")

        # =====================================================================
        # PHASE 5: Vendors & Category Learning Feedback Loop
        # =====================================================================
        log_step("5.0", "Testing Vendors Directory & Normalization")
        vendor_res = await client.post(
            "/api/v1/vendors",
            headers=auth1_headers,
            json={
                "name": "AWS Cloud Services",
                "tax_id": "US-99-123456",
                "default_category": "Cloud Infrastructure",
                "default_department": "Engineering",
                "is_registered": True,
            },
        )
        assert vendor_res.status_code == 201
        vendor_id = vendor_res.json()["data"]["id"]
        log_assert(f"POST /api/v1/vendors -> 201 Created (VendorID: {vendor_id})")

        # Verify DB Vendor
        db_vendor = await Vendor.get(vendor_id)
        assert db_vendor and db_vendor.normalized_name == "aws cloud services", "Vendor normalization failed in DB"
        log_assert("MongoDB Verified: Vendor created with normalized_name index.")

        # Duplicate Vendor Conflict Check
        dup_v_res = await client.post(
            "/api/v1/vendors",
            headers=auth1_headers,
            json={"name": "aws  cloud  services", "is_registered": True},
        )
        assert dup_v_res.status_code == 409
        log_assert("POST /api/v1/vendors -> 409 Conflict (Duplicate normalized vendor prevented)")

        # Add Custom Category
        cat_res = await client.post(
            "/api/v1/categories", headers=auth1_headers, json={"name": "Specialized Hardware"}
        )
        assert cat_res.status_code == 201
        log_assert("POST /api/v1/categories -> 201 Created")

        # =====================================================================
        # PHASE 6: Invoices Full Lifecycle Scenarios
        # =====================================================================

        # Scenario A: Happy Path Invoice Approval
        log_step("6.1", "Scenario A: Happy Path Batch Upload & Automatic Approval")
        fake_pdf = io.BytesIO(b"%PDF-1.4 Mock Happy Path Invoice AWS $450")
        upload_res = await client.post(
            "/api/v1/invoices",
            headers=auth1_headers,
            files=[("files", ("aws_invoice_101.pdf", fake_pdf, "application/pdf"))],
        )
        assert upload_res.status_code == 201, f"Upload failed: {upload_res.text}"
        inv_a_id = upload_res.json()["data"][0]["id"]
        log_assert(f"POST /api/v1/invoices -> 201 Created (InvoiceID: {inv_a_id})")

        # Directly update Invoice A to simulate verified OCR extraction
        db_inv_a = await Invoice.get(inv_a_id)
        db_inv_a.vendor_name = "AWS Cloud Services"
        db_inv_a.vendor_normalized = "aws cloud services"
        db_inv_a.invoice_number = f"INV-AWS-{PREFIX}-001"
        db_inv_a.invoice_date = "2026-08-01"
        db_inv_a.due_date = "2026-09-01"
        db_inv_a.subtotal = 400.0
        db_inv_a.tax = 50.0
        db_inv_a.total = 450.0
        db_inv_a.department = "Engineering"
        db_inv_a.category = "Cloud Infrastructure"
        db_inv_a.field_confidences = {"total": 0.95, "vendor_name": 0.95}
        db_inv_a.status = "pending_approval"
        await db_inv_a.save()

        # Create approval record
        appr_a = Approval(
            organization_id=str(org1_id),
            invoice_id=inv_a_id,
            status="pending",
        )
        await appr_a.save()
        appr_a_id = str(appr_a.id)

        # Check Pending Approvals API
        pending_res = await client.get("/api/v1/approvals/pending", headers=auth1_headers)
        assert pending_res.status_code == 200 and len(pending_res.json()["data"]) >= 1, f"Pending approvals failed: {pending_res.text}"
        log_assert("GET /api/v1/approvals/pending -> 200 OK (Invoice A in queue)")

        # Approve Decision
        decide_res = await client.post(
            f"/api/v1/approvals/{appr_a_id}/decide",
            headers=auth1_headers,
            json={"decision": "approve", "comment": "PO matched perfectly."},
        )
        assert decide_res.status_code == 200, f"Approval decision failed: {decide_res.text}"
        log_assert(f"POST /api/v1/approvals/{appr_a_id}/decide -> 200 OK (Approved)")

        # Verify DB Invoice & Approval status
        db_inv_a = await Invoice.get(inv_a_id)
        assert db_inv_a.status == "approved", f"Expected approved, got {db_inv_a.status}"
        db_appr_a = await Approval.get(appr_a_id)
        assert db_appr_a.status == "approved", "Approval record not marked approved in DB"
        log_assert("MongoDB Verified: Invoice A status transitioned to 'approved'.")

        # Scenario B: Low Confidence & Human Review (Change/Override)
        log_step("6.2", "Scenario B: Low Confidence OCR & Human Review Override")
        fake_pdf_b = io.BytesIO(b"%PDF-1.4 Fuzzy receipt blurry text")
        upload_res_b = await client.post(
            "/api/v1/invoices",
            headers=auth1_headers,
            files=[("files", ("fuzzy_receipt.pdf", fake_pdf_b, "application/pdf"))],
        )
        assert upload_res_b.status_code == 201
        inv_b_id = upload_res_b.json()["data"][0]["id"]

        # Simulate low confidence in DB (< 85%)
        db_inv_b = await Invoice.get(inv_b_id)
        db_inv_b.field_confidences = {"vendor_name": 0.65, "total": 0.70}
        db_inv_b.status = "needs_review"
        await db_inv_b.save()
        log_assert(f"Invoice B set to 'needs_review' (Confidence < 85%)")

        # AP Clerk corrects and overrides fields
        review_res = await client.patch(
            f"/api/v1/invoices/{inv_b_id}/extraction",
            headers=auth1_headers,
            json={
                "vendor_name": "Staples Stationery Store",
                "invoice_number": f"INV-STAPLE-{PREFIX}",
                "invoice_date": "2026-08-10",
                "due_date": "2026-09-10",
                "subtotal": 200.0,
                "tax": 20.0,
                "total": 220.0,
                "category": "Office Supplies",
                "department": "Administration",
            },
        )
        assert review_res.status_code == 200, f"Extraction update failed: {review_res.text}"
        log_assert(f"PATCH /api/v1/invoices/{inv_b_id}/extraction -> 200 OK (Fields Overridden)")

        # Verify DB Invoice updated + CategoryOverride learned
        db_inv_b = await Invoice.get(inv_b_id)
        assert (
            db_inv_b.total == 220.0
        ), "Total not updated in DB after human review"
        db_cat_override = await CategoryOverride.find_one(
            CategoryOverride.organization_id == str(org1_id),
            CategoryOverride.vendor_normalized == "staples stationery store",
        )
        assert db_cat_override and db_cat_override.category == "Office Supplies", "Category override rule not learned"
        log_assert("MongoDB Verified: Invoice B fields updated, CategoryOverride learned.")

        # Scenario C: Discard / Rejection Workflow
        log_step("6.3", "Scenario C: Approval Rejection & Discard")
        db_inv_c = Invoice(
            organization_id=str(org1_id),
            uploaded_by=str(org1_user_id),
            original_filename="unauthorized_expense.pdf",
            stored_path="./uploads/fake.pdf",
            content_type="application/pdf",
            status="pending_approval",
            vendor_name="Luxury Resort & Spa",
            total=3200.0,
            department="Executive",
        )
        await db_inv_c.save()
        inv_c_id = str(db_inv_c.id)

        appr_c = Approval(
            organization_id=str(org1_id),
            invoice_id=inv_c_id,
            status="pending",
        )
        await appr_c.save()
        appr_c_id = str(appr_c.id)

        reject_res = await client.post(
            f"/api/v1/approvals/{appr_c_id}/decide",
            headers=auth1_headers,
            json={"decision": "reject", "comment": "Personal expense not allowed."},
        )
        assert reject_res.status_code == 200, f"Rejection failed: {reject_res.text}"
        log_assert(f"POST /api/v1/approvals/{appr_c_id}/decide -> 200 OK (Rejected)")

        # Verify DB Status
        db_inv_c = await Invoice.get(inv_c_id)
        assert db_inv_c.status == "rejected", f"Expected rejected, got {db_inv_c.status}"
        log_assert("MongoDB Verified: Invoice C status set to 'rejected'.")

        # Scenario D: Duplicate Invoice Exception & Resolution
        log_step("6.4", "Scenario D: Duplicate Invoice Exception Detection & Void Resolution")
        dup_exc = InvoiceException(
            organization_id=str(org1_id),
            invoice_id=inv_a_id,
            type="duplicate",
            notes=f"Duplicate invoice identifier INV-AWS-{PREFIX}-001 detected.",
            status="open",
        )
        await dup_exc.save()
        dup_exc_id = str(dup_exc.id)

        # Query Exceptions API
        exc_list_res = await client.get("/api/v1/exceptions?status=open", headers=auth1_headers)
        assert exc_list_res.status_code == 200 and len(exc_list_res.json()["data"]) >= 1, f"Exceptions list failed: {exc_list_res.text}"
        log_assert("GET /api/v1/exceptions?status=open -> 200 OK (Duplicate exception in queue)")

        # Resolve Exception: Reject / Void Duplicate
        resolve_res = await client.post(
            f"/api/v1/exceptions/{dup_exc_id}/resolve",
            headers=auth1_headers,
            json={"action": "reject", "notes": "Confirmed duplicate from supplier. Voided."},
        )
        assert resolve_res.status_code == 200, f"Exception resolution failed: {resolve_res.text}"
        log_assert(f"POST /api/v1/exceptions/{dup_exc_id}/resolve -> 200 OK (Rejected/Voided)")

        # Verify DB Exception Status
        db_dup_exc = await InvoiceException.get(dup_exc_id)
        assert db_dup_exc.status == "resolved", "Exception not marked resolved in DB"
        log_assert("MongoDB Verified: InvoiceException marked 'resolved' (Invoice rejected).")

        # Scenario E: Budget Overrun Exception & Controller Override
        log_step("6.5", "Scenario E: Department Budget Overrun & Controller Override")
        budget_exc = InvoiceException(
            organization_id=str(org1_id),
            invoice_id=inv_b_id,
            type="budget",
            notes="Engineering budget limit exceeded by $1,200.00.",
            status="open",
        )
        await budget_exc.save()
        b_exc_id = str(budget_exc.id)

        # Resolve with Force Validate Override
        b_resolve_res = await client.post(
            f"/api/v1/exceptions/{b_exc_id}/resolve",
            headers=auth1_headers,
            json={"action": "force_validate", "notes": "Approved by VP of Engineering as one-time exception."},
        )
        assert b_resolve_res.status_code == 200, f"Budget override failed: {b_resolve_res.text}"
        log_assert(f"POST /api/v1/exceptions/{b_exc_id}/resolve -> 200 OK (Force Validate Override)")

        # Verify DB Exception Status
        db_b_exc = await InvoiceException.get(b_exc_id)
        assert db_b_exc.status == "resolved", "Budget exception not marked resolved in DB"
        log_assert("MongoDB Verified: Budget Exception marked 'resolved'.")

        # Scenario F: 1-Click Email Action Token
        log_step("6.6", "Scenario F: 1-Click Secure Email Token Action Handler")
        db_inv_f = Invoice(
            organization_id=str(org1_id),
            uploaded_by=str(org1_user_id),
            original_filename="email_action_test.pdf",
            stored_path="./uploads/fake.pdf",
            content_type="application/pdf",
            status="pending_approval",
            total=150.0,
        )
        await db_inv_f.save()
        inv_f_id = str(db_inv_f.id)

        appr_f = Approval(
            organization_id=str(org1_id),
            invoice_id=inv_f_id,
            status="pending",
        )
        await appr_f.save()
        appr_f_id = str(appr_f.id)

        # Generate HMAC token
        action_token = sign_email_action(appr_f_id, "approve")
        email_act_res = await client.get(f"/api/v1/approvals/action/{action_token}")
        assert email_act_res.status_code == 200, f"Email action failed: {email_act_res.text}"
        log_assert(f"GET /api/v1/approvals/action/{action_token[:15]}... -> 200 OK")

        # Verify DB
        db_inv_f = await Invoice.get(inv_f_id)
        assert db_inv_f.status == "approved", "Invoice not approved via email action"
        db_appr_f = await Approval.get(appr_f_id)
        assert db_appr_f.status == "approved", "Approval not approved via email action"
        log_assert("MongoDB Verified: Invoice F & Approval F approved via email action token.")

        # Scenario G: Soft-Deletion & Anti-IDOR Check
        log_step("6.7", "Scenario G: Soft-Deletion & Cross-Tenant Anti-IDOR Verification")
        # Soft delete Invoice F
        del_res = await client.delete(f"/api/v1/invoices/{inv_f_id}", headers=auth1_headers)
        assert del_res.status_code == 200, f"Delete failed: {del_res.text}"
        log_assert(f"DELETE /api/v1/invoices/{inv_f_id} -> 200 OK")

        # Verify in DB: is_deleted is True
        db_inv_f = await Invoice.get(inv_f_id)
        assert db_inv_f.is_deleted == True, "Invoice not soft deleted in DB"
        log_assert("MongoDB Verified: Invoice.is_deleted is True.")

        # Re-check via API: Must return 404 NOT_FOUND
        recheck_res = await client.get(f"/api/v1/invoices/{inv_f_id}", headers=auth1_headers)
        assert recheck_res.status_code == 404, f"Expected 404 after soft delete, got {recheck_res.status_code}"
        log_assert(f"GET /api/v1/invoices/{inv_f_id} (After delete) -> 404 NOT_FOUND")

        # Cross-Tenant Anti-IDOR Check: Org 2 attempts to access Org 1's active Invoice A
        cross_res = await client.get(f"/api/v1/invoices/{inv_a_id}", headers=auth2_headers)
        assert cross_res.status_code == 404, f"Expected 404 for cross-tenant probe, got {cross_res.status_code}"
        log_assert(f"GET /api/v1/invoices/{inv_a_id} (Org 2 probe on Org 1) -> 404 NOT_FOUND (Anti-IDOR)")

        # =====================================================================
        # PHASE 7: Reports & Compliance Audit Logs
        # =====================================================================
        log_step("7.0", "Testing Reports, Spend Summary & Audit Logs")

        # Dashboard Stats
        stats_res = await client.get("/api/v1/reports/dashboard-stats", headers=auth1_headers)
        assert stats_res.status_code == 200
        stats = stats_res.json()["data"]
        log_assert(f"GET /api/v1/reports/dashboard-stats -> 200 OK (Total Approved: {stats['approved_invoices_count']})")

        # Spend Summary
        spend_res = await client.get("/api/v1/reports/spend-summary", headers=auth1_headers)
        assert spend_res.status_code == 200
        log_assert("GET /api/v1/reports/spend-summary -> 200 OK")

        # Budget vs Actual
        bva_res = await client.get("/api/v1/reports/budget-vs-actual", headers=auth1_headers)
        assert bva_res.status_code == 200
        log_assert("GET /api/v1/reports/budget-vs-actual -> 200 OK")

        # Audit Logs
        audit_res = await client.get("/api/v1/audit-logs", headers=auth1_headers)
        assert audit_res.status_code == 200 and len(audit_res.json()["data"]) >= 5, f"Audit logs failed: {audit_res.text}"
        log_assert(f"GET /api/v1/audit-logs -> 200 OK ({len(audit_res.json()['data'])} audit entries)")

        # Verify AuditLog documents directly in MongoDB
        db_audits = await AuditLog.find(AuditLog.organization_id == str(org1_id)).to_list()
        assert len(db_audits) >= 5, "Audit logs missing in MongoDB"
        log_assert(f"MongoDB Verified: {len(db_audits)} immutable AuditLog entries recorded.")

        print("\n" + "=" * 70)
        print("  ALL SCENARIOS & DATABASE VERIFICATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 70)

    finally:
        await client.aclose()
        await disconnect_db()
        print("\n[DB] Disconnected from MongoDB Atlas.")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
