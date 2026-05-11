from typing import Any

from app.db.mysql import execute
from app.utils.json import dumps


class ApiLogRepository:
    def insert(
        self,
        *,
        client_id: str,
        api_key_fingerprint: str | None,
        endpoint: str,
        http_status: int | None,
        success: bool,
        duration_ms: int | None,
        request_payload: Any,
        response_payload: Any,
        error_message: str | None = None,
        request_id: str | None = None,
    ) -> None:
        execute(
            """
            INSERT INTO ozon_api_call_logs
              (client_id, api_key_fingerprint, request_id, endpoint, http_method, http_status,
               success, duration_ms, request_payload, response_payload, error_message)
            VALUES
              (%s, %s, %s, %s, 'POST', %s, %s, %s, %s, %s, %s)
            """,
            (
                client_id,
                api_key_fingerprint,
                request_id,
                endpoint,
                http_status,
                1 if success else 0,
                duration_ms,
                dumps(request_payload),
                dumps(response_payload),
                error_message,
            ),
        )
