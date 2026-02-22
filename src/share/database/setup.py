from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.share.core.config import settings


engine = create_async_engine(
    settings.database_url,
    echo=True if settings.log_level == 'DEBUG' else False,
    future=True,
)


AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

@asynccontextmanager
async def auto_commit_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def auto_commit_session_gen() -> AsyncGenerator[AsyncSession]:
    async with auto_commit_session() as session:
        yield session
