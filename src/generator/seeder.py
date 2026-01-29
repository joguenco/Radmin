from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config.db import async_engine
from src.generator.models import Role


async def seed_roles():
    """Seed the database with default roles"""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        roles = ['Manager']
        for role_name in roles:
            result = await session.exec(
                select(Role).where(Role.name == role_name)
            )
            role = result.one_or_none()
            if not role:
                session.add(Role(name=role_name))
        await session.commit()
