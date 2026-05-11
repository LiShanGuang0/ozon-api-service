from typing import Any

from app.db.mysql import execute, fetch_one
from app.utils.json import dumps


class ProductRepository:
    def get_by_offer_id(self, *, client_id: str, offer_id: str) -> dict[str, Any] | None:
        return fetch_one(
            "SELECT * FROM ozon_products WHERE client_id = %s AND offer_id = %s",
            (client_id, offer_id),
        )

    def upsert_from_import_item(
        self,
        *,
        client_id: str,
        item: dict[str, Any],
        task_id: int | None = None,
        status: str = "pending",
    ) -> None:
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

    def update_identifiers_from_info_item(self, *, client_id: str, item: dict[str, Any]) -> None:
        offer_id = item.get("offer_id")
        if not offer_id:
            return
        execute(
            """
            UPDATE ozon_products
            SET product_id = COALESCE(%s, product_id),
                sku = COALESCE(%s, sku),
                last_response_payload = %s
            WHERE client_id = %s AND offer_id = %s
            """,
            (
                item.get("id") or item.get("product_id"),
                item.get("sku"),
                dumps(item),
                client_id,
                offer_id,
            ),
        )

    def update_from_task_item(self, *, client_id: str, item: dict[str, Any]) -> None:
        offer_id = item.get("offer_id")
        if not offer_id:
            return
        execute(
            """
            UPDATE ozon_products
            SET product_id = COALESCE(%s, product_id),
                sync_status = %s,
                last_error = %s,
                last_response_payload = %s
            WHERE client_id = %s AND offer_id = %s
            """,
            (
                item.get("product_id"),
                item.get("status") or "pending",
                dumps(item.get("errors")),
                dumps(item),
                client_id,
                offer_id,
            ),
        )
