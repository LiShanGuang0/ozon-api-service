from typing import Any

from fastapi import APIRouter, Depends, Path, Request

from app.api.deps import OzonCredentials, get_ozon_credentials
from app.services.ozon_forwarder import OzonForwarder

router = APIRouter(prefix="/ozon", tags=["ozon-proxy"])


@router.post(
    "/proxy/{endpoint:path}",
    summary="通用 Ozon API 转发",
    description="把请求体原样转发到指定 Ozon endpoint，并自动补充 Client-Id 和 Api-Key Header，同时记录调用日志。",
)
async def proxy_post(
    request: Request,
    endpoint: str = Path(..., description="Ozon API path, for example v1/description-category/tree"),
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> dict[str, Any]:
    payload = await request.json()
    return await OzonForwarder().post(endpoint, payload, credentials, request.headers.get("X-Request-Id"))
