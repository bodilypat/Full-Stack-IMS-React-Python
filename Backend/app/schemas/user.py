#app/aschemas/user.py
# pyright: reportMissingImports=false

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    role: str = Field(..., min_length=2, max_length=50)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: EmailStr) -> EmailStr:
        return str(value).lower()

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        return value.strip()


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    role: str | None = Field(default=None, min_length=2, max_length=50)
    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: EmailStr | None) -> EmailStr | None:
        if value is None:
            return value
        return str(value).lower()


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, extra="ignore")
