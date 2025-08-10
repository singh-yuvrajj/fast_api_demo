from datetime import datetime
import uuid
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):

    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(default="Unknown User")
    password: str = Field(default="Unknown Password")
    email: str = Field(default="Unknown Email")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
