from typing import Any

from app.clients.ozon_endpoints import OzonEndpoint
from app.core.config import get_settings
from app.core.security import OzonCredentials
from app.services.business_events import BusinessEventLogger
from app.services.ozon_forwarder import OzonForwarder
from app.services.redis_cache import RedisJsonCache, stable_cache_part


class CategoryService:
    def __init__(
        self,
        forwarder: OzonForwarder | None = None,
        cache: RedisJsonCache | None = None,
        events: BusinessEventLogger | None = None,
    ) -> None:
        self.forwarder = forwarder or OzonForwarder()
        self.cache = cache or RedisJsonCache()
        self.events = events or BusinessEventLogger()
        self.settings = get_settings()

    async def tree(self, *, payload: dict[str, Any] | None, credentials: OzonCredentials) -> dict[str, Any]:
        request_payload = payload or {"language": "DEFAULT"}
        return await self._with_event(
            credentials=credentials,
            payload=request_payload,
            event_type="category_query",
            start_message="开始查询商品类目树",
            success_message="商品类目树查询完成",
            failure_message="商品类目树查询失败",
            call=lambda: self._cached_post(
                key=self._key("tree", credentials.client_id, request_payload),
                endpoint=OzonEndpoint.CATEGORY_TREE,
                payload=request_payload,
                credentials=credentials,
                ttl_seconds=self.settings.ozon_category_tree_ttl_seconds,
            ),
        )

    async def attributes(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        return await self._with_event(
            credentials=credentials,
            payload=payload,
            event_type="category_query",
            start_message="开始查询商品类目属性",
            success_message="商品类目属性查询完成",
            failure_message="商品类目属性查询失败",
            call=lambda: self._cached_post(
                key=self._key("attributes", credentials.client_id, payload),
                endpoint=OzonEndpoint.CATEGORY_ATTRIBUTES,
                payload=payload,
                credentials=credentials,
                ttl_seconds=self.settings.ozon_category_attributes_ttl_seconds,
            ),
        )

    async def values(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        return await self._with_event(
            credentials=credentials,
            payload=payload,
            event_type="category_query",
            start_message="开始查询商品属性字典值",
            success_message="商品属性字典值查询完成",
            failure_message="商品属性字典值查询失败",
            call=lambda: self._cached_post(
                key=self._key("values", credentials.client_id, payload),
                endpoint=OzonEndpoint.CATEGORY_ATTRIBUTE_VALUES,
                payload=payload,
                credentials=credentials,
                ttl_seconds=self.settings.ozon_attribute_values_ttl_seconds,
            ),
        )

    async def search_values(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        return await self._with_event(
            credentials=credentials,
            payload=payload,
            event_type="category_query",
            start_message="开始搜索商品属性字典值",
            success_message="商品属性字典值搜索完成",
            failure_message="商品属性字典值搜索失败",
            call=lambda: self._cached_post(
                key=self._key("values-search", credentials.client_id, payload),
                endpoint=OzonEndpoint.CATEGORY_ATTRIBUTE_VALUES_SEARCH,
                payload=payload,
                credentials=credentials,
                ttl_seconds=self.settings.ozon_attribute_values_ttl_seconds,
            ),
        )

    async def _with_event(
        self,
        *,
        credentials: OzonCredentials,
        payload: dict[str, Any],
        event_type: str,
        start_message: str,
        success_message: str,
        failure_message: str,
        call: Any,
    ) -> dict[str, Any]:
        self.events.emit(
            client_id=credentials.client_id,
            event_type=event_type,
            status="pending",
            message=start_message,
            payload=payload,
        )
        try:
            data = await call()
            self.events.emit(
                client_id=credentials.client_id,
                event_type=event_type,
                status="success",
                message=success_message,
                payload=payload,
            )
            return data
        except Exception as exc:
            self.events.emit(
                client_id=credentials.client_id,
                event_type=event_type,
                status="failed",
                message=failure_message,
                error_message=str(exc),
                payload=payload,
            )
            raise

    async def _cached_post(
        self,
        *,
        key: str,
        endpoint: str,
        payload: dict[str, Any],
        credentials: OzonCredentials,
        ttl_seconds: int,
    ) -> dict[str, Any]:
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        data = await self.forwarder.post(endpoint, payload, credentials)
        self.cache.set(key, data, ttl_seconds)
        return data

    def _key(self, cache_type: str, client_id: str, payload: dict[str, Any]) -> str:
        return f"ozon:category-cache:{client_id}:{cache_type}:{stable_cache_part(payload)}"
