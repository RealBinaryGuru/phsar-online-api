from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core import database
from src.model import models

router = APIRouter(
    prefix="/order_items",
    tags=["Order Items"]
)


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order_items(order_id: int, db: Session = Depends(database.get_db)):
    items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()
    if not items:
        raise HTTPException(status_code=404, detail="Order items not found")
    return items
