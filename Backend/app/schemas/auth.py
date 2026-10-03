#app/schemas/auth.py 

from typing import Literal

from pydantic import BaseModel, EmailStr, Field  # type: ignore[import-not-found]


class AuthSchema(BaseModel):
    class Config:
        extra = "forbid"


class LoginRequest(AuthSchema):
    email: EmailStr
    password: str = Field(min_length=8)

class RegisterRequest(AuthSchema):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)

class RefreshTokenRequest(AuthSchema):
    refresh_token: str = Field(min_length=1)


class ForgotPasswordRequest(AuthSchema):
    email: EmailStr

class ResetPasswordRequest(AuthSchema):
    token: str = Field(min_length=1)
    password: str = Field(min_length=8)

class TokenResponse(AuthSchema):
    access_token: str = Field(min_length=1)
    refresh_token: str = Field(min_length=1)
    token_type: Literal["bearer"] = "bearer"
