from __future__ import annotations

import asyncio
from typing import Any

import httpx


class TranslationService:
    """Best-effort text translation for merchant H5 dynamic content."""

    _target_map = {
        "zh": "zh",
        "en": "en",
        "ru": "ru",
    }

    _youdao_type_map = {
        "en": "ZH_CN2EN",
        "ru": "ZH_CN2RU",
        "zh": "AUTO",
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
        if not cleaned:
            return {"items": []}

        async with httpx.AsyncClient(timeout=2.5) as client:
            semaphore = asyncio.Semaphore(4)

            async def translate_one(text: str) -> dict[str, Any]:
                async with semaphore:
                    return await self._translate_one(
                        client=client,
                        text=text,
                        target=target,
                        target_language=target_language,
                        source=source,
                    )

            tasks = [(text, asyncio.create_task(translate_one(text))) for text in cleaned]
            done, pending = await asyncio.wait((task for _, task in tasks), timeout=6.0)
            for task in pending:
                task.cancel()

            items = []
            for text, task in tasks:
                if task in done:
                    items.append(task.result())
                else:
                    items.append(self._fallback_item(text=text, target_language=target_language, error="translation timeout"))

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
            errors: list[str] = []
            try:
                translated_text = await self._translate_with_jianxin(
                    client=client,
                    text=text,
                    target=target,
                    source=source,
                )
            except Exception as exc:
                translated_text = ""
                errors.append(f"jianxin: {exc}")

            try:
                if not translated_text:
                    translated_text = await self._translate_with_youdao(
                        client=client,
                        text=text,
                        target_language=target_language,
                    )
            except Exception as exc:
                translated_text = ""
                errors.append(f"youdao: {exc}")

            if not translated_text:
                try:
                    translated_text = await self._translate_with_iciba(
                        client=client,
                        text=text,
                        target=target,
                        source=source,
                    )
                except Exception as exc:
                    translated_text = ""
                    errors.append(f"iciba: {exc}")
            translated_text = translated_text or text
            item = {
                "text": text,
                "translated_text": translated_text,
                "source_language": source,
                "target_language": target_language,
                "translated": translated_text != text,
            }
            if errors and translated_text == text:
                item["error"] = "; ".join(errors)
            return item
        except Exception as exc:  # pragma: no cover - network fallback
            return self._fallback_item(text=text, target_language=target_language, error=str(exc))

    async def _translate_with_jianxin(
        self,
        *,
        client: httpx.AsyncClient,
        text: str,
        target: str,
        source: str,
    ) -> str:
        source_value = self._source_for_jianxin(text=text, source=source, target=target)
        if source_value == target:
            return text
        response = await client.get(
            "https://api.qvqa.cn/api/fanyi",
            params={
                "text": text,
                "source": source_value,
                "target": target,
            },
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()
        return self._parse_jianxin_result(response.json())

    async def _translate_with_youdao(
        self,
        *,
        client: httpx.AsyncClient,
        text: str,
        target_language: str,
    ) -> str:
        response = await client.post(
            "https://fanyi.youdao.com/translate",
            data={
                "doctype": "json",
                "type": self._youdao_type(text=text, target_language=target_language),
                "i": text,
            },
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://fanyi.youdao.com/",
            },
        )
        response.raise_for_status()
        return self._parse_youdao_result(response.json())

    async def _translate_with_iciba(
        self,
        *,
        client: httpx.AsyncClient,
        text: str,
        target: str,
        source: str,
    ) -> str:
        response = await client.get(
            "https://fy.iciba.com/ajax.php",
            params={
                "a": "fy",
                "f": source if source and source != "auto" else "auto",
                "t": target,
                "w": text,
            },
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()
        return self._parse_iciba_result(response.json())

    def _youdao_type(self, *, text: str, target_language: str) -> str:
        if target_language == "zh":
            return "AUTO"
        if self._contains_cjk(text):
            return self._youdao_type_map.get(target_language, "AUTO")
        return "AUTO"

    def _source_for_jianxin(self, *, text: str, source: str, target: str) -> str:
        supported = {"zh", "en", "ru"}
        if source in supported:
            return source
        detected = self._detect_source_language(text)
        if detected in supported:
            return detected
        return "en" if target == "zh" else "zh"

    @staticmethod
    def _parse_jianxin_result(data: Any) -> str:
        payload = data.get("data") if isinstance(data, dict) else None
        if not isinstance(payload, dict):
            return ""
        value = payload.get("targetText")
        return value.strip() if isinstance(value, str) else ""

    def _parse_youdao_result(self, data: Any) -> str:
        result = data.get("translateResult") if isinstance(data, dict) else None
        if not isinstance(result, list):
            return ""
        parts: list[str] = []
        for group in result:
            if not isinstance(group, list):
                continue
            for segment in group:
                if isinstance(segment, dict) and isinstance(segment.get("tgt"), str):
                    parts.append(segment["tgt"])
        return "".join(parts).strip()

    @staticmethod
    def _parse_iciba_result(data: Any) -> str:
        content = data.get("content") if isinstance(data, dict) else None
        if not isinstance(content, dict):
            return ""
        if isinstance(content.get("out"), str) and content["out"].strip():
            return content["out"].strip()
        word_mean = content.get("word_mean")
        if isinstance(word_mean, list) and word_mean:
            return "; ".join(str(item) for item in word_mean if item).strip()
        return ""

    @staticmethod
    def _contains_cjk(text: str) -> bool:
        return any("\u4e00" <= char <= "\u9fff" for char in text)

    @staticmethod
    def _contains_cyrillic(text: str) -> bool:
        return any("\u0400" <= char <= "\u04ff" for char in text)

    def _detect_source_language(self, text: str) -> str:
        if self._contains_cjk(text):
            return "zh"
        if self._contains_cyrillic(text):
            return "ru"
        return "en"

    @staticmethod
    def _fallback_item(*, text: str, target_language: str, error: str) -> dict[str, Any]:
        return {
            "text": text,
            "translated_text": text,
            "source_language": None,
            "target_language": target_language,
            "translated": False,
            "error": error,
        }
