import uuid
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.auth.models import User
from src.auth.schema import UserCreate, UserUpdate


class UserService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.db.add(user)
        await self.db.commit()
        return user

    async def get_all_users(self) -> list[User]:
        query = select(User)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_user(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user_data.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)

        self.db.add(user)
        await self.db.commit()
        return user

    async def delete_user(self, user_id: uuid.UUID) -> User:

        user = await self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self.db.delete(user)
        await self.db.commit()
        return user
