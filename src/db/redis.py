from typing import Optional, Union

from aioredis import Redis, from_url

from services.base import MODEL_TYPE, MODELS_TYPE

from .base import AbstractStorage


class RedisCache(AbstractStorage):
    """Класс кэширования через redis"""

    CACHE_EXPIRE_IN_SECONDS = 60 * 5

    def __init__(self):
        self.redis: Optional[Redis] = None

    @classmethod
    async def connect(cls, url: str) -> 'RedisCache':
        self = RedisCache()
        self.redis = await from_url(url)
        return self

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, data: Union[MODEL_TYPE, MODELS_TYPE]):
        await self.redis.set(key, data.json(), ex=self.CACHE_EXPIRE_IN_SECONDS)

    async def close(self):
        await self.redis.close()


redis: Optional[Redis] = None


async def get_redis() -> Redis:
    return redis
