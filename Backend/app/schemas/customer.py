#app/schemas/customer.py

try:
    from pydantic import BaseModel, ConfigDict, EmailStr  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    from pydantic import BaseModel, EmailStr  # type: ignore[import-not-found]

    ConfigDict = None


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None

    if ConfigDict is not None:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            orm_mode = True
