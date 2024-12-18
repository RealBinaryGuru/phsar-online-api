import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from .core import database
from .model import models
from .route import auth, product


@asynccontextmanager
async def lifespan(_app: FastAPI):
    max_retries = 10
    retry_interval = 1  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            with database.SessionLocal() as db:
                db.execute(text('SELECT 1'))
            print("Database connection successful.")
            break
        except OperationalError:
            print(f"Database not ready. Retrying {attempt}/{max_retries}...")
            await asyncio.sleep(retry_interval)
    else:
        print("Failed to connect to the database after multiple attempts.")
        raise Exception("Database connection failed.")

    models.Base.metadata.create_all(bind=database.engine)
    print("Database tables initialized.")
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Phsar Online API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Phsar Online API"}


app.include_router(auth.router)
app.include_router(product.router)
