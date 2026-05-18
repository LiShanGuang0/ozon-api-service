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

    async def list_with_attributes(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        list_payload = self._product_list_payload(payload)
        product_list = await self._with_event(
            credentials=credentials,
            event_type="product_query",
            start_message="开始查询商品列表",
            success_message="商品列表查询完成",
            failure_message="商品列表查询失败",
            payload=list_payload,
            call=lambda: self.forwarder.post(OzonEndpoint.PRODUCT_LIST, list_payload, credentials),
        )

        list_items = _product_list_items(product_list)
        attributes_payload = self._attributes_payload_from_list_items(
            list_items=list_items,
            attributes_limit=int(payload.get("attributes_limit") or 1000),
        )
        attributes_result: dict[str, Any] = {}
        attribute_items: list[dict[str, Any]] = []
        if attributes_payload:
            attributes_result = await self._with_event(
                credentials=credentials,
                event_type="product_query",
                start_message="开始查询商品属性详情",
                success_message="商品属性详情查询完成",
                failure_message="商品属性详情查询失败",
                payload=attributes_payload,
                call=lambda: self.forwarder.post(OzonEndpoint.PRODUCT_INFO_ATTRIBUTES, attributes_payload, credentials),
            )
            attribute_items = _product_attribute_items(attributes_result)

        attributes_by_product_id = {
            product_id: item for item in attribute_items if (product_id := _item_product_id(item)) is not None
        }
        attributes_by_offer_id = {
            offer_id: item for item in attribute_items if (offer_id := item.get("offer_id")) is not None
        }

        merged_items = []
        for item in list_items:
            product_id = _item_product_id(item)
            offer_id = item.get("offer_id")
            attributes = None
            if product_id is not None:
                attributes = attributes_by_product_id.get(product_id)
            if attributes is None and offer_id is not None:
                attributes = attributes_by_offer_id.get(offer_id)
            merged_items.append(
                {
                    "product_id": product_id,
                    "offer_id": offer_id,
                    "list_item": item,
                    "attributes": attributes,
                }
            )

        list_result = product_list.get("result") if isinstance(product_list.get("result"), dict) else {}
        return {
            "items": merged_items,
            "total": list_result.get("total"),
            "last_id": str(list_result.get("last_id") or ""),
            "attribute_total": _product_attribute_total(attributes_result),
            "attribute_last_id": _product_attribute_last_id(attributes_result),
            "product_list": product_list,
            "attributes_result": attributes_result,
        }

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

    def _product_list_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        filters = payload.get("filter") or {}
        cleaned_filter: dict[str, Any] = {}
        if filters.get("offer_id"):
            cleaned_filter["offer_id"] = filters["offer_id"]
        if filters.get("product_id"):
            cleaned_filter["product_id"] = [str(value) for value in filters["product_id"]]
        if filters.get("visibility"):
            cleaned_filter["visibility"] = filters["visibility"]

        return {
            "filter": cleaned_filter,
            "last_id": payload.get("last_id") or "",
            "limit": int(payload.get("limit") or 100),
        }

    def _attributes_payload_from_list_items(
        self,
        *,
        list_items: list[dict[str, Any]],
        attributes_limit: int,
    ) -> dict[str, Any] | None:
        product_ids = []
        offer_ids = []
        for item in list_items:
            product_id = _item_product_id(item)
            if product_id is not None:
                product_ids.append(product_id)
            elif item.get("offer_id"):
                offer_ids.append(item["offer_id"])

        filter_payload: dict[str, Any]
        if product_ids:
            filter_payload = {"product_id": product_ids[:1000]}
        elif offer_ids:
            filter_payload = {"offer_id": offer_ids[:1000]}
        else:
            return None

        return {
            "filter": filter_payload,
            "limit": min(attributes_limit, len(product_ids or offer_ids), 1000),
            "last_id": "",
        }

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


def _product_list_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    result = data.get("result")
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return [item for item in result["items"] if isinstance(item, dict)]
    return [item for item in _response_items(data) if isinstance(item, dict)]


def _product_attribute_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    result = data.get("result")
    if isinstance(result, list):
        return [item for item in result if isinstance(item, dict)]
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return [item for item in result["items"] if isinstance(item, dict)]
    if isinstance(data.get("items"), list):
        return [item for item in data["items"] if isinstance(item, dict)]
    return []


def _product_attribute_total(data: dict[str, Any]) -> int | str | None:
    if data.get("total") is not None:
        return data["total"]
    result = data.get("result")
    if isinstance(result, dict):
        return result.get("total")
    return None


def _product_attribute_last_id(data: dict[str, Any]) -> str:
    if data.get("last_id") is not None:
        return str(data["last_id"] or "")
    result = data.get("result")
    if isinstance(result, dict):
        return str(result.get("last_id") or "")
    return ""


def _item_product_id(item: dict[str, Any]) -> int | None:
    value = item.get("id") or item.get("product_id")
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
