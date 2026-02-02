from typing import Optional
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
    role: list[str] = ['demo']
