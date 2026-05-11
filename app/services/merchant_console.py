from typing import Any

from app.clients.ozon_endpoints import OzonEndpoint
from app.core.exceptions import ServiceError
from app.core.security import OzonCredentials
from app.repositories.merchant import (
    MerchantImportTaskRepository,
    MerchantProductRepository,
    MerchantRepository,
    TaskEventRepository,
)
from app.repositories.stocks import ProductStockRepository
from app.services.product_import import normalized_import_item_status
from app.services.ozon_forwarder import OzonForwarder
from app.utils.json import loads


STATUS_LABELS = {
    "draft": "草稿",
    "pending": "处理中",
    "running": "执行中",
    "imported": "已成功",
    "success": "已成功",
    "failed": "失败",
    "partial": "部分成功",
    "skipped": "商品数据创建重复（跳过）",
    "info": "提示",
    "archived": "已归档",
}


def status_label(status: str | None) -> str:
    if not status:
        return "未知"
    return STATUS_LABELS.get(status, status)


def parse_json_field(value: Any) -> Any:
    if not isinstance(value, str) or not value:
        return value
    try:
        return loads(value)
    except ValueError:
        return value


class MerchantConsoleService:
    def __init__(
        self,
        *,
        merchants: MerchantRepository | None = None,
        products: MerchantProductRepository | None = None,
        tasks: MerchantImportTaskRepository | None = None,
        events: TaskEventRepository | None = None,
        forwarder: OzonForwarder | None = None,
        stocks: ProductStockRepository | None = None,
    ) -> None:
        self.merchants = merchants or MerchantRepository()
        self.products = products or MerchantProductRepository()
        self.tasks = tasks or MerchantImportTaskRepository()
        self.events = events or TaskEventRepository()
        self.forwarder = forwarder or OzonForwarder()
        self.stocks = stocks or ProductStockRepository()

    async def bootstrap(self, *, credentials: OzonCredentials) -> dict[str, Any]:
        merchant = self.merchants.get_by_client_id(client_id=credentials.client_id)
        initialized = False
        if merchant is None:
            merchant = await self._init_merchant_from_ozon(credentials=credentials)
            initialized = True
        return {
            "profile": merchant,
            "initialized_from_ozon": initialized,
            "credential_valid": True,
        }

    def profile(self, *, client_id: str) -> dict[str, Any]:
        merchant = self.merchants.get_by_client_id(client_id=client_id)
        if merchant:
            return merchant
        return {
            "merchant_id": None,
            "client_id": client_id,
            "shop_name": None,
            "display_name": None,
            "logo_url": None,
            "status": "active",
            "currency_code": None,
            "default_warehouse_id": None,
            "contact_name": None,
            "contact_phone": None,
            "contact_email": None,
            "last_connected_at": None,
            "last_error": None,
        }

    def dashboard(self, *, client_id: str) -> dict[str, Any]:
        profile = self.profile(client_id=client_id)
        task_counts = self._merge_skipped_into_failed(self._counts_dict(self.tasks.today_status_counts(client_id=client_id)))
        product_counts = self._merge_skipped_into_failed(self._counts_dict(self.products.status_counts(client_id=client_id)))
        today_event_count = self.events.today_count(client_id=client_id)
        recent_events = self.task_events(client_id=client_id, limit=8)["items"]

        success_count = task_counts.get("imported", 0) + task_counts.get("success", 0)
        failed_count = task_counts.get("failed", 0)
        pending_count = task_counts.get("pending", 0)
        total_count = sum(task_counts.values())

        return {
            "profile": profile,
            "metrics": [
                {"key": "today_tasks", "label": "今日推送", "value": total_count},
                {"key": "success_tasks", "label": "成功任务", "value": success_count},
                {"key": "failed_tasks", "label": "失败任务", "value": failed_count},
                {"key": "pending_tasks", "label": "处理中", "value": pending_count},
            ],
            "task_status_counts": task_counts,
            "product_status_counts": product_counts,
            "today_event_count": today_event_count,
            "recent_events": recent_events,
        }

    def product_page(
        self,
        *,
        client_id: str,
        page: int,
        size: int,
        keyword: str | None = None,
        status: str | None = None,
    ) -> dict[str, Any]:
        page, size, offset = self._page(page, size)
        rows = self.products.list(
            client_id=client_id,
            keyword=keyword,
            status=status,
            limit=size,
            offset=offset,
        )
        total = self.products.count(client_id=client_id, keyword=keyword, status=status)
        items = []
        for row in rows:
            row["last_error"] = parse_json_field(row.get("last_error"))
            row["sync_status_label"] = status_label(row.get("sync_status"))
            items.append(row)
        return {"total": total, "page": page, "size": size, "items": items}

    def task_page(
        self,
        *,
        client_id: str,
        page: int,
        size: int,
        status: str | None = None,
    ) -> dict[str, Any]:
        page, size, offset = self._page(page, size)
        rows = self.tasks.list(client_id=client_id, status=status, limit=size, offset=offset)
        total = self.tasks.count(client_id=client_id, status=status)
        items = []
        for row in rows:
            row["status_label"] = status_label(row.get("status"))
            items.append(row)
        return {"total": total, "page": page, "size": size, "items": items}

    def task_detail(self, *, client_id: str, task_id: int) -> dict[str, Any]:
        task = self.tasks.get(client_id=client_id, task_id=task_id)
        if not task:
            raise ServiceError("Task not found", status_code=404, detail={"task_id": task_id})

        task["request_payload"] = parse_json_field(task.get("request_payload"))
        task["response_payload"] = parse_json_field(task.get("response_payload"))
        task["result_payload"] = parse_json_field(task.get("result_payload"))
        task["error_payload"] = parse_json_field(task.get("error_payload"))
        items = []
        for item in self.tasks.items(client_id=client_id, task_id=task_id):
            item["errors"] = parse_json_field(item.get("errors"))
            item["raw_item"] = parse_json_field(item.get("raw_item"))
            item["status"] = normalized_import_item_status(item)
            item["status_label"] = status_label(item.get("status"))
            items.append(item)
        derived_status = self._task_status_from_items(items)
        if derived_status:
            task["status"] = derived_status
        task["status_label"] = status_label(task.get("status"))
        return {"task": task, "items": items}

    def task_events(
        self,
        *,
        client_id: str,
        limit: int,
        before_id: int | None = None,
        status: str | None = None,
        event_type: str | None = None,
    ) -> dict[str, Any]:
        limit = min(max(limit, 1), 100)
        rows = self.events.list(
            client_id=client_id,
            limit=limit,
            before_id=before_id,
            status=status,
            event_type=event_type,
        )
        items = []
        for row in rows:
            row["status_label"] = status_label(row.get("status"))
            items.append(row)
        return {
            "items": items,
            "next_before_id": items[-1]["id"] if len(items) == limit else None,
            "today_count": self.events.today_count(client_id=client_id),
        }

    def _counts_dict(self, rows: list[dict[str, Any]]) -> dict[str, int]:
        return {str(row.get("status") or "unknown"): int(row.get("count") or 0) for row in rows}

    def _merge_skipped_into_failed(self, counts: dict[str, int]) -> dict[str, int]:
        merged = dict(counts)
        skipped_count = merged.pop("skipped", 0)
        if skipped_count:
            merged["failed"] = merged.get("failed", 0) + skipped_count
        return merged

    def _task_status_from_items(self, items: list[dict[str, Any]]) -> str | None:
        if not items:
            return None
        statuses = {item.get("status") or "pending" for item in items}
        if statuses == {"imported"}:
            return "imported"
        if statuses == {"skipped"}:
            return "skipped"
        if statuses == {"failed"}:
            return "failed"
        if "pending" in statuses:
            return "pending"
        if "failed" in statuses:
            return "partial"
        return next(iter(statuses))

    def _page(self, page: int, size: int) -> tuple[int, int, int]:
        page = max(page, 1)
        size = min(max(size, 1), 100)
        return page, size, (page - 1) * size

    async def _init_merchant_from_ozon(self, *, credentials: OzonCredentials) -> dict[str, Any]:
        warehouse_data: dict[str, Any] = {}
        warehouse_error: str | None = None

        seller_data = await self.forwarder.post(OzonEndpoint.SELLER_INFO, {}, credentials)

        seller = self._seller_info(seller_data)
        try:
            warehouse_data = await self.forwarder.post(
                OzonEndpoint.WAREHOUSE_LIST,
                {"cursor": "", "limit": 1, "warehouse_ids": []},
                credentials,
            )
        except ServiceError as exc:
            warehouse_error = exc.message

        warehouse = self._first_warehouse(warehouse_data)
        if warehouse:
            self.stocks.upsert_warehouse(client_id=credentials.client_id, warehouse=warehouse)

        merchant_id = str(
            seller.get("company_id")
            or seller.get("seller_id")
            or seller.get("id")
            or credentials.client_id
        )
        shop_name = str(
            seller.get("name")
            or seller.get("company_name")
            or seller.get("seller_name")
            or f"Ozon 店铺 {credentials.client_id}"
        )
        default_warehouse_id = self._warehouse_id(warehouse)

        self.merchants.upsert_from_ozon(
            merchant_id=merchant_id,
            client_id=credentials.client_id,
            shop_name=shop_name,
            display_name=shop_name,
            currency_code=seller.get("currency_code"),
            default_warehouse_id=default_warehouse_id,
            api_key_fingerprint=credentials.api_key_fingerprint,
            last_error=warehouse_error,
        )
        merchant = self.merchants.get_by_client_id(client_id=credentials.client_id)
        if merchant is None:
            raise ServiceError("Merchant initialization failed", status_code=500)
        return merchant

    def _seller_info(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.get("result")
        if isinstance(result, dict):
            return result
        return data if isinstance(data, dict) else {}

    def _first_warehouse(self, data: dict[str, Any]) -> dict[str, Any] | None:
        warehouses = data.get("warehouses")
        if isinstance(warehouses, list) and warehouses:
            first = warehouses[0]
            return first if isinstance(first, dict) else None
        result = data.get("result")
        if isinstance(result, list) and result:
            first = result[0]
            return first if isinstance(first, dict) else None
        return None

    def _warehouse_id(self, warehouse: dict[str, Any] | None) -> int | None:
        if not warehouse:
            return None
        value = warehouse.get("warehouse_id")
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
