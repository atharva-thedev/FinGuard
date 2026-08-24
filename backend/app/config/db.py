from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.env import settings
from app.models.documents import DOCUMENT_MODELS

_client: AsyncIOMotorClient | None = None


async def connect_db() -> None:
    global _client
    _client = AsyncIOMotorClient(settings.mongodb_uri)
    db = _client[settings.mongodb_db]
    await init_beanie(database=db, document_models=DOCUMENT_MODELS)


async def ping_db() -> bool:
    if _client is None:
        return False
    try:
        await _client.admin.command("ping")
        return True
    except Exception:
        return False


async def disconnect_db() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None
