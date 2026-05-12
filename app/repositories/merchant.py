from __future__ import annotations

from typing import Any

from app.db.mysql import execute, fetch_all, fetch_one
from app.utils.json import dumps


class MerchantRepository:
    def get_by_client_id(self, *, client_id: str) -> dict[str, Any] | None:
        return fetch_one(
            """
            SELECT *
            FROM ozon_merchants
            WHERE client_id = %s
            """,
            (client_id,),
        )

    def upsert_from_ozon(
        self,
        *,
        merchant_id: str,
        client_id: str,
        shop_name: str,
        display_name: str | None = None,
        currency_code: str | None = None,
        default_warehouse_id: int | None = None,
        api_key_fingerprint: str | None = None,
        last_error: str | None = None,
    ) -> None:
        execute(
            """
            INSERT INTO ozon_merchants
              (merchant_id, client_id, shop_name, display_name, status, currency_code,
               default_warehouse_id, api_key_fingerprint, last_connected_at, last_error)
            VALUES
              (%s, %s, %s, %s, 'active', %s, %s, %s, CURRENT_TIMESTAMP, %s)
            ON DUPLICATE KEY UPDATE
              shop_name = VALUES(shop_name),
              display_name = VALUES(display_name),
              status = 'active',
              currency_code = COALESCE(VALUES(currency_code), currency_code),
              default_warehouse_id = COALESCE(VALUES(default_warehouse_id), default_warehouse_id),
              api_key_fingerprint = VALUES(api_key_fingerprint),
              last_connected_at = CURRENT_TIMESTAMP,
              last_error = VALUES(last_error)
            """,
            (
                merchant_id,
                client_id,
                shop_name,
                display_name,
                currency_code,
                default_warehouse_id,
                api_key_fingerprint,
                last_error,
            ),
        )


class MerchantProductRepository:
    def list(
        self,
        *,
        client_id: str,
        keyword: str | None,
        status: str | None,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]]:
        filters = ["p.client_id = %s"]
        params: list[Any] = [client_id]
        if status:
            filters.append("p.sync_status = %s")
            params.append(status)
        if keyword:
            filters.append("(p.offer_id LIKE %s OR p.name LIKE %s OR p.local_sku LIKE %s)")
            like = f"%{keyword}%"
            params.extend([like, like, like])

        params.extend([limit, offset])
        return fetch_all(
            f"""
            SELECT
              p.id, p.client_id, p.local_sku, p.offer_id, p.product_id, p.sku, p.name,
              p.description_category_id, p.type_id, p.currency_code, p.price, p.old_price,
              p.warehouse_id, w.name AS warehouse_name, p.stock, p.cover_image_url,
              p.sync_status, p.ozon_status, p.last_task_id, p.last_error, p.updated_at, p.created_at
            FROM ozon_products p
            LEFT JOIN ozon_warehouses w
              ON w.client_id = p.client_id AND w.warehouse_id = p.warehouse_id
            WHERE {" AND ".join(filters)}
            ORDER BY p.updated_at DESC, p.id DESC
            LIMIT %s OFFSET %s
            """,
            params,
        )

    def count(self, *, client_id: str, keyword: str | None, status: str | None) -> int:
        filters = ["client_id = %s"]
        params: list[Any] = [client_id]
        if status:
            filters.append("sync_status = %s")
            params.append(status)
        if keyword:
            filters.append("(offer_id LIKE %s OR name LIKE %s OR local_sku LIKE %s)")
            like = f"%{keyword}%"
            params.extend([like, like, like])

        row = fetch_one(
            f"""
            SELECT COUNT(*) AS total
            FROM ozon_products
            WHERE {" AND ".join(filters)}
            """,
            params,
        )
        return int((row or {}).get("total") or 0)

    def status_counts(self, *, client_id: str) -> list[dict[str, Any]]:
        return fetch_all(
            """
            SELECT sync_status AS status, COUNT(*) AS count
            FROM ozon_products
            WHERE client_id = %s
            GROUP BY sync_status
            """,
            (client_id,),
        )


class MerchantImportTaskRepository:
    def list(
        self,
        *,
        client_id: str,
        status: str | None,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]]:
        filters = ["client_id = %s"]
        params: list[Any] = [client_id]
        if status:
            filters.append("status = %s")
            params.append(status)

        params.extend([limit, offset])
        return fetch_all(
            f"""
            SELECT
              t.id, t.client_id, t.task_id, t.action_type, t.status, t.workflow_status,
              t.submitted_at, t.last_polled_at, t.finished_at,
              COALESCE(i.total_count, 0) AS total_count,
              COALESCE(i.success_count, 0) AS success_count,
              COALESCE(i.failed_count, 0) AS failed_count
            FROM ozon_import_tasks t
            LEFT JOIN (
              SELECT
                client_id,
                task_id,
                COUNT(*) AS total_count,
                SUM(CASE WHEN status = 'imported' THEN 1 ELSE 0 END) AS success_count,
                SUM(CASE WHEN status IN ('failed', 'skipped') THEN 1 ELSE 0 END) AS failed_count
              FROM ozon_import_task_items
              WHERE client_id = %s
              GROUP BY client_id, task_id
            ) i ON i.client_id = t.client_id AND i.task_id = t.task_id
            WHERE {" AND ".join(filters)}
            ORDER BY t.submitted_at DESC, t.id DESC
            LIMIT %s OFFSET %s
            """,
            [client_id, *params],
        )

    def count(self, *, client_id: str, status: str | None) -> int:
        filters = ["client_id = %s"]
        params: list[Any] = [client_id]
        if status:
            filters.append("status = %s")
            params.append(status)

        row = fetch_one(
            f"""
            SELECT COUNT(*) AS total
            FROM ozon_import_tasks
            WHERE {" AND ".join(filters)}
            """,
            params,
        )
        return int((row or {}).get("total") or 0)

    def get(self, *, client_id: str, task_id: int) -> dict[str, Any] | None:
        return fetch_one(
            """
            SELECT *
            FROM ozon_import_tasks
            WHERE client_id = %s AND task_id = %s
            """,
            (client_id, task_id),
        )

    def items(self, *, client_id: str, task_id: int) -> list[dict[str, Any]]:
        return fetch_all(
            """
            SELECT id, client_id, task_id, offer_id, product_id, warehouse_id, stock, status, errors, raw_item, created_at, updated_at
            FROM ozon_import_task_items
            WHERE client_id = %s AND task_id = %s
            ORDER BY id ASC
            """,
            (client_id, task_id),
        )

    def today_status_counts(self, *, client_id: str) -> list[dict[str, Any]]:
        return fetch_all(
            """
            SELECT workflow_status AS status, COUNT(*) AS count
            FROM ozon_import_tasks
            WHERE client_id = %s AND submitted_at >= CURDATE()
            GROUP BY workflow_status
            """,
            (client_id,),
        )


class TaskEventRepository:
    def insert(
        self,
        *,
        client_id: str,
        event_type: str,
        status: str,
        message: str,
        ref_type: str | None = None,
        ref_id: int | None = None,
        ozon_task_id: int | None = None,
        request_id: str | None = None,
        offer_id: str | None = None,
        product_id: int | None = None,
        sku: int | None = None,
        error_message: str | None = None,
        payload: Any = None,
        is_visible: bool = True,
    ) -> None:
        execute(
            """
            INSERT INTO ozon_task_events
              (client_id, event_type, ref_type, ref_id, ozon_task_id, request_id, offer_id,
               product_id, sku, status, message, error_message, payload, is_visible)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                client_id,
                event_type,
                ref_type,
                ref_id,
                ozon_task_id,
                request_id,
                offer_id,
                product_id,
                sku,
                status,
                message,
                error_message,
                dumps(payload),
                int(is_visible),
            ),
        )

    def list(
        self,
        *,
        client_id: str,
        limit: int,
        before_id: int | None = None,
        status: str | None = None,
        event_type: str | None = None,
    ) -> list[dict[str, Any]]:
        filters = ["client_id = %s", "is_visible = 1"]
        params: list[Any] = [client_id]
        if before_id:
            filters.append("id < %s")
            params.append(before_id)
        if status:
            filters.append("status = %s")
            params.append(status)
        if event_type:
            filters.append("event_type = %s")
            params.append(event_type)

        params.append(limit)
        return fetch_all(
            f"""
            SELECT
              id, client_id, event_type, ref_type, ref_id, ozon_task_id, request_id,
              offer_id, product_id, sku, status, message, error_message, payload, created_at
            FROM ozon_task_events
            WHERE {" AND ".join(filters)}
            ORDER BY id DESC
            LIMIT %s
            """,
            params,
        )

    def today_count(self, *, client_id: str) -> int:
        row = fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM ozon_task_events
            WHERE client_id = %s AND is_visible = 1 AND created_at >= CURDATE()
            """,
            (client_id,),
        )
        return int((row or {}).get("total") or 0)
