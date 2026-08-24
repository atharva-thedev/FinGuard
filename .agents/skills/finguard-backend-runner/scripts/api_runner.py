"""
FinGuard Automated API Runner Script
Executes an end-to-end integration test against the running FastAPI backend.
"""
import sys
import httpx

BASE_URL = "http://localhost:5000"


def run_smoke_test():
    print(f">> Starting FinGuard Smoke Test against {BASE_URL}...\n")
    client = httpx.Client(base_url=BASE_URL, timeout=10.0)

    # 1. Health Check
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[OK] [1/5] Health Check passed: 200 OK")

    # 2. Database Readiness
    res = client.get("/ready")
    assert res.status_code == 200, f"Readiness check failed: {res.text}"
    print("[OK] [2/5] Database Ping passed: 200 OK (connected)")

    # 3. Login Test
    login_payload = {
        "email": "atharva@company.com",
        "password": "Password123!"
    }
    res = client.post("/api/v1/auth/login", json=login_payload)
    if res.status_code != 200:
        reg_payload = {
            "email": "atharva@company.com",
            "password": "Password123!",
            "full_name": "Atharva Patil",
            "organization_name": "FinGuard Test Org"
        }
        res = client.post("/api/v1/auth/register", json=reg_payload)
        assert res.status_code in (200, 201), f"Registration failed: {res.text}"
        print("[OK] [3/5] Registered user: 201 Created")
    else:
        print("[OK] [3/5] Login successful: 200 OK")

    data = res.json()["data"]
    access_token = data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 4. Fetch User Profile
    res = client.get("/api/v1/users/me", headers=headers)
    assert res.status_code == 200, f"Profile fetch failed: {res.text}"
    user_info = res.json()["data"]
    print(f"[OK] [4/5] Profile verified for: {user_info['full_name']} ({user_info['role']})")

    # 5. Fetch Dashboard Stats
    res = client.get("/api/v1/reports/dashboard-stats", headers=headers)
    assert res.status_code == 200, f"Dashboard stats failed: {res.text}"
    stats = res.json()["data"]
    print(f"[OK] [5/5] Dashboard Stats retrieved: {stats}")

    print("\n==========================================")
    print("SUCCESS: ALL SMOKE TESTS PASSED!")
    print("==========================================")


if __name__ == "__main__":
    try:
        run_smoke_test()
    except Exception as e:
        print(f"\n❌ Test Failed: {e}", file=sys.stderr)
        sys.exit(1)
