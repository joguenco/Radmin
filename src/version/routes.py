import sys
import platform
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config.db import get_session
from sqlmodel import text
from src.security.validate import check_token

router = APIRouter()


@router.get('/version')
async def version(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(check_token),
):
    result = await session.exec(text('select version()'))
    version_db = result.one()[0]

    return {
        'name': 'Radmin',
        'author': 'Jorge Luis',
        'website': 'https://resolvedor.dev',
        'version': '1.0.0',
        'versionOS': platform.platform(),
        'versionRuntime': f'Python {sys.version}',
        'versionDatabase': version_db,
    }
