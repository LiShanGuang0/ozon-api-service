from time import perf_counter
from typing import Any

import httpx

from app.core.config import get_settings
from app.core.exceptions import ServiceError
from app.core.security import OzonCredentials


class OzonClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def post(
        self,
        path: str,
        payload: dict[str, Any] | None,
        credentials: OzonCredentials,
    ) -> tuple[dict[str, Any], int, int]:
        normalized_path = "/" + path.strip("/")
        url = f"{self.settings.ozon_base_url.rstrip('/')}{normalized_path}"
        headers = {
            "Client-Id": credentials.client_id,
            "Api-Key": credentials.api_key,
            "Content-Type": "application/json",
        }
        started = perf_counter()
        async with httpx.AsyncClient(timeout=self.settings.ozon_timeout_seconds) as client:
            response = await client.post(url, json=payload or {}, headers=headers)
        duration_ms = int((perf_counter() - started) * 1000)

        try:
            data = response.json()
        except ValueError:
            data = {"raw": response.text}

        if response.status_code >= 400:
            raise ServiceError("Ozon API request failed", status_code=response.status_code, detail=data)
        return data, response.status_code, duration_ms


ozon_client = OzonClient()
