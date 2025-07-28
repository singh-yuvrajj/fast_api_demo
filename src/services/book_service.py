from datetime import datetime
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.models import Book
from src.schemas import BookCreate
from src.schemas import BookUpdate


class BookService:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all_books(self) -> list[Book]:

        query = select(Book).order_by(Book.id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_book(self, book_data: BookCreate) -> Book:

        book = Book(**book_data.model_dump())
        self.db.add(book)
        await self.db.commit()

        # Needed when database level default values are used
        # await self.db.refresh(book)

        return book

    async def get_book(self, book_id: int) -> Book:

        query = select(Book).where(Book.id == book_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_book(self, book_id: int, book_data: BookUpdate) -> Book:

        book = await self.get_book(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)

        book.updated_at = datetime.now()

        await self.db.commit()

        return book

    async def delete_book(self, book_id: int) -> Book:

        book = await self.get_book(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        await self.db.delete(book)
        await self.db.commit()

        return book
