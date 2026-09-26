"""Middleware personalizado: tiempo de respuesta, cabeceras y request ID."""

import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = str(round(process_time, 4))
        response.headers["X-Request-ID"] = request_id

        print(f"{request.method} {request.url.path} -> {response.status_code}")

        return response