from fastapi import APIRouter, Depends

from app.api.deps import OzonCredentials, get_ozon_credentials
from app.schemas.archive import ProductArchiveRequest, ProductArchiveResponse
from app.schemas.unarchive import ProductUnarchiveRequest, ProductUnarchiveResponse
from app.services.product_archive import ProductArchiveService
from app.services.product_unarchive import ProductUnarchiveService

router = APIRouter(prefix="/ozon", tags=["ozon-product-archive"])


@router.post(
    "/products/archive",
    response_model=ProductArchiveResponse,
    summary="归档商品",
    description=(
        "整合归档流程：对外只接收 offer_id，先调用 Ozon /v3/product/info/list 查询商品并转换 product_id，"
        "过滤已归档商品后调用 /v1/product/archive，最后再次查询确认 is_archived=true。"
    ),
)
async def archive_products(
    payload: ProductArchiveRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> ProductArchiveResponse:
    data = await ProductArchiveService().archive_products(payload=payload.model_dump(), credentials=credentials)
    return ProductArchiveResponse.model_validate(data)


@router.post(
    "/products/unarchive",
    response_model=ProductUnarchiveResponse,
    summary="从归档还原商品",
    description=(
        "整合从归档还原流程：对外只接收 offer_id，先调用 Ozon /v3/product/info/list 查询商品并转换 product_id，"
        "过滤未归档商品后调用 /v1/product/unarchive，最后再次查询确认 is_archived=false。"
    ),
)
async def unarchive_products(
    payload: ProductUnarchiveRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> ProductUnarchiveResponse:
    data = await ProductUnarchiveService().unarchive_products(payload=payload.model_dump(), credentials=credentials)
    return ProductUnarchiveResponse.model_validate(data)
