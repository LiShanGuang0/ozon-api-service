from typing import Any, Literal

from pydantic import ConfigDict, Field, model_validator

from app.schemas.common import SchemaModel


class WarehouseListRequest(SchemaModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    cursor: str = Field(default="", description="分页游标。首次请求留空。")
    limit: int = Field(default=200, ge=1, le=200, description="返回数量，最大 200。")
    warehouse_ids: list[int | str] = Field(
        default_factory=list,
        max_length=200,
        description="按仓库 ID 过滤，最多 200 个。",
    )


class ProductStockUpdateItem(SchemaModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    offer_id: str = Field(
        description="卖家系统商品货号。",
        examples=["LOCAL-SKU-001"],
    )
    warehouse_id: int = Field(description="Ozon 仓库 ID，来自 /v2/warehouse/list。", examples=[22142605386000])
    stock: int = Field(ge=0, description="要设置的可售库存数量，不包含已预留库存。", examples=[10])


class ProductsStocksRequest(SchemaModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    offer_id: str = Field(
        min_length=1,
        max_length=50,
        description="卖家系统商品货号。服务会转为 Ozon stocks[].offer_id。",
        examples=["LOCAL-SKU-001"],
    )
    warehouse_id: int = Field(description="Ozon 仓库 ID，来自 /v2/warehouse/list。", examples=[22142605386000])
    stock: int = Field(ge=0, description="要设置的可售库存数量，不包含已预留库存。", examples=[10])

    @model_validator(mode="after")
    def validate_offer_id(self) -> "ProductsStocksRequest":
        self.offer_id = self.offer_id.strip()
        if not self.offer_id:
            raise ValueError("offer_id 是必填项")
        return self


class ProductStockUpdateRequest(SchemaModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    stocks: list[ProductStockUpdateItem] = Field(
        min_length=1,
        max_length=100,
        description="库存更新列表。Ozon /v2/products/stocks 单次最多 100 个商品。",
    )
    check_reserved: bool = Field(
        default=False,
        description="兼容旧参数，当前库存更新流程不再调用仓库维度预留库存查询接口。",
    )
    confirm: bool = Field(
        default=True,
        description="是否在更新后调用 /v4/product/info/stocks 做商品级库存确认。",
    )


class ProductStockUpdateItemResult(SchemaModel):
    offer_id: str | None = Field(default=None, description="卖家系统商品货号")
    product_id: int | None = Field(default=None, description="Ozon 商品 ID")
    sku: int | None = Field(default=None, description="Ozon SKU")
    warehouse_id: int = Field(description="仓库 ID")
    requested_stock: int = Field(description="本次请求设置的可售库存数量")
    present: int | None = Field(default=None, description="仓库维度当前库存；当前更新流程不再查询，通常为 null")
    reserved: int | None = Field(default=None, description="仓库维度已预留数量；当前更新流程不再查询，通常为 null")
    updated: bool = Field(default=False, description="Ozon 是否返回更新成功")
    status: Literal["success", "failed"] = Field(description="单商品处理状态")
    error_message: str | None = Field(default=None, description="失败原因")


class ProductStockUpdateResponse(SchemaModel):
    request_id: str = Field(description="本地库存更新请求 ID")
    stock_task_id: int = Field(description="本地库存更新批次 ID")
    status: Literal["success", "partial", "failed"] = Field(description="批次状态")
    total_count: int = Field(description="本次请求商品数量")
    success_count: int = Field(description="成功数量")
    failed_count: int = Field(description="失败数量")
    warehouse_result: dict[str, Any] = Field(default_factory=dict, description="Ozon /v2/warehouse/list 原始响应")
    product_result: dict[str, Any] = Field(default_factory=dict, description="Ozon /v3/product/info/list 原始响应")
    reserved_result: dict[str, Any] = Field(default_factory=dict, description="兼容旧字段；当前库存更新流程不再查询预留库存，通常为空对象")
    update_result: dict[str, Any] = Field(default_factory=dict, description="Ozon /v2/products/stocks 原始响应")
    confirm_result: dict[str, Any] = Field(default_factory=dict, description="库存确认查询原始响应")
    items: list[ProductStockUpdateItemResult] = Field(default_factory=list, description="单商品库存更新结果")
