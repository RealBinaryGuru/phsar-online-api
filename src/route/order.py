from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.core import database
from src.model import schemas, models
from src.service.jwt import verify_access_token
from src.util.exceptions import ErrorHandler

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        print(f"Debug: Received token: {token}")  # Debug: Print the received token
        payload = verify_access_token(token)
        print(f"Debug: Decoded payload: {payload}")  # Debug: Print the decoded payload
        return payload["user_id"]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Debug: Token verification failed: {e}")  # Debug: Print the error
        raise ErrorHandler.Unauthorized("Invalid or expired token")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    request: schemas.OrderCreate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(get_current_user)
):
    order = models.Order(user_id=user_id, total_price=0)
    db.add(order)
    db.commit()
    db.refresh(order)

    total_price = 0
    for item in request.items:
        product = db.query(models.Product).filter(models.Product.product_id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for Product {item.product_id}")

        product.stock -= item.quantity
        db.commit()

        order_item = models.OrderItem(
            order_id=order.order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(order_item)
        total_price += product.price * item.quantity

    order.total_price = total_price
    db.commit()
    return order


@router.get("/", status_code=status.HTTP_200_OK)
async def get_orders(
    db: Session = Depends(database.get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(
    order_id: int,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(get_current_user)
):
    order = db.query(models.Order).filter(models.Order.order_id == order_id, models.Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
