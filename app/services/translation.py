from __future__ import annotations

import asyncio
from typing import Any

import httpx


class TranslationService:
    """Best-effort text translation for merchant H5 dynamic content."""

    _target_map = {
        "zh": "zh-CN",
        "en": "en",
        "ru": "ru",
    }

    async def translate_many(
        self,
        *,
        texts: list[str],
        target_language: str,
        source_language: str | None = "auto",
    ) -> dict[str, Any]:
        target = self._target_map.get(target_language, target_language)
        source = source_language or "auto"
        cleaned = [text.strip() for text in texts if text and text.strip()]

        async with httpx.AsyncClient(timeout=8.0) as client:
            semaphore = asyncio.Semaphore(6)

            async def translate_one(text: str) -> dict[str, Any]:
                async with semaphore:
                    return await self._translate_one(
                        client=client,
                        text=text,
                        target=target,
                        target_language=target_language,
                        source=source,
                    )

            items = await asyncio.gather(*(translate_one(text) for text in cleaned))

        return {"items": items}

    async def _translate_one(
        self,
        *,
        client: httpx.AsyncClient,
        text: str,
        target: str,
        target_language: str,
        source: str,
    ) -> dict[str, Any]:
        try:
            response = await client.get(
                "https://translate.googleapis.com/translate_a/single",
                params={
                    "client": "gtx",
                    "sl": source,
                    "tl": target,
                    "dt": "t",
                    "q": text,
                },
            )
            response.raise_for_status()
            data = response.json()
            translated_text = self._parse_google_result(data) or text
            detected_language = data[2] if isinstance(data, list) and len(data) > 2 else None
            return {
                "text": text,
                "translated_text": translated_text,
                "source_language": detected_language,
                "target_language": target_language,
                "translated": translated_text != text,
            }
        except Exception as exc:  # pragma: no cover - network fallback
            return {
                "text": text,
                "translated_text": text,
                "source_language": None,
                "target_language": target_language,
                "translated": False,
                "error": str(exc),
            }

    @staticmethod
    def _parse_google_result(data: Any) -> str:
        if not isinstance(data, list) or not data or not isinstance(data[0], list):
            return ""
        parts: list[str] = []
        for segment in data[0]:
            if isinstance(segment, list) and segment and isinstance(segment[0], str):
                parts.append(segment[0])
        return "".join(parts).strip()
