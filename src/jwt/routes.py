from src.security.validate import check_token
from src.jwt.dto.subscription import (
    SubscriptionOut,
    SubscriptionIn,
)
from fastapi.encoders import jsonable_encoder
from src.jwt.generate_token import generate_token
from fastapi import APIRouter, Request, status, Body, Depends
from src.config.settings import settings

router = APIRouter()
private_key = settings.PRIVATE_KEY


@router.post(
    '/subscriptions',
    response_description='Create a new subscription',
    status_code=status.HTTP_201_CREATED,
    response_model=SubscriptionOut,
)
async def create_subscription(
    request: Request,
    data: SubscriptionIn = Body(...),
    token: str = Depends(check_token),
):
    data = jsonable_encoder(data)

    client_token = generate_token(
        data['identifier'],
        data['name'],
        data['email'],
        data['role'],
        private_key,
    )

    return SubscriptionOut(
        identifier=data['identifier'],
        name=data['name'],
        email=data['email'],
        token=client_token,
        role=data['role'],
    )
