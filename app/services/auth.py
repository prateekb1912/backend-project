from app.core.security import DUMMY_HASH, hash_password, verify_password
from app.models.user import UserInDB
from app.schemas.user import UserCreate

users_db: dict[str, dict] = {}


class UserAlreadyExists(Exception): ...


class UserNotExists(Exception): ...


def get_user(username: str) -> UserInDB | None:
    data = users_db.get(username)
    return UserInDB(**data) if data else None


def register_user(payload: UserCreate) -> UserInDB:
    if payload.username in users_db:
        raise UserAlreadyExists
    user = UserInDB(
        **payload.model_dump(exclude={"password"}),
        hashed_password=hash_password(payload.password),
        disabled=False,
    )
    users_db[user.username] = user.model_dump()
    return user


def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = get_user(username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
