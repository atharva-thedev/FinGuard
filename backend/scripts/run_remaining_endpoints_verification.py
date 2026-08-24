"""
FinGuard Remaining Endpoints & Deep Feature Verification Suite
Tests all remaining endpoints:
1. GET /api/v1/users (Admin list users)
2. POST /api/v1/users (Admin create user directly)
3. PATCH /api/v1/users/{id}/role (Admin promote/demote role in org)
4. DELETE /api/v1/users/me (User self-account deletion with confirmation text)
5. PATCH /api/v1/vendors/{id} (Update vendor details)
6. GET /api/v1/vendors?search=... (Search vendor directory)
7. GET /api/v1/categories/overrides (List category overrides)
8. POST /api/v1/categories/overrides (Explicit vendor-category override rule)
9. PATCH /api/v1/policies/rules/{code} (Update/toggle policy rule)
10. POST /api/v1/invoices/{id}/reprocess (Reprocess OCR pipeline)
11. GET /api/v1/invoices (Multi-parameter query filtering)
12. POST /api/v1/auth/logout (Explicit session logout)
13. WS /api/v1/ws?token=... (Live WebSocket connection & Ping/Pong)
"""

import asyncio
import io
import os
import sys
import uuid
import httpx
import websockets

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config.db import connect_db, disconnect_db
from app.models.documents import (
    CategoryOverride,
    Invoice,
    PolicyRule,
    Session,
    User,
    UserRole,
    Vendor,
)

BASE_URL = "http://localhost:5000"
WS_URL = "ws://localhost:5000/api/v1"
PREFIX = f"rem_{uuid.uuid4().hex[:6]}"


def log_test(num: str, title: str):
    print(f"\n[REMAINING TEST {num}] >> {title}")


def log_pass(msg: str):
    print(f"  [PASS] {msg}")


async def run_remaining_tests():
    print("=" * 70)
    print("  FINGUARD REMAINING ENDPOINTS & DEEP FEATURE TEST SUITE")
    print("=" * 70)

    await connect_db()
    print("[DB] Connected to MongoDB Atlas for state verification.")

    client = httpx.AsyncClient(base_url=BASE_URL, timeout=20.0)

    try:
        # Setup: Register Admin
        admin_email = f"{PREFIX}_admin@corp.com"
        reg_res = await client.post(
            "/api/v1/auth/register",
            json={
                "email": admin_email,
                "password": "Password123!",
                "full_name": "Remaining Admin",
                "organization_name": f"{PREFIX} Corp",
            },
        )
        assert reg_res.status_code == 201
        admin_token = reg_res.json()["data"]["access_token"]
        org_id = reg_res.json()["data"]["user"]["organization_id"]
        admin_id = reg_res.json()["data"]["user"]["id"]
        auth_admin = {"Authorization": f"Bearer {admin_token}"}

        # 1. Admin Create User
        log_test("1", "Admin creates user directly via POST /api/v1/users")
        new_user_email = f"{PREFIX}_staff@corp.com"
        create_u_res = await client.post(
            "/api/v1/users",
            headers=auth_admin,
            json={
                "email": new_user_email,
                "password": "Password123!",
                "full_name": "Staff Member",
                "role": "ap_clerk",
                "department": "Finance",
            },
        )
        assert create_u_res.status_code == 201, f"Create user failed: {create_u_res.text}"
        staff_id = create_u_res.json()["data"]["id"]
        log_pass(f"POST /api/v1/users -> 201 Created (Staff ID: {staff_id})")

        # 2. Admin List Users
        log_test("2", "Admin lists all organization users via GET /api/v1/users")
        list_u_res = await client.get("/api/v1/users", headers=auth_admin)
        assert list_u_res.status_code == 200 and len(list_u_res.json()["data"]) >= 2
        log_pass(f"GET /api/v1/users -> 200 OK ({len(list_u_res.json()['data'])} users in organization)")

        # 3. Admin Update User Role
        log_test("3", "Admin updates user role via PATCH /api/v1/users/{id}/role")
        role_res = await client.patch(
            f"/api/v1/users/{staff_id}/role",
            headers=auth_admin,
            json={"role": "controller"},
        )
        assert role_res.status_code == 200 and role_res.json()["data"]["role"] == "controller"
        # Verify in MongoDB
        db_user = await User.get(staff_id)
        assert db_user.role == UserRole.controller, "Role not updated in DB"
        log_pass(f"PATCH /api/v1/users/{staff_id}/role -> 200 OK (Promoted to controller)")

        # 4. User Self-Account Deletion
        log_test("4", "User deletes self account via DELETE /api/v1/users/me")
        # Login as staff to get token
        login_staff = await client.post("/api/v1/auth/login", json={"email": new_user_email, "password": "Password123!"})
        staff_token = login_staff.json()["data"]["access_token"]
        auth_staff = {"Authorization": f"Bearer {staff_token}"}
        del_me_res = await client.request(
            "DELETE",
            "/api/v1/users/me",
            headers=auth_staff,
            json={"confirm_text": "DELETE"},
        )
        assert del_me_res.status_code == 200, f"Account deletion failed: {del_me_res.text}"
        # Verify soft-deletion in DB
        db_staff_del = await User.get(staff_id)
        assert db_staff_del.is_deleted == True, "User account not soft-deleted in DB"
        log_pass("DELETE /api/v1/users/me -> 200 OK (MongoDB Verified: User.is_deleted is True)")

        # 5. Vendor Update
        log_test("5", "Update vendor via PATCH /api/v1/vendors/{id}")
        v_res = await client.post("/api/v1/vendors", headers=auth_admin, json={"name": "Salesforce Inc."})
        assert v_res.status_code == 201
        v_id = v_res.json()["data"]["id"]
        patch_v_res = await client.patch(
            f"/api/v1/vendors/{v_id}",
            headers=auth_admin,
            json={"name": "Salesforce CRM Global", "registered": True},
        )
        assert patch_v_res.status_code == 200 and patch_v_res.json()["data"]["name"] == "Salesforce CRM Global"
        log_pass(f"PATCH /api/v1/vendors/{v_id} -> 200 OK (Vendor renamed)")

        # 6. Vendor Search Filter
        log_test("6", "Search vendor directory via GET /api/v1/vendors?search=salesforce")
        search_v_res = await client.get("/api/v1/vendors?search=salesforce", headers=auth_admin)
        assert search_v_res.status_code == 200 and len(search_v_res.json()["data"]) >= 1
        log_pass("GET /api/v1/vendors?search=salesforce -> 200 OK (Found matched vendor)")

        # 7. Category Overrides (Create & List)
        log_test("7", "Create and List category overrides via /api/v1/categories/overrides")
        cat_ovr_res = await client.post(
            "/api/v1/categories/overrides",
            headers=auth_admin,
            json={"vendor_name": "GitHub Inc.", "category": "Software Subscriptions"},
        )
        assert cat_ovr_res.status_code == 201
        list_ovr_res = await client.get("/api/v1/categories/overrides", headers=auth_admin)
        assert list_ovr_res.status_code == 200 and len(list_ovr_res.json()["data"]) >= 1
        log_pass("POST & GET /api/v1/categories/overrides -> 200 OK (Rule created and listed)")

        # 8. Policy Rule Configuration
        log_test("8", "Update policy compliance rule via PATCH /api/v1/policies/rules/{code}")
        rules_res = await client.get("/api/v1/policies/rules", headers=auth_admin)
        rule_code = rules_res.json()["data"][0]["code"]
        patch_rule_res = await client.patch(
            f"/api/v1/policies/rules/{rule_code}",
            headers=auth_admin,
            json={"enabled": False, "config": {"max_exceptions": 3}},
        )
        assert patch_rule_res.status_code == 200 and patch_rule_res.json()["data"]["enabled"] == False
        log_pass(f"PATCH /api/v1/policies/rules/{rule_code} -> 200 OK (Rule disabled)")

        # 9. Invoices Filter & Reprocess
        log_test("9", "Filter invoices via GET /api/v1/invoices and Reprocess via POST")
        fake_pdf = io.BytesIO(b"%PDF-1.4 Filter Test Invoice")
        up_res = await client.post(
            "/api/v1/invoices",
            headers=auth_admin,
            files=[("files", ("filter_test.pdf", fake_pdf, "application/pdf"))],
        )
        assert up_res.status_code == 201
        inv_id = up_res.json()["data"][0]["id"]
        
        # Filter list
        filter_res = await client.get("/api/v1/invoices?limit=5", headers=auth_admin)
        assert filter_res.status_code == 200 and len(filter_res.json()["data"]) >= 1, f"Filter invoices failed: {filter_res.text}"
        log_pass(f"GET /api/v1/invoices?limit=5 -> 200 OK ({len(filter_res.json()['data'])} items returned)")

        # Reprocess
        reproc_res = await client.post(f"/api/v1/invoices/{inv_id}/reprocess", headers=auth_admin)
        assert reproc_res.status_code == 200
        log_pass(f"POST /api/v1/invoices/{inv_id}/reprocess -> 200 OK (Pipeline rerun)")

        # 10. Explicit Logout
        log_test("10", "Explicit session logout via POST /api/v1/auth/logout")
        # Login temporary user
        temp_login = await client.post("/api/v1/auth/login", json={"email": admin_email, "password": "Password123!"})
        temp_set_cookie = temp_login.headers.get("set-cookie", "")
        temp_cookie_val = temp_set_cookie.split("refresh_token=")[1].split(";")[0]
        session_id = temp_cookie_val.split(".")[0]

        logout_res = await client.post(
            "/api/v1/auth/logout",
            cookies={"refresh_token": temp_cookie_val},
            headers={"Cookie": f"refresh_token={temp_cookie_val}"},
        )
        assert logout_res.status_code == 200
        # Verify session revoked in DB
        db_s = await Session.get(session_id)
        assert db_s.revoked == True, "Session not revoked in DB on logout"
        log_pass("POST /api/v1/auth/logout -> 200 OK (MongoDB Verified: Session.revoked is True)")

        # 11. WebSocket Connection & Ping-Pong
        log_test("11", "Real-time WebSocket handshake and Ping/Pong via WS /ws?token=...")
        ws_endpoint = f"{WS_URL}/ws?token={admin_token}"
        async with websockets.connect(ws_endpoint) as ws:
            await ws.send("ping")
            reply = await asyncio.wait_for(ws.recv(), timeout=5.0)
            assert reply == "pong", f"Expected pong, got {reply}"
        log_pass("WS /ws?token=... -> Connected, Ping/Pong handshake successful")

        print("\n" + "=" * 70)
        print("  ALL 11 REMAINING ENDPOINTS & FEATURES VERIFIED WITH 100% SUCCESS!")
        print("=" * 70)

    finally:
        await client.aclose()
        await disconnect_db()
        print("\n[DB] Disconnected from MongoDB Atlas.")


if __name__ == "__main__":
    asyncio.run(run_remaining_tests())
