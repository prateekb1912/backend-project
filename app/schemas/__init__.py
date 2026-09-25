from pydantic import BaseModel, field_validator


class UserCreate(BaseModel):
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None

    @field_validator("password")
    @classmethod
    def password_min_length(cls, pw: str) -> str:
        if len(pw) < 8:
            raise ValueError("password must be at least 8 characters")
        return pw


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
