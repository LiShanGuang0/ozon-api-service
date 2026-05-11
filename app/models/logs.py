from datetime import datetime

from app.models.base import JsonValue, TableModel


class OzonApiCallLog(TableModel):
    id: int | None = None
    client_id: str
    api_key_fingerprint: str | None = None
    request_id: str | None = None
    endpoint: str
    http_method: str = "POST"
    http_status: int | None = None
    success: bool = False
    duration_ms: int | None = None
    request_payload: JsonValue = None
    response_payload: JsonValue = None
    error_message: str | None = None
    created_at: datetime | None = None
