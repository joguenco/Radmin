from typing import Tuple
import jwt
from datetime import datetime, timezone


def generate_token(
    identifier: str, name: str, email, role: str, private_key: str
) -> Tuple[str, datetime]:
    current_time = datetime.now(timezone.utc)

    payload = {
        'iss': 'radmin.resolvedor.dev',
        'iat': current_time,
        'aud': 'resolvedor.dev',
        'client': identifier,
        'name': name,
        'email': email,
        'role': role,
        'service': 'Radmin',
    }

    jwt_token = jwt.encode(payload, private_key, algorithm='HS256')

    return jwt_token
