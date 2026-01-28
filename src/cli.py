import jwt
import click
from datetime import timedelta, datetime, timezone
from config.settings import settings

current_time = datetime.now(timezone.utc)
expiration_time = current_time + timedelta(days=365)
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

print(jwt_token)
