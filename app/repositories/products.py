from typing import Any

from app.db.mysql import execute, fetch_all, fetch_one
from app.utils.json import dumps


class ProductRepository:
    def get_by_offer_id(self, *, client_id: str, offer_id: str) -> dict[str, Any] | None:
        return fetch_one(
            "SELECT * FROM ozon_products WHERE client_id = %s AND offer_id = %s",
            (client_id, offer_id),
        )

    def list_completion_cards(self, *, client_id: str, offer_ids: list[str]) -> list[dict[str, Any]]:
        if not offer_ids:
            return []
        placeholders = ", ".join(["%s"] * len(offer_ids))
        return fetch_all(
            f"""
            SELECT
              p.offer_id,
              p.name,
              p.product_id,
              p.sku,
              p.price,
              p.currency_code,
              p.cover_image_url,
              p.warehouse_id,
              w.name AS warehouse_name,
              p.stock AS requested_stock,
              ps.stock AS stock,
              ps.present,
              ps.reserved
            FROM ozon_products p
            LEFT JOIN ozon_warehouses w
              ON w.client_id = p.client_id AND w.warehouse_id = p.warehouse_id
            LEFT JOIN ozon_product_stocks ps
              ON ps.client_id = p.client_id
             AND ps.offer_id = p.offer_id
             AND ps.warehouse_id = p.warehouse_id
            WHERE p.client_id = %s AND p.offer_id IN ({placeholders})
            ORDER BY FIELD(p.offer_id, {placeholders})
            """,
            [client_id, *offer_ids, *offer_ids],
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
               price, old_price, vat, barcode, warehouse_id, stock, cover_image_url,
               sync_status, last_task_id, last_request_payload)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              name = VALUES(name),
              description_category_id = VALUES(description_category_id),
              type_id = VALUES(type_id),
              currency_code = VALUES(currency_code),
              price = VALUES(price),
              old_price = VALUES(old_price),
              vat = VALUES(vat),
              barcode = VALUES(barcode),
              warehouse_id = COALESCE(VALUES(warehouse_id), warehouse_id),
              stock = COALESCE(VALUES(stock), stock),
              cover_image_url = COALESCE(VALUES(cover_image_url), cover_image_url),
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
                item.get("warehouse_id"),
                item.get("stock"),
                self.cover_image_url(item),
                status,
                task_id,
                dumps(item),
            ),
        )
        self.sync_images_from_item(client_id=client_id, item=item)

    def update_identifiers_from_info_item(self, *, client_id: str, item: dict[str, Any]) -> None:
        offer_id = item.get("offer_id")
        if not offer_id:
            return
        execute(
            """
            UPDATE ozon_products
            SET product_id = COALESCE(%s, product_id),
                sku = COALESCE(%s, sku),
                cover_image_url = COALESCE(%s, cover_image_url),
                last_response_payload = %s
            WHERE client_id = %s AND offer_id = %s
            """,
            (
                item.get("id") or item.get("product_id"),
                item.get("sku"),
                self.cover_image_url(item),
                dumps(item),
                client_id,
                offer_id,
            ),
        )
        self.sync_images_from_item(client_id=client_id, item=item)

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

    def replace_attributes_from_info_item(self, *, client_id: str, item: dict[str, Any]) -> int:
        offer_id = item.get("offer_id")
        if not offer_id:
            return 0

        execute(
            "DELETE FROM ozon_product_attributes WHERE client_id = %s AND offer_id = %s",
            (client_id, offer_id),
        )

        rows = self._attribute_rows(item)
        for row in rows:
            execute(
                """
                INSERT INTO ozon_product_attributes
                  (client_id, offer_id, attribute_id, complex_id, dictionary_value_id,
                   value, value_json, is_required, source)
                VALUES
                  (%s, %s, %s, %s, %s, %s, %s, 0, 'ozon')
                ON DUPLICATE KEY UPDATE
                  value = VALUES(value),
                  value_json = VALUES(value_json),
                  source = 'ozon',
                  updated_at = CURRENT_TIMESTAMP
                """,
                (
                    client_id,
                    offer_id,
                    row["attribute_id"],
                    row["complex_id"],
                    row["dictionary_value_id"],
                    row["value"],
                    dumps(row["value_json"]),
                ),
            )

        execute(
            """
            UPDATE ozon_products
            SET product_id = COALESCE(%s, product_id),
                sku = COALESCE(%s, sku),
                cover_image_url = COALESCE(%s, cover_image_url),
                last_response_payload = %s
            WHERE client_id = %s AND offer_id = %s
            """,
            (
                item.get("id") or item.get("product_id"),
                item.get("sku"),
                self.cover_image_url(item),
                dumps(item),
                client_id,
                offer_id,
            ),
        )
        self.sync_images_from_item(client_id=client_id, item=item)
        return len(rows)

    def sync_images_from_item(self, *, client_id: str, item: dict[str, Any]) -> None:
        offer_id = item.get("offer_id")
        if not offer_id or not self._has_image_fields(item):
            return

        rows = self._image_rows(item)
        execute(
            """
            UPDATE ozon_products
            SET cover_image_url = %s
            WHERE client_id = %s AND offer_id = %s
            """,
            (self.cover_image_url(item), client_id, offer_id),
        )
        execute(
            "DELETE FROM ozon_product_images WHERE client_id = %s AND offer_id = %s",
            (client_id, offer_id),
        )
        for row in rows:
            execute(
                """
                INSERT INTO ozon_product_images
                  (client_id, offer_id, product_id, url, image_type, sort_order, is_primary, state)
                VALUES
                  (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                  product_id = COALESCE(VALUES(product_id), product_id),
                  sort_order = VALUES(sort_order),
                  is_primary = VALUES(is_primary),
                  state = VALUES(state),
                  updated_at = CURRENT_TIMESTAMP
                """,
                (
                    client_id,
                    offer_id,
                    item.get("id") or item.get("product_id"),
                    row["url"],
                    row["image_type"],
                    row["sort_order"],
                    int(row["is_primary"]),
                    row.get("state"),
                ),
            )

    def cover_image_url(self, item: dict[str, Any]) -> str | None:
        primary = self._extract_url(item.get("primary_image"))
        if primary:
            return primary
        images = item.get("images") or []
        if isinstance(images, list) and images:
            return self._extract_url(images[0])
        image = self._extract_url(item.get("image"))
        if image:
            return image
        return self._extract_url(item.get("cover_image_url"))

    def _has_image_fields(self, item: dict[str, Any]) -> bool:
        return any(key in item for key in ("primary_image", "images", "images360", "color_image", "image", "cover_image_url"))

    def _image_rows(self, item: dict[str, Any]) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        cover = self.cover_image_url(item)

        def append(value: Any, image_type: str, sort_order: int, state: str | None = None) -> None:
            url = self._extract_url(value)
            if not url:
                return
            rows.append(
                {
                    "url": url,
                    "image_type": image_type,
                    "sort_order": sort_order,
                    "is_primary": url == cover and image_type in {"primary", "image"},
                    "state": state or self._extract_state(value),
                }
            )

        append(item.get("primary_image") or item.get("cover_image_url") or item.get("image"), "primary", 0)
        for index, value in enumerate(item.get("images") or []):
            append(value, "image", index)
        for index, value in enumerate(item.get("images360") or []):
            append(value, "images360", index)
        append(item.get("color_image"), "color", 0)
        return rows

    def _extract_url(self, value: Any) -> str | None:
        if isinstance(value, str):
            return value or None
        if isinstance(value, dict):
            for key in ("url", "file_name", "image_url", "src"):
                if value.get(key):
                    return str(value[key])
        return None

    def _extract_state(self, value: Any) -> str | None:
        if isinstance(value, dict) and value.get("state"):
            return str(value["state"])
        return None

    def _attribute_rows(self, item: dict[str, Any]) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []

        def append_attribute(attribute: dict[str, Any], default_complex_id: int = 0) -> None:
            attribute_id = attribute.get("attribute_id") or attribute.get("id")
            if attribute_id is None:
                return
            complex_id = int(attribute.get("complex_id") or default_complex_id or 0)
            values = attribute.get("values") or []
            if not values:
                values = [{"dictionary_value_id": 0, "value": None}]
            for value in values:
                dictionary_value_id = int(value.get("dictionary_value_id") or value.get("id") or 0)
                rows.append(
                    {
                        "attribute_id": int(attribute_id),
                        "complex_id": complex_id,
                        "dictionary_value_id": dictionary_value_id,
                        "value": self._attribute_value_text(value),
                        "value_json": value,
                    }
                )

        for attribute in item.get("attributes") or []:
            if isinstance(attribute, dict):
                append_attribute(attribute)

        for complex_attribute in item.get("complex_attributes") or []:
            if not isinstance(complex_attribute, dict):
                continue
            default_complex_id = int(complex_attribute.get("complex_id") or 0)
            for attribute in complex_attribute.get("attributes") or []:
                if isinstance(attribute, dict):
                    append_attribute(attribute, default_complex_id=default_complex_id)

        return rows

    def _attribute_value_text(self, value: dict[str, Any]) -> str | None:
        raw_value = value.get("value")
        if raw_value is None:
            raw_value = value.get("name") or value.get("value_name")
        if raw_value is None:
            return None
        return str(raw_value)
