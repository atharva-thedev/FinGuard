from celery import Celery

from app.config.env import settings

celery_app = Celery(
    "finguard_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(name="app.workers.tasks.process_invoice")
def process_invoice_task(invoice_id: str, actor_id: str):
    import asyncio

    from app.config.db import connect_db, disconnect_db
    from app.modules.invoices.service import run_pipeline

    async def _runner():
        await connect_db()
        try:
            await run_pipeline(invoice_id, actor_id)
        finally:
            await disconnect_db()

    asyncio.run(_runner())
