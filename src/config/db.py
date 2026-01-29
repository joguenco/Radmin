from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings

async_engine = create_async_engine(url=settings.POSTGRES_URL, echo=True)


async def init_db():
    """Create the database tables"""
    async with async_engine.begin() as conn:
        from src.security.models import UnauthorizedMessage  # noqa: F401
        from src.generator.models import (
            AdministratorRoleLink,
            Role,
            Administrator,
        )  # noqa: F401

        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:  # type: ignore
    """Dependency to provide the session object"""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
