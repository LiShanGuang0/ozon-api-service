"""Compatibility router for the older ``app.routes.ozon`` import path.

The canonical HTTP layer now lives in ``app.api.routes`` and the business
logic lives in ``app.services``. Keeping this module thin prevents the old
single-file route implementation from drifting away from the current API.
"""

from fastapi import APIRouter

from app.api.routes import archive, categories, products, proxy, stocks, tasks

router = APIRouter()
router.include_router(proxy.router, prefix="/api")
router.include_router(categories.router, prefix="/api")
router.include_router(products.router, prefix="/api")
router.include_router(archive.router, prefix="/api")
router.include_router(stocks.router, prefix="/api")
router.include_router(tasks.router, prefix="/api")
