import logging
from typing import Any

from app.repositories.merchant import TaskEventRepository

logger = logging.getLogger(__name__)


class BusinessEventLogger:
    def __init__(self, events: TaskEventRepository | None = None) -> None:
        self.events = events or TaskEventRepository()

    def emit(
        self,
        *,
        client_id: str,
        event_type: str,
        status: str,
        message: str,
        ref_type: str | None = None,
        ref_id: int | None = None,
        request_id: str | None = None,
        offer_id: str | None = None,
        product_id: int | None = None,
        sku: int | None = None,
        error_message: str | None = None,
        payload: Any = None,
    ) -> None:
        try:
            self.events.insert(
                client_id=client_id,
                event_type=event_type,
                status=status,
                message=message,
                ref_type=ref_type,
                ref_id=ref_id,
                request_id=request_id,
                offer_id=offer_id,
                product_id=product_id,
                sku=sku,
                error_message=error_message,
                payload=payload,
            )
        except Exception as exc:
            logger.warning("Failed to write business event: %s", exc)
