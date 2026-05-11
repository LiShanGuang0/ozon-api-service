from typing import Annotated

from fastapi import APIRouter, Depends, Header, Query

from app.schemas.merchant import (
    MerchantBootstrapRequest,
    MerchantBootstrapResponse,
    MerchantDashboardResponse,
    MerchantProfileResponse,
    MerchantTaskDetailResponse,
    MerchantTaskEventsResponse,
    PageResponse,
)
from app.core.security import OzonCredentials
from app.services.merchant_console import MerchantConsoleService
from app.schemas.translation import TranslateRequest, TranslateResponse
from app.services.translation import TranslationService

router = APIRouter(prefix="/merchant", tags=["merchant-console"])


def get_merchant_client_id(
    x_merchant_client_id: Annotated[str | None, Header(alias="X-Merchant-Client-Id")] = None,
    client_id: Annotated[str | None, Header(alias="Client-Id")] = None,
) -> str:
    value = x_merchant_client_id or client_id
    if not value:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required header: X-Merchant-Client-Id",
        )
    return value


@router.post(
    "/bootstrap",
    response_model=MerchantBootstrapResponse,
    summary="商户端凭证校验并初始化",
    description="H5 首次进入时提交 Client-Id 和 Api-Key。先查本地商户资料；不存在时调用 Ozon 接口初始化商户资料。",
)
async def merchant_bootstrap(payload: MerchantBootstrapRequest) -> MerchantBootstrapResponse:
    credentials = OzonCredentials(client_id=payload.client_id, api_key=payload.api_key)
    return MerchantBootstrapResponse.model_validate(
        await MerchantConsoleService().bootstrap(credentials=credentials)
    )


@router.get(
    "/profile",
    response_model=MerchantProfileResponse,
    summary="商户端店铺信息",
    description="查询当前商户 H5 展示所需的店铺资料。读取 X-Merchant-Client-Id 或 Client-Id Header。",
)
def merchant_profile(
    client_id: str = Depends(get_merchant_client_id),
) -> MerchantProfileResponse:
    return MerchantProfileResponse.model_validate(MerchantConsoleService().profile(client_id=client_id))


@router.get(
    "/dashboard",
    response_model=MerchantDashboardResponse,
    summary="商户端工作台统计",
    description="查询当前商户今日推送、成功、失败、处理中数量，以及最近推送流水。",
)
def merchant_dashboard(
    client_id: str = Depends(get_merchant_client_id),
) -> MerchantDashboardResponse:
    return MerchantDashboardResponse.model_validate(MerchantConsoleService().dashboard(client_id=client_id))


@router.get(
    "/products",
    response_model=PageResponse,
    summary="商户端商品列表",
    description="按当前商户 client_id 查询已推送商品列表，可按状态和关键字过滤。",
)
def merchant_products(
    client_id: str = Depends(get_merchant_client_id),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    keyword: str | None = Query(default=None),
    status: str | None = Query(default=None),
) -> PageResponse:
    return PageResponse.model_validate(
        MerchantConsoleService().product_page(
            client_id=client_id,
            page=page,
            size=size,
            keyword=keyword,
            status=status,
        )
    )


@router.get(
    "/push-tasks",
    response_model=PageResponse,
    summary="商户端推送任务列表",
    description="查询当前商户的 Ozon 商品导入任务列表。",
)
def merchant_push_tasks(
    client_id: str = Depends(get_merchant_client_id),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    status: str | None = Query(default=None),
) -> PageResponse:
    return PageResponse.model_validate(
        MerchantConsoleService().task_page(
            client_id=client_id,
            page=page,
            size=size,
            status=status,
        )
    )


@router.get(
    "/push-tasks/{task_id}",
    response_model=MerchantTaskDetailResponse,
    summary="商户端推送任务详情",
    description="查询某个 Ozon 商品导入任务及其单商品结果。",
)
def merchant_push_task_detail(
    task_id: int,
    client_id: str = Depends(get_merchant_client_id),
) -> MerchantTaskDetailResponse:
    return MerchantTaskDetailResponse.model_validate(
        MerchantConsoleService().task_detail(client_id=client_id, task_id=task_id)
    )


@router.get(
    "/task-events",
    response_model=MerchantTaskEventsResponse,
    summary="商户端滚动推送流水",
    description="查询当前商户最新推送流水。流水文案不包含商户/店铺名。",
)
def merchant_task_events(
    client_id: str = Depends(get_merchant_client_id),
    limit: int = Query(default=30, ge=1, le=100),
    before_id: int | None = Query(default=None, ge=1),
    status: str | None = Query(default=None),
    event_type: str | None = Query(default=None),
) -> MerchantTaskEventsResponse:
    return MerchantTaskEventsResponse.model_validate(
        MerchantConsoleService().task_events(
            client_id=client_id,
            limit=limit,
            before_id=before_id,
            status=status,
            event_type=event_type,
        )
    )


@router.post(
    "/translate",
    response_model=TranslateResponse,
    summary="商户端动态文案翻译",
    description="翻译商品名称、Ozon 错误信息等动态文本，供 H5 多语言切换使用。",
)
async def merchant_translate(payload: TranslateRequest) -> TranslateResponse:
    return TranslateResponse.model_validate(
        await TranslationService().translate_many(
            texts=payload.texts,
            target_language=payload.target_language,
            source_language=payload.source_language,
        )
    )
