from typing import Any

from typing import Literal

from pydantic import Field

from app.schemas.common import SchemaModel


class CategoryTreeRequest(SchemaModel):
    language: Literal["DEFAULT", "RU", "EN", "TR", "ZH_HANS"] = Field(
        default="DEFAULT",
        description="响应语言。DEFAULT 默认使用俄语；RU 俄语；EN 英语；TR 土耳其语；ZH_HANS 中文。",
        examples=["DEFAULT"],
    )


class CategoryAttributesRequest(SchemaModel):
    description_category_id: int = Field(
        description="类目 ID。来自 /v1/description-category/tree 的 description_category_id。",
        examples=[17028922],
    )
    type_id: int = Field(
        description="商品类型 ID。来自 /v1/description-category/tree 的 type_id。",
        examples=[91565],
    )
    language: Literal["DEFAULT", "RU", "EN", "TR", "ZH_HANS"] = Field(
        default="DEFAULT",
        description="响应语言。DEFAULT 默认使用俄语；RU 俄语；EN 英语；TR 土耳其语；ZH_HANS 中文。",
        examples=["DEFAULT"],
    )


class AttributeValuesRequest(SchemaModel):
    description_category_id: int = Field(description="类目 ID。", examples=[17028922])
    type_id: int = Field(description="商品类型 ID。", examples=[91565])
    attribute_id: int = Field(
        description="属性 ID。来自 /v1/description-category/attribute 的 result[].id。",
        examples=[85],
    )
    limit: int = Field(
        default=2000,
        ge=1,
        le=2000,
        description="本次返回的属性值数量。Ozon 限制 1 到 2000。",
        examples=[2000],
    )
    last_value_id: int = Field(
        default=0,
        description="分页起点。首次请求传 0；如果响应 has_next=true，用最后一个值 ID 继续请求。",
        examples=[0],
    )
    language: Literal["DEFAULT", "RU", "EN", "TR", "ZH_HANS"] = Field(
        default="DEFAULT",
        description="响应语言。DEFAULT 默认使用俄语；RU 俄语；EN 英语；TR 土耳其语；ZH_HANS 中文。",
        examples=["DEFAULT"],
    )


class AttributeValuesSearchRequest(SchemaModel):
    description_category_id: int = Field(description="类目 ID。", examples=[17028922])
    type_id: int = Field(description="商品类型 ID。", examples=[91565])
    attribute_id: int = Field(description="属性 ID。", examples=[85])
    value: str = Field(
        min_length=2,
        description="搜索关键词，至少 2 个字符。用于搜索属性字典值。",
        examples=["Samsung"],
    )
    limit: int = Field(default=100, ge=1, le=100, description="返回数量，Ozon 限制 1 到 100。", examples=[100])


class OzonRawResponse(SchemaModel):
    data: dict[str, Any] = Field(default_factory=dict)
