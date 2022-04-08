import asyncio
from typing import Optional

import aiohttp
import aioredis
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from .settings import API_VERSION, SERVICE_URL, TestSettings
from .testdata.constants import EsIndexes
from .testdata.films import FILM_INDEX, FILMS
from .testdata.genres import GENRE_INDEX, GENRES
from .testdata.persons import PERSON_INDEX, PERSONS
from .utils import HTTPResponse, populate_es


@pytest.fixture(scope='session')
def settings():
    """Инициализируем настройки"""
    return TestSettings()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def es_client(settings):
    """Открываем соединение с ES"""
    client = AsyncElasticsearch(hosts=settings.es_host)
    await populate_es(client, EsIndexes.movies.value, FILM_INDEX, FILMS)
    await populate_es(client, EsIndexes.persons.value, PERSON_INDEX, PERSONS)
    await populate_es(client, EsIndexes.genres.value, GENRE_INDEX, GENRES)
    yield client
    for index in EsIndexes:
        await client.indices.delete(index=index.value, ignore=[400, 404])
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client(settings):
    """Открываем соединение с Redis"""
    redis = await aioredis.from_url(f'{settings.redis_host}:{settings.redis_port}')
    yield redis
    await redis.close()


@pytest_asyncio.fixture(autouse=True)
async def clear_redis(redis_client):
    """Очищаем redis после каждого теста"""
    keys = await redis_client.keys()
    for key in keys:
        await redis_client.delete(key)


@pytest_asyncio.fixture(scope='session')
async def session():
    """Создаем экземпляр сессии"""
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
def make_get_request(session):
    """Делаем запрос к серверу"""
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + API_VERSION + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
