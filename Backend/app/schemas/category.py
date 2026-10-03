#app/schemas/category.py
# pyright: reportMissingImports=false

from pydantic import BaseModel, ConfigDict, Field

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, strip_whitespace=True)
    description: str | None = Field(default=None, max_length=500, strip_whitespace=True)

class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100, strip_whitespace=True)
    description: str | None = Field(default=None, max_length=500, strip_whitespace=True)

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


