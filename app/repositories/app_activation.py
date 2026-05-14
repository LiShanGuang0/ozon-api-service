from __future__ import annotations

from datetime import datetime
from typing import Any

from app.db.mysql import execute, fetch_all, fetch_one


class AppActivationRepository:
    def get_by_device_id(self, *, device_id: str) -> dict[str, Any] | None:
        return fetch_one(
            """
            SELECT *
            FROM ozon_app_activations
            WHERE device_id = %s
            """,
            (device_id,),
        )

    def upsert_code(
        self,
        *,
        device_id: str,
        mac_address: str | None,
        client_id: str,
        api_key_fingerprint: str,
        activation_code: str,
        activation_code_hash: str,
        expires_at: datetime,
    ) -> None:
        execute(
            """
            INSERT INTO ozon_app_activations
              (device_id, mac_address, client_id, api_key_fingerprint, activation_code, activation_code_hash,
               status, expires_at, activated_at, last_seen_at)
            VALUES
              (%s, %s, %s, %s, %s, %s, 'pending', %s, NULL, NULL)
            ON DUPLICATE KEY UPDATE
              mac_address = VALUES(mac_address),
              client_id = VALUES(client_id),
              api_key_fingerprint = VALUES(api_key_fingerprint),
              activation_code = VALUES(activation_code),
              activation_code_hash = VALUES(activation_code_hash),
              status = 'pending',
              expires_at = VALUES(expires_at),
              activated_at = NULL,
              last_seen_at = NULL
            """,
            (
                device_id,
                mac_address,
                client_id,
                api_key_fingerprint,
                activation_code,
                activation_code_hash,
                expires_at,
            ),
        )

    def list(self) -> list[dict[str, Any]]:
        return fetch_all(
            """
            SELECT
              id, device_id, mac_address, client_id, activation_code, status,
              expires_at, activated_at, last_seen_at, created_at, updated_at
            FROM ozon_app_activations
            ORDER BY created_at DESC, id DESC
            """
        )

    def activate(self, *, device_id: str, mac_address: str | None) -> None:
        execute(
            """
            UPDATE ozon_app_activations
            SET
              mac_address = COALESCE(%s, mac_address),
              status = 'active',
              activated_at = COALESCE(activated_at, CURRENT_TIMESTAMP),
              last_seen_at = CURRENT_TIMESTAMP
            WHERE device_id = %s
            """,
            (mac_address, device_id),
        )

    def touch(self, *, device_id: str, mac_address: str | None = None) -> None:
        execute(
            """
            UPDATE ozon_app_activations
            SET
              mac_address = COALESCE(%s, mac_address),
              last_seen_at = CURRENT_TIMESTAMP
            WHERE device_id = %s
            """,
            (mac_address, device_id),
        )
