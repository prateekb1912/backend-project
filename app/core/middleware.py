import time
from collections import defaultdict
from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

import app.services.auth as auth_service
from app.core.config import PUBLIC_PATHS, get_settings
from app.core.security import decode_access_token

_hits: defaultdict[str, list[float]] = defaultdict(list)


async def rate_limiter(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    settings = get_settings()
    limit = settings.rate_limit_max_requests
    window = settings.rate_limit_window_seconds
    host = request.client.host if request.client else "unknown"

    now = time.monotonic()
    key = host
    hits = [t for t in _hits[key] if now - t < window]
    if len(hits) >= limit:
        _hits[key] = hits
        return JSONResponse(
            {"detail": "Too many requests"},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            headers={"Retry-After": str(int(window - (now - hits[0])) + 1)},
        )

    hits.append(now)
    _hits[key] = hits
    print(_hits)
    return await call_next(request)


async def require_auth(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    if request.method == "OPTIONS" or request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    scheme, _, token = request.headers.get("Authorization", "").partition(" ")
    username = decode_access_token(token) if scheme.lower() == "bearer" else None
    user = auth_service.get_user(username) if username else None
    if not user or user.disabled:
        return JSONResponse(
            {"detail": "Not authenticated"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )

    request.state.user = user
    return await call_next(request)
