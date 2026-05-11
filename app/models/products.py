from datetime import datetime
from decimal import Decimal

from app.models.base import JsonValue, TableModel


class OzonProduct(TableModel):
    id: int | None = None
    client_id: str
    local_sku: str | None = None
    offer_id: str
    product_id: int | None = None
    sku: int | None = None
    name: str | None = None
    description_category_id: int | None = None
    type_id: int | None = None
    currency_code: str | None = None
    price: Decimal | None = None
    old_price: Decimal | None = None
    vat: str | None = None
    barcode: str | None = None
    sync_status: str = "draft"
    ozon_status: str | None = None
    last_task_id: int | None = None
    last_error: JsonValue = None
    last_request_payload: JsonValue = None
    last_response_payload: JsonValue = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class OzonProductAttribute(TableModel):
    id: int | None = None
    client_id: str
    offer_id: str
    attribute_id: int
    complex_id: int = 0
    dictionary_value_id: int = 0
    value: str | None = None
    value_json: JsonValue = None
    is_required: bool = False
    source: str = "local"
    created_at: datetime | None = None
    updated_at: datetime | None = None


class OzonProductImage(TableModel):
    id: int | None = None
    client_id: str
    offer_id: str
    product_id: int | None = None
    url: str
    image_type: str = "image"
    sort_order: int = 0
    is_primary: bool = False
    state: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
