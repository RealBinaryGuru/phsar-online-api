from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core import database
from src.model import schemas, models

router = APIRouter(prefix="/products",
                   tags=["Products"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(request: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    product = models.Product(**request.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/", status_code=status.HTTP_200_OK)
async def get_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
