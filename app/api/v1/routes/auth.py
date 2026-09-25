from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import app.services.auth as auth_service
from app.core.security import create_access_token
from app.models.user import User, UserInDB
from app.schemas import Token, UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def signup(payload: UserCreate) -> UserInDB:
    try:
        return auth_service.register_user(payload)
    except auth_service.UserAlreadyExists:
        raise HTTPException(status_code=409, detail="Username already taken")


@router.post("/token", response_model=Token)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = auth_service.authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user.username))
