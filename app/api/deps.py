from typing import Annotated

from fastapi import Depends, HTTPException, status

import app.services.auth as auth_service
from app.core.security import decode_access_token, oauth2_scheme
from app.models.user import UserInDB

CREDENTIALS_EXC = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    username = decode_access_token(token)
    if not username:
        raise CREDENTIALS_EXC
    user = auth_service.get_user(username)
    if not user:
        raise CREDENTIALS_EXC
    return user


async def get_current_active_user(
    user: Annotated[UserInDB, Depends(get_current_user)],
) -> UserInDB:
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
