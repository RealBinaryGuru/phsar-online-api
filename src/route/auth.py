from datetime import timedelta

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.core import database
from src.core.getenv import Environment
from src.model import schemas, models
from src.util import hash
from src.util.exceptions import ErrorHandler
from src.util.hash import Encryption
from src.service import jwt

env = Environment()
SECRET_KEY = env.SECRET_KEY
ALGORITHM = env.ALGORITHM
TOKEN_EXPIRE = env.TOKEN_EXPIRE

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


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: schemas.UserAuth, db: Session = Depends(database.get_db)):
    user = validate_user(request.email, request.password, db)
    if not user:
        return ErrorHandler.Unauthorized("Invalid email or password")

    access_token_expires = timedelta(minutes=15)
    access_token = jwt.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return JSONResponse(content={"access_token": access_token})


def validate_user(email: str, password: str, session: Session):
    user = session.query(models.User).filter(models.User.email == email).first()
    if user and Encryption.check_pw(user.password, password):
        return user
