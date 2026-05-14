from fastapi import APIRouter

from app.api.routes import app_activation, archive, categories, health, merchant, products, proxy, stocks, tasks

api_router = APIRouter(prefix="/api")
api_router.include_router(proxy.router)
api_router.include_router(categories.router)
api_router.include_router(products.router)
api_router.include_router(archive.router)
api_router.include_router(stocks.router)
api_router.include_router(tasks.router)
api_router.include_router(merchant.router)
api_router.include_router(app_activation.router)
api_router.include_router(health.router, prefix="")
