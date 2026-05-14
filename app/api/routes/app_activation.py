from typing import Annotated

import hmac
from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.core.config import get_settings
from app.core.exceptions import ServiceError
from app.schemas.app_activation import (
    AppActivationBindRequest,
    AppActivationBindResponse,
    AppActivationCheckRequest,
    AppActivationCheckResponse,
    AppActivationCodeCreateRequest,
    AppActivationCodeCreateResponse,
    AppActivationListResponse,
)
from app.services.app_activation import AppActivationService

router = APIRouter(prefix="/app-activations", tags=["app-activations"])


def require_admin_token(
    x_admin_token: Annotated[str | None, Header(alias="X-Admin-Token")] = None,
) -> None:
    expected = get_settings().app_activation_admin_token
    if not expected:
        raise ServiceError("APP_ACTIVATION_ADMIN_TOKEN is not configured", status.HTTP_503_SERVICE_UNAVAILABLE)
    if not x_admin_token or not hmac.compare_digest(x_admin_token, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")


@router.post(
    "/codes",
    response_model=AppActivationCodeCreateResponse,
    summary="生成 App 设备激活码",
    description="管理员为指定设备、Client-Id 和 Api-Key 生成激活码；Api-Key 仅保存 SHA-256 指纹。",
    dependencies=[Depends(require_admin_token)],
)
async def create_activation_code(payload: AppActivationCodeCreateRequest) -> AppActivationCodeCreateResponse:
    return AppActivationCodeCreateResponse.model_validate(await AppActivationService().create_code(payload=payload))


@router.get(
    "/codes",
    response_model=AppActivationListResponse,
    summary="激活码列表",
    description="管理员查看历史激活码、设备绑定状态和有效期。",
    dependencies=[Depends(require_admin_token)],
)
def list_activation_codes() -> AppActivationListResponse:
    return AppActivationListResponse.model_validate(AppActivationService().list_codes())


@router.post(
    "/check",
    response_model=AppActivationCheckResponse,
    summary="检查 App 设备绑定状态",
    description="App 启动时根据 device_id 查询是否已绑定且未过期。",
)
def check_activation(payload: AppActivationCheckRequest) -> AppActivationCheckResponse:
    return AppActivationCheckResponse.model_validate(AppActivationService().check(payload=payload))


@router.post(
    "/bind",
    response_model=AppActivationBindResponse,
    summary="绑定 App 设备激活码",
    description="App 首次激活时提交设备标识、Client-Id、Api-Key 和激活码，校验通过后绑定设备。",
)
async def bind_activation(payload: AppActivationBindRequest) -> AppActivationBindResponse:
    return AppActivationBindResponse.model_validate(await AppActivationService().bind(payload=payload))
