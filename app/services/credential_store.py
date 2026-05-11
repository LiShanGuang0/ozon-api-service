import json
import uuid
from typing import Any

from app.core.config import get_settings
from app.core.security import OzonCredentials
from app.db.redis import redis_client


class CredentialStore:
    def store(self, credentials: OzonCredentials) -> str:
        settings = get_settings()
        key = f"ozon:credentials:{uuid.uuid4().hex}"
        payload = {"client_id": credentials.client_id, "api_key": credentials.api_key}
        redis_client().setex(key, settings.ozon_credential_ttl_seconds, json.dumps(payload, ensure_ascii=False))
        return key

    def load(self, ref: str) -> OzonCredentials | None:
        raw = redis_client().get(ref)
        if not raw:
            return None
        data: dict[str, Any] = json.loads(raw)
        return OzonCredentials(client_id=data["client_id"], api_key=data["api_key"])
