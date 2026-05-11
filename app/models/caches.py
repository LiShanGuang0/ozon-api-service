from datetime import datetime

from app.models.base import JsonValue, TableModel


class OzonCategoryTreeCache(TableModel):
    id: int | None = None
    language: str = "ZH_HANS"
    tree_json: JsonValue
    source_hash: str | None = None
    expired_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class OzonCategoryAttributesCache(TableModel):
    id: int | None = None
    description_category_id: int
    type_id: int
    language: str = "ZH_HANS"
    attributes_json: JsonValue
    source_hash: str | None = None
    expired_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class OzonAttributeValuesCache(TableModel):
    id: int | None = None
    description_category_id: int
    type_id: int
    attribute_id: int
    language: str = "ZH_HANS"
    search_value: str = ""
    last_value_id: int = 0
    has_next: bool = False
    values_json: JsonValue
    source_hash: str | None = None
    expired_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
