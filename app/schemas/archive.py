from typing import Any, Literal

from pydantic import ConfigDict, Field, model_validator

from app.schemas.common import SchemaModel


class ProductArchiveRequest(SchemaModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    offer_id: list[str] = Field(
        default_factory=list,
        description="卖家系统商品货号。服务会先调用 /v3/product/info/list 转换为 Ozon product_id。",
        examples=[["LOCAL-SKU-001", "LOCAL-SKU-002"]],
    )
    confirm: bool = Field(
        default=True,
        description="是否在归档后再次查询商品信息，并用 is_archived=true 确认归档结果。",
    )

    @model_validator(mode="after")
    def validate_identifiers(self) -> "ProductArchiveRequest":
        total = len(self.offer_id)
        if total == 0:
            raise ValueError("offer_id 至少传一个")
        if total > 1000:
            raise ValueError("offer_id 总数不能超过 1000")
        return self


class ProductArchiveItemResult(SchemaModel):
    offer_id: str | None = Field(default=None, description="卖家系统商品货号")
    product_id: int | None = Field(default=None, description="Ozon 商品 ID")
    sku: int | None = Field(default=None, description="Ozon SKU")
    before_is_archived: bool | None = Field(default=None, description="归档前是否已手动归档")
    before_is_autoarchived: bool | None = Field(default=None, description="归档前是否已自动归档")
    after_is_archived: bool | None = Field(default=None, description="归档后是否已手动归档")
    after_is_autoarchived: bool | None = Field(default=None, description="归档后是否已自动归档")
    status: Literal["success", "failed", "skipped", "not_found", "already_archived"] = Field(description="单商品处理状态")
    skip_reason: str | None = Field(default=None, description="跳过原因")
    error_message: str | None = Field(default=None, description="失败原因")


class ProductArchiveResponse(SchemaModel):
    request_id: str = Field(description="本地归档请求 ID")
    archive_task_id: int = Field(description="本地归档批次 ID")
    status: Literal["success", "partial", "failed", "skipped"] = Field(description="批次状态")
    total_count: int = Field(description="请求或解析出的商品总数")
    success_count: int = Field(description="成功数量")
    failed_count: int = Field(description="失败数量")
    skipped_count: int = Field(description="跳过数量")
    precheck: dict[str, Any] = Field(default_factory=dict, description="Ozon /v3/product/info/list 归档前查询响应")
    archive_result: dict[str, Any] = Field(default_factory=dict, description="Ozon /v1/product/archive 归档接口响应，批量超过 100 时包含 chunks")
    confirm: dict[str, Any] = Field(default_factory=dict, description="Ozon /v3/product/info/list 归档后确认响应")
    items: list[ProductArchiveItemResult] = Field(default_factory=list, description="单商品归档结果")
