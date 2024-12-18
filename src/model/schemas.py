from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


# Users
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
    description: Optional[str] = None
    price: float
    stock: int
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    product_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Orders
class OrderBase(BaseModel):
    total_price: float = 0.0
    status: str = "Pending"


class OrderCreate(BaseModel):
    items: List["OrderItemCreate"]


class OrderOut(OrderBase):
    order_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Order Items
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    order_item_id: int
    price: float

    class Config:
        from_attributes = True
