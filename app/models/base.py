from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict


class TableModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")


JsonValue = dict[str, Any] | list[Any] | str | int | float | bool | None
