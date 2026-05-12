from typing import Any
from uuid import uuid4

from app.clients.ozon_endpoints import OzonEndpoint
from app.core.security import OzonCredentials
from app.repositories.stocks import ProductStockRepository, StockTaskItemRepository, StockTaskRepository
from app.services.business_events import BusinessEventLogger
from app.services.ozon_forwarder import OzonForwarder
from app.services.product_archive import compact_payload, item_product_id, item_sku, response_items


def result_items(data: dict[str, Any], key: str = "result") -> list[dict[str, Any]]:
    value = data.get(key)
    return value if isinstance(value, list) else []


def warehouse_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    return result_items(data, key="warehouses")


class ProductStockService:
    def __init__(
        self,
        *,
        forwarder: OzonForwarder | None = None,
        tasks: StockTaskRepository | None = None,
        task_items: StockTaskItemRepository | None = None,
        stocks: ProductStockRepository | None = None,
        events: BusinessEventLogger | None = None,
    ) -> None:
        self.forwarder = forwarder or OzonForwarder()
        self.tasks = tasks or StockTaskRepository()
        self.task_items = task_items or StockTaskItemRepository()
        self.stocks = stocks or ProductStockRepository()
        self.events = events or BusinessEventLogger()

    async def list_warehouses(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        request_payload = self._warehouse_list_payload(payload)
        self.events.emit(
            client_id=credentials.client_id,
            event_type="warehouse_query",
            status="pending",
            message="开始查询可用仓库",
            payload=request_payload,
        )
        try:
            data = await self.forwarder.post(OzonEndpoint.WAREHOUSE_LIST, request_payload, credentials)
            warehouses = warehouse_items(data)
            for warehouse in warehouses:
                self.stocks.upsert_warehouse(client_id=credentials.client_id, warehouse=warehouse)
            self.events.emit(
                client_id=credentials.client_id,
                event_type="warehouse_query",
                status="success",
                message=f"可用仓库查询完成，返回 {len(warehouses)} 个仓库",
                payload={"count": len(warehouses), "request": request_payload},
            )
            return data
        except Exception as exc:
            self.events.emit(
                client_id=credentials.client_id,
                event_type="warehouse_query",
                status="failed",
                message="可用仓库查询失败",
                error_message=str(exc),
                payload=request_payload,
            )
            raise

    async def products_stocks(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        request_payload = {
            "stocks": [
                {
                    "offer_id": payload["offer_id"],
                    "warehouse_id": payload["warehouse_id"],
                    "stock": payload["stock"],
                }
            ]
        }
        self.events.emit(
            client_id=credentials.client_id,
            event_type="stock_update",
            status="pending",
            message="开始转发商品库存更新",
            offer_id=str(payload["offer_id"]),
            payload=request_payload,
        )
        try:
            data = await self.forwarder.post(OzonEndpoint.PRODUCTS_STOCKS_UPDATE, request_payload, credentials)
            self.events.emit(
                client_id=credentials.client_id,
                event_type="stock_update",
                status="success",
                message="商品库存更新转发完成",
                offer_id=str(payload["offer_id"]),
                payload=request_payload,
            )
            return data
        except Exception as exc:
            self.events.emit(
                client_id=credentials.client_id,
                event_type="stock_update",
                status="failed",
                message="商品库存更新转发失败",
                offer_id=str(payload["offer_id"]),
                error_message=str(exc),
                payload=request_payload,
            )
            raise

    async def update_stocks(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        request_id = str(uuid4())
        stock_rows = payload.get("stocks") or []
        task_id = self.tasks.insert(
            client_id=credentials.client_id,
            request_id=request_id,
            status="pending",
            request_payload=payload,
            total_count=len(stock_rows),
        )
        self.events.emit(
            client_id=credentials.client_id,
            event_type="stock_update",
            status="pending",
            message="库存更新任务已建立，开始处理",
            ref_type="stock_task",
            ref_id=task_id,
            request_id=request_id,
            payload={"total": len(stock_rows)},
        )

        try:
            requested_warehouse_ids = list(dict.fromkeys(int(row["warehouse_id"]) for row in stock_rows))
            self.events.emit(
                client_id=credentials.client_id,
                event_type="stock_update",
                status="pending",
                message="开始校验库存更新仓库",
                ref_type="stock_task",
                ref_id=task_id,
                request_id=request_id,
                payload={"warehouse_ids": requested_warehouse_ids},
            )
            warehouse_data = await self.forwarder.post(
                OzonEndpoint.WAREHOUSE_LIST,
                self._warehouse_list_payload({"warehouse_ids": requested_warehouse_ids}),
                credentials,
                request_id,
            )
            warehouse_ids = {int(item["warehouse_id"]) for item in warehouse_items(warehouse_data) if item.get("warehouse_id") is not None}
            for warehouse in warehouse_items(warehouse_data):
                self.stocks.upsert_warehouse(client_id=credentials.client_id, warehouse=warehouse)
            self.events.emit(
                client_id=credentials.client_id,
                event_type="stock_update",
                status="success",
                message=f"库存更新仓库校验完成，有效仓库 {len(warehouse_ids)} 个",
                ref_type="stock_task",
                ref_id=task_id,
                request_id=request_id,
                payload={"warehouse_count": len(warehouse_ids)},
            )

            offer_ids = list(dict.fromkeys(row["offer_id"] for row in stock_rows if row.get("offer_id")))
            product_query = compact_payload({"offer_id": offer_ids})
            self.events.emit(
                client_id=credentials.client_id,
                event_type="stock_update",
                status="pending",
                message="开始查询库存更新商品信息",
                ref_type="stock_task",
                ref_id=task_id,
                request_id=request_id,
                payload=product_query,
            )
            product_data = (
                await self.forwarder.post(OzonEndpoint.PRODUCT_INFO_LIST, product_query, credentials, request_id)
                if product_query
                else {}
            )
            products = response_items(product_data)
            by_offer = {item.get("offer_id"): item for item in products if item.get("offer_id")}
            self.events.emit(
                client_id=credentials.client_id,
                event_type="stock_update",
                status="success",
                message=f"库存更新商品信息查询完成，匹配到 {len(by_offer)} 个商品",
                ref_type="stock_task",
                ref_id=task_id,
                request_id=request_id,
                payload={"found": len(by_offer), "requested": len(offer_ids)},
            )

            operation_items = self._build_operation_items(stock_rows, by_offer, warehouse_ids)

            update_payload = {
                "stocks": [
                    self._to_ozon_stock_payload(item)
                    for item in operation_items
                    if item["status"] == "pending"
                ]
            }
            update_data: dict[str, Any] = {"result": [], "skipped": True}
            if update_payload["stocks"]:
                self.events.emit(
                    client_id=credentials.client_id,
                    event_type="stock_update",
                    status="pending",
                    message=f"开始提交库存更新，数量 {len(update_payload['stocks'])}",
                    ref_type="stock_task",
                    ref_id=task_id,
                    request_id=request_id,
                    payload={"count": len(update_payload["stocks"])},
                )
                update_data = await self.forwarder.post(OzonEndpoint.PRODUCTS_STOCKS_UPDATE, update_payload, credentials, request_id)
                self.events.emit(
                    client_id=credentials.client_id,
                    event_type="stock_update",
                    status="success",
                    message=f"库存更新提交完成，数量 {len(update_payload['stocks'])}",
                    ref_type="stock_task",
                    ref_id=task_id,
                    request_id=request_id,
                    payload={"count": len(update_payload["stocks"])},
                )
            else:
                self.events.emit(
                    client_id=credentials.client_id,
                    event_type="stock_update",
                    status="skipped",
                    message="没有可提交的库存更新商品",
                    ref_type="stock_task",
                    ref_id=task_id,
                    request_id=request_id,
                    payload={"total": len(stock_rows)},
                )

            confirm_data: dict[str, Any] = {}
            if payload.get("confirm", True):
                self.events.emit(
                    client_id=credentials.client_id,
                    event_type="stock_update",
                    status="pending",
                    message="开始确认库存更新结果",
                    ref_type="stock_task",
                    ref_id=task_id,
                    request_id=request_id,
                )
                confirm_data = await self._confirm_product_stocks(operation_items, credentials, request_id)
                self.events.emit(
                    client_id=credentials.client_id,
                    event_type="stock_update",
                    status="success",
                    message="库存更新结果确认完成",
                    ref_type="stock_task",
                    ref_id=task_id,
                    request_id=request_id,
                    payload={"confirm": bool(confirm_data)},
                )

            final_items = self._build_final_items(
                operation_items,
                update_data,
            )
            counts = self._counts(final_items)
            status = self._batch_status(counts)

            for item in final_items:
                db_item = {
                    **item,
                    "stock_task_id": task_id,
                    "reserved_payload": None,
                    "response_payload": update_data,
                    "confirm_payload": confirm_data,
                }
                self.task_items.insert(client_id=credentials.client_id, stock_task_id=task_id, request_id=request_id, item=db_item)
                self.stocks.upsert_stock(client_id=credentials.client_id, item=db_item)
                self._emit_item_event(credentials.client_id, task_id, request_id, item)

            self.tasks.finish(
                task_id=task_id,
                client_id=credentials.client_id,
                status=status,
                warehouse_payload=warehouse_data,
                product_payload=product_data,
                reserved_payload={},
                response_payload=update_data,
                confirm_payload={"product": confirm_data},
                error_payload=None,
                success_count=counts["success"],
                failed_count=counts["failed"],
            )
            self.events.emit(
                client_id=credentials.client_id,
                event_type="stock_update",
                status="success" if status == "success" else "failed",
                message=f"库存更新处理完成：成功 {counts['success']}，失败 {counts['failed']}",
                ref_type="stock_task",
                ref_id=task_id,
                request_id=request_id,
                payload={"status": status, "counts": counts},
            )

            return {
                "request_id": request_id,
                "stock_task_id": task_id,
                "status": status,
                "total_count": len(final_items),
                "success_count": counts["success"],
                "failed_count": counts["failed"],
                "warehouse_result": warehouse_data,
                "product_result": product_data,
                "reserved_result": {},
                "update_result": update_data,
                "confirm_result": {"product": confirm_data},
                "items": [
                    {key: value for key, value in item.items() if key not in {"precheck_payload"}}
                    for item in final_items
                ],
            }
        except Exception as exc:
            self.tasks.finish(
                task_id=task_id,
                client_id=credentials.client_id,
                status="failed",
                warehouse_payload=None,
                product_payload=None,
                reserved_payload=None,
                response_payload=None,
                confirm_payload=None,
                error_payload={"message": str(exc)},
                success_count=0,
                failed_count=len(stock_rows),
            )
            self.events.emit(
                client_id=credentials.client_id,
                event_type="stock_update",
                status="failed",
                message="库存更新处理失败",
                ref_type="stock_task",
                ref_id=task_id,
                request_id=request_id,
                error_message=str(exc),
                payload={"total": len(stock_rows)},
            )
            raise

    def _emit_item_event(self, client_id: str, task_id: int, request_id: str, item: dict[str, Any]) -> None:
        if item.get("status") == "success":
            status = "success"
            message = "商品库存更新完成"
        else:
            status = "failed"
            message = "商品库存更新失败"
        self.events.emit(
            client_id=client_id,
            event_type="stock_update",
            status=status,
            message=message,
            ref_type="stock_task",
            ref_id=task_id,
            request_id=request_id,
            offer_id=item.get("offer_id"),
            product_id=item.get("product_id"),
            sku=item.get("sku"),
            error_message=item.get("error_message"),
            payload={key: value for key, value in item.items() if key != "precheck_payload"},
        )

    def _build_operation_items(
        self,
        stock_rows: list[dict[str, Any]],
        by_offer: dict[str, dict[str, Any]],
        warehouse_ids: set[int],
    ) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        for row in stock_rows:
            product = by_offer.get(row.get("offer_id"))
            product_id = item_product_id(product or {})
            sku = item_sku(product or {})
            warehouse_id = int(row["warehouse_id"])
            error = None
            if warehouse_id not in warehouse_ids:
                error = "warehouse_id 不在 /v2/warehouse/list 返回的仓库列表中"
            if not row.get("offer_id"):
                error = "缺少 offer_id"
            elif not product:
                error = "商品信息查询未返回该 offer_id"
            items.append(
                {
                    "offer_id": row.get("offer_id") or (product or {}).get("offer_id"),
                    "product_id": product_id,
                    "sku": sku,
                    "warehouse_id": warehouse_id,
                    "requested_stock": int(row["stock"]),
                    "present": None,
                    "reserved": None,
                    "updated": False,
                    "status": "failed" if error else "pending",
                    "error_message": error,
                    "precheck_payload": product,
                }
            )
        return items

    def _to_ozon_stock_payload(self, item: dict[str, Any]) -> dict[str, Any]:
        return {
            "offer_id": item["offer_id"],
            "stock": item["requested_stock"],
            "warehouse_id": item["warehouse_id"],
        }

    def _warehouse_list_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        warehouse_ids = list(dict.fromkeys(payload.get("warehouse_ids") or []))
        limit = payload.get("limit") or (len(warehouse_ids) if warehouse_ids else 200)
        return {
            "cursor": payload.get("cursor") or "",
            "limit": min(max(int(limit), 1), 200),
            "warehouse_ids": [str(value) for value in warehouse_ids],
        }

    async def _confirm_product_stocks(
        self,
        operation_items: list[dict[str, Any]],
        credentials: OzonCredentials,
        request_id: str,
    ) -> dict[str, Any]:
        offer_ids = list(dict.fromkeys(item["offer_id"] for item in operation_items if item.get("offer_id")))
        product_ids = list(dict.fromkeys(str(item["product_id"]) for item in operation_items if item.get("product_id") is not None))
        if not offer_ids and not product_ids:
            return {}
        return await self.forwarder.post(
            OzonEndpoint.PRODUCT_INFO_STOCKS,
            {
                "filter": compact_payload({"offer_id": offer_ids, "product_id": product_ids}),
                "limit": min(max(len(offer_ids) + len(product_ids), 1), 1000),
            },
            credentials,
            request_id,
        )

    def _build_final_items(
        self,
        operation_items: list[dict[str, Any]],
        update_data: dict[str, Any],
    ) -> list[dict[str, Any]]:
        update_by_key: dict[tuple[str, str, int], dict[str, Any]] = {}
        for result in result_items(update_data):
            warehouse_id = int(result.get("warehouse_id") or 0)
            if result.get("offer_id"):
                update_by_key[("offer_id", str(result["offer_id"]), warehouse_id)] = result
            if result.get("product_id") is not None:
                update_by_key[("product_id", str(result["product_id"]), warehouse_id)] = result

        for item in operation_items:
            if item["status"] == "failed":
                continue

            result = None
            if item.get("offer_id"):
                result = update_by_key.get(("offer_id", str(item["offer_id"]), item["warehouse_id"]))
            if not result and item.get("product_id") is not None:
                result = update_by_key.get(("product_id", str(item["product_id"]), item["warehouse_id"]))

            errors = result.get("errors") if result else None
            item["updated"] = bool(result and result.get("updated") and not errors)
            item["status"] = "success" if item["updated"] else "failed"
            item["error_message"] = self._error_message(errors) if errors else (None if item["updated"] else "Ozon 未返回更新成功")
        return operation_items

    def _error_message(self, errors: Any) -> str | None:
        if not errors:
            return None
        if isinstance(errors, list):
            return "; ".join(str(error.get("message") or error.get("code") or error) for error in errors)
        return str(errors)

    def _counts(self, items: list[dict[str, Any]]) -> dict[str, int]:
        success = sum(1 for item in items if item["status"] == "success")
        failed = sum(1 for item in items if item["status"] == "failed")
        return {"success": success, "failed": failed}

    def _batch_status(self, counts: dict[str, int]) -> str:
        if counts["success"] and counts["failed"]:
            return "partial"
        if counts["failed"]:
            return "failed"
        return "success"
