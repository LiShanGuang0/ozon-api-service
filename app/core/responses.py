from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response


SUCCESS_CODE = 200


def success_payload(data: Any = None, msg: str = "success", code: int = SUCCESS_CODE) -> dict[str, Any]:
    return {"code": code, "msg": msg, "data": data}


def error_payload(code: int, msg: str, data: Any = None) -> dict[str, Any]:
    return {"code": code, "msg": msg, "data": data}


def is_enveloped(payload: Any) -> bool:
    return isinstance(payload, dict) and {"code", "msg", "data"}.issubset(payload.keys())


class ApiResponseEnvelopeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if not request.url.path.startswith("/api"):
            return response

        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            return response

        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        if not body:
            return Response(status_code=response.status_code, headers=dict(response.headers))

        import json

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            return Response(content=body, status_code=response.status_code, headers=dict(response.headers))

        if is_enveloped(payload):
            wrapped = payload
        elif 200 <= response.status_code < 400:
            wrapped = success_payload(payload)
        else:
            msg = payload.get("detail") if isinstance(payload, dict) else None
            wrapped = error_payload(response.status_code, str(msg or "request failed"), payload)

        headers = {
            key: value
            for key, value in response.headers.items()
            if key.lower() not in {"content-length", "content-type"}
        }
        return JSONResponse(content=wrapped, status_code=response.status_code, headers=headers)
