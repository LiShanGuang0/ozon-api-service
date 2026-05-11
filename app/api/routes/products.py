from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import OzonCredentials, get_ozon_credentials
from app.schemas.products import (
    ProductAttributesUpdateRequest,
    ProductAttributesUpdateResponse,
    ProductImportRequest,
    ProductImportResponse,
    ProductInfoAttributesRequest,
    ProductInfoListRequest,
    ProductPicturesImportRequest,
)
from app.services.product_import import ProductImportService
from app.services.products import ProductQueryService

router = APIRouter(prefix="/ozon", tags=["ozon-products"])


@router.post(
    "/product/info/limit",
    summary="查询商品创建/更新额度",
    description="转发 Ozon /v4/product/info/limit。创建或更新商品前建议调用，避免触发额度限制。",
)
async def product_info_limit(
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> dict[str, Any]:
    return await ProductQueryService().info_limit(credentials=credentials)


@router.post(
    "/products/import",
    response_model=ProductImportResponse,
    summary="创建或更新商品",
    description=(
        "整合调用：先查询 /v4/product/info/limit，再提交 /v3/product/import。"
        "成功后保存 task_id、本地商品快照，并将 Api-Key 短期写入 Redis 供后续轮询。"
    ),
)
async def product_import(
    body: ProductImportRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> ProductImportResponse:
    return await ProductImportService().import_products(payload=body.model_dump(), credentials=credentials)


@router.post(
    "/products/attributes/update",
    response_model=ProductAttributesUpdateResponse,
    summary="仅更新商品属性",
    description="转发 Ozon /v1/product/attributes/update。适合只修改 attributes 的场景，返回 task_id 后仍需查询任务状态。",
)
async def product_attributes_update(
    payload: ProductAttributesUpdateRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> ProductAttributesUpdateResponse:
    return await ProductImportService().update_attributes(payload=payload.model_dump(), credentials=credentials)


@router.post(
    "/products/pictures/import",
    summary="上传或更新商品图片",
    description=(
        "按 offer_id 上传或更新商品图片。服务内部会先解析 Ozon product_id，再转发 /v1/product/pictures/import。"
        "注意：该接口会以本次传入的图片列表作为最终图片列表，不是只追加新图片。"
    ),
)
async def product_pictures_import(
    payload: ProductPicturesImportRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> dict[str, Any]:
    return await ProductQueryService().pictures_import(payload=payload.model_dump(), credentials=credentials)


@router.post(
    "/products/info/list",
    summary="根据标识符查询商品信息",
    description="转发 Ozon /v3/product/info/list。对外仅支持按 offer_id 查询商品基础信息、状态、图片等。",
)
async def product_info_list(
    payload: ProductInfoListRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> dict[str, Any]:
    return await ProductQueryService().info_list(payload=payload.model_dump(), credentials=credentials)


@router.post(
    "/products/info/attributes",
    summary="查询商品已填写属性",
    description="转发 Ozon /v3/products/info/attributes。更新商品前可用它获取已有属性、尺寸、重量、图片等信息。",
)
async def product_info_attributes(
    payload: ProductInfoAttributesRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> dict[str, Any]:
    return await ProductQueryService().info_attributes(payload=payload.model_dump(), credentials=credentials)
