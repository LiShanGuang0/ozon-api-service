from typing import Any

from app.db.mysql import execute, fetch_one
from app.utils.json import dumps


class ImportTaskRepository:
    def insert(
        self,
        *,
        client_id: str,
        task_id: int,
        action_type: str,
        status: str,
        credential_ref: str | None,
        request_payload: Any,
        response_payload: Any,
    ) -> None:
        execute(
            """
            INSERT INTO ozon_import_tasks
              (client_id, task_id, action_type, status, credential_ref, request_payload, response_payload)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              action_type = VALUES(action_type),
              status = VALUES(status),
              credential_ref = VALUES(credential_ref),
              request_payload = VALUES(request_payload),
              response_payload = VALUES(response_payload)
            """,
            (client_id, task_id, action_type, status, credential_ref, dumps(request_payload), dumps(response_payload)),
        )

    def get(self, *, client_id: str, task_id: int) -> dict[str, Any] | None:
        return fetch_one(
            "SELECT * FROM ozon_import_tasks WHERE client_id = %s AND task_id = %s",
            (client_id, task_id),
        )

    def update_result(self, *, client_id: str, task_id: int, status: str, result_payload: Any, error_payload: Any = None) -> None:
        execute(
            """
            UPDATE ozon_import_tasks
            SET status = %s,
                result_payload = %s,
                error_payload = %s,
                last_polled_at = CURRENT_TIMESTAMP,
                finished_at = CASE WHEN %s IN ('imported', 'failed', 'skipped', 'partial') THEN CURRENT_TIMESTAMP ELSE finished_at END
            WHERE client_id = %s AND task_id = %s
            """,
            (status, dumps(result_payload), dumps(error_payload), status, client_id, task_id),
        )


class ImportTaskItemRepository:
    def upsert(self, *, client_id: str, task_id: int, item: dict[str, Any]) -> None:
        offer_id = item.get("offer_id")
        if not offer_id:
            return
        execute(
            """
            INSERT INTO ozon_import_task_items
              (client_id, task_id, offer_id, product_id, status, errors, raw_item)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              product_id = VALUES(product_id),
              status = VALUES(status),
              errors = VALUES(errors),
              raw_item = VALUES(raw_item)
            """,
            (
                client_id,
                task_id,
                offer_id,
                item.get("product_id"),
                item.get("status") or "pending",
                dumps(item.get("errors")),
                dumps(item),
            ),
        )
