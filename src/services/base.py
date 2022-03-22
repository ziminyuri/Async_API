from functools import lru_cache
from typing import Optional, Union

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from models.film import Film

CACHE_EXPIRE_IN_SECONDS = 60 * 5

MODELS_TYPE = Union[Film, Person]


class BaseService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, model: MODELS_TYPE, index: str):
        self.redis = redis
        self.elastic = elastic
        self.model = model
        self.index = index

    async def get_by_id(self, id: str) -> Optional[MODELS_TYPE]:
        current = await self._current_from_cache(f'{self.index}:{id}')

        if not current:
            current = await self._get_current_from_elastic(id)
            if not current:
                return None
            await self._put_current_to_cache(f'{self.index}:{id}', current)

        return current

    async def _get_current_from_elastic(self, id: str) -> Optional[MODELS_TYPE]:
        try:
            doc = await self.elastic.get(index=self.index, id=id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])

    async def _current_from_cache(self, key: str) -> Optional[MODELS_TYPE]:
        data = await self.redis.get(key)
        if not data:
            return None

        current = self.model.parse_raw(data)
        return current

    async def _put_current_to_cache(self, key: str, current: MODELS_TYPE):
        await self.redis.set(key, current.json(), ex=CACHE_EXPIRE_IN_SECONDS)

