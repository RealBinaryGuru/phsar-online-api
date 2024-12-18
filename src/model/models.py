from sqlalchemy import Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from src.core.database import Base


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String)
    time: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)


class Product(Base):
    __tablename__ = 'products'

    product_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Order(Base):
    __tablename__ = 'orders'

    order_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String, default="Pending")  # Pending, Shipped, Delivered
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)


class OrderItem(Base):
    __tablename__ = 'order_items'

    order_item_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
