from typing import Any

from pydantic import Field

from app.schemas.common import SchemaModel


class ImportTaskStatusResponse(SchemaModel):
    task_id: int
    status: str
    data: dict[str, Any] = Field(default_factory=dict)
