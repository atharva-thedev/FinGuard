import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.config.env import settings


def encrypt_secret(plaintext: str) -> str:
    key = bytes.fromhex(settings.encryption_key)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, plaintext.encode("utf-8"), None)
    return (nonce + ct).hex()


def decrypt_secret(blob_hex: str) -> str:
    key = bytes.fromhex(settings.encryption_key)
    raw = bytes.fromhex(blob_hex)
    nonce, ct = raw[:12], raw[12:]
    aes = AESGCM(key)
    return aes.decrypt(nonce, ct, None).decode("utf-8")
