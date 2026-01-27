import sys
import platform
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config.db import get_session
from sqlmodel import text


router = APIRouter()


@router.get('/version')
async def version(session: AsyncSession = Depends(get_session)):
    result = await session.exec(text('select version()'))
    version_db = result.one()[0]

    return {
        'name': 'Radmin',
        'author': 'Jorge Luis',
        'website': 'https://resolvedor.dev',
        'version': '0.0.1',
        'versionOS': platform.platform(),
        'versionRuntime': f'Python {sys.version}',
        'versionDatabase': version_db,
    }
