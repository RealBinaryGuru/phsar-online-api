from pydantic import BaseModel
from typing import Optional, List


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_admin: Optional[bool] = False

    class Config:
        from_attributes = True


class UserAuth(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


# Products
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int
    is_active: bool = True


class ProductCreate(ProductBase):
    pass
