from fastapi import APIRouter, Request

from app.models.user import User

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/me")
async def read_users_me(request: Request) -> User:
    return request.state.user


## Using dependency injection
# @router.get("/me")
# async def read_users_me(
#     user: Annotated[UserInDB, Depends(get_current_active_user)], s
# ) -> User:
#     return user
