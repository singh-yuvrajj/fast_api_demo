from typing import Optional
import uuid
from pydantic import BaseModel
from datetime import datetime


class BookSchema(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str


class BookCreate(BookSchema):
    pass


class BookRead(BookSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[datetime] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
