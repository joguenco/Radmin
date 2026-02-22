from typing import Tuple
import jwt
from datetime import datetime, timezone


def generate_token(
    identifier: str,
    name: str,
    email,
    role: list[str],
    private_key: str,
    expiration_date: str,
    issuer: str = 'radmin.resolvedor.dev',
    service: str = 'Radmin',
) -> Tuple[str, datetime]:
    current_time = datetime.now(timezone.utc)
    date_object = datetime.strptime(expiration_date, '%Y-%m-%d')
    integer_date = date_object.timestamp()

    payload = {
        'iss': issuer,
        'iat': current_time,
        'exp': integer_date,
        'aud': 'resolvedor.dev',
        'sub': 'bussines@resolvedor.dev',
        'client': identifier,
        'name': name,
        'email': email,
        'role': role,
        'service': service,
    }

    jwt_token = jwt.encode(payload, private_key, algorithm='HS256')

    return jwt_token
