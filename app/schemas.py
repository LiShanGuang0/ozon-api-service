from typing import Any

from pydantic import BaseModel, Field


class OzonForwardResponse(BaseModel):
    endpoint: str
    data: dict[str, Any]


class ProductImportRequest(BaseModel):
    items: list[dict[str, Any]] = Field(default_factory=list)


class PictureImportRequest(BaseModel):
    product_id: int
    images: list[str] = Field(default_factory=list)
    images360: list[str] = Field(default_factory=list)
    color_image: str | None = None


class AttributeValuesRequest(BaseModel):
    description_category_id: int
    type_id: int
    attribute_id: int
    limit: int = 100
    language: str = "ZH_HANS"
    last_value_id: int = 0


class AttributeValuesSearchRequest(BaseModel):
    description_category_id: int
    type_id: int
    attribute_id: int
    value: str
    limit: int = 100
