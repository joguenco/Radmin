from src.security.validate import check_token
from src.generator.dto.subscription import (
    SubscriptionOut,
    SubscriptionIn,
)
from fastapi.encoders import jsonable_encoder
from src.generator.generate_token import generate_token
from fastapi import APIRouter, Request, status, Body, Depends
from src.config.settings import settings

router = APIRouter()
PRIVATE_KEY = settings.PRIVATE_KEY


@router.post(
    '/generator',
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

    if data['private_key'] is None:
        data['private_key'] = PRIVATE_KEY

    client_token = generate_token(
        data['identifier'],
        data['name'],
        data['email'],
        data['role'],
        data['private_key'],
        data['expitation_date'],
        data['issuer'],
        data['service'],
    )

    return SubscriptionOut(
        identifier=data['identifier'],
        name=data['name'],
        email=data['email'],
        token=client_token,
        role=data['role'],
    )
