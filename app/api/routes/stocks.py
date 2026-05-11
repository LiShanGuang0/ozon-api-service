from fastapi import APIRouter, Depends

from app.api.deps import OzonCredentials, get_ozon_credentials
from app.schemas.stocks import (
    ProductStockUpdateRequest,
    ProductStockUpdateResponse,
    WarehouseListRequest,
)
from app.services.product_stocks import ProductStockService

router = APIRouter(prefix="/ozon", tags=["ozon-product-stocks"])


@router.post(
    "/warehouses/list",
    summary="查询仓库列表",
    description="转发 Ozon /v2/warehouse/list，查询当前 Client-Id 下的仓库列表，并缓存到本地 ozon_warehouses。",
)
async def list_warehouses(
    payload: WarehouseListRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> dict:
    return await ProductStockService().list_warehouses(payload=payload.model_dump(), credentials=credentials)


@router.post(
    "/products/stocks/update",
    response_model=ProductStockUpdateResponse,
    summary="设置商品上架数量",
    description=(
        "整合库存设置流程：对外只接收 offer_id，查询仓库、查询商品信息、调用 Ozon /v2/products/stocks，"
        "并可选通过 /v4/product/info/stocks 做商品级确认；不再调用 /v1/product/info/stocks-by-warehouse/fbs。"
    ),
)
async def update_product_stocks(
    payload: ProductStockUpdateRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> ProductStockUpdateResponse:
    data = await ProductStockService().update_stocks(payload=payload.model_dump(), credentials=credentials)
    return ProductStockUpdateResponse.model_validate(data)
