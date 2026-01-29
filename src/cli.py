from sqlmodel import select
import jwt
import click
from datetime import timedelta, datetime, timezone
from config.settings import settings
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from generator.models import Administrator, Role


async_engine = create_async_engine(url=settings.POSTGRES_URL, echo=True)


async def get_session() -> AsyncSession:  # type: ignore
    """Dependency to provide the session object"""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session


async def main_async() -> str:
    current_time = datetime.now(timezone.utc)
    expiration_time = current_time + timedelta(days=180)
    private_key = settings.PRIVATE_KEY

    client_id = click.prompt('Enter identificator client', type=click.STRING)
    client_name = click.prompt('Enter name client', type=click.STRING)
    client_email = click.prompt('Enter email client', type=click.STRING)

    payload = {
        'iss': 'radmin.resolvedor.dev',
        'iat': current_time,
        'exp': expiration_time,
        'aud': 'resolvedor.dev',
        'sub': 'bussines@resolvedor.dev',
        'name': client_name,
        'email': client_email,
        'role': ['Manager'],
        'service': 'Radmin',
    }
    jwt_token = jwt.encode(payload, private_key, algorithm='HS256')

    session_gen = get_session()
    session = await session_gen.__anext__()

    statement = select(Role).where(Role.name == 'Manager')

    result = await session.exec(statement)
    result = result.first()
    if result:
        administrator_data = Administrator(
            identifier=client_id,
            name=client_name,
            email=client_email,
            token=jwt_token,
            roles=[result],
        )

        session.add(administrator_data)
        await session.commit()

        return jwt_token

    raise Exception('Role Manager not found in database')


asyncio.run(main_async())
