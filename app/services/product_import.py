import logging
from copy import deepcopy
from typing import Any

from app.clients.ozon_endpoints import OzonEndpoint
from app.core.exceptions import ServiceError
from app.core.security import OzonCredentials
from app.repositories.merchant import TaskEventRepository
from app.repositories.products import ProductRepository
from app.repositories.tasks import ImportTaskItemRepository, ImportTaskRepository
from app.services.credential_store import CredentialStore
from app.services.ozon_forwarder import OzonForwarder

logger = logging.getLogger(__name__)


def task_id_from_import_response(data: dict[str, Any]) -> int | None:
    result = data.get("result")
    if isinstance(result, dict) and result.get("task_id") is not None:
        return int(result["task_id"])
    if data.get("task_id") is not None:
        return int(data["task_id"])
    return None


def has_import_errors(errors: Any) -> bool:
    if not errors:
        return False
    if isinstance(errors, (list, tuple, set)):
        return any(bool(error) for error in errors)
    if isinstance(errors, dict):
        return bool(errors)
    return True


def normalized_import_item_status(item: dict[str, Any]) -> str:
    if has_import_errors(item.get("errors")):
        return "failed"
    return item.get("status") or "pending"


def normalized_import_info_data(data: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(data)
    result = normalized.get("result")
    if not isinstance(result, dict):
        return normalized

    items = result.get("items")
    if not isinstance(items, list):
        return normalized

    for item in items:
        if not isinstance(item, dict):
            continue
        ozon_status = item.get("status") or "pending"
        item_status = normalized_import_item_status(item)
        if item_status != ozon_status:
            item["ozon_status"] = ozon_status
        item["status"] = item_status
    return normalized


def status_from_import_info(data: dict[str, Any]) -> str:
    result = data.get("result") or {}
    items = result.get("items") or []
    if not items:
        if has_import_errors(data.get("errors")) or has_import_errors(result.get("errors")):
            return "failed"
        return "pending"
    statuses = {normalized_import_item_status(item) for item in items}
    if statuses == {"imported"}:
        return "imported"
    if statuses == {"skipped"}:
        return "skipped"
    if "failed" in statuses and len(statuses) == 1:
        return "failed"
    if "pending" in statuses:
        return "pending"
    if "failed" in statuses:
        return "partial"
    return next(iter(statuses))


class ProductImportService:
    def __init__(
        self,
        forwarder: OzonForwarder | None = None,
        products: ProductRepository | None = None,
        tasks: ImportTaskRepository | None = None,
        task_items: ImportTaskItemRepository | None = None,
        credentials: CredentialStore | None = None,
        events: TaskEventRepository | None = None,
    ) -> None:
        self.forwarder = forwarder or OzonForwarder()
        self.products = products or ProductRepository()
        self.tasks = tasks or ImportTaskRepository()
        self.task_items = task_items or ImportTaskItemRepository()
        self.credentials = credentials or CredentialStore()
        self.events = events or TaskEventRepository()

    async def import_products(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        self._safe_event(
            client_id=credentials.client_id,
            event_type="product_import",
            status="pending",
            message="开始查询商品创建额度",
            ref_type="import_task",
            payload={"total": len(payload.get("items") or [])},
        )
        limit_data = await self.forwarder.post(OzonEndpoint.PRODUCT_INFO_LIMIT, {}, credentials)
        self._safe_event(
            client_id=credentials.client_id,
            event_type="product_import",
            status="success",
            message="商品创建额度查询完成",
            ref_type="import_task",
            payload={"total": len(payload.get("items") or [])},
        )
        try:
            import_data = await self.forwarder.post(OzonEndpoint.PRODUCT_IMPORT, payload, credentials)
        except ServiceError as exc:
            for item in payload.get("items") or []:
                self.products.upsert_from_import_item(
                    client_id=credentials.client_id,
                    item=item,
                    status="failed",
                )
                self._safe_event(
                    client_id=credentials.client_id,
                    event_type="product_import",
                    status="failed",
                    message="商品数据推送失败",
                    ref_type="import_task",
                    offer_id=item.get("offer_id"),
                    error_message=exc.message,
                    payload={"item": item, "error": exc.detail},
                )
            raise

        task_id = task_id_from_import_response(import_data)

        credential_ref = self.credentials.store(credentials) if task_id else None
        if task_id:
            self.tasks.insert(
                client_id=credentials.client_id,
                task_id=task_id,
                action_type="product_import",
                status="pending",
                credential_ref=credential_ref,
                request_payload=payload,
                response_payload=import_data,
            )
            self._safe_event(
                client_id=credentials.client_id,
                event_type="product_import",
                status="pending",
                message="Ozon 推送任务建立成功，等待平台处理",
                ref_type="import_task",
                ozon_task_id=task_id,
                payload={"task_id": task_id, "total": len(payload.get("items") or [])},
            )
        else:
            self._safe_event(
                client_id=credentials.client_id,
                event_type="product_import",
                status="failed",
                message="Ozon 未返回任务编号，商品数据推送失败",
                ref_type="import_task",
                payload={"response": import_data, "total": len(payload.get("items") or [])},
            )

        for item in payload.get("items") or []:
            self.products.upsert_from_import_item(
                client_id=credentials.client_id,
                item=item,
                task_id=task_id,
                status="pending" if task_id else "failed",
            )
            self._safe_event(
                client_id=credentials.client_id,
                event_type="product_import",
                status="pending" if task_id else "failed",
                message="商品数据已提交至 Ozon" if task_id else "商品数据推送失败",
                ref_type="import_task",
                ozon_task_id=task_id,
                offer_id=item.get("offer_id"),
                payload={"item": item, "task_id": task_id},
            )

        return {
            "limit": limit_data,
            "import_result": import_data,
            "task_id": task_id,
            "credential_ref_saved": bool(credential_ref),
        }

    async def poll_import_task(self, *, task_id: int, credentials: OzonCredentials) -> dict[str, Any]:
        task = self.tasks.get(client_id=credentials.client_id, task_id=task_id)
        polling_credentials = credentials
        if task and task.get("credential_ref"):
            polling_credentials = self.credentials.load(task["credential_ref"]) or credentials

        raw_data = await self.forwarder.post(OzonEndpoint.PRODUCT_IMPORT_INFO, {"task_id": task_id}, polling_credentials)
        data = normalized_import_info_data(raw_data)
        status = status_from_import_info(data)
        result = data.get("result") or {}
        self._safe_event(
            client_id=credentials.client_id,
            event_type="product_import",
            status=self._task_event_status(status),
            message=f"任务查询成功，当前处理结果：{self._task_status_message(status)}",
            ref_type="import_task",
            ozon_task_id=task_id,
            payload={"task_id": task_id, "status": status, "total": result.get("total")},
        )
        errors = []
        for item in result.get("items") or []:
            item_status = normalized_import_item_status(item)
            self.task_items.upsert(client_id=credentials.client_id, task_id=task_id, item=item)
            self.products.update_from_task_item(client_id=credentials.client_id, item=item)
            if item.get("errors"):
                errors.append({"offer_id": item.get("offer_id"), "errors": item.get("errors")})
            self._safe_event(
                client_id=credentials.client_id,
                event_type="product_import",
                status=self._event_status(item_status, item.get("errors")),
                message=self._event_message(item_status, item.get("errors")),
                ref_type="import_task",
                ozon_task_id=task_id,
                offer_id=item.get("offer_id"),
                product_id=item.get("product_id"),
                error_message=self._error_message(item.get("errors")),
                payload=item,
            )

        self.tasks.update_result(
            client_id=credentials.client_id,
            task_id=task_id,
            status=status,
            result_payload=data,
            error_payload=errors or None,
        )
        return {"task_id": task_id, "status": status, "data": data}

    async def update_attributes(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        data = await self.forwarder.post(OzonEndpoint.PRODUCT_ATTRIBUTES_UPDATE, payload, credentials)
        task_id = task_id_from_import_response(data)
        if task_id:
            self.tasks.insert(
                client_id=credentials.client_id,
                task_id=task_id,
                action_type="attribute_update",
                status="pending",
                credential_ref=self.credentials.store(credentials),
                request_payload=payload,
                response_payload=data,
            )
        return {"task_id": task_id, "data": data}

    def _safe_event(self, **kwargs: Any) -> None:
        try:
            self.events.insert(**kwargs)
        except Exception as exc:
            logger.warning("Failed to write ozon_task_events: %s", exc)

    def _event_status(self, ozon_status: str, errors: Any = None) -> str:
        if has_import_errors(errors):
            return "failed"
        if ozon_status == "imported":
            return "success"
        if ozon_status == "failed":
            return "failed"
        if ozon_status == "skipped":
            return "skipped"
        return "pending"

    def _event_message(self, ozon_status: str, errors: Any = None) -> str:
        if has_import_errors(errors):
            return "商品数据创建失败"
        if ozon_status == "imported":
            return "商品数据创建完成"
        if ozon_status == "failed":
            return "商品数据创建失败"
        if ozon_status == "skipped":
            return "商品数据创建重复（跳过）"
        return "商品数据创建处理中"

    def _task_event_status(self, status: str) -> str:
        if status in {"imported", "success"}:
            return "success"
        if status in {"failed", "skipped"}:
            return "failed"
        if status == "partial":
            return "failed"
        return "pending"

    def _task_status_message(self, status: str) -> str:
        messages = {
            "imported": "商品数据创建完成",
            "success": "商品数据创建完成",
            "failed": "商品数据创建失败",
            "partial": "部分商品数据创建失败",
            "skipped": "商品数据创建重复（跳过）",
            "pending": "处理中",
        }
        return messages.get(status, status)

    def _error_message(self, errors: Any) -> str | None:
        if not errors:
            return None
        if isinstance(errors, list):
            return "; ".join(str(error.get("message") or error.get("code") or error) for error in errors)
        return str(errors)
