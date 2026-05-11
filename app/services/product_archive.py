from typing import Any
from uuid import uuid4

from app.clients.ozon_endpoints import OzonEndpoint
from app.core.security import OzonCredentials
from app.repositories.archive import ArchiveTaskItemRepository, ArchiveTaskRepository, ProductArchiveStateRepository
from app.services.business_events import BusinessEventLogger
from app.services.ozon_forwarder import OzonForwarder


def compact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value}


def chunked(values: list[int], size: int) -> list[list[int]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def response_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(data.get("items"), list):
        return data["items"]
    result = data.get("result")
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return result["items"]
    return []


def item_product_id(item: dict[str, Any]) -> int | None:
    value = item.get("id") or item.get("product_id")
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def item_sku(item: dict[str, Any]) -> int | None:
    if item.get("sku") is not None:
        try:
            return int(item["sku"])
        except (TypeError, ValueError):
            return None

    sources = item.get("sources") or []
    if isinstance(sources, list):
        for source in sources:
            if isinstance(source, dict) and source.get("sku") is not None:
                try:
                    return int(source["sku"])
                except (TypeError, ValueError):
                    return None
    return None


class ProductArchiveService:
    def __init__(
        self,
        *,
        forwarder: OzonForwarder | None = None,
        tasks: ArchiveTaskRepository | None = None,
        task_items: ArchiveTaskItemRepository | None = None,
        states: ProductArchiveStateRepository | None = None,
        events: BusinessEventLogger | None = None,
    ) -> None:
        self.forwarder = forwarder or OzonForwarder()
        self.tasks = tasks or ArchiveTaskRepository()
        self.task_items = task_items or ArchiveTaskItemRepository()
        self.states = states or ProductArchiveStateRepository()
        self.events = events or BusinessEventLogger()

    async def archive_products(self, *, payload: dict[str, Any], credentials: OzonCredentials) -> dict[str, Any]:
        request_id = str(uuid4())
        offer_ids = list(dict.fromkeys(payload.get("offer_id") or []))
        confirm_enabled = bool(payload.get("confirm", True))
        input_identifiers = compact_payload({"offer_id": offer_ids})
        total_input_count = len(offer_ids)

        archive_task_id = self.tasks.insert(
            client_id=credentials.client_id,
            request_id=request_id,
            action_type="archive",
            status="pending",
            input_identifiers=input_identifiers,
            total_count=total_input_count,
        )
        self.events.emit(
            client_id=credentials.client_id,
            event_type="archive",
            status="pending",
            message="商品归档任务已建立，开始处理",
            ref_type="archive_task",
            ref_id=archive_task_id,
            request_id=request_id,
            payload={"offer_id": offer_ids, "total": total_input_count},
        )

        try:
            self.events.emit(
                client_id=credentials.client_id,
                event_type="archive",
                status="pending",
                message="开始查询待归档商品信息",
                ref_type="archive_task",
                ref_id=archive_task_id,
                request_id=request_id,
                payload=input_identifiers,
            )
            precheck_payload = compact_payload(
                {
                    "offer_id": offer_ids,
                }
            )
            precheck_data = await self.forwarder.post(OzonEndpoint.PRODUCT_INFO_LIST, precheck_payload, credentials, request_id)
            precheck_items = response_items(precheck_data)
            self.events.emit(
                client_id=credentials.client_id,
                event_type="archive",
                status="success",
                message=f"待归档商品信息查询完成，匹配到 {len(precheck_items)} 个商品",
                ref_type="archive_task",
                ref_id=archive_task_id,
                request_id=request_id,
                payload={"found": len(precheck_items), "requested": total_input_count},
            )
            operation_items = self._build_precheck_items(precheck_items)
            operation_items.extend(self._build_not_found_items(offer_ids, operation_items))

            target_ids = [
                item["product_id"]
                for item in operation_items
                if item.get("product_id") is not None and not item.get("before_is_archived") and item["status"] != "not_found"
            ]
            target_ids = list(dict.fromkeys(target_ids))

            archive_payload = {"product_id": target_ids}
            archive_data: dict[str, Any] = {"chunks": [], "skipped": True}
            operation_error: dict[str, Any] | None = None
            if target_ids:
                archive_data = {"chunks": []}
                for product_id_chunk in chunked(target_ids, 100):
                    self.events.emit(
                        client_id=credentials.client_id,
                        event_type="archive",
                        status="pending",
                        message=f"开始提交商品归档，数量 {len(product_id_chunk)}",
                        ref_type="archive_task",
                        ref_id=archive_task_id,
                        request_id=request_id,
                        payload={"product_id": product_id_chunk},
                    )
                    chunk_payload = {"product_id": product_id_chunk}
                    chunk_response = await self.forwarder.post(OzonEndpoint.PRODUCT_ARCHIVE, chunk_payload, credentials, request_id)
                    archive_data["chunks"].append({"request": chunk_payload, "response": chunk_response})
                    self.events.emit(
                        client_id=credentials.client_id,
                        event_type="archive",
                        status="success",
                        message=f"商品归档提交完成，数量 {len(product_id_chunk)}",
                        ref_type="archive_task",
                        ref_id=archive_task_id,
                        request_id=request_id,
                        payload={"product_id": product_id_chunk},
                    )
            else:
                self.events.emit(
                    client_id=credentials.client_id,
                    event_type="archive",
                    status="skipped",
                    message="没有需要提交归档的商品",
                    ref_type="archive_task",
                    ref_id=archive_task_id,
                    request_id=request_id,
                    payload=input_identifiers,
                )

            confirm_data: dict[str, Any] = {}
            confirm_by_product_id: dict[int, dict[str, Any]] = {}
            if confirm_enabled and target_ids:
                self.events.emit(
                    client_id=credentials.client_id,
                    event_type="archive",
                    status="pending",
                    message="开始确认商品归档结果",
                    ref_type="archive_task",
                    ref_id=archive_task_id,
                    request_id=request_id,
                    payload={"product_id": target_ids},
                )
                confirm_payload = {"product_id": [str(value) for value in target_ids]}
                confirm_data = await self.forwarder.post(OzonEndpoint.PRODUCT_INFO_LIST, confirm_payload, credentials, request_id)
                confirm_by_product_id = {
                    product_id: item
                    for item in response_items(confirm_data)
                    if (product_id := item_product_id(item)) is not None
                }
                self.events.emit(
                    client_id=credentials.client_id,
                    event_type="archive",
                    status="success",
                    message="商品归档结果确认完成",
                    ref_type="archive_task",
                    ref_id=archive_task_id,
                    request_id=request_id,
                    payload={"confirmed": len(confirm_by_product_id)},
                )

            final_items = self._build_final_items(operation_items, target_ids, archive_data, confirm_by_product_id, confirm_enabled)
            counts = self._counts(final_items)
            status = self._batch_status(counts)

            for item in final_items:
                db_item = {
                    **item,
                    "operation_response_payload": archive_data,
                    "confirm_payload": confirm_by_product_id.get(item.get("product_id")) if item.get("product_id") else None,
                }
                self.task_items.insert(
                    client_id=credentials.client_id,
                    archive_task_id=archive_task_id,
                    request_id=request_id,
                    item=db_item,
                )
                if item.get("offer_id"):
                    self.states.upsert_state(client_id=credentials.client_id, request_id=request_id, item=db_item)
                    self.states.insert_history(
                        client_id=credentials.client_id,
                        archive_task_id=archive_task_id,
                        request_id=request_id,
                        item=db_item,
                    )
                self._emit_item_event(credentials.client_id, archive_task_id, request_id, item)

            self.tasks.finish(
                task_id=archive_task_id,
                client_id=credentials.client_id,
                status=status,
                precheck_payload=precheck_data,
                request_payload=archive_payload,
                response_payload=archive_data,
                confirm_payload=confirm_data,
                error_payload=operation_error,
                total_count=len(final_items),
                success_count=counts["success"],
                failed_count=counts["failed"],
                skipped_count=counts["skipped"],
            )
            self.events.emit(
                client_id=credentials.client_id,
                event_type="archive",
                status=self._batch_event_status(status),
                message=f"商品归档处理完成：成功 {counts['success']}，失败 {counts['failed']}，跳过 {counts['skipped']}",
                ref_type="archive_task",
                ref_id=archive_task_id,
                request_id=request_id,
                payload={"status": status, "counts": counts},
            )

            return {
                "request_id": request_id,
                "archive_task_id": archive_task_id,
                "status": status,
                "total_count": len(final_items),
                "success_count": counts["success"],
                "failed_count": counts["failed"],
                "skipped_count": counts["skipped"],
                "precheck": precheck_data,
                "archive_result": archive_data,
                "confirm": confirm_data,
                "items": [
                    {key: value for key, value in item.items() if key not in {"precheck_payload"}}
                    for item in final_items
                ],
            }
        except Exception as exc:
            self.tasks.finish(
                task_id=archive_task_id,
                client_id=credentials.client_id,
                status="failed",
                precheck_payload=None,
                request_payload=input_identifiers,
                response_payload=None,
                confirm_payload=None,
                error_payload={"message": str(exc)},
                total_count=total_input_count,
                success_count=0,
                failed_count=total_input_count,
                skipped_count=0,
            )
            self.events.emit(
                client_id=credentials.client_id,
                event_type="archive",
                status="failed",
                message="商品归档处理失败",
                ref_type="archive_task",
                ref_id=archive_task_id,
                request_id=request_id,
                error_message=str(exc),
                payload=input_identifiers,
            )
            raise

    def _emit_item_event(self, client_id: str, task_id: int, request_id: str, item: dict[str, Any]) -> None:
        status = item.get("status")
        if status == "success":
            event_status = "success"
            message = "商品归档完成"
        elif status == "failed":
            event_status = "failed"
            message = "商品归档失败"
        else:
            event_status = "skipped"
            message = item.get("skip_reason") or "商品归档跳过"
        self.events.emit(
            client_id=client_id,
            event_type="archive",
            status=event_status,
            message=message,
            ref_type="archive_task",
            ref_id=task_id,
            request_id=request_id,
            offer_id=item.get("offer_id"),
            product_id=item.get("product_id"),
            sku=item.get("sku"),
            error_message=item.get("error_message") or item.get("skip_reason"),
            payload={key: value for key, value in item.items() if key != "precheck_payload"},
        )

    def _batch_event_status(self, status: str) -> str:
        if status == "success":
            return "success"
        if status in {"failed", "partial"}:
            return "failed"
        return "skipped"

    def _build_precheck_items(self, precheck_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        for item in precheck_items:
            product_id = item_product_id(item)
            sku = item_sku(item)
            is_archived = bool(item.get("is_archived"))
            items.append(
                {
                    "identifier_type": "product_id" if product_id is not None else "offer_id",
                    "identifier_value": str(product_id or item.get("offer_id") or ""),
                    "offer_id": item.get("offer_id"),
                    "product_id": product_id,
                    "sku": sku,
                    "before_is_archived": is_archived,
                    "before_is_autoarchived": bool(item.get("is_autoarchived")),
                    "after_is_archived": is_archived,
                    "after_is_autoarchived": bool(item.get("is_autoarchived")),
                    "status": "already_archived" if is_archived else "pending",
                    "skip_reason": "商品已归档" if is_archived else None,
                    "error_message": None,
                    "precheck_payload": item,
                }
            )
        return items

    def _build_not_found_items(
        self,
        offer_ids: list[str],
        found_items: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        found_offer_ids = {item.get("offer_id") for item in found_items if item.get("offer_id")}

        missing: list[dict[str, Any]] = []
        for offer_id in offer_ids:
            if offer_id not in found_offer_ids:
                missing.append(self._not_found_item("offer_id", offer_id))
        return missing

    def _not_found_item(self, identifier_type: str, identifier_value: str, product_id: int | None = None) -> dict[str, Any]:
        return {
            "identifier_type": identifier_type,
            "identifier_value": identifier_value,
            "offer_id": None,
            "product_id": product_id,
            "sku": int(identifier_value) if identifier_type == "sku" and identifier_value.isdigit() else None,
            "before_is_archived": None,
            "before_is_autoarchived": None,
            "after_is_archived": None,
            "after_is_autoarchived": None,
            "status": "not_found",
            "skip_reason": "商品信息查询未返回该标识",
            "error_message": None,
            "precheck_payload": None,
        }

    def _build_final_items(
        self,
        operation_items: list[dict[str, Any]],
        target_ids: list[int],
        archive_data: dict[str, Any],
        confirm_by_product_id: dict[int, dict[str, Any]],
        confirm_enabled: bool,
    ) -> list[dict[str, Any]]:
        target_id_set = set(target_ids)
        archive_ok = self._archive_ok(archive_data)
        final_items: list[dict[str, Any]] = []
        for item in operation_items:
            product_id = item.get("product_id")
            if item["status"] in {"not_found", "already_archived"}:
                final_items.append(item)
                continue
            if product_id not in target_id_set:
                item["status"] = "skipped"
                item["skip_reason"] = "缺少 product_id，无法调用归档接口"
                final_items.append(item)
                continue
            if not archive_ok:
                item["status"] = "failed"
                item["error_message"] = "Ozon 归档接口未返回成功结果"
                final_items.append(item)
                continue
            confirm_item = confirm_by_product_id.get(product_id)
            if confirm_enabled and not confirm_item:
                item["status"] = "failed"
                item["error_message"] = "归档后确认查询未返回该商品"
                final_items.append(item)
                continue
            if confirm_item:
                item["after_is_archived"] = bool(confirm_item.get("is_archived"))
                item["after_is_autoarchived"] = bool(confirm_item.get("is_autoarchived"))
                item["offer_id"] = confirm_item.get("offer_id") or item.get("offer_id")
                item["sku"] = item_sku(confirm_item) or item.get("sku")
            else:
                item["after_is_archived"] = True

            if item.get("after_is_archived"):
                item["status"] = "success"
            else:
                item["status"] = "failed"
                item["error_message"] = "归档后确认 is_archived 不为 true"
            final_items.append(item)
        return final_items

    def _archive_ok(self, archive_data: dict[str, Any]) -> bool:
        chunks = archive_data.get("chunks")
        if not chunks:
            return bool(archive_data.get("skipped"))
        for chunk in chunks:
            response = chunk.get("response") or {}
            if response.get("result") is not True:
                return False
        return True

    def _counts(self, items: list[dict[str, Any]]) -> dict[str, int]:
        success = sum(1 for item in items if item["status"] == "success")
        failed = sum(1 for item in items if item["status"] == "failed")
        skipped = sum(1 for item in items if item["status"] in {"skipped", "not_found", "already_archived"})
        return {"success": success, "failed": failed, "skipped": skipped}

    def _batch_status(self, counts: dict[str, int]) -> str:
        if counts["failed"] and counts["success"]:
            return "partial"
        if counts["failed"]:
            return "failed"
        if counts["success"]:
            return "success" if not counts["skipped"] else "partial"
        return "skipped"
