from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/me")
async def read_users_me(
    user: Annotated[UserInDB, Depends(get_current_active_user)],
) -> User:
    return user
