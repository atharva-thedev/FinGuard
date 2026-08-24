from app.core.security import hash_password, verify_password
from app.utils.encryption import decrypt_secret, encrypt_secret
from app.utils.jwt import (
    decode_access,
    sign_access,
    sign_email_action,
    verify_email_action,
)
from app.utils.token_compare import safe_compare


def test_password_hashing():
    pw = "super_secret_password_123!"
    hashed = hash_password(pw)
    assert hashed != pw
    assert verify_password(pw, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_jwt_access_sign_and_decode():
    token = sign_access(user_id="user_123", organization_id="org_456", role="admin")
    payload = decode_access(token)
    assert payload["sub"] == "user_123"
    assert payload["org"] == "org_456"
    assert payload["role"] == "admin"
    assert payload["typ"] == "access"


def test_email_action_sign_and_verify():
    token = sign_email_action(approval_id="appr_789", action="approve")
    payload = verify_email_action(token)
    assert payload["sub"] == "appr_789"
    assert payload["act"] == "approve"
    assert payload["typ"] == "email_action"


def test_encryption_roundtrip():
    secret_text = "qbo_refresh_token_xyz_987654"
    encrypted = encrypt_secret(secret_text)
    assert encrypted != secret_text
    decrypted = decrypt_secret(encrypted)
    assert decrypted == secret_text


def test_safe_compare():
    assert safe_compare("token_abc", "token_abc") is True
    assert safe_compare("token_abc", "token_xyz") is False
    assert safe_compare("token_abc", "token_ab") is False
