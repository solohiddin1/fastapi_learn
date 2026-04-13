import json
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging_config import logger


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        body = await request.body()
        logger.info(f"Request: {request.method} {request.url} - Body: {body.decode() or 'empty'} \n")

        response = await call_next(request)

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type or "text/" in content_type:
            try:
                decoded_body = json.loads(response_body.decode("utf-8"))
            except Exception:
                decoded_body = response_body.decode("utf-8", errors="replace") or "empty"
        else:
            decoded_body = f"<binary content-type: {content_type}>"

        duration = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = f"{duration:.4f} seconds"

        logger.info(f" Response body: {decoded_body} \n <-- {response.status_code}: {duration:.4f} seconds \n\n")

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
