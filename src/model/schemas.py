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


class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    name: Optional[str]
    quantity: int
    price: int
    total: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    order_id: int
    user_id: int
    product: List[OrderItemCreate]

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    name: str
    user_id: int
    email: str
    is_admin: bool

    class Config:
        from_attributes = True


class OrderUpdateStatus(BaseModel):
    order_id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    email: Optional[str] = None


class UserDetailResponse(BaseModel):
    user_id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class PasswordResetRequest(BaseModel):
    email: str
