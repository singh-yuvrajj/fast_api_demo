from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from src.dependencies import get_book_service
from src.schemas import BookCreate, BookRead, BookUpdate
from src.services import BookService


book_router = APIRouter()


@book_router.get("/", response_model=List[BookRead])
async def get_all_books(book_service: BookService = Depends(get_book_service)):

    try:
        books = await book_service.get_all_books()
        return books
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@book_router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate, book_service: BookService = Depends(get_book_service)
) -> dict:

    try:
        book = await book_service.create_book(book_data)
        return book
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@book_router.get("/{book_id}", response_model=BookRead, status_code=status.HTTP_200_OK)
async def get_book(book_id: int, book_service: BookService = Depends(get_book_service)):

    try:
        book = await book_service.get_book_by_id(book_id)
        return book
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@book_router.patch(
    "/{book_id}", response_model=BookRead, status_code=status.HTTP_200_OK
)
async def update_book(
    book_id: int,
    book_update_data: BookUpdate,
    book_service: BookService = Depends(get_book_service),
):

    try:
        book = await book_service.update_book(book_id, book_update_data)
        return book
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@book_router.delete(
    "/{book_id}", response_model=BookRead, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(
    book_id: int, book_service: BookService = Depends(get_book_service)
):

    try:

        book = await book_service.delete_book(book_id)
        return book
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
