from collections.abc import AsyncGenerator

import pytest_asyncio
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import clear_mappers

from src.core.config import settings
from src.infrastructure.models import start_mappers


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.postgres.connection_url)
    try:
        async with engine.connect() as connection:
            transaction = await connection.begin()
            start_mappers()
            session_factory = async_sessionmaker(
                bind=connection,
                expire_on_commit=False,
                join_transaction_mode="create_savepoint",
            )
            try:
                async with session_factory() as session:
                    yield session
            finally:
                await transaction.rollback()
    finally:
        clear_mappers()
        await engine.dispose()


@pytest_asyncio.fixture
async def redis_client() -> AsyncGenerator[Redis, None]:
    client = Redis.from_url(settings.redis.url)
    try:
        await client.flushdb()
        yield client
    finally:
        await client.flushdb()
        await client.aclose()
