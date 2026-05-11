import hashlib
import json
from typing import Any

from app.db.redis import redis_client


def stable_cache_part(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class RedisJsonCache:
    def get(self, key: str) -> dict[str, Any] | None:
        raw = redis_client().get(key)
        if not raw:
            return None
        return json.loads(raw)

    def set(self, key: str, value: dict[str, Any], ttl_seconds: int) -> None:
        redis_client().setex(key, ttl_seconds, json.dumps(value, ensure_ascii=False))
