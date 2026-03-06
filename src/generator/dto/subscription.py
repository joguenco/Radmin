from typing import Optional
from datetime import date

from pydantic import BaseModel


class SubscriptionOut(BaseModel):
    identifier: str
    name: str
    email: str
    token: Optional[str] = None
    status: Optional[bool] = True
    role: list[str]


class SubscriptionIn(BaseModel):
    identifier: str
    name: str
    email: str
    expitation_date: date
    role: list[str] = ['demo']
    private_key: Optional[str] = None
    issuer: str
    service: str
