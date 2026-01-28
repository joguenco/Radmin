from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime


class UnauthorizedMessage(SQLModel, table=True):
    __tablename__ = 'unauthorized_messages'
    uid: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4)
    )

    description: str
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )

    def __repr__(self) -> str:
        return f'UnauthorizedMessage => {self.description}'
