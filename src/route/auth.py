from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core import database
from src.model import schemas, models
from src.util import hash

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    hashed_password = hash.Encryption.bcrypt(request.password)

    new_user = models.User(
        **request.model_dump(exclude={"password"}),
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User successfully registered"}
