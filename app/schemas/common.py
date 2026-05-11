from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

DataT = TypeVar("DataT")


class SchemaModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class RawOzonResponse(SchemaModel):
    data: dict[str, Any] = Field(default_factory=dict, description="Ozon 原始响应")


class ProxyResponse(SchemaModel):
    endpoint: str
    data: dict[str, Any] = Field(default_factory=dict)
