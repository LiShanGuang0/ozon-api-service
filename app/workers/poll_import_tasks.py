import asyncio
import logging

from app.core.security import OzonCredentials
from app.db.mysql import fetch_all
from app.services.credential_store import CredentialStore
from app.services.product_import import ProductImportService

logger = logging.getLogger(__name__)


async def poll_once(limit: int = 50, min_age_seconds: int = 300) -> None:
    rows = fetch_all(
        """
        SELECT client_id, task_id, credential_ref
        FROM ozon_import_tasks
        WHERE status = 'pending'
          AND submitted_at <= DATE_SUB(NOW(), INTERVAL %s SECOND)
        ORDER BY COALESCE(last_polled_at, submitted_at), id
        LIMIT %s
        """,
        (max(min_age_seconds, 0), limit),
    )
    store = CredentialStore()
    service = ProductImportService()
    for row in rows:
        credentials = store.load(row["credential_ref"]) if row.get("credential_ref") else None
        if credentials is None:
            logger.warning("Skip task %s: credential is missing or expired", row["task_id"])
            continue
        await service.poll_import_task(task_id=int(row["task_id"]), credentials=credentials)


def main() -> None:
    asyncio.run(poll_once())


if __name__ == "__main__":
    main()
