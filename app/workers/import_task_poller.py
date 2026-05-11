import asyncio
import logging

from app.core.config import get_settings
from app.workers.poll_import_tasks import poll_once

logger = logging.getLogger(__name__)


class ImportTaskPoller:
    def __init__(self) -> None:
        self._task: asyncio.Task[None] | None = None
        self._stop_event: asyncio.Event | None = None

    def start(self) -> None:
        if self._task is not None and not self._task.done():
            return

        self._stop_event = asyncio.Event()
        self._task = asyncio.create_task(self._run(), name="import-task-poller")
        logger.info("Import task poller started")

    async def stop(self) -> None:
        if self._task is None:
            return

        if self._stop_event is not None:
            self._stop_event.set()

        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        finally:
            self._task = None
            self._stop_event = None
            logger.info("Import task poller stopped")

    async def _run(self) -> None:
        settings = get_settings()
        interval_seconds = max(settings.import_task_poller_interval_seconds, 1)
        batch_size = max(settings.import_task_poller_batch_size, 1)
        min_age_seconds = max(settings.import_task_poller_min_age_seconds, 0)

        while self._stop_event is not None and not self._stop_event.is_set():
            try:
                await poll_once(limit=batch_size, min_age_seconds=min_age_seconds)
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Import task poller failed")

            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=interval_seconds)
            except asyncio.TimeoutError:
                continue


import_task_poller = ImportTaskPoller()
