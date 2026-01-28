from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config.db import init_db
from src.ping.routes import router as ping_router
from src.version.routes import router as version_router
from src.jwt.routes import router as jwt_router
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info('Database initialized successfully.')
    yield
    # Place for shutdown code if needed in the future
    logger.info('Application shutdown complete.')


app = FastAPI(lifespan=lifespan)

app.include_router(ping_router)
app.include_router(version_router)
app.include_router(jwt_router)
