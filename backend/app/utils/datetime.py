from datetime import UTC, datetime


def utcnow() -> datetime:
    """Returns current UTC datetime as an offset-naive datetime compatible with MongoDB BSON dates."""
    return datetime.now(UTC).replace(tzinfo=None)


def ensure_naive(dt: datetime | None) -> datetime | None:
    """Ensures datetime is offset-naive UTC."""
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.astimezone(UTC).replace(tzinfo=None)
    return dt
