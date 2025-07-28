import uuid
from sqlmodel import Field, SQLModel
from datetime import datetime


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(default=uuid.uuid4, primary_key=True)
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str
    created_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now)
