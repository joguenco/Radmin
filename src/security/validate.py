import typing
from fastapi import HTTPException, Request, status, Depends
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from src.security.models import UnauthorizedMessage
from src.config.db import get_session
from src.generator.models import Administrator
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
        detail = 'No token provided'
        await message_unauthorized(request, session, detail)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )

    token = auth.credentials

    if len(token) < 180:
        detail = 'Not authorized'
        await message_unauthorized(request, session, detail)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )

    statement = (
        select(Administrator)
        .where(Administrator.token == token)
        .where(Administrator.status)
        .order_by(Administrator.created_at.desc())
    )
    result = await session.exec(statement)

    if result.first() is None:
        detail = 'Not authorized'
        await message_unauthorized(request, session, detail)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )

    return token


async def message_unauthorized(
    request: Request,
    session: AsyncSession = Depends(get_session),
    detail: str = 'Not authorized',
) -> None:
    message = request.url.path + ' - ' + request.url.hostname
    session.add(UnauthorizedMessage(description=f'{message} - {detail}'))
    await session.commit()
