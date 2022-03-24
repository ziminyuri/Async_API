from typing import Optional, Union

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from orjson import loads

from helpers import orjson_dumps
from models.film import Film, Films
from models.genre import Genre, Genres
from models.person import Person, Persons
from redis import get_key_for_list
from services.es_parser import make_query_body

CACHE_EXPIRE_IN_SECONDS = 60 * 5

MODELS_TYPE = Union[Film, Person, Genre]


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

    async def get_by_params(self, params) -> list[MODELS_TYPE]:
        query_body = make_query_body(params)
        redis_key = get_key_for_list(self.index, query_body)
        #
        # object_list = await self._list_from_cache(redis_key)
        object_list = None
        if not object_list:
            try:
                doc = await self.elastic.search(body=query_body, index=self.index)
            except NotFoundError:
                object_list = None
            else:
                plural_model = self.get_plural_models()
                object_list = plural_model.parse_obj(self.parse_es_response(doc))
                # object_list = [
                #     self.model(**_doc["_source"]) for _doc in doc["hits"]["hits"]
                # ]
                await self._put_list_to_cache(redis_key, object_list)

        return object_list

    async def _list_from_cache(self, redis_key: str) -> Optional[list[MODELS_TYPE]]:
        data = await self.redis.get(redis_key)
        if not data:
            return None

        obj = [self.model.parse_raw(_data) for _data in loads(data)]
        return obj

    async def _put_list_to_cache(self, redis_key: str, object_list: list[MODELS_TYPE]):
        await self.redis.set(
            redis_key,
            orjson_dumps(object_list, default=self.model.json),
            ex=CACHE_EXPIRE_IN_SECONDS,
        )

    @staticmethod
    def parse_es_response(data):
        return [record['_source'] for record in data['hits']['hits']]

    def get_plural_models(self):
        if self.model == Film:
            return Films
        elif self.model == Genre:
            return Genres
        elif self.model == Person:
            return Persons
