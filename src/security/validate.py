import typing
from fastapi import HTTPException, Request, status, Depends
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from src.security.models import UnauthorizedMessage
from src.config.db import get_session
from src.jwt.models import Administrator
from sqlmodel import select


get_bearer_token = HTTPBearer(auto_error=False)


async def check_token(
    request: Request,
    auth: typing.Optional[HTTPAuthorizationCredentials] = Depends(
        get_bearer_token
    ),
    session: AsyncSession = Depends(get_session),
) -> str:
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not token provided',
        )

    token = auth.credentials

    statement = select(Administrator).where(Administrator.token == token)
    result = await session.exec(statement)

    if result.first() is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authorized',
        )

    return token
