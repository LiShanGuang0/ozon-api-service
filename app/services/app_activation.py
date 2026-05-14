from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Any

from fastapi import status

from app.core.exceptions import ServiceError
from app.core.security import OzonCredentials
from app.repositories.app_activation import AppActivationRepository
from app.schemas.app_activation import (
    AppActivationBindRequest,
    AppActivationCheckRequest,
    AppActivationCodeCreateRequest,
)
from app.services.merchant_console import MerchantConsoleService


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _activation_code_hash(value: str) -> str:
    return _sha256(value.strip().upper())


class AppActivationService:
    def __init__(
        self,
        *,
        activations: AppActivationRepository | None = None,
        merchants: MerchantConsoleService | None = None,
    ) -> None:
        self.activations = activations or AppActivationRepository()
        self.merchants = merchants or MerchantConsoleService()

    def list_codes(self) -> dict[str, Any]:
        return {"items": self.activations.list()}

    async def create_code(self, *, payload: AppActivationCodeCreateRequest) -> dict[str, Any]:
        device_id = payload.device_id.strip()
        client_id = payload.client_id.strip()
        api_key = payload.api_key.strip()
        mac_address = payload.mac_address.strip() if payload.mac_address else None
        activation_code = (payload.activation_code or self._generate_code()).strip().upper()
        expires_at = self._naive_datetime(payload.expires_at or (datetime.now() + timedelta(days=payload.valid_days)))

        self.activations.upsert_code(
            device_id=device_id,
            mac_address=mac_address,
            client_id=client_id,
            api_key_fingerprint=OzonCredentials(client_id=client_id, api_key=api_key).api_key_fingerprint,
            activation_code=activation_code,
            activation_code_hash=_activation_code_hash(activation_code),
            expires_at=expires_at,
        )
        return {
            "device_id": device_id,
            "client_id": client_id,
            "activation_code": activation_code,
            "expires_at": expires_at,
            "status": "pending",
        }

    def check(self, *, payload: AppActivationCheckRequest) -> dict[str, Any]:
        device_id = payload.device_id.strip()
        mac_address = payload.mac_address.strip() if payload.mac_address else None
        row = self.activations.get_by_device_id(device_id=device_id)
        if not row:
            return {
                "bound": False,
                "expired": False,
                "activation_required": True,
                "reason": "not_found",
            }

        expires_at = row.get("expires_at")
        expired = bool(expires_at and expires_at <= datetime.now())
        status_value = row.get("status")
        if expired:
            return self._check_response(row, bound=False, expired=True, reason="expired")
        if status_value != "active":
            return self._check_response(row, bound=False, expired=False, reason=status_value or "inactive")

        self.activations.touch(device_id=device_id, mac_address=mac_address)
        return self._check_response(row, bound=True, expired=False, reason=None)

    async def bind(self, *, payload: AppActivationBindRequest) -> dict[str, Any]:
        device_id = payload.device_id.strip()
        mac_address = payload.mac_address.strip() if payload.mac_address else None
        client_id = payload.client_id.strip()
        api_key = payload.api_key.strip()
        activation_code = payload.activation_code.strip().upper()
        row = self.activations.get_by_device_id(device_id=device_id)
        if not row:
            raise ServiceError("激活码不存在，请先生成设备激活码。", status.HTTP_404_NOT_FOUND)
        if row.get("status") == "revoked":
            raise ServiceError("该设备授权已被撤销。", status.HTTP_403_FORBIDDEN)
        expires_at = row.get("expires_at")
        if expires_at and expires_at <= datetime.now():
            raise ServiceError("激活码已过期，请重新生成。", status.HTTP_403_FORBIDDEN)
        if row.get("client_id") != client_id:
            raise ServiceError("Client-Id 与激活码不匹配。", status.HTTP_403_FORBIDDEN)

        api_key_fingerprint = OzonCredentials(client_id=client_id, api_key=api_key).api_key_fingerprint
        if not hmac.compare_digest(str(row.get("api_key_fingerprint") or ""), api_key_fingerprint):
            raise ServiceError("Api-Key 与激活码不匹配。", status.HTTP_403_FORBIDDEN)
        if not hmac.compare_digest(str(row.get("activation_code_hash") or ""), _activation_code_hash(activation_code)):
            raise ServiceError("激活码不正确。", status.HTTP_403_FORBIDDEN)

        bootstrap = await self.merchants.bootstrap(credentials=OzonCredentials(client_id=client_id, api_key=api_key))
        self.activations.activate(device_id=device_id, mac_address=mac_address)
        return {
            "bound": True,
            "client_id": client_id,
            "expires_at": expires_at,
            "profile": bootstrap["profile"],
        }

    def _check_response(
        self,
        row: dict[str, Any],
        *,
        bound: bool,
        expired: bool,
        reason: str | None,
    ) -> dict[str, Any]:
        return {
            "bound": bound,
            "expired": expired,
            "activation_required": not bound,
            "status": row.get("status"),
            "reason": reason,
            "client_id": row.get("client_id"),
            "expires_at": row.get("expires_at"),
        }

    def _generate_code(self) -> str:
        token = secrets.token_hex(6).upper()
        return f"{token[:4]}-{token[4:8]}-{token[8:]}"

    def _naive_datetime(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value
        return value.astimezone().replace(tzinfo=None)
