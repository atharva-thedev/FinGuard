import hmac


def safe_compare(a: str, b: str) -> bool:
    if a is None or b is None:
        return False
    return hmac.compare_digest(a, b)
