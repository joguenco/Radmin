import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class AdministratorRoleLink(SQLModel, table=True):
    __tablename__ = 'administrator_role_link'
    role_id: int | None = Field(
        default=None, foreign_key='roles.id', primary_key=True
    )
    administrator_id: int | None = Field(
        default=None, foreign_key='administrators.id', primary_key=True
    )
    created_at: datetime.datetime = Field(default=datetime.datetime.now)


class Role(SQLModel, table=True):
    __tablename__ = 'roles'
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    status: Optional[bool] = True
    created_at: datetime.datetime = Field(default=datetime.datetime.now)
    updated_at: datetime.datetime = Field(
        default=datetime.datetime.now,
        sa_column_kwargs={'onupdate': datetime.datetime.now},
    )

    administrators: list['Administrator'] = Relationship(
        back_populates='roles', link_model=AdministratorRoleLink
    )


class Administrator(SQLModel, table=True):
    __tablename__ = 'administrators'
    id: int | None = Field(default=None, primary_key=True)
    identifier: str = Field(index=True, unique=True)
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    token: str
    status: Optional[bool] = True
    expiration_date: datetime.datetime = Field()
    created_at: datetime.datetime = Field(default=datetime.datetime.now)
    updated_at: datetime.datetime = Field(
        default=datetime.datetime.now,
        sa_column_kwargs={'onupdate': datetime.datetime.now},
    )

    roles: list[Role] = Relationship(
        back_populates='administrators', link_model=AdministratorRoleLink
    )
