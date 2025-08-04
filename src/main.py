from fastapi import FastAPI
from src.auth.router import auth_router
from src.routers import book_router
from contextlib import asynccontextmanager

from src.db.main import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server has started")
    await create_db_and_tables()
    yield
    print("server has ended")


version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
    lifespan=lifespan,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
