from typing import Any

from app.clients.ozon_endpoints import OzonEndpoint
from app.core.exceptions import ServiceError
from app.core.security import OzonCredentials
from app.repositories.products import ProductRepository
from app.services.business_events import BusinessEventLogger
from app.services.ozon_forwarder import OzonForwarder


class ProductQueryService:
    def __init__(
        self,
        forwarder: OzonForwarder | None = None,
        products: ProductRepository | None = None,
        events: BusinessEventLogger | None = None,
    ) -> None:
        self.forwarder = forwarder or OzonForwarder()
        self.products = products or ProductRepository()
        self.events = events or BusinessEventLogger()

    async def info_limit(self, *, credentials: OzonCredentials) -> dict[str, Any]:
        return await self._with_event(
            credentials=credentials,
            event_type="product_query",
            start_message="开始查询商品创建额度",
            success_message="商品创建额度查询完成",
            failure_message="商品创建额度查询失败",
            payload={},
            call=lambda: self.forwarder.post(OzonEndpoint.PRODUCT_INFO_LIMIT, {}, credentials),
        )

    async def pictures_import(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        offer_id = payload.get("offer_id")
        if not offer_id:
            raise ServiceError("offer_id is required", status_code=422, detail={"field": "offer_id"})

        self.events.emit(
            client_id=credentials.client_id,
            event_type="product_picture",
            status="pending",
            message="开始处理商品图片更新",
            offer_id=str(offer_id),
            payload={"offer_id": offer_id, "image_count": len(payload.get("images") or [])},
        )
        product_id = await self._resolve_product_id_by_offer_id(offer_id=str(offer_id), credentials=credentials)
        request_payload = {
            "product_id": product_id,
            "images": payload.get("images") or [],
            "images360": payload.get("images360") or [],
            "color_image": payload.get("color_image"),
        }
        try:
            data = await self.forwarder.post(OzonEndpoint.PRODUCT_PICTURES_IMPORT, request_payload, credentials)
            self.events.emit(
                client_id=credentials.client_id,
                event_type="product_picture",
                status="success",
                message="商品图片更新提交完成",
                offer_id=str(offer_id),
                product_id=product_id,
                payload={"image_count": len(request_payload["images"])},
            )
            self.products.sync_images_from_item(
                client_id=credentials.client_id,
                item={
                    "offer_id": offer_id,
                    "product_id": product_id,
                    "images": request_payload["images"],
                    "images360": request_payload["images360"],
                    "color_image": request_payload["color_image"],
                    "primary_image": request_payload["images"][0] if request_payload["images"] else None,
                },
            )
            return data
        except Exception as exc:
            self.events.emit(
                client_id=credentials.client_id,
                event_type="product_picture",
                status="failed",
                message="商品图片更新提交失败",
                offer_id=str(offer_id),
                product_id=product_id,
                error_message=str(exc),
                payload={"image_count": len(request_payload["images"])},
            )
            raise

    async def info_list(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        data = await self._with_event(
            credentials=credentials,
            event_type="product_query",
            start_message="开始查询商品信息",
            success_message="商品信息查询完成",
            failure_message="商品信息查询失败",
            payload=payload,
            call=lambda: self.forwarder.post(OzonEndpoint.PRODUCT_INFO_LIST, payload, credentials),
        )
        for item in _response_items(data):
            self.products.update_identifiers_from_info_item(client_id=credentials.client_id, item=item)
        return data

    async def info_attributes(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        request_payload = {
            "filter": {"offer_id": [payload["offer_id"]]},
            "limit": 100,
            "last_id": "",
        }
        return await self._with_event(
            credentials=credentials,
            event_type="product_query",
            start_message="开始查询商品已填写属性",
            success_message="商品已填写属性查询完成",
            failure_message="商品已填写属性查询失败",
            payload=request_payload,
            call=lambda: self.forwarder.post(OzonEndpoint.PRODUCT_INFO_ATTRIBUTES, request_payload, credentials),
        )

    async def _with_event(
        self,
        *,
        credentials: OzonCredentials,
        event_type: str,
        start_message: str,
        success_message: str,
        failure_message: str,
        payload: dict[str, Any],
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

    async def _resolve_product_id_by_offer_id(self, *, offer_id: str, credentials: OzonCredentials) -> int:
        product = self.products.get_by_offer_id(client_id=credentials.client_id, offer_id=offer_id)
        if product and product.get("product_id") is not None:
            return int(product["product_id"])

        data = await self.forwarder.post(OzonEndpoint.PRODUCT_INFO_LIST, {"offer_id": [offer_id]}, credentials)
        items = _response_items(data)
        if not items:
            raise ServiceError(
                "Product not found by offer_id",
                status_code=404,
                detail={"offer_id": offer_id},
            )

        item = items[0]
        product_id = _item_product_id(item)
        if product_id is None:
            raise ServiceError(
                "Product has no product_id yet",
                status_code=409,
                detail={"offer_id": offer_id},
            )

        self.products.update_identifiers_from_info_item(client_id=credentials.client_id, item=item)
        return product_id


def _response_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(data.get("items"), list):
        return data["items"]
    result = data.get("result")
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return result["items"]
    return []


def _item_product_id(item: dict[str, Any]) -> int | None:
    value = item.get("id") or item.get("product_id")
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
