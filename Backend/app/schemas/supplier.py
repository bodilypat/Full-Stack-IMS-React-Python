#app/schemas/supplier.py

# pyright: reportMissingImports=false
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr | None = Field(default=None)
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=500)

    model_config = ConfigDict(from_attributes=True, extra="forbid")

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = Field(default=None)
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None

    model_config = ConfigDict(from_attributes=True, extra="forbid")

class SupplierResponse(SupplierBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True, extra="forbid")
