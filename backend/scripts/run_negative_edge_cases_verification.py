"""
FinGuard Exhaustive Negative & Edge-Case Verification Suite
Tests all endpoints for validation errors, security boundaries, RBAC permissions,
tampered tokens, duplicate violations, and multi-tenant Anti-IDOR isolation.
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
    Invoice,
    InvoiceException,
    Organization,
    PolicyRule,
    Session,
    User,
    UserRole,
    Vendor,
)
from app.utils.jwt import sign_access, sign_email_action

BASE_URL = "http://localhost:5000"
PREFIX = f"neg_{uuid.uuid4().hex[:6]}"


def log_test(num: str, title: str):
    print(f"\n[TEST {num}] >> {title}")


def log_pass(msg: str):
    print(f"  [PASS] {msg}")


async def run_negative_tests():
    print("=" * 70)
    print("  FINGUARD EXHAUSTIVE NEGATIVE & EDGE-CASE TEST SUITE")
    print("=" * 70)

    await connect_db()
    print("[DB] Connected to MongoDB Atlas for state verification.")

    client = httpx.AsyncClient(base_url=BASE_URL, timeout=20.0)

    try:
        # =====================================================================
        # SETUP: Create Org 1 (Admin & AP Clerk) and Org 2 (Admin)
        # =====================================================================
        print("\n[SETUP] Creating isolated test organizations and users...")
        
        # Org 1 Admin
        org1_admin_email = f"{PREFIX}_admin1@org1.com"
        reg1_res = await client.post(
            "/api/v1/auth/register",
            json={
                "email": org1_admin_email,
                "password": "Password123!",
                "full_name": "Org1 Admin",
                "organization_name": f"{PREFIX} Organization 1",
            },
        )
        assert reg1_res.status_code == 201
        org1_token = reg1_res.json()["data"]["access_token"]
        org1_id = reg1_res.json()["data"]["user"]["organization_id"]
        org1_admin_id = reg1_res.json()["data"]["user"]["id"]
        auth1_admin = {"Authorization": f"Bearer {org1_token}"}

        # Org 1 AP Clerk
        org1_clerk = User(
            organization_id=str(org1_id),
            email=f"{PREFIX}_clerk1@org1.com",
            password_hash="$2b$12$eXfakehashforclerktesting1234567890",
            full_name="Org1 AP Clerk",
            role=UserRole.ap_clerk,
            department="Finance",
        )
        await org1_clerk.save()
        org1_clerk_id = str(org1_clerk.id)
        clerk_token = sign_access(org1_clerk_id, str(org1_id), UserRole.ap_clerk.value)
        auth1_clerk = {"Authorization": f"Bearer {clerk_token}"}

        # Org 2 Admin (Attacker / Cross-Tenant Prober)
        org2_admin_email = f"{PREFIX}_admin2@org2.com"
        reg2_res = await client.post(
            "/api/v1/auth/register",
            json={
                "email": org2_admin_email,
                "password": "Password123!",
                "full_name": "Org2 Admin",
                "organization_name": f"{PREFIX} Organization 2",
            },
        )
        assert reg2_res.status_code == 201
        org2_token = reg2_res.json()["data"]["access_token"]
        org2_id = reg2_res.json()["data"]["user"]["organization_id"]
        org2_admin_id = reg2_res.json()["data"]["user"]["id"]
        auth2_admin = {"Authorization": f"Bearer {org2_token}"}
        print("  [OK] Setup complete: Org 1 (Admin + AP Clerk) & Org 2 (Admin).")

        # =====================================================================
        # SUITE 1: Authentication & Session Security Edge Cases
        # =====================================================================
        log_test("1.1", "Register with empty payload -> 400 VALIDATION_ERROR")
        r = await client.post("/api/v1/auth/register", json={})
        assert r.status_code == 400 and r.json()["error"]["code"] == "VALIDATION_ERROR"
        log_pass("Empty payload correctly returned 400 VALIDATION_ERROR")

        log_test("1.2", "Register with malformed email -> 400 VALIDATION_ERROR")
        r = await client.post(
            "/api/v1/auth/register",
            json={"email": "notanemail", "password": "Pass", "full_name": "A", "organization_name": "B"},
        )
        assert r.status_code == 400 and "email" in str(r.json()["error"].get("fields", {}))
        log_pass("Malformed email rejected with structured field error")

        log_test("1.3", "Register duplicate email -> 409 EMAIL_ALREADY_REGISTERED")
        r = await client.post(
            "/api/v1/auth/register",
            json={
                "email": org1_admin_email,
                "password": "Password123!",
                "full_name": "Duplicate User",
                "organization_name": "Duplicate Org",
            },
        )
        assert r.status_code == 409 and r.json()["error"]["code"] == "EMAIL_ALREADY_REGISTERED"
        log_pass("Duplicate email rejected with 409 Conflict")

        log_test("1.4", "Login non-existent user -> 401 UNAUTHORIZED")
        r = await client.post("/api/v1/auth/login", json={"email": "ghost@company.com", "password": "Password123!"})
        assert r.status_code == 401 and r.json()["error"]["code"] == "UNAUTHORIZED"
        log_pass("Non-existent user rejected with 401 UNAUTHORIZED")

        log_test("1.5", "Login incorrect password -> 401 UNAUTHORIZED")
        r = await client.post("/api/v1/auth/login", json={"email": org1_admin_email, "password": "WrongPassword!"})
        assert r.status_code == 401 and r.json()["error"]["code"] == "UNAUTHORIZED"
        log_pass("Incorrect password rejected with 401 UNAUTHORIZED")

        log_test("1.6", "Refresh token missing cookie -> 401 REFRESH_TOKEN_INVALID")
        async with httpx.AsyncClient(base_url=BASE_URL) as unauthed_client:
            r = await unauthed_client.post("/api/v1/auth/refresh")
            assert r.status_code == 401 and r.json()["error"]["code"] == "REFRESH_TOKEN_INVALID", f"Expected 401 REFRESH_TOKEN_INVALID, got {r.status_code}: {r.text}"
        log_pass("Missing refresh cookie rejected with 401 REFRESH_TOKEN_INVALID")

        log_test("1.7", "Refresh token malformed format (no dot) -> 401 REFRESH_TOKEN_INVALID")
        async with httpx.AsyncClient(base_url=BASE_URL) as unauthed_client:
            r = await unauthed_client.post(
                "/api/v1/auth/refresh",
                cookies={"refresh_token": "malformedtokenwithoutdot"},
                headers={"Cookie": "refresh_token=malformedtokenwithoutdot"},
            )
            assert r.status_code == 401 and r.json()["error"]["code"] == "REFRESH_TOKEN_INVALID", f"Expected 401, got {r.status_code}: {r.text}"
        log_pass("Malformed refresh token rejected with 401")

        log_test("1.8", "Refresh token reuse breach detection -> 401 & Cascading Revocation")
        login_res = await client.post("/api/v1/auth/login", json={"email": org1_admin_email, "password": "Password123!"})
        set_cookie = login_res.headers.get("set-cookie", "")
        old_refresh_cookie = set_cookie.split("refresh_token=")[1].split(";")[0]
        
        # First valid refresh (rotates session)
        r1 = await client.post(
            "/api/v1/auth/refresh",
            cookies={"refresh_token": old_refresh_cookie},
            headers={"Cookie": f"refresh_token={old_refresh_cookie}"},
        )
        assert r1.status_code == 200
        
        # Second refresh with OLD rotated token (Replay Attack simulation)
        r2 = await client.post(
            "/api/v1/auth/refresh",
            cookies={"refresh_token": old_refresh_cookie},
            headers={"Cookie": f"refresh_token={old_refresh_cookie}"},
        )
        assert r2.status_code == 401 and r2.json()["error"]["code"] == "REFRESH_TOKEN_INVALID"
        
        # Verify all sessions revoked for this user in DB
        active_sessions = await Session.find(Session.user_id == str(org1_admin_id), Session.revoked == False).to_list()
        assert len(active_sessions) == 0, "Breach detection failed to revoke all user sessions!"
        log_pass("Replay attack detected: 401 returned and all sessions revoked in MongoDB Atlas.")

        # Re-login Org 1 Admin to get fresh token for remaining suites
        relogin = await client.post("/api/v1/auth/login", json={"email": org1_admin_email, "password": "Password123!"})
        org1_token = relogin.json()["data"]["access_token"]
        auth1_admin = {"Authorization": f"Bearer {org1_token}"}

        # =====================================================================
        # SUITE 2: Users & Security Boundaries
        # =====================================================================
        log_test("2.1", "Protected route without token -> 401 UNAUTHORIZED")
        r = await client.get("/api/v1/users/me")
        assert r.status_code == 401 and r.json()["error"]["code"] == "UNAUTHORIZED"
        log_pass("Missing Bearer header returned 401 UNAUTHORIZED")

        log_test("2.2", "Protected route with tampered token -> 401 TOKEN_INVALID")
        r = await client.get("/api/v1/users/me", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsIn.tampered.signature"})
        assert r.status_code == 401 and r.json()["error"]["code"] == "TOKEN_INVALID"
        log_pass("Tampered token returned 401 TOKEN_INVALID")

        log_test("2.3", "Change password with incorrect current password -> 400 INVALID_CURRENT_PASSWORD")
        r = await client.post(
            "/api/v1/users/me/change-password",
            headers=auth1_admin,
            json={"current_password": "WrongCurrentPassword123!", "new_password": "NewValidPassword456!"},
        )
        assert r.status_code == 400 and r.json()["error"]["code"] == "INVALID_CURRENT_PASSWORD"
        log_pass("Incorrect current password rejected with 400 INVALID_CURRENT_PASSWORD")

        log_test("2.4", "Delete non-existent session -> 404 NOT_FOUND")
        r = await client.delete(f"/api/v1/users/me/sessions/{uuid.uuid4().hex[:24]}", headers=auth1_admin)
        assert r.status_code == 404 and r.json()["error"]["code"] == "NOT_FOUND"
        log_pass("Non-existent session deletion returned 404 NOT_FOUND")

        log_test("2.5", "Admin user creation by AP Clerk -> 403 FORBIDDEN")
        r = await client.post(
            "/api/v1/users",
            headers=auth1_clerk,
            json={"email": f"{PREFIX}_unauthorized@org1.com", "password": "Password123!", "full_name": "Hacker", "role": "admin"},
        )
        assert r.status_code == 403 and r.json()["error"]["code"] == "FORBIDDEN"
        log_pass("RBAC enforced: AP Clerk cannot create users (403 FORBIDDEN)")

        log_test("2.6", "Cross-Tenant User Role Update -> 404 NOT_FOUND (Anti-IDOR)")
        r = await client.patch(
            f"/api/v1/users/{org1_clerk_id}/role",
            headers=auth2_admin,
            json={"role": "admin"},
        )
        assert r.status_code == 404, f"Expected 404 for cross-tenant user update, got {r.status_code}"
        log_pass("Anti-IDOR: Org 2 updating Org 1 user role returned 404 NOT_FOUND")

        # =====================================================================
        # SUITE 3: Organizations, Policies & Budgets Edge Cases
        # =====================================================================
        log_test("3.1", "Update organization settings by AP Clerk -> 403 FORBIDDEN")
        r = await client.patch(
            "/api/v1/organizations/me",
            headers=auth1_clerk,
            json={"approval_threshold": 999.0},
        )
        assert r.status_code == 403 and r.json()["error"]["code"] == "FORBIDDEN"
        log_pass("RBAC enforced: AP Clerk cannot modify organization settings (403 FORBIDDEN)")

        log_test("3.2", "Create budget with negative/zero limit -> 400 VALIDATION_ERROR")
        r = await client.post(
            "/api/v1/policies/budgets",
            headers=auth1_admin,
            json={"department": "Engineering", "category": "Cloud Infrastructure", "monthly_limit": -500.0},
        )
        assert r.status_code == 400 and r.json()["error"]["code"] == "VALIDATION_ERROR"
        log_pass("Negative budget limit rejected with 400 VALIDATION_ERROR")

        # Create valid budget in Org 1
        b_res = await client.post(
            "/api/v1/policies/budgets",
            headers=auth1_admin,
            json={"department": "Marketing", "category": "Advertising", "monthly_limit": 10000.0},
        )
        assert b_res.status_code == 201
        org1_budget_id = b_res.json()["data"]["id"]

        log_test("3.3", "Cross-Tenant Budget Update probe -> 404 NOT_FOUND (Anti-IDOR)")
        r = await client.patch(
            f"/api/v1/policies/budgets/{org1_budget_id}",
            headers=auth2_admin,
            json={"monthly_limit": 1.0},
        )
        assert r.status_code == 404, f"Expected 404 for cross-tenant budget update, got {r.status_code}"
        log_pass("Anti-IDOR: Org 2 updating Org 1 budget returned 404 NOT_FOUND")

        log_test("3.4", "Cross-Tenant Budget Delete probe -> 404 NOT_FOUND (Anti-IDOR)")
        r = await client.delete(
            f"/api/v1/policies/budgets/{org1_budget_id}",
            headers=auth2_admin,
        )
        assert r.status_code == 404, f"Expected 404 for cross-tenant budget delete, got {r.status_code}"
        log_pass("Anti-IDOR: Org 2 deleting Org 1 budget returned 404 NOT_FOUND")

        # =====================================================================
        # SUITE 4: Vendors & Categories Edge Cases
        # =====================================================================
        log_test("4.1", "Create vendor with empty name -> 400 VALIDATION_ERROR")
        r = await client.post("/api/v1/vendors", headers=auth1_admin, json={"name": ""})
        assert r.status_code == 400 and r.json()["error"]["code"] == "VALIDATION_ERROR"
        log_pass("Empty vendor name rejected with 400 VALIDATION_ERROR")

        # Create Vendor in Org 1
        v_res = await client.post("/api/v1/vendors", headers=auth1_admin, json={"name": "Stripe Payments"})
        assert v_res.status_code == 201
        org1_vendor_id = v_res.json()["data"]["id"]

        log_test("4.2", "Create duplicate normalized vendor -> 409 VENDOR_ALREADY_EXISTS")
        r = await client.post("/api/v1/vendors", headers=auth1_admin, json={"name": "  stripe payments  "})
        assert r.status_code == 409 and r.json()["error"]["code"] == "VENDOR_ALREADY_EXISTS"
        log_pass("Duplicate normalized vendor rejected with 409 Conflict")

        log_test("4.3", "Cross-Tenant Vendor Delete probe -> 404 NOT_FOUND (Anti-IDOR)")
        r = await client.delete(f"/api/v1/vendors/{org1_vendor_id}", headers=auth2_admin)
        assert r.status_code == 404, f"Expected 404 for cross-tenant vendor delete, got {r.status_code}"
        log_pass("Anti-IDOR: Org 2 deleting Org 1 vendor returned 404 NOT_FOUND")

        log_test("4.4", "Create category with empty name -> 400 VALIDATION_ERROR")
        r = await client.post("/api/v1/categories", headers=auth1_admin, json={"name": ""})
        assert r.status_code == 400 and r.json()["error"]["code"] == "VALIDATION_ERROR"
        log_pass("Empty category name rejected with 400 VALIDATION_ERROR")

        log_test("4.5", "Create duplicate category name -> 409 CATEGORY_ALREADY_EXISTS")
        await client.post("/api/v1/categories", headers=auth1_admin, json={"name": "Legal & Compliance"})
        r = await client.post("/api/v1/categories", headers=auth1_admin, json={"name": "Legal & Compliance"})
        assert r.status_code == 409 and r.json()["error"]["code"] == "CATEGORY_ALREADY_EXISTS"
        log_pass("Duplicate category name rejected with 409 Conflict")

        # =====================================================================
        # SUITE 5: Invoices Lifecycle & Multi-Tenant IDOR
        # =====================================================================
        log_test("5.1", "Get non-existent invoice -> 404 NOT_FOUND")
        r = await client.get(f"/api/v1/invoices/{uuid.uuid4().hex[:24]}", headers=auth1_admin)
        assert r.status_code == 404 and r.json()["error"]["code"] == "NOT_FOUND"
        log_pass("Non-existent invoice returned 404 NOT_FOUND")

        # Create valid Invoice in Org 1
        fake_pdf = io.BytesIO(b"%PDF-1.4 Edge Case Testing Invoice")
        up_res = await client.post(
            "/api/v1/invoices",
            headers=auth1_admin,
            files=[("files", ("edge_case.pdf", fake_pdf, "application/pdf"))],
        )
        assert up_res.status_code == 201
        org1_inv_id = up_res.json()["data"][0]["id"]

        log_test("5.2", "Cross-Tenant Invoice Get probe -> 404 NOT_FOUND (Anti-IDOR)")
        r = await client.get(f"/api/v1/invoices/{org1_inv_id}", headers=auth2_admin)
        assert r.status_code == 404, f"Expected 404 for cross-tenant invoice probe, got {r.status_code}"
        log_pass("Anti-IDOR: Org 2 querying Org 1 invoice returned 404 NOT_FOUND")

        log_test("5.3", "Cross-Tenant Invoice Extraction Update probe -> 404 NOT_FOUND (Anti-IDOR)")
        r = await client.patch(
            f"/api/v1/invoices/{org1_inv_id}/extraction",
            headers=auth2_admin,
            json={"total": 999.0},
        )
        assert r.status_code == 404, f"Expected 404 for cross-tenant extraction update, got {r.status_code}"
        log_pass("Anti-IDOR: Org 2 updating Org 1 extraction returned 404 NOT_FOUND")

        log_test("5.4", "Delete invoice as AP Clerk -> 403 FORBIDDEN")
        r = await client.delete(f"/api/v1/invoices/{org1_inv_id}", headers=auth1_clerk)
        assert r.status_code == 403 and r.json()["error"]["code"] == "FORBIDDEN"
        log_pass("RBAC enforced: AP Clerk cannot delete invoices (403 FORBIDDEN)")

        log_test("5.5", "Cross-Tenant Invoice Delete probe -> 404 NOT_FOUND (Anti-IDOR)")
        r = await client.delete(f"/api/v1/invoices/{org1_inv_id}", headers=auth2_admin)
        assert r.status_code == 404, f"Expected 404 for cross-tenant invoice delete, got {r.status_code}"
        log_pass("Anti-IDOR: Org 2 deleting Org 1 invoice returned 404 NOT_FOUND")

        # Soft delete invoice by Org 1 Admin
        del_res = await client.delete(f"/api/v1/invoices/{org1_inv_id}", headers=auth1_admin)
        assert del_res.status_code == 200

        log_test("5.6", "Access soft-deleted invoice -> 404 NOT_FOUND")
        r = await client.get(f"/api/v1/invoices/{org1_inv_id}", headers=auth1_admin)
        assert r.status_code == 404, f"Expected 404 for soft-deleted invoice, got {r.status_code}"
        log_pass("Soft-deleted invoice correctly returns 404 NOT_FOUND")

        # =====================================================================
        # SUITE 6: Approvals & Action Tokens
        # =====================================================================
        # Create a fresh invoice and approval for Org 1
        db_inv = Invoice(
            organization_id=str(org1_id),
            uploaded_by=str(org1_admin_id),
            original_filename="approval_edge_case.pdf",
            stored_path="./uploads/fake.pdf",
            content_type="application/pdf",
            status="pending_approval",
            total=100.0,
        )
        await db_inv.save()
        appr_inv_id = str(db_inv.id)

        appr = Approval(
            organization_id=str(org1_id),
            invoice_id=appr_inv_id,
            status="pending",
        )
        await appr.save()
        appr_id = str(appr.id)

        log_test("6.1", "Decide approval with invalid decision enum -> 400 VALIDATION_ERROR")
        r = await client.post(
            f"/api/v1/approvals/{appr_id}/decide",
            headers=auth1_admin,
            json={"decision": "maybe", "comment": "Undecided"},
        )
        assert r.status_code == 400 and r.json()["error"]["code"] == "VALIDATION_ERROR"
        log_pass("Invalid decision enum ('maybe') rejected with 400 VALIDATION_ERROR")

        log_test("6.2", "Cross-Tenant Approval Decision probe -> 404 NOT_FOUND (Anti-IDOR)")
        r = await client.post(
            f"/api/v1/approvals/{appr_id}/decide",
            headers=auth2_admin,
            json={"decision": "approve", "comment": "Hacker approval"},
        )
        assert r.status_code == 404, f"Expected 404 for cross-tenant approval, got {r.status_code}"
        log_pass("Anti-IDOR: Org 2 deciding Org 1 approval returned 404 NOT_FOUND")

        # First valid decision
        dec1 = await client.post(
            f"/api/v1/approvals/{appr_id}/decide",
            headers=auth1_admin,
            json={"decision": "approve", "comment": "Legitimate approval"},
        )
        assert dec1.status_code == 200

        log_test("6.3", "Double decision on already approved approval -> 400 INVALID_REQUEST")
        r = await client.post(
            f"/api/v1/approvals/{appr_id}/decide",
            headers=auth1_admin,
            json={"decision": "reject", "comment": "Trying to reverse already approved"},
        )
        assert r.status_code == 400 and r.json()["error"]["code"] == "INVALID_REQUEST"
        log_pass("Double decision rejected with 400 INVALID_REQUEST (APPROVAL_ALREADY_DECIDED)")

        log_test("6.4", "Action Token with tampered signature -> 401 TOKEN_INVALID")
        valid_token = sign_email_action(appr_id, "approve")
        tampered_token = valid_token[:-5] + "XXXXX"
        r = await client.get(f"/api/v1/approvals/action/{tampered_token}")
        assert r.status_code == 401 and r.json()["error"]["code"] == "TOKEN_INVALID"
        log_pass("Tampered HMAC action token returned 401 TOKEN_INVALID")

        # =====================================================================
        # SUITE 7: Exceptions Queue & RBAC Resolution
        # =====================================================================
        # Create an open budget exception for Org 1
        exc = InvoiceException(
            organization_id=str(org1_id),
            invoice_id=appr_inv_id,
            type="budget",
            notes="Engineering budget overrun by $500",
            status="open",
        )
        await exc.save()
        exc_id = str(exc.id)

        log_test("7.1", "Resolve exception with invalid action enum -> 400 VALIDATION_ERROR")
        r = await client.post(
            f"/api/v1/exceptions/{exc_id}/resolve",
            headers=auth1_admin,
            json={"action": "destroy", "notes": "Invalid action"},
        )
        assert r.status_code == 400 and r.json()["error"]["code"] == "VALIDATION_ERROR"
        log_pass("Invalid action enum ('destroy') rejected with 400 VALIDATION_ERROR")

        log_test("7.2", "AP Clerk attempts to resolve budget exception -> 403 FORBIDDEN")
        r = await client.post(
            f"/api/v1/exceptions/{exc_id}/resolve",
            headers=auth1_clerk,
            json={"action": "force_validate", "notes": "AP Clerk override attempt"},
        )
        assert r.status_code == 403 and r.json()["error"]["code"] == "FORBIDDEN"
        log_pass("RBAC enforced: AP Clerk cannot resolve budget exceptions (403 FORBIDDEN)")

        log_test("7.3", "Cross-Tenant Exception Resolution probe -> 404 NOT_FOUND (Anti-IDOR)")
        r = await client.post(
            f"/api/v1/exceptions/{exc_id}/resolve",
            headers=auth2_admin,
            json={"action": "force_validate", "notes": "Org 2 override attempt"},
        )
        assert r.status_code == 404, f"Expected 404 for cross-tenant exception resolution, got {r.status_code}"
        log_pass("Anti-IDOR: Org 2 resolving Org 1 exception returned 404 NOT_FOUND")

        # Valid resolution by Org 1 Admin
        res_ok = await client.post(
            f"/api/v1/exceptions/{exc_id}/resolve",
            headers=auth1_admin,
            json={"action": "force_validate", "notes": "Controller authorized"},
        )
        assert res_ok.status_code == 200

        log_test("7.4", "Double resolution on already resolved exception -> 400 INVALID_REQUEST")
        r = await client.post(
            f"/api/v1/exceptions/{exc_id}/resolve",
            headers=auth1_admin,
            json={"action": "reject", "notes": "Trying to re-resolve"},
        )
        assert r.status_code == 400 and r.json()["error"]["code"] == "INVALID_REQUEST"
        log_pass("Double resolution rejected with 400 INVALID_REQUEST")

        # =====================================================================
        # SUITE 8: Audit Logs & Reports RBAC
        # =====================================================================
        log_test("8.1", "Audit logs fetched by AP Clerk -> 403 FORBIDDEN")
        r = await client.get("/api/v1/audit-logs", headers=auth1_clerk)
        assert r.status_code == 403 and r.json()["error"]["code"] == "FORBIDDEN"
        log_pass("RBAC enforced: AP Clerk cannot access audit logs (403 FORBIDDEN)")

        log_test("8.2", "Audit logs tenant isolation check")
        r1 = await client.get("/api/v1/audit-logs", headers=auth1_admin)
        r2 = await client.get("/api/v1/audit-logs", headers=auth2_admin)
        assert r1.status_code == 200 and r2.status_code == 200
        org1_logs = r1.json()["data"]
        org2_logs = r2.json()["data"]
        
        # Verify 0 overlap between Org 1 and Org 2 audit logs
        org1_log_ids = {l["id"] for l in org1_logs}
        org2_log_ids = {l["id"] for l in org2_logs}
        assert org1_log_ids.isdisjoint(org2_log_ids), "Audit logs leaked across tenants!"
        log_pass(f"Complete Tenant Isolation verified: Org 1 ({len(org1_logs)} logs) vs Org 2 ({len(org2_logs)} logs) with 0 leak.")

        print("\n" + "=" * 70)
        print("  ALL 30+ NEGATIVE & EDGE-CASE TESTS PASSED WITH 100% SUCCESS!")
        print("=" * 70)

    finally:
        await client.aclose()
        await disconnect_db()
        print("\n[DB] Disconnected from MongoDB Atlas.")


if __name__ == "__main__":
    asyncio.run(run_negative_tests())
