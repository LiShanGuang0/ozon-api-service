from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import OzonCredentials, get_ozon_credentials
from app.schemas.categories import (
    AttributeValuesRequest,
    AttributeValuesSearchRequest,
    CategoryAttributesRequest,
    CategoryTreeRequest,
)
from app.services.categories import CategoryService

router = APIRouter(prefix="/ozon/categories", tags=["ozon-categories"])


@router.post(
    "/tree",
    summary="查询 Ozon 类目树",
    description="转发 Ozon /v1/description-category/tree，用于获取 description_category_id 和 type_id。创建商品前通常需要先调用。",
)
async def category_tree(
    payload: CategoryTreeRequest | None = None,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> dict[str, Any]:
    return await CategoryService().tree(payload=payload.model_dump() if payload else None, credentials=credentials)


@router.post(
    "/attributes",
    summary="查询类目特征列表",
    description="转发 Ozon /v1/description-category/attribute，用于获取指定类目和类型下的属性、必填属性、字典属性等。",
)
async def category_attributes(
    payload: CategoryAttributesRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> dict[str, Any]:
    return await CategoryService().attributes(payload=payload.model_dump(), credentials=credentials)


@router.post(
    "/attribute-values",
    summary="查询属性字典值",
    description="转发 Ozon /v1/description-category/attribute/values。当属性 dictionary_id 大于 0 时，用它获取 dictionary_value_id。",
)
async def attribute_values(
    payload: AttributeValuesRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> dict[str, Any]:
    return await CategoryService().values(payload=payload.model_dump(), credentials=credentials)


@router.post(
    "/attribute-values/search",
    summary="搜索属性字典值",
    description="转发 Ozon /v1/description-category/attribute/values/search。适合字典值很多时按关键词搜索。",
)
async def attribute_values_search(
    payload: AttributeValuesSearchRequest,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> dict[str, Any]:
    return await CategoryService().search_values(payload=payload.model_dump(), credentials=credentials)
