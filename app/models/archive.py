from datetime import datetime

from app.models.base import JsonValue, TableModel


class OzonArchiveTask(TableModel):
    id: int | None = None
    client_id: str
    request_id: str
    action_type: str = "archive"
    status: str = "pending"
    credential_ref: str | None = None
    input_identifiers: JsonValue = None
    precheck_payload: JsonValue = None
    request_payload: JsonValue = None
    response_payload: JsonValue = None
    confirm_payload: JsonValue = None
    error_payload: JsonValue = None
    total_count: int = 0
    success_count: int = 0
    failed_count: int = 0
    skipped_count: int = 0
    submitted_at: datetime | None = None
    finished_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class OzonArchiveTaskItem(TableModel):
    id: int | None = None
    client_id: str
    archive_task_id: int
    request_id: str
    identifier_type: str | None = None
    identifier_value: str | None = None
    offer_id: str | None = None
    product_id: int | None = None
    sku: int | None = None
    before_is_archived: bool | None = None
    before_is_autoarchived: bool | None = None
    after_is_archived: bool | None = None
    after_is_autoarchived: bool | None = None
    status: str = "pending"
    skip_reason: str | None = None
    error_message: str | None = None
    precheck_payload: JsonValue = None
    operation_response_payload: JsonValue = None
    confirm_payload: JsonValue = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class OzonProductArchiveHistory(TableModel):
    id: int | None = None
    client_id: str
    archive_task_id: int | None = None
    request_id: str | None = None
    action_type: str
    source: str = "archive_workflow"
    offer_id: str | None = None
    product_id: int | None = None
    sku: int | None = None
    from_is_archived: bool | None = None
    to_is_archived: bool | None = None
    from_is_autoarchived: bool | None = None
    to_is_autoarchived: bool | None = None
    payload: JsonValue = None
    created_at: datetime | None = None
