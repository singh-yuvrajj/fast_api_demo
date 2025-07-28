from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.schemas import BookCreate, BookRead, BookUpdate
from src.models import Book
from src.services import BookService


book_router = APIRouter()


@book_router.get("/", response_model=List[BookRead])
async def get_all_books(db: AsyncSession = Depends(get_session)):

    try:
        book_service = BookService(db)
        books = await book_service.get_all_books()
        return books
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookCreate) -> dict:
    pass


@book_router.get("/{book_id}", response_model=BookRead, status_code=status.HTTP_200_OK)
async def get_book(book_id: int):
    pass


@book_router.patch("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, book_update_data: BookUpdate):
    pass


@book_router.delete(
    "/{book_id}", response_model=BookRead, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(book_id: int):
    pass
