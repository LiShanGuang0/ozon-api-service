from datetime import datetime
from typing import Literal

from pydantic import Field, model_validator

from app.schemas.common import SchemaModel
from app.schemas.merchant import MerchantProfileResponse


ActivationStatus = Literal["pending", "active", "revoked"]


class AppActivationCodeCreateRequest(SchemaModel):
    device_id: str = Field(min_length=1, max_length=128, description="App 设备唯一标识。")
    mac_address: str | None = Field(default=None, max_length=64, description="可选 MAC 地址。")
    client_id: str = Field(min_length=1, max_length=64, description="Ozon Client-Id。")
    api_key: str = Field(min_length=1, description="Ozon Api-Key，仅用于计算指纹，不入库。")
    activation_code: str | None = Field(default=None, min_length=4, max_length=64, description="可选自定义激活码。")
    expires_at: datetime | None = Field(default=None, description="授权过期时间。")
    valid_days: int = Field(default=365, ge=1, le=3650, description="未传 expires_at 时的有效天数。")


class AppActivationCodeCreateResponse(SchemaModel):
    device_id: str
    client_id: str
    activation_code: str = Field(description="管理员页面可查看的激活码。")
    expires_at: datetime
    status: ActivationStatus = "pending"


class AppActivationListItem(SchemaModel):
    id: int
    device_id: str
    mac_address: str | None = None
    client_id: str
    activation_code: str | None = None
    status: str
    expires_at: datetime
    activated_at: datetime | None = None
    last_seen_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class AppActivationListResponse(SchemaModel):
    items: list[AppActivationListItem] = Field(default_factory=list)


class AppActivationCheckRequest(SchemaModel):
    device_id: str = Field(min_length=1, max_length=128, description="App 设备唯一标识。")
    mac_address: str | None = Field(default=None, max_length=64, description="可选 MAC 地址。")


class AppActivationCheckResponse(SchemaModel):
    bound: bool
    expired: bool = False
    activation_required: bool = True
    status: str | None = None
    reason: str | None = None
    client_id: str | None = None
    expires_at: datetime | None = None


class AppActivationBindRequest(SchemaModel):
    device_id: str = Field(min_length=1, max_length=128, description="App 设备唯一标识。")
    mac_address: str | None = Field(default=None, max_length=64, description="可选 MAC 地址。")
    client_id: str = Field(min_length=1, max_length=64, description="Ozon Client-Id。")
    api_key: str = Field(min_length=1, description="Ozon Api-Key。")
    activation_code: str = Field(min_length=4, max_length=64, description="设备激活码。")

    @model_validator(mode="after")
    def trim_inputs(self) -> "AppActivationBindRequest":
        self.device_id = self.device_id.strip()
        self.client_id = self.client_id.strip()
        self.api_key = self.api_key.strip()
        self.activation_code = self.activation_code.strip()
        if self.mac_address:
            self.mac_address = self.mac_address.strip()
        return self


class AppActivationBindResponse(SchemaModel):
    bound: bool = True
    client_id: str
    expires_at: datetime
    profile: MerchantProfileResponse
