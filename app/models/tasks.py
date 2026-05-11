from datetime import datetime

from app.models.base import JsonValue, TableModel


class OzonImportTask(TableModel):
    id: int | None = None
    client_id: str
    task_id: int
    action_type: str
    status: str = "pending"
    credential_ref: str | None = None
    request_payload: JsonValue = None
    response_payload: JsonValue = None
    result_payload: JsonValue = None
    error_payload: JsonValue = None
    submitted_at: datetime | None = None
    last_polled_at: datetime | None = None
    finished_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class OzonImportTaskItem(TableModel):
    id: int | None = None
    client_id: str
    task_id: int
    offer_id: str
    product_id: int | None = None
    status: str = "pending"
    errors: JsonValue = None
    raw_item: JsonValue = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
