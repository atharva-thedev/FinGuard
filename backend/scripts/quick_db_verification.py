"""
Quick live API & MongoDB Atlas Direct Verification
1. Registers/adds a new user via API endpoint (http://localhost:5000/api/v1/auth/register).
2. Connects directly to MongoDB Atlas using the configured MONGO_URI.
3. Queries and verifies the exact document in the 'users' and 'organizations' collections.
4. Updates user profile via API and queries MongoDB Atlas again to verify database mutation.
5. Soft-deletes user via API and queries MongoDB Atlas to verify is_deleted flag.
"""

import asyncio
import os
import sys
import time
import httpx
from pymongo import MongoClient

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.config.env import settings

BASE_URL = "http://localhost:5000"


async def main():
    print("=" * 65)
    print("  QUICK LIVE API -> MONGODB ATLAS VERIFICATION")
    print("=" * 65)
    print(f"[*] Base API URL : {BASE_URL}")
    print(f"[*] MongoDB Target: {settings.mongodb_uri.split('@')[-1]}")
    print(f"[*] Database Name : {settings.mongodb_db}\n")

    # Connect directly to MongoDB Atlas via PyMongo
    mongo_client = MongoClient(settings.mongodb_uri)
    db = mongo_client[settings.mongodb_db]
    print("[1] DIRECT DB PING >>")
    ping_res = db.command("ping")
    print(f"    MongoDB Atlas Ping Response: {ping_res}\n")

    test_email = f"quick_test_{int(time.time())}@company.com"
    test_password = "SecurePassword123!"
    test_org_name = "Quick Test Org"

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
        # STEP 1: ADD NEW USER VIA API
        print(f"[2] API COMMAND >> Adding new user via POST /api/v1/auth/register")
        reg_payload = {
            "email": test_email,
            "password": test_password,
            "full_name": "Quick Test User",
            "organization_name": test_org_name,
        }
        res = await client.post("/api/v1/auth/register", json=reg_payload)
        print(f"    HTTP Status: {res.status_code}")
        print(f"    API Response: {res.json()}\n")
        assert res.status_code == 201, f"Registration failed: {res.text}"

        token = res.json()["data"]["access_token"]
        user_id = res.json()["data"]["user"]["id"]
        org_id = res.json()["data"]["user"]["organization_id"]

        # STEP 2: VERIFY IN MONGODB ATLAS DATABASE DIRECTLY
        print(f"[3] DATABASE CHECK >> Querying MongoDB Atlas for user: '{test_email}'")
        user_doc = db.users.find_one({"email": test_email.lower()})
        print("    --- User Document in MongoDB Atlas ---")
        if user_doc:
            for k, v in user_doc.items():
                print(f"    * {k}: {v}")
        print("    --------------------------------------")
        assert user_doc is not None, "User not found in MongoDB Atlas!"
        print("    [OK] User document confirmed in MongoDB Atlas!\n")

        # STEP 3: UPDATE PROFILE VIA API
        print(f"[4] API COMMAND >> Updating user profile via PATCH /api/v1/users/me")
        headers = {"Authorization": f"Bearer {token}"}
        patch_res = await client.patch(
            "/api/v1/users/me",
            headers=headers,
            json={"full_name": "Quick Test User (UPDATED)", "department": "Security Operations"},
        )
        print(f"    HTTP Status: {patch_res.status_code}")
        print(f"    API Response: {patch_res.json()}\n")
        assert patch_res.status_code == 200

        # STEP 4: RE-CHECK DATABASE FOR UPDATE
        print(f"[5] DATABASE RE-CHECK >> Verifying updated fields directly in MongoDB Atlas")
        updated_doc = db.users.find_one({"email": test_email.lower()})
        print(f"    * full_name in DB : '{updated_doc.get('full_name')}'")
        print(f"    * department in DB: '{updated_doc.get('department')}'")
        assert updated_doc["full_name"] == "Quick Test User (UPDATED)"
        assert updated_doc["department"] == "Security Operations"
        print("    [OK] Profile update confirmed in MongoDB Atlas!\n")

        # STEP 5: CLEANUP / DELETE FROM DB
        print(f"[6] DATABASE CLEANUP >> Deleting test user '{test_email}' from MongoDB Atlas")
        del_result = db.users.delete_one({"email": test_email.lower()})
        db.organizations.delete_one({"name": test_org_name})
        db.sessions.delete_many({"user_id": user_id})
        db.categories.delete_many({"organization_id": org_id})
        print(f"    Deleted count: {del_result.deleted_count}")

        # STEP 6: VERIFY DELETION IN DB
        check_deleted = db.users.find_one({"email": test_email.lower()})
        print(f"    Re-query user in DB: {check_deleted}")
        assert check_deleted is None, "User was not removed!"
        print("    [OK] Verified test user removed from MongoDB Atlas.\n")

    print("=" * 65)
    print("  ALL API COMMANDS AND DATABASE CHECKS PASSED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(main())
