import logging
from copy import deepcopy
from typing import Any

from app.clients.ozon_endpoints import OzonEndpoint
from app.core.exceptions import ServiceError
from app.core.security import OzonCredentials
from app.repositories.merchant import TaskEventRepository
from app.repositories.products import ProductRepository
from app.repositories.stocks import ProductStockRepository
from app.repositories.tasks import ImportTaskItemRepository, ImportTaskRepository
from app.services.credential_store import CredentialStore
from app.services.ozon_forwarder import OzonForwarder
from app.utils.json import loads

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
        stocks: ProductStockRepository | None = None,
    ) -> None:
        self.forwarder = forwarder or OzonForwarder()
        self.products = products or ProductRepository()
        self.tasks = tasks or ImportTaskRepository()
        self.task_items = task_items or ImportTaskItemRepository()
        self.credentials = credentials or CredentialStore()
        self.events = events or TaskEventRepository()
        self.stocks = stocks or ProductStockRepository()

    async def import_products(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        payload = self._normalize_import_payload(payload)
        ozon_payload = self._ozon_import_payload(payload)
        self._safe_event(
            client_id=credentials.client_id,
            event_type="product_import",
            status="pending",
            message="开始查询商品创建额度",
            ref_type="import_task",
            payload={"total": len(payload.get("items") or [])},
        )
        for item in payload.get("items") or []:
            self.products.upsert_from_import_item(
                client_id=credentials.client_id,
                item=item,
                status="pending",
            )
        await self._sync_warehouses_for_stock_rows(
            task_id=None,
            stock_rows=self._warehouse_rows_from_request_payload(payload),
            credentials=credentials,
        )
        try:
            limit_data = await self.forwarder.post(OzonEndpoint.PRODUCT_INFO_LIMIT, {}, credentials)
        except ServiceError as exc:
            for item in payload.get("items") or []:
                failed_item = {
                    **item,
                    "status": "failed",
                    "errors": [{"message": exc.message, "detail": exc.detail}],
                }
                self.products.update_from_task_item(client_id=credentials.client_id, item=failed_item)
                self._safe_event(
                    client_id=credentials.client_id,
                    event_type="product_import",
                    status="failed",
                    message="商品创建额度查询失败，商品数据未推送至 Ozon",
                    ref_type="import_task",
                    offer_id=item.get("offer_id"),
                    error_message=exc.message,
                    payload={"item": item, "error": exc.detail},
                )
            raise
        self._safe_event(
            client_id=credentials.client_id,
            event_type="product_import",
            status="success",
            message="商品创建额度查询完成",
            ref_type="import_task",
            payload={"total": len(payload.get("items") or [])},
        )
        try:
            import_data = await self.forwarder.post(OzonEndpoint.PRODUCT_IMPORT, ozon_payload, credentials)
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
                workflow_status="import_pending",
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
        request_payload = self._task_request_payload(task) if task else {}

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
        post_process: dict[str, Any] = {}
        post_process_errors: list[dict[str, Any]] = []
        workflow_status = self._workflow_status_from_import_status(status)
        for item in result.get("items") or []:
            item = self._enrich_item_stock_config(item, request_payload)
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

        if status == "imported":
            self.tasks.update_workflow_status(
                client_id=credentials.client_id,
                task_id=task_id,
                workflow_status="imported",
            )
            workflow_status = "completed"
        if status == "imported" and self._should_run_post_process(task, result.get("items") or []):
            try:
                post_process = await self._run_post_import_flow(
                    task=task,
                    task_id=task_id,
                    import_items=result.get("items") or [],
                    credentials=polling_credentials,
                )
                workflow_status = str(post_process.get("workflow_status") or workflow_status)
            except Exception as exc:
                workflow_status = "failed"
                post_process_errors.append({"message": str(exc)})
                self.tasks.update_workflow_status(
                    client_id=credentials.client_id,
                    task_id=task_id,
                    workflow_status="failed",
                    error_payload={"stage": "post_process", "message": str(exc)},
                )
                self._safe_event(
                    client_id=credentials.client_id,
                    event_type="product_import_postprocess",
                    status="failed",
                    message="导入后处理失败",
                    ref_type="import_task",
                    ozon_task_id=task_id,
                    error_message=str(exc),
                    payload={"task_id": task_id},
                )

        result_payload = data if not post_process else {"import_info": data, "post_process": post_process}
        error_payload = errors or None
        if post_process_errors:
            error_payload = {"import_errors": errors, "post_process_errors": post_process_errors}
        self.tasks.update_result(
            client_id=credentials.client_id,
            task_id=task_id,
            status=status,
            result_payload=result_payload,
            error_payload=error_payload,
            workflow_status=workflow_status,
        )
        return {"task_id": task_id, "status": status, "workflow_status": workflow_status, "data": data}

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

    def _normalize_import_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        normalized = deepcopy(payload)
        normalized["items"] = [dict(item) for item in normalized.get("items") or []]
        return normalized

    def _ozon_import_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        ozon_payload = deepcopy(payload)
        ozon_payload.pop("warehouse_id", None)
        ozon_payload.pop("stock", None)
        ozon_payload["items"] = [
            {key: value for key, value in item.items() if key not in {"warehouse_id", "stock"}}
            for item in ozon_payload.get("items") or []
        ]
        return ozon_payload

    def _should_run_post_process(self, task: dict[str, Any] | None, import_items: list[dict[str, Any]]) -> bool:
        if not task or not task.get("request_payload"):
            return False

        result_payload = task.get("result_payload")
        if isinstance(result_payload, str) and result_payload:
            result_payload = loads(result_payload) or {}
        if isinstance(result_payload, dict) and result_payload.get("post_process"):
            return False

        request_payload = self._task_request_payload(task)
        stock_rows = self._stock_rows_for_imported_items(request_payload, import_items)
        if not stock_rows:
            return task.get("workflow_status") not in {"completed", "failed"}
        if task.get("workflow_status") in {"stock_updated", "attributes_synced", "stock_synced"}:
            return False
        if task.get("workflow_status") == "failed":
            return not bool(result_payload and isinstance(result_payload, dict) and result_payload.get("post_process"))
        return True

    async def _run_post_import_flow(
        self,
        *,
        task: dict[str, Any],
        task_id: int,
        import_items: list[dict[str, Any]],
        credentials: OzonCredentials,
    ) -> dict[str, Any]:
        request_payload = self._task_request_payload(task)
        stock_rows = self._stock_rows_for_imported_items(request_payload, import_items)
        if not stock_rows:
            self._safe_event(
                client_id=credentials.client_id,
                event_type="product_import_postprocess",
                status="skipped",
                message="导入后未配置仓库或库存，跳过库存设置",
                ref_type="import_task",
                ozon_task_id=task_id,
                payload={"task_id": task_id},
            )
            self.tasks.update_workflow_status(
                client_id=credentials.client_id,
                task_id=task_id,
                workflow_status="completed",
            )
            return {"workflow_status": "completed", "stock": {"skipped": True}, "attributes": {}, "stock_query": {}}

        await self._sync_warehouses_for_stock_rows(
            task_id=task_id,
            stock_rows=stock_rows,
            credentials=credentials,
        )
        stock_result = await self._set_imported_product_stocks(
            task_id=task_id,
            stock_rows=stock_rows,
            credentials=credentials,
        )
        success_rows = stock_result["success_rows"]
        if len(success_rows) != len(stock_rows):
            detail = {
                "stage": "stock_update",
                "success": len(success_rows),
                "failed": len(stock_rows) - len(success_rows),
                "response": stock_result["data"],
            }
            self.tasks.update_workflow_status(
                client_id=credentials.client_id,
                task_id=task_id,
                workflow_status="failed",
                error_payload=detail,
            )
            raise ServiceError("Imported product stock update was not fully successful", status_code=502, detail=detail)

        self.tasks.update_workflow_status(
            client_id=credentials.client_id,
            task_id=task_id,
            workflow_status="stock_updated",
        )

        attributes_result = await self._query_and_store_attributes(
            task_id=task_id,
            stock_rows=success_rows,
            credentials=credentials,
        )
        self.tasks.update_workflow_status(
            client_id=credentials.client_id,
            task_id=task_id,
            workflow_status="attributes_synced",
        )
        stock_query_result = await self._query_and_store_stock_snapshot(
            task_id=task_id,
            stock_rows=success_rows,
            credentials=credentials,
        )
        self._emit_import_completion_card(
            task_id=task_id,
            stock_rows=success_rows,
            credentials=credentials,
        )
        self.tasks.update_workflow_status(
            client_id=credentials.client_id,
            task_id=task_id,
            workflow_status="stock_synced",
        )
        self.tasks.update_workflow_status(
            client_id=credentials.client_id,
            task_id=task_id,
            workflow_status="completed",
        )
        return {
            "workflow_status": "completed",
            "stock": stock_result["data"],
            "attributes": attributes_result,
            "stock_query": stock_query_result,
        }

    def _emit_import_completion_card(
        self,
        *,
        task_id: int,
        stock_rows: list[dict[str, Any]],
        credentials: OzonCredentials,
    ) -> None:
        offer_ids = list(dict.fromkeys(row["offer_id"] for row in stock_rows if row.get("offer_id")))
        products = self.products.list_completion_cards(client_id=credentials.client_id, offer_ids=offer_ids)
        if not products:
            return
        self._safe_event(
            client_id=credentials.client_id,
            event_type="product_import_completion",
            status="success",
            message="商品推送完整链路完成",
            ref_type="import_task",
            ozon_task_id=task_id,
            payload={"task_id": task_id, "products": self._json_safe(products)},
        )

    def _json_safe(self, value: Any) -> Any:
        if isinstance(value, list):
            return [self._json_safe(item) for item in value]
        if isinstance(value, dict):
            return {key: self._json_safe(item) for key, item in value.items()}
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)

    async def _sync_warehouses_for_stock_rows(
        self,
        *,
        task_id: int | None,
        stock_rows: list[dict[str, Any]],
        credentials: OzonCredentials,
    ) -> None:
        warehouse_ids = list(dict.fromkeys(row["warehouse_id"] for row in stock_rows if row.get("warehouse_id")))
        if not warehouse_ids:
            return

        payload = {
            "cursor": "",
            "limit": min(max(len(warehouse_ids), 1), 200),
            "warehouse_ids": [str(value) for value in warehouse_ids],
        }
        self._safe_event(
            client_id=credentials.client_id,
            event_type="warehouse_query",
            status="pending",
            message="开始同步导入商品仓库信息",
            ref_type="import_task",
            ozon_task_id=task_id,
            payload={"warehouse_ids": warehouse_ids},
        )
        try:
            data = await self.forwarder.post(OzonEndpoint.WAREHOUSE_LIST, payload, credentials)
        except Exception as exc:
            self._safe_event(
                client_id=credentials.client_id,
                event_type="warehouse_query",
                status="failed",
                message="导入商品仓库信息同步失败",
                ref_type="import_task",
                ozon_task_id=task_id,
                error_message=str(exc),
                payload={"warehouse_ids": warehouse_ids},
            )
            return

        warehouses = self._warehouse_items(data)
        for warehouse in warehouses:
            self.stocks.upsert_warehouse(client_id=credentials.client_id, warehouse=warehouse)
        self._safe_event(
            client_id=credentials.client_id,
            event_type="warehouse_query",
            status="success",
            message=f"导入商品仓库信息同步完成，返回 {len(warehouses)} 个仓库",
            ref_type="import_task",
            ozon_task_id=task_id,
            payload={"warehouse_ids": warehouse_ids, "returned": len(warehouses)},
        )

    def _warehouse_rows_from_request_payload(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for item in payload.get("items") or []:
            warehouse_id = item.get("warehouse_id")
            if warehouse_id is None:
                continue
            rows.append(
                {
                    "offer_id": item.get("offer_id"),
                    "warehouse_id": int(warehouse_id),
                    "stock": item.get("stock"),
                }
            )
        return rows

    def _task_request_payload(self, task: dict[str, Any]) -> dict[str, Any]:
        payload = task.get("request_payload")
        if isinstance(payload, dict):
            return payload
        if isinstance(payload, str) and payload:
            return loads(payload) or {}
        return {}

    def _enrich_item_stock_config(self, item: dict[str, Any], request_payload: dict[str, Any]) -> dict[str, Any]:
        offer_id = item.get("offer_id")
        if not offer_id:
            return item
        normalized_payload = self._normalize_import_payload(request_payload)
        request_item = next(
            (
                row
                for row in normalized_payload.get("items") or []
                if str(row.get("offer_id")) == str(offer_id)
            ),
            {},
        )
        if not request_item:
            return item
        enriched = dict(item)
        if request_item.get("warehouse_id") is not None:
            enriched["warehouse_id"] = request_item.get("warehouse_id")
        if request_item.get("stock") is not None:
            enriched["stock"] = request_item.get("stock")
        return enriched

    def _stock_rows_for_imported_items(
        self,
        request_payload: dict[str, Any],
        import_items: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        normalized_payload = self._normalize_import_payload(request_payload)
        requested_by_offer = {
            str(item.get("offer_id")): item
            for item in normalized_payload.get("items") or []
            if item.get("offer_id")
        }
        rows: list[dict[str, Any]] = []
        for item in import_items:
            if normalized_import_item_status(item) != "imported":
                continue
            offer_id = item.get("offer_id")
            if not offer_id:
                continue
            request_item = requested_by_offer.get(str(offer_id)) or {}
            warehouse_id = request_item.get("warehouse_id")
            stock = request_item.get("stock")
            if warehouse_id is None or stock is None:
                continue
            rows.append(
                {
                    "offer_id": str(offer_id),
                    "product_id": self._as_int(item.get("product_id")),
                    "sku": self._as_int(item.get("sku")),
                    "warehouse_id": int(warehouse_id),
                    "stock": int(stock),
                }
            )
        return rows

    async def _set_imported_product_stocks(
        self,
        *,
        task_id: int,
        stock_rows: list[dict[str, Any]],
        credentials: OzonCredentials,
    ) -> dict[str, Any]:
        payload = {
            "stocks": [
                {
                    "offer_id": row["offer_id"],
                    "warehouse_id": row["warehouse_id"],
                    "stock": row["stock"],
                }
                for row in stock_rows
            ]
        }
        self._safe_event(
            client_id=credentials.client_id,
            event_type="stock_update",
            status="pending",
            message="开始设置导入商品库存",
            ref_type="import_task",
            ozon_task_id=task_id,
            payload={"count": len(stock_rows)},
        )
        try:
            data = await self.forwarder.post(OzonEndpoint.PRODUCTS_STOCKS_UPDATE, payload, credentials)
        except Exception as exc:
            self._safe_event(
                client_id=credentials.client_id,
                event_type="stock_update",
                status="failed",
                message="导入商品库存设置失败",
                ref_type="import_task",
                ozon_task_id=task_id,
                error_message=str(exc),
                payload={"count": len(stock_rows)},
            )
            raise

        result_items = self._response_items(data)
        success_rows: list[dict[str, Any]] = []
        for row in stock_rows:
            result = self._match_stock_update_result(result_items, row)
            errors = result.get("errors") if result else None
            updated = bool(result and result.get("updated") and not has_import_errors(errors))
            status = "success" if updated else "failed"
            error_message = self._error_message(errors) if errors else (None if updated else "Ozon 未返回库存更新成功")
            db_item = {
                **row,
                "requested_stock": row["stock"],
                "updated": updated,
                "status": status,
                "error_message": error_message,
                "response_payload": data,
            }
            self.stocks.upsert_stock(client_id=credentials.client_id, item=db_item)
            self._safe_event(
                client_id=credentials.client_id,
                event_type="stock_update",
                status=status,
                message="导入商品库存设置完成" if updated else "导入商品库存设置失败",
                ref_type="import_task",
                ozon_task_id=task_id,
                offer_id=row["offer_id"],
                product_id=row.get("product_id"),
                sku=row.get("sku"),
                error_message=error_message,
                payload=db_item,
            )
            if updated:
                success_rows.append(row)

        self._safe_event(
            client_id=credentials.client_id,
            event_type="stock_update",
            status="success" if len(success_rows) == len(stock_rows) else "failed",
            message=f"导入商品库存设置处理完成：成功 {len(success_rows)}，失败 {len(stock_rows) - len(success_rows)}",
            ref_type="import_task",
            ozon_task_id=task_id,
            payload={"success": len(success_rows), "failed": len(stock_rows) - len(success_rows)},
        )
        return {"data": data, "success_rows": success_rows}

    async def _query_and_store_attributes(
        self,
        *,
        task_id: int,
        stock_rows: list[dict[str, Any]],
        credentials: OzonCredentials,
    ) -> dict[str, Any]:
        offer_ids = list(dict.fromkeys(row["offer_id"] for row in stock_rows))
        payload = {"filter": {"offer_id": offer_ids}, "limit": min(max(len(offer_ids), 1), 1000), "last_id": ""}
        self._safe_event(
            client_id=credentials.client_id,
            event_type="product_attributes_query",
            status="pending",
            message="开始查询商品已填写属性",
            ref_type="import_task",
            ozon_task_id=task_id,
            payload={"count": len(offer_ids)},
        )
        try:
            data = await self.forwarder.post(OzonEndpoint.PRODUCT_INFO_ATTRIBUTES, payload, credentials)
        except Exception as exc:
            self._safe_event(
                client_id=credentials.client_id,
                event_type="product_attributes_query",
                status="failed",
                message="商品已填写属性查询失败",
                ref_type="import_task",
                ozon_task_id=task_id,
                error_message=str(exc),
                payload={"count": len(offer_ids)},
            )
            raise

        items = self._response_items(data)
        for item in items:
            count = self.products.replace_attributes_from_info_item(client_id=credentials.client_id, item=item)
            self._safe_event(
                client_id=credentials.client_id,
                event_type="product_attributes_query",
                status="success",
                message=f"商品已填写属性查询完成，属性 {count} 条",
                ref_type="import_task",
                ozon_task_id=task_id,
                offer_id=item.get("offer_id"),
                product_id=self._as_int(item.get("id") or item.get("product_id")),
                sku=self._as_int(item.get("sku")),
                payload={"attribute_count": count},
            )

        self._safe_event(
            client_id=credentials.client_id,
            event_type="product_attributes_query",
            status="success",
            message=f"商品已填写属性批量查询完成，返回 {len(items)} 个商品",
            ref_type="import_task",
            ozon_task_id=task_id,
            payload={"requested": len(offer_ids), "returned": len(items)},
        )
        return data

    async def _query_and_store_stock_snapshot(
        self,
        *,
        task_id: int,
        stock_rows: list[dict[str, Any]],
        credentials: OzonCredentials,
    ) -> dict[str, Any]:
        offer_ids = list(dict.fromkeys(row["offer_id"] for row in stock_rows))
        product_ids = list(dict.fromkeys(str(row["product_id"]) for row in stock_rows if row.get("product_id") is not None))
        payload = {
            "filter": {key: value for key, value in {"offer_id": offer_ids, "product_id": product_ids}.items() if value},
            "limit": min(max(len(offer_ids) + len(product_ids), 1), 1000),
        }
        requested_by_offer = {row["offer_id"]: row for row in stock_rows}
        requested_by_product = {str(row["product_id"]): row for row in stock_rows if row.get("product_id") is not None}
        self._safe_event(
            client_id=credentials.client_id,
            event_type="stock_query",
            status="pending",
            message="开始查询商品库存",
            ref_type="import_task",
            ozon_task_id=task_id,
            payload={"count": len(offer_ids)},
        )
        try:
            data = await self.forwarder.post(OzonEndpoint.PRODUCT_INFO_STOCKS, payload, credentials)
        except Exception as exc:
            self._safe_event(
                client_id=credentials.client_id,
                event_type="stock_query",
                status="failed",
                message="商品库存查询失败",
                ref_type="import_task",
                ozon_task_id=task_id,
                error_message=str(exc),
                payload={"count": len(offer_ids)},
            )
            raise

        stored_count = 0
        for item in self._response_items(data):
            offer_id = item.get("offer_id")
            product_id = item.get("product_id") or item.get("id")
            requested = requested_by_offer.get(str(offer_id)) if offer_id else None
            if not requested and product_id is not None:
                requested = requested_by_product.get(str(product_id))
            for stock in item.get("stocks") or []:
                warehouse_id = stock.get("warehouse_id") or (requested or {}).get("warehouse_id")
                if warehouse_id is None:
                    continue
                snapshot = {
                    "offer_id": offer_id or (requested or {}).get("offer_id"),
                    "product_id": self._as_int(product_id) or (requested or {}).get("product_id"),
                    "sku": self._as_int(stock.get("sku")) or self._as_int(item.get("sku")) or (requested or {}).get("sku"),
                    "warehouse_id": int(warehouse_id),
                    "present": self._as_int(stock.get("present")),
                    "reserved": self._as_int(stock.get("reserved")),
                    "raw_stock": stock,
                    "confirm_payload": data,
                }
                self.stocks.upsert_stock_snapshot(client_id=credentials.client_id, item=snapshot)
                stored_count += 1

        self._safe_event(
            client_id=credentials.client_id,
            event_type="stock_query",
            status="success",
            message=f"商品库存查询完成，写入库存快照 {stored_count} 条",
            ref_type="import_task",
            ozon_task_id=task_id,
            payload={"requested": len(offer_ids), "stored": stored_count},
        )
        return data

    def _match_stock_update_result(self, result_items: list[dict[str, Any]], row: dict[str, Any]) -> dict[str, Any] | None:
        for item in result_items:
            if item.get("offer_id") and str(item.get("offer_id")) == row["offer_id"]:
                if not item.get("warehouse_id") or int(item.get("warehouse_id")) == row["warehouse_id"]:
                    return item
            if row.get("product_id") is not None and item.get("product_id") is not None:
                if int(item["product_id"]) == int(row["product_id"]):
                    if not item.get("warehouse_id") or int(item.get("warehouse_id")) == row["warehouse_id"]:
                        return item
        return None

    def _response_items(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        if isinstance(data.get("items"), list):
            return data["items"]
        if isinstance(data.get("result"), list):
            return data["result"]
        result = data.get("result")
        if isinstance(result, dict) and isinstance(result.get("items"), list):
            return result["items"]
        return []

    def _warehouse_items(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        if isinstance(data.get("warehouses"), list):
            return data["warehouses"]
        if isinstance(data.get("result"), list):
            return data["result"]
        result = data.get("result")
        if isinstance(result, dict) and isinstance(result.get("warehouses"), list):
            return result["warehouses"]
        return []

    def _as_int(self, value: Any) -> int | None:
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

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

    def _workflow_status_from_import_status(self, status: str) -> str:
        if status in {"pending", "running"}:
            return "import_pending"
        if status == "imported":
            return "imported"
        return "failed"

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
