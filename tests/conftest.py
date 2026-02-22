import os
import httpx
import pytest

from testcontainers.postgres import PostgresContainer 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool


from scripts.load_test_data import load_data_to_database
from src.share.database.setup import auto_commit_session_gen
from src.web.setup import get_app


os.environ['TESTCONTAINERS_RYUK_DISABLED'] = 'true'


@pytest.fixture(scope='session')
def postgres_container():
    with PostgresContainer('postgres:15') as postgres:
        yield postgres


@pytest.fixture(scope='session')
async def engine(postgres_container):
    url = postgres_container.get_connection_url()
    url = url.replace('psycopg2', 'asyncpg')
    engine = create_async_engine(
        url,
        poolclass=NullPool,
        echo=False,
    )
    yield engine
    await engine.dispose()

    
@pytest.fixture(scope='session', autouse=True)
async def prepare_db(engine):
    from src.share.database.models.base import BaseSqlAlchemyModel
    from src.share.database.models.ticker_price_model import TickerPriceModel  # noqa: F401
    
    async with engine.begin() as conn:
        await conn.run_sync(BaseSqlAlchemyModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseSqlAlchemyModel.metadata.drop_all)


@pytest.fixture(scope='session', autouse=True)
async def prepare_db_data(engine, prepare_db):
    await load_data_to_database('tests/data/ticker_prices.jsonl', engine)
    
    
@pytest.fixture(scope='function')
async def session(engine):
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
        await session.rollback()


@pytest.fixture(scope='function')
async def fake_app(session):
    async def _fake_session():
        return session
    
    app = get_app()
    app.dependency_overrides[auto_commit_session_gen] = _fake_session
    
    return app


@pytest.fixture(scope='function')
async def client(fake_app):
    transport = httpx.ASGITransport(app=fake_app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        yield client
