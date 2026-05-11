from typing import Any

from app.db.mysql import execute, execute_lastrowid
from app.utils.json import dumps


class ArchiveTaskRepository:
    def insert(
        self,
        *,
        client_id: str,
        request_id: str,
        action_type: str,
        status: str,
        input_identifiers: Any,
        total_count: int,
    ) -> int:
        return execute_lastrowid(
            """
            INSERT INTO ozon_archive_tasks
              (client_id, request_id, action_type, status, input_identifiers, total_count)
            VALUES
              (%s, %s, %s, %s, %s, %s)
            """,
            (client_id, request_id, action_type, status, dumps(input_identifiers), total_count),
        )

    def finish(
        self,
        *,
        task_id: int,
        client_id: str,
        status: str,
        precheck_payload: Any,
        request_payload: Any,
        response_payload: Any,
        confirm_payload: Any,
        error_payload: Any,
        total_count: int,
        success_count: int,
        failed_count: int,
        skipped_count: int,
    ) -> None:
        execute(
            """
            UPDATE ozon_archive_tasks
            SET status = %s,
                precheck_payload = %s,
                request_payload = %s,
                response_payload = %s,
                confirm_payload = %s,
                error_payload = %s,
                total_count = %s,
                success_count = %s,
                failed_count = %s,
                skipped_count = %s,
                finished_at = CURRENT_TIMESTAMP
            WHERE id = %s AND client_id = %s
            """,
            (
                status,
                dumps(precheck_payload),
                dumps(request_payload),
                dumps(response_payload),
                dumps(confirm_payload),
                dumps(error_payload),
                total_count,
                success_count,
                failed_count,
                skipped_count,
                task_id,
                client_id,
            ),
        )


class ArchiveTaskItemRepository:
    def insert(self, *, client_id: str, archive_task_id: int, request_id: str, item: dict[str, Any]) -> None:
        execute(
            """
            INSERT INTO ozon_archive_task_items
              (client_id, archive_task_id, request_id, identifier_type, identifier_value,
               offer_id, product_id, sku, before_is_archived, before_is_autoarchived,
               after_is_archived, after_is_autoarchived, status, skip_reason, error_message,
               precheck_payload, operation_response_payload, confirm_payload)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              offer_id = VALUES(offer_id),
              sku = VALUES(sku),
              before_is_archived = VALUES(before_is_archived),
              before_is_autoarchived = VALUES(before_is_autoarchived),
              after_is_archived = VALUES(after_is_archived),
              after_is_autoarchived = VALUES(after_is_autoarchived),
              status = VALUES(status),
              skip_reason = VALUES(skip_reason),
              error_message = VALUES(error_message),
              precheck_payload = VALUES(precheck_payload),
              operation_response_payload = VALUES(operation_response_payload),
              confirm_payload = VALUES(confirm_payload)
            """,
            (
                client_id,
                archive_task_id,
                request_id,
                item.get("identifier_type"),
                item.get("identifier_value"),
                item.get("offer_id"),
                item.get("product_id"),
                item.get("sku"),
                item.get("before_is_archived"),
                item.get("before_is_autoarchived"),
                item.get("after_is_archived"),
                item.get("after_is_autoarchived"),
                item.get("status"),
                item.get("skip_reason"),
                item.get("error_message"),
                dumps(item.get("precheck_payload")),
                dumps(item.get("operation_response_payload")),
                dumps(item.get("confirm_payload")),
            ),
        )


class ProductArchiveStateRepository:
    def upsert_state(
        self,
        *,
        client_id: str,
        request_id: str,
        item: dict[str, Any],
    ) -> None:
        offer_id = item.get("offer_id")
        if not offer_id:
            return

        status = "archived" if item.get("after_is_archived") else "active"
        execute(
            """
            INSERT INTO ozon_products
              (client_id, offer_id, product_id, sku, sync_status, is_archived, is_autoarchived,
               archive_status, archived_at, archive_checked_at, last_archive_request_id, last_archive_error,
               last_response_payload)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s, %s,
               CASE WHEN %s = 1 THEN CURRENT_TIMESTAMP ELSE NULL END,
               CURRENT_TIMESTAMP, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              product_id = COALESCE(VALUES(product_id), product_id),
              sku = COALESCE(VALUES(sku), sku),
              sync_status = VALUES(sync_status),
              is_archived = VALUES(is_archived),
              is_autoarchived = VALUES(is_autoarchived),
              archive_status = VALUES(archive_status),
              archived_at = CASE WHEN VALUES(is_archived) = 1 THEN COALESCE(archived_at, CURRENT_TIMESTAMP) ELSE NULL END,
              archive_checked_at = CURRENT_TIMESTAMP,
              last_archive_request_id = VALUES(last_archive_request_id),
              last_archive_error = VALUES(last_archive_error),
              last_response_payload = VALUES(last_response_payload)
            """,
            (
                client_id,
                offer_id,
                item.get("product_id"),
                item.get("sku"),
                status,
                int(bool(item.get("after_is_archived"))),
                int(bool(item.get("after_is_autoarchived"))),
                status,
                int(bool(item.get("after_is_archived"))),
                request_id,
                item.get("error_message"),
                dumps(item.get("confirm_payload") or item.get("precheck_payload")),
            ),
        )

    def insert_history(
        self,
        *,
        client_id: str,
        archive_task_id: int,
        request_id: str,
        action_type: str = "archive",
        source: str = "archive_workflow",
        item: dict[str, Any],
    ) -> None:
        execute(
            """
            INSERT INTO ozon_product_archive_history
              (client_id, archive_task_id, request_id, action_type, source, offer_id, product_id, sku,
               from_is_archived, to_is_archived, from_is_autoarchived, to_is_autoarchived, payload)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                client_id,
                archive_task_id,
                request_id,
                action_type,
                source,
                item.get("offer_id"),
                item.get("product_id"),
                item.get("sku"),
                item.get("before_is_archived"),
                item.get("after_is_archived"),
                item.get("before_is_autoarchived"),
                item.get("after_is_autoarchived"),
                dumps(item.get("confirm_payload") or item.get("precheck_payload")),
            ),
        )
