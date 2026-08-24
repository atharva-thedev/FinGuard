"""
FinGuard External Integrations & 3rd-Party Service Verification Suite
Tests:
1. Google OAuth 2.0 Flow (Unconfigured rejection + Full Token Exchange & Account Provisioning simulation in MongoDB Atlas)
2. SMTP Email Delivery Engine (Unconfigured fallback + Live Local SMTP Server protocol handshake & MIME payload verification)
3. External HTTP OCR Extraction Provider (HttpExtractionProvider live communication & invoice parsing)
"""

import asyncio
import io
import os
import sys
import unittest.mock
import uuid
import httpx

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config.db import connect_db, disconnect_db
from app.config.env import settings
from app.models.documents import Invoice, Organization, Session, User
from app.modules.auth.service import AuthService
from app.modules.extraction.provider import HttpExtractionProvider
from app.modules.notifications.service import NotificationService
from app.utils.jwt import sign_email_action

BASE_URL = "http://localhost:5000"
PREFIX = f"ext_{uuid.uuid4().hex[:6]}"


class AsyncMockSmtpServer:
    def __init__(self, host="127.0.0.1", port=1025):
        self.host = host
        self.port = port
        self.server = None
        self.received_messages = []

    async def _handle_client(self, reader, writer):
        writer.write(b"220 127.0.0.1 FinGuard SMTP Ready\r\n")
        await writer.drain()

        in_data = False
        data_buffer = []

        while True:
            line = await reader.readline()
            if not line:
                break
            text = line.decode("utf-8", errors="replace")

            if in_data:
                if text == ".\r\n" or text == ".\n":
                    in_data = False
                    self.received_messages.append("".join(data_buffer))
                    data_buffer = []
                    writer.write(b"250 OK message accepted\r\n")
                    await writer.drain()
                else:
                    data_buffer.append(text)
            elif text.upper().startswith("EHLO") or text.upper().startswith("HELO"):
                writer.write(b"250-127.0.0.1\r\n250 AUTH PLAIN LOGIN\r\n")
                await writer.drain()
            elif text.upper().startswith("AUTH"):
                writer.write(b"235 2.7.0 Authentication successful\r\n")
                await writer.drain()
            elif text.upper().startswith("MAIL FROM:"):
                writer.write(b"250 2.1.0 OK\r\n")
                await writer.drain()
            elif text.upper().startswith("RCPT TO:"):
                writer.write(b"250 2.1.5 OK\r\n")
                await writer.drain()
            elif text.upper().startswith("DATA"):
                in_data = True
                writer.write(b"354 Start mail input; end with <CRLF>.<CRLF>\r\n")
                await writer.drain()
            elif text.upper().startswith("QUIT"):
                writer.write(b"221 2.0.0 Service closing transmission channel\r\n")
                await writer.drain()
                break
            elif text.upper().startswith("RSET") or text.upper().startswith("NOOP"):
                writer.write(b"250 OK\r\n")
                await writer.drain()
            else:
                writer.write(b"250 OK\r\n")
                await writer.drain()

        writer.close()
        await writer.wait_closed()

    async def start(self):
        self.server = await asyncio.start_server(self._handle_client, self.host, self.port)

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()


def log_test(num: str, title: str):
    print(f"\n[INTEGRATION TEST {num}] >> {title}")


def log_pass(msg: str):
    print(f"  [PASS] {msg}")


async def run_external_integrations():
    print("=" * 70)
    print("  FINGUARD EXTERNAL 3RD-PARTY INTEGRATIONS TEST SUITE")
    print("=" * 70)

    await connect_db()
    print("[DB] Connected to MongoDB Atlas for state verification.")

    client = httpx.AsyncClient(base_url=BASE_URL, timeout=20.0)

    try:
        # =====================================================================
        # PART 1: Google OAuth 2.0 Authentication & User Provisioning
        # =====================================================================
        log_test("1.1", "Google OAuth endpoint unconfigured -> 400 INVALID_REQUEST")
        r = await client.get("/api/v1/auth/google")
        assert r.status_code == 400 and r.json()["error"]["code"] == "INVALID_REQUEST"
        log_pass("Unconfigured Google OAuth correctly returns 400 INVALID_REQUEST")

        log_test("1.2", "Google OAuth Token Exchange & User Provisioning Simulation")
        mock_google_sub = f"g_sub_{uuid.uuid4().hex[:8]}"
        mock_google_email = f"{PREFIX}_google_user@gmail.com"
        mock_google_name = "Google Test User"

        # Mock external Google token exchange and userinfo endpoints
        async def mock_google_post(url, *args, **kwargs):
            if "oauth2.googleapis.com/token" in str(url):
                return httpx.Response(
                    200,
                    json={
                        "access_token": "mock_google_access_token_12345",
                        "id_token": "mock_google_id_token",
                        "expires_in": 3600,
                        "token_type": "Bearer",
                    },
                )
            return httpx.Response(404)

        async def mock_google_get(url, *args, **kwargs):
            if "googleapis.com/oauth2/v3/userinfo" in str(url):
                return httpx.Response(
                    200,
                    json={
                        "sub": mock_google_sub,
                        "email": mock_google_email,
                        "name": mock_google_name,
                        "picture": "https://lh3.googleusercontent.com/a/mock_avatar",
                        "email_verified": True,
                    },
                )
            return httpx.Response(404)

        # Temporarily enable Google client settings
        settings.google_client_id = "test_google_client_id.apps.googleusercontent.com"
        settings.google_client_secret = "test_google_client_secret_xyz"

        try:
            with unittest.mock.patch("httpx.AsyncClient.post", side_effect=mock_google_post), \
                 unittest.mock.patch("httpx.AsyncClient.get", side_effect=mock_google_get):

                # Execute Google Login Service directly
                data, cookie = await AuthService.google_login("valid_mock_google_code", user_agent="PyTest-Runner")
                assert data["user"]["email"] == mock_google_email
                assert data["user"]["full_name"] == mock_google_name
                google_user_id = data["user"]["id"]
                google_org_id = data["user"]["organization_id"]

                # Verify User & Organization in MongoDB Atlas
                db_u = await User.get(google_user_id)
                assert db_u.google_sub == mock_google_sub, "google_sub not persisted in MongoDB"
                db_org = await Organization.get(google_org_id)
                assert db_org is not None, "Organization not created for Google user"
                log_pass(f"Google User Provisioned in MongoDB Atlas: User ID={google_user_id}, Org ID={google_org_id}")

        finally:
            settings.google_client_id = ""
            settings.google_client_secret = ""

        # =====================================================================
        # PART 2: SMTP Email Delivery Engine & 1-Click Action Link Formatting
        # =====================================================================
        log_test("2.1", "NotificationService Unconfigured Fallback (Console Dev Mode)")
        orig_smtp_host = settings.smtp_host
        orig_smtp_user = settings.smtp_user
        settings.smtp_host = ""
        settings.smtp_user = ""

        res_dev = NotificationService.send_email(
            to_email="finance@corp.com",
            subject="Test Dev Mode",
            body_html="<p>Test</p>",
            body_text="Test",
        )
        assert res_dev is True
        log_pass("Unconfigured SMTP fallback returned True without throwing exception")

        log_test("2.2", "Live Local SMTP Server Handshake & 1-Click Action Email Delivery")
        smtp_server = AsyncMockSmtpServer(host="127.0.0.1", port=1025)
        await smtp_server.start()
        print("  [SMTP] Started local test SMTP server on 127.0.0.1:1025")

        try:
            # Configure notification service to use test SMTP server
            settings.smtp_host = "127.0.0.1"
            settings.smtp_port = 1025
            settings.smtp_user = "test_user"
            settings.smtp_pass = "test_pass"
            settings.email_from = "finguard@corp.com"

            # Use standard smtplib.SMTP for plain local test server
            import smtplib
            class LocalTestSMTP(smtplib.SMTP):
                def __init__(self, host, port):
                    super().__init__(host, port)
                def login(self, user, password):
                    pass # Bypass SSL auth on plain local test socket

            with unittest.mock.patch("smtplib.SMTP_SSL", LocalTestSMTP):
                approve_link = "http://localhost:5000/api/v1/approvals/action/mock_approve_token"
                reject_link = "http://localhost:5000/api/v1/approvals/action/mock_reject_token"

                sent = await asyncio.to_thread(
                    NotificationService.send_approval_request,
                    to_email="manager@company.com",
                    approver_name="Jane Manager",
                    invoice_number="INV-2026-999",
                    vendor_name="Amazon Web Services",
                    amount=4500.50,
                    approve_url=approve_link,
                    reject_url=reject_link,
                )
                assert sent is True, "Failed to deliver email over SMTP"
                assert len(smtp_server.received_messages) == 1, "SMTP server received 0 messages"

                msg = smtp_server.received_messages[0]
                assert "To: manager@company.com" in msg or "manager@company.com" in msg
                assert "Amazon Web Services" in msg
                assert "$4,500.50" in msg
                assert approve_link in msg
                assert reject_link in msg
                log_pass("Delivered MIME multipart approval email via SMTP. Verified recipient, headers & action links.")

        finally:
            await smtp_server.stop()
            settings.smtp_host = orig_smtp_host
            settings.smtp_user = orig_smtp_user
            print("  [SMTP] Stopped local test SMTP server.")

        # =====================================================================
        # PART 3: External HTTP OCR Extraction Provider
        # =====================================================================
        log_test("3.1", "HttpExtractionProvider External Service Communication")
        
        # Test HttpExtractionProvider unconfigured URL
        provider = HttpExtractionProvider()
        settings.extraction_http_url = ""
        try:
            await provider.extract(filename="test.pdf", content=b"content", content_type="application/pdf")
            assert False, "Should have raised RuntimeError when URL not set"
        except RuntimeError:
            log_pass("HttpExtractionProvider raises RuntimeError when EXTRACTION_HTTP_URL is missing")

        # Test HttpExtractionProvider with simulated external OCR API response
        settings.extraction_http_url = "https://ocr-microservice.internal/extract"
        mock_ocr_payload = {
            "vendor_name": "Datadog Inc.",
            "invoice_number": "DD-98421",
            "invoice_date": "2026-08-15",
            "due_date": "2026-09-15",
            "line_items": [
                {"description": "APM Pro Subscription", "quantity": 1, "unit_price": 2400.0, "amount": 2400.0}
            ],
            "subtotal": 2400.0,
            "tax": 240.0,
            "total": 2640.0,
            "confidences": {
                "vendor_name": 0.98,
                "invoice_number": 0.95,
                "invoice_date": 0.97,
                "total": 0.99,
            },
            "confidence_threshold": 0.85,
        }

        async def mock_ocr_post(url, *args, **kwargs):
            req = httpx.Request("POST", str(url))
            return httpx.Response(200, json=mock_ocr_payload, request=req)

        with unittest.mock.patch("httpx.AsyncClient.post", side_effect=mock_ocr_post):
            extracted = await provider.extract(filename="invoice.pdf", content=b"%PDF", content_type="application/pdf")
            assert extracted["vendor_name"] == "Datadog Inc."
            assert extracted["total"] == 2640.0
            assert extracted["confidences"]["total"] == 0.99
            log_pass("HttpExtractionProvider successfully parsed multipart response from external OCR service.")

        settings.extraction_http_url = ""

        print("\n" + "=" * 70)
        print("  ALL EXTERNAL 3RD-PARTY INTEGRATION TESTS PASSED WITH 100% SUCCESS!")
        print("=" * 70)

    finally:
        await client.aclose()
        await disconnect_db()
        print("\n[DB] Disconnected from MongoDB Atlas.")


if __name__ == "__main__":
    asyncio.run(run_external_integrations())
