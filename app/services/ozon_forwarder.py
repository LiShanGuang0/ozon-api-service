from typing import Any

from app.clients.ozon import OzonClient, ozon_client
from app.core.exceptions import ServiceError
from app.core.security import OzonCredentials
from app.repositories.api_logs import ApiLogRepository


class OzonForwarder:
    def __init__(
        self,
        client: OzonClient = ozon_client,
        logs: ApiLogRepository | None = None,
    ) -> None:
        self.client = client
        self.logs = logs or ApiLogRepository()

    async def post(
        self,
        endpoint: str,
        payload: dict[str, Any] | None,
        credentials: OzonCredentials,
        request_id: str | None = None,
    ) -> dict[str, Any]:
        normalized_endpoint = "/" + endpoint.strip("/")
        try:
            data, status_code, duration_ms = await self.client.post(endpoint, payload, credentials)
            self.logs.insert(
                client_id=credentials.client_id,
                api_key_fingerprint=credentials.api_key_fingerprint,
                request_id=request_id,
                endpoint=normalized_endpoint,
                http_status=status_code,
                success=True,
                duration_ms=duration_ms,
                request_payload=payload,
                response_payload=data,
            )
            return data
        except ServiceError as exc:
            self.logs.insert(
                client_id=credentials.client_id,
                api_key_fingerprint=credentials.api_key_fingerprint,
                request_id=request_id,
                endpoint=normalized_endpoint,
                http_status=exc.status_code,
                success=False,
                duration_ms=None,
                request_payload=payload,
                response_payload=exc.detail,
                error_message=exc.message,
            )
            raise
