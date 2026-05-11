import json
from typing import Any

from app.db import execute, fetch_one


def dumps(value: Any) -> str | None:
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def insert_api_log(
    *,
    client_id: str,
    api_key_fingerprint: str | None,
    endpoint: str,
    http_status: int | None,
    success: bool,
    duration_ms: int | None,
    request_payload: Any,
    response_payload: Any,
    error_message: str | None = None,
    request_id: str | None = None,
) -> None:
    execute(
        """
        INSERT INTO ozon_api_call_logs
          (client_id, api_key_fingerprint, request_id, endpoint, http_method, http_status,
           success, duration_ms, request_payload, response_payload, error_message)
        VALUES
          (%s, %s, %s, %s, 'POST', %s, %s, %s, %s, %s, %s)
        """,
        (
            client_id,
            api_key_fingerprint,
            request_id,
            endpoint,
            http_status,
            1 if success else 0,
            duration_ms,
            dumps(request_payload),
            dumps(response_payload),
            error_message,
        ),
    )


def upsert_product_from_item(client_id: str, item: dict[str, Any], task_id: int | None = None, status: str = "pending") -> None:
    offer_id = item.get("offer_id")
    if not offer_id:
        return
    execute(
        """
        INSERT INTO ozon_products
          (client_id, offer_id, local_sku, name, description_category_id, type_id, currency_code,
           price, old_price, vat, barcode, sync_status, last_task_id, last_request_payload)
        VALUES
          (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
          name = VALUES(name),
          description_category_id = VALUES(description_category_id),
          type_id = VALUES(type_id),
          currency_code = VALUES(currency_code),
          price = VALUES(price),
          old_price = VALUES(old_price),
          vat = VALUES(vat),
          barcode = VALUES(barcode),
          sync_status = VALUES(sync_status),
          last_task_id = VALUES(last_task_id),
          last_request_payload = VALUES(last_request_payload)
        """,
        (
            client_id,
            offer_id,
            item.get("local_sku"),
            item.get("name"),
            item.get("description_category_id"),
            item.get("type_id"),
            item.get("currency_code"),
            item.get("price"),
            item.get("old_price"),
            item.get("vat"),
            item.get("barcode"),
            status,
            task_id,
            dumps(item),
        ),
    )


def insert_import_task(
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


def get_import_task(client_id: str, task_id: int) -> dict[str, Any] | None:
    return fetch_one(
        "SELECT * FROM ozon_import_tasks WHERE client_id = %s AND task_id = %s",
        (client_id, task_id),
    )


def update_import_task_result(client_id: str, task_id: int, status: str, result_payload: Any, error_payload: Any = None) -> None:
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


def upsert_task_item(client_id: str, task_id: int, item: dict[str, Any]) -> None:
    offer_id = item.get("offer_id")
    if not offer_id:
        return
    status = item.get("status") or "pending"
    product_id = item.get("product_id")
    errors = item.get("errors")
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
        (client_id, task_id, offer_id, product_id, status, dumps(errors), dumps(item)),
    )
    execute(
        """
        UPDATE ozon_products
        SET product_id = COALESCE(%s, product_id),
            sync_status = %s,
            last_error = %s,
            last_response_payload = %s
        WHERE client_id = %s AND offer_id = %s
        """,
        (product_id, status, dumps(errors), dumps(item), client_id, offer_id),
    )
