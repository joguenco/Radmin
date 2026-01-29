import jwt
from datetime import timedelta, datetime, timezone
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config.db import async_engine
from src.generator.models import Administrator, Role
from src.config.settings import settings

ADMIN_IDENTIFIER = settings.ADMIN_IDENTIFIER
ADMIN_NAME = settings.ADMIN_NAME
ADMIN_EMAIL = settings.ADMIN_EMAIL
PRIVATE_KEY = settings.PRIVATE_KEY
ROLES = ['Manager']


async def seed_roles():
    """Seed the database with default roles"""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        for role_name in ROLES:
            result = await session.exec(
                select(Role).where(Role.name == role_name)
            )
            role = result.one_or_none()
            if not role:
                session.add(Role(name=role_name))
        await session.commit()


async def seed_administrators():
    """Seed the database with default administrators"""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        # Add logic to seed default administrators if needed
        result = await session.exec(
            select(Administrator).where(Administrator.status)
        )
        admin = result.first()
        if not admin:
            current_time = datetime.now(timezone.utc)
            expiration_time = current_time + timedelta(days=180)

            payload = {
                'iss': 'radmin.resolvedor.dev',
                'iat': current_time,
                'exp': expiration_time,
                'aud': 'resolvedor.dev',
                'sub': 'bussines@resolvedor.dev',
                'client': ADMIN_IDENTIFIER,
                'name': ADMIN_NAME,
                'email': ADMIN_EMAIL,
                'role': ROLES,
                'service': 'Radmin',
            }

            jwt_token = jwt.encode(payload, PRIVATE_KEY, algorithm='HS256')

            statement = select(Role).where(Role.name == ROLES[0])

            result = await session.exec(statement)
            role = result.first()

            new_admin = Administrator(
                identifier=ADMIN_IDENTIFIER,
                name=ADMIN_NAME,
                email=ADMIN_EMAIL,
                token=jwt_token,
                roles=[role],
            )
            session.add(new_admin)
            await session.commit()
