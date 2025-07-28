from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.services import BookService


async def get_book_service(db: AsyncSession = Depends(get_session)) -> BookService:
    return BookService(db)
