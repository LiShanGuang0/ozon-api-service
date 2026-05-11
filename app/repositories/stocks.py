from typing import Any

from app.db.mysql import execute, execute_lastrowid
from app.utils.json import dumps


class StockTaskRepository:
    def insert(self, *, client_id: str, request_id: str, status: str, request_payload: Any, total_count: int) -> int:
        return execute_lastrowid(
            """
            INSERT INTO ozon_stock_update_tasks
              (client_id, request_id, status, request_payload, total_count)
            VALUES
              (%s, %s, %s, %s, %s)
            """,
            (client_id, request_id, status, dumps(request_payload), total_count),
        )

    def finish(
        self,
        *,
        task_id: int,
        client_id: str,
        status: str,
        warehouse_payload: Any,
        product_payload: Any,
        reserved_payload: Any,
        response_payload: Any,
        confirm_payload: Any,
        error_payload: Any,
        success_count: int,
        failed_count: int,
    ) -> None:
        execute(
            """
            UPDATE ozon_stock_update_tasks
            SET status = %s,
                warehouse_payload = %s,
                product_payload = %s,
                reserved_payload = %s,
                response_payload = %s,
                confirm_payload = %s,
                error_payload = %s,
                success_count = %s,
                failed_count = %s,
                finished_at = CURRENT_TIMESTAMP
            WHERE id = %s AND client_id = %s
            """,
            (
                status,
                dumps(warehouse_payload),
                dumps(product_payload),
                dumps(reserved_payload),
                dumps(response_payload),
                dumps(confirm_payload),
                dumps(error_payload),
                success_count,
                failed_count,
                task_id,
                client_id,
            ),
        )


class StockTaskItemRepository:
    def insert(self, *, client_id: str, stock_task_id: int, request_id: str, item: dict[str, Any]) -> None:
        execute(
            """
            INSERT INTO ozon_stock_update_task_items
              (client_id, stock_task_id, request_id, offer_id, product_id, sku, warehouse_id,
               requested_stock, present, reserved, updated, status, error_message,
               precheck_payload, reserved_payload, response_payload, confirm_payload)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              offer_id = VALUES(offer_id),
              product_id = VALUES(product_id),
              sku = VALUES(sku),
              requested_stock = VALUES(requested_stock),
              present = VALUES(present),
              reserved = VALUES(reserved),
              updated = VALUES(updated),
              status = VALUES(status),
              error_message = VALUES(error_message),
              precheck_payload = VALUES(precheck_payload),
              reserved_payload = VALUES(reserved_payload),
              response_payload = VALUES(response_payload),
              confirm_payload = VALUES(confirm_payload)
            """,
            (
                client_id,
                stock_task_id,
                request_id,
                item.get("offer_id"),
                item.get("product_id"),
                item.get("sku"),
                item.get("warehouse_id"),
                item.get("requested_stock"),
                item.get("present"),
                item.get("reserved"),
                int(bool(item.get("updated"))),
                item.get("status"),
                item.get("error_message"),
                dumps(item.get("precheck_payload")),
                dumps(item.get("reserved_payload")),
                dumps(item.get("response_payload")),
                dumps(item.get("confirm_payload")),
            ),
        )


class ProductStockRepository:
    def upsert_stock(self, *, client_id: str, item: dict[str, Any]) -> None:
        execute(
            """
            INSERT INTO ozon_product_stocks
              (client_id, offer_id, product_id, sku, warehouse_id, stock, present, reserved,
               last_stock_task_id, last_error, last_response_payload)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              offer_id = COALESCE(VALUES(offer_id), offer_id),
              product_id = COALESCE(VALUES(product_id), product_id),
              sku = COALESCE(VALUES(sku), sku),
              stock = VALUES(stock),
              present = VALUES(present),
              reserved = VALUES(reserved),
              last_stock_task_id = VALUES(last_stock_task_id),
              last_error = VALUES(last_error),
              last_response_payload = VALUES(last_response_payload),
              updated_at = CURRENT_TIMESTAMP
            """,
            (
                client_id,
                item.get("offer_id"),
                item.get("product_id"),
                item.get("sku"),
                item.get("warehouse_id"),
                item.get("requested_stock"),
                item.get("present"),
                item.get("reserved"),
                item.get("stock_task_id"),
                item.get("error_message"),
                dumps(item.get("confirm_payload") or item.get("response_payload")),
            ),
        )

    def upsert_stock_snapshot(self, *, client_id: str, item: dict[str, Any]) -> None:
        execute(
            """
            INSERT INTO ozon_product_stocks
              (client_id, offer_id, product_id, sku, warehouse_id, stock, present, reserved,
               last_error, last_response_payload)
            VALUES
              (%s, %s, %s, %s, %s, 0, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              offer_id = COALESCE(VALUES(offer_id), offer_id),
              product_id = COALESCE(VALUES(product_id), product_id),
              sku = COALESCE(VALUES(sku), sku),
              present = VALUES(present),
              reserved = VALUES(reserved),
              last_error = VALUES(last_error),
              last_response_payload = VALUES(last_response_payload),
              updated_at = CURRENT_TIMESTAMP
            """,
            (
                client_id,
                item.get("offer_id"),
                item.get("product_id"),
                item.get("sku"),
                item.get("warehouse_id"),
                item.get("present"),
                item.get("reserved"),
                item.get("error_message"),
                dumps(item.get("raw_stock") or item.get("confirm_payload") or item),
            ),
        )

    def upsert_warehouse(self, *, client_id: str, warehouse: dict[str, Any]) -> None:
        warehouse_id = warehouse.get("warehouse_id")
        if warehouse_id is None:
            return
        execute(
            """
            INSERT INTO ozon_warehouses
              (client_id, warehouse_id, name, status, is_rfbs, is_kgt, raw_payload)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              name = VALUES(name),
              status = VALUES(status),
              is_rfbs = VALUES(is_rfbs),
              is_kgt = VALUES(is_kgt),
              raw_payload = VALUES(raw_payload),
              updated_at = CURRENT_TIMESTAMP
            """,
            (
                client_id,
                warehouse_id,
                warehouse.get("name"),
                warehouse.get("status"),
                int(bool(warehouse.get("is_rfbs"))),
                int(bool(warehouse.get("is_kgt"))),
                dumps(warehouse),
            ),
        )
