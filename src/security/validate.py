import typing
from fastapi import HTTPException, Request, status, Depends
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

from src.security.models import UnauthorizedMessage


get_bearer_token = HTTPBearer(auto_error=False)


async def check_token(
    request: Request,
    auth: typing.Optional[HTTPAuthorizationCredentials] = Depends(
        get_bearer_token
    ),
) -> str:
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message='Not token provided',
        )

    token = auth.credentials
    subscription = await request.app.mongodb['subscriptions'].find_one(
        {'token': token, 'status': True, 'role': 'Manager'}
    )

    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message='Not authorized',
        )

    return token
