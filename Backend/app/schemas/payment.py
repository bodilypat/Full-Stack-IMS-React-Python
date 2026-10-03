#app/schemas/payment.py

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field  # pyright: ignore[reportMissingImports]

class PaymentBase(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    method: str = Field(min_length=1, max_length=50, strip_whitespace=True)
    reference: str | None = Field(default=None, max_length=100, strip_whitespace=True)

class PaymentCreate(PaymentBase):
    sale_id: int = Field(gt=0)

class PaymentResponse(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sale_id: int
    created_at: datetime
