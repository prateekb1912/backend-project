from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

import app.services.auth as auth_service
from app.core.config import PUBLIC_PATHS
from app.core.security import decode_access_token


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
