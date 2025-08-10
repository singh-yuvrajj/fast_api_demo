from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from src.config import get_settings

settings = get_settings()

engine = AsyncEngine(create_engine(url=settings.DATABASE_URL, echo=True))

async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False
)


async def get_session():

    async with async_session() as session:
        yield session


async def create_db_and_tables():

    async with engine.begin() as conn:

        from src.models.book import Book
        from src.auth.models import User

        # print("Dropping all tables")
        # await conn.run_sync(SQLModel.metadata.drop_all)
        # print("Dropped all tables")

        print("Creating all tables")
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Created all tables")
