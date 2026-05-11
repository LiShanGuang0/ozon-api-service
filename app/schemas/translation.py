from typing import Literal

from pydantic import Field

from app.schemas.common import SchemaModel


class TranslateRequest(SchemaModel):
    texts: list[str] = Field(default_factory=list, max_length=100)
    target_language: Literal["zh", "ru", "en"] = "zh"
    source_language: str | None = "auto"


class TranslateItem(SchemaModel):
    text: str
    translated_text: str
    source_language: str | None = None
    target_language: str
    translated: bool = False
    error: str | None = None


class TranslateResponse(SchemaModel):
    items: list[TranslateItem] = Field(default_factory=list)
