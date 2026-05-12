from typing import Any

from pydantic import ConfigDict, Field, model_validator

from app.schemas.common import SchemaModel


class ProductAttributeValue(SchemaModel):
    dictionary_value_id: int = Field(
        default=0,
        description="属性字典值 ID。来自属性值指南/搜索接口；无字典属性通常填 0。",
        examples=[5060050],
    )
    value: str | int | float | bool | None = Field(
        default=None,
        description="属性值。字典属性填展示值；非字典属性填自定义文本、数字或布尔值。",
        examples=["Samsung"],
    )


class ProductAttribute(SchemaModel):
    complex_id: int = Field(
        default=0,
        description="复合属性 ID。普通属性填 0；嵌套/复合属性按 Ozon 类目属性返回值填写。",
        examples=[0],
    )
    id: int = Field(description="Ozon 属性 ID。来自类目特征列表 result[].id。", examples=[85])
    values: list[ProductAttributeValue] = Field(default_factory=list, description="属性值数组。多值属性可传多个元素。")


class ProductImportItem(SchemaModel):
    @model_validator(mode="before")
    @classmethod
    def reject_platform_identifiers(cls, data: Any) -> Any:
        if isinstance(data, dict):
            forbidden = {"product_id", "sku"} & set(data)
            if forbidden:
                raise ValueError("请求参数只支持 offer_id，不允许传 product_id 或 sku")
        return data

    offer_id: str = Field(
        max_length=50,
        description="卖家系统商品货号。创建后用于后续更新，同一个 Client-Id 下应唯一。",
        examples=["LOCAL-SKU-001"],
    )
    name: str | None = Field(default=None, max_length=500, description="商品名称，最多 500 字符。", examples=["一套X3NFC保护膜"])
    description_category_id: int | None = Field(
        default=None,
        description="Ozon 类目 ID，来自类目树 description_category_id。",
        examples=[17028922],
    )
    type_id: int | None = Field(default=None, description="Ozon 商品类型 ID，来自类目树 type_id。", examples=[91565])
    barcode: str | None = Field(default=None, description="商品条码。", examples=["112772873170"])
    currency_code: str | None = Field(
        default=None,
        description="币种，必须与 Ozon 个人中心设置匹配。常用：RUB、CNY、USD。",
        examples=["RUB"],
    )
    price: str | None = Field(default=None, description="当前售价，字符串格式。", examples=["1000"])
    old_price: str | None = Field(default=None, description="划线价/折扣前价格，字符串格式。", examples=["1100"])
    vat: str | None = Field(default=None, description="增值税税率，例如 0、0.05、0.07、0.1、0.2。", examples=["0.1"])
    depth: int | None = Field(default=None, description="包装深度/厚度。不要传 0。", examples=[10])
    width: int | None = Field(default=None, description="包装宽度。不要传 0。", examples=[150])
    height: int | None = Field(default=None, description="包装高度。不要传 0。", examples=[250])
    dimension_unit: str | None = Field(default=None, description="尺寸单位：mm、cm、in。", examples=["mm"])
    weight: int | None = Field(default=None, description="含包装重量。不要传 0。", examples=[100])
    weight_unit: str | None = Field(default=None, description="重量单位：g、kg、lb。", examples=["g"])
    images: list[str] = Field(
        default_factory=list,
        description="普通商品图片 URL 数组，公共可访问 JPG/PNG。最多 15 张；不传 primary_image 时第一张为主图。",
        examples=[["https://example.com/image-1.jpg"]],
    )
    primary_image: str | None = Field(default=None, description="主图 URL。传此字段时 images 最多 14 张。", examples=["https://example.com/image-1.jpg"])
    images360: list[str] = Field(default_factory=list, description="360 图片 URL 数组，最多 70 张。")
    color_image: str | None = Field(default=None, description="营销色彩图 URL，通常为 JPG。")
    pdf_list: list[dict[str, Any]] = Field(default_factory=list, description="PDF 文件列表。")
    attributes: list[ProductAttribute] = Field(default_factory=list, description="商品普通属性。必填属性来自类目特征接口 is_required=true。")
    complex_attributes: list[dict[str, Any]] = Field(default_factory=list, description="商品复合/嵌套属性，例如视频、视频封面等。")
    warehouse_id: int | None = Field(
        default=None,
        gt=0,
        description="导入成功后要设置库存的 Ozon 仓库 ID。该字段仅供本服务后处理使用，不会转发给 /v3/product/import。",
        examples=[1020000000000],
    )
    stock: int | None = Field(
        default=None,
        ge=0,
        description="导入成功后要设置的可售库存。该字段仅供本服务后处理使用，不会转发给 /v3/product/import。",
        examples=[10],
    )


class ProductImportRequest(SchemaModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    items: list[ProductImportItem] = Field(
        default_factory=list,
        max_length=100,
        description="要创建或更新的商品数组。Ozon 一次最多提交 100 个商品。",
    )


class ProductImportResponse(SchemaModel):
    limit: dict[str, Any] = Field(default_factory=dict, description="Ozon /v4/product/info/limit 原始响应。")
    import_result: dict[str, Any] = Field(default_factory=dict, description="Ozon /v3/product/import 原始响应。")
    task_id: int | None = Field(default=None, description="Ozon 异步任务 ID，用于查询创建/更新结果。", examples=[172549793])
    credential_ref_saved: bool = Field(default=False, description="是否已把本次 Api-Key 短期写入 Redis，用于后续后台轮询。")


class ProductImportTaskResponse(SchemaModel):
    task_id: int = Field(description="Ozon 异步任务 ID。", examples=[172549793])
    status: str = Field(description="任务状态：pending/imported/failed/skipped/partial。", examples=["imported"])
    data: dict[str, Any] = Field(default_factory=dict, description="Ozon /v1/product/import/info 原始响应。")


class ProductAttributesUpdateRequest(SchemaModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    items: list[dict[str, Any]] = Field(
        default_factory=list,
        description="需要更新属性的商品数组。每个元素通常包含 offer_id 和 attributes。",
        examples=[
            [
                {
                    "offer_id": "LOCAL-SKU-001",
                    "attributes": [
                        {"complex_id": 0, "id": 9048, "values": [{"dictionary_value_id": 0, "value": "新的属性值"}]}
                    ],
                }
            ]
        ],
    )

    @model_validator(mode="after")
    def validate_items(self) -> "ProductAttributesUpdateRequest":
        for item in self.items:
            forbidden = {"product_id", "sku"} & set(item)
            if forbidden:
                raise ValueError("items 中只支持 offer_id，不允许传 product_id 或 sku")
            if not item.get("offer_id"):
                raise ValueError("items[].offer_id 是必填项")
        return self


class ProductAttributesUpdateResponse(SchemaModel):
    task_id: int | None = Field(default=None, description="Ozon 异步任务 ID。", examples=[172549793])
    data: dict[str, Any] = Field(default_factory=dict, description="Ozon /v1/product/attributes/update 原始响应。")


class ProductPicturesImportRequest(SchemaModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    offer_id: str = Field(description="卖家系统商品货号。", examples=["LOCAL-SKU-001"])
    images: list[str] = Field(
        default_factory=list,
        description="最终要保留的普通图片 URL 列表。注意：该接口会用本次列表替换原图片列表。",
        examples=[["https://example.com/image-1.jpg", "https://example.com/image-2.jpg"]],
    )
    images360: list[str] = Field(default_factory=list, description="最终要保留的 360 图片 URL 列表。")
    color_image: str | None = Field(default=None, description="营销色彩图 URL。")


class ProductInfoListRequest(SchemaModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    offer_id: list[str] = Field(default_factory=list, description="按卖家货号查询。三类标识总数最多 1000。", examples=[["LOCAL-SKU-001"]])

    @model_validator(mode="after")
    def validate_offer_ids(self) -> "ProductInfoListRequest":
        if not self.offer_id:
            raise ValueError("offer_id 至少传一个")
        if len(self.offer_id) > 1000:
            raise ValueError("offer_id 总数不能超过 1000")
        return self


class ProductInfoAttributesRequest(SchemaModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    offer_id: str = Field(
        min_length=1,
        max_length=50,
        description="卖家系统商品货号。服务会转为 Ozon filter.offer_id 查询商品已填写属性。",
        examples=["LOCAL-SKU-001"],
    )

    @model_validator(mode="after")
    def validate_offer_id(self) -> "ProductInfoAttributesRequest":
        self.offer_id = self.offer_id.strip()
        if not self.offer_id:
            raise ValueError("offer_id 是必填项")
        return self
