from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import Field

from app.schemas.common import SchemaModel


class PageResponse(SchemaModel):
    total: int = Field(description="总数")
    page: int = Field(description="当前页码")
    size: int = Field(description="每页数量")
    items: list[dict[str, Any]] = Field(default_factory=list, description="数据列表")


class MerchantProfileResponse(SchemaModel):
    merchant_id: str | None = Field(default=None, description="运营平台商户 ID")
    client_id: str = Field(description="Ozon Client-Id")
    shop_name: str | None = Field(default=None, description="店铺名称")
    display_name: str | None = Field(default=None, description="展示名称")
    logo_url: str | None = Field(default=None, description="店铺 Logo")
    status: str = Field(default="active", description="商户状态")
    currency_code: str | None = Field(default=None, description="币种")
    default_warehouse_id: int | None = Field(default=None, description="默认仓库 ID")
    contact_name: str | None = Field(default=None, description="联系人")
    contact_phone: str | None = Field(default=None, description="联系电话")
    contact_email: str | None = Field(default=None, description="联系邮箱")
    last_connected_at: datetime | None = Field(default=None, description="最近连接 Ozon 时间")
    last_error: str | None = Field(default=None, description="最近错误")


class MerchantBootstrapRequest(SchemaModel):
    client_id: str = Field(min_length=1, description="Ozon Client-Id")
    api_key: str = Field(min_length=1, description="Ozon Api-Key")


class MerchantBootstrapResponse(SchemaModel):
    profile: MerchantProfileResponse
    initialized_from_ozon: bool = Field(description="是否通过 Ozon 接口初始化了商户资料")
    credential_valid: bool = Field(default=True, description="凭证是否校验通过")


class DashboardMetric(SchemaModel):
    key: str
    label: str
    value: int


class MerchantDashboardResponse(SchemaModel):
    profile: MerchantProfileResponse
    metrics: list[DashboardMetric]
    task_status_counts: dict[str, int] = Field(default_factory=dict)
    product_status_counts: dict[str, int] = Field(default_factory=dict)
    today_event_count: int = 0
    recent_events: list[dict[str, Any]] = Field(default_factory=list)


class MerchantProductItem(SchemaModel):
    id: int
    offer_id: str
    local_sku: str | None = None
    name: str | None = None
    product_id: int | None = None
    sku: int | None = None
    currency_code: str | None = None
    price: Decimal | None = None
    old_price: Decimal | None = None
    warehouse_id: int | None = None
    warehouse_name: str | None = None
    stock: int | None = None
    cover_image_url: str | None = None
    sync_status: str
    sync_status_label: str
    ozon_status: str | None = None
    last_task_id: int | None = None
    last_error: Any = None
    updated_at: datetime | None = None
    created_at: datetime | None = None


class MerchantTaskItem(SchemaModel):
    id: int
    task_id: int
    action_type: str
    status: str
    status_label: str
    workflow_status: str | None = None
    workflow_status_label: str | None = None
    total_count: int = 0
    success_count: int = 0
    failed_count: int = 0
    submitted_at: datetime | None = None
    last_polled_at: datetime | None = None
    finished_at: datetime | None = None


class MerchantTaskDetailResponse(SchemaModel):
    task: dict[str, Any]
    items: list[dict[str, Any]] = Field(default_factory=list)


class MerchantTaskEventItem(SchemaModel):
    id: int
    event_type: str
    status: str
    status_label: str
    offer_id: str | None = None
    product_id: int | None = None
    sku: int | None = None
    ozon_task_id: int | None = None
    request_id: str | None = None
    message: str
    error_message: str | None = None
    payload: Any = None
    created_at: datetime


class MerchantTaskEventsResponse(SchemaModel):
    items: list[MerchantTaskEventItem] = Field(default_factory=list)
    next_before_id: int | None = Field(default=None, description="下一页 before_id")
    today_count: int = Field(default=0, description="今日流水数量")
