from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.service import UserService
from src.db.main import get_session
from src.services import BookService


def create_service_dependency(service_class):
    """Helper to create service dependencies"""

    async def get_service(db: AsyncSession = Depends(get_session)):
        return service_class(db)

    return get_service


# Create dependencies
get_book_service = create_service_dependency(BookService)
get_user_service = create_service_dependency(UserService)
