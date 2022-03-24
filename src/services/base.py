from typing import Optional, Union

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError

from db.redis import get_key_for_list
from models import Film, Films, Genre, Genres, Person, Persons
from services.es_parser import PARAMS_TYPE, make_query_body

CACHE_EXPIRE_IN_SECONDS = 60 * 5

MODEL_TYPE = Union[Film, Person, Genre]
MODELS_TYPE = Union[Films, Persons, Genres]


class BaseService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch,
                 model: MODEL_TYPE, models: MODELS_TYPE, index: str):
        self.redis = redis
        self.elastic = elastic
        self.model = model
        self.models = models
        self.index = index

    async def get_by_id(self, id_: str) -> Optional[MODEL_TYPE]:
        hash_ = get_key_for_list(self.index, id_)
        data = await self._data_from_cache(hash_)

        if not data:
            data = await self._get_doc_from_elastic(id_)
            if not data:
                return None
            await self._put_data_to_cache(hash_, data)

        return data

    async def get_by_params(self, params: PARAMS_TYPE) -> Optional[MODELS_TYPE]:
        query_body = make_query_body(params)
        hash_ = get_key_for_list(self.index, params.__dict__)

        data = await self._data_from_cache(hash_, many=True)
        if not data:
            data = await self._search_docs_in_elastic(query_body)
            if not data:
                return None
            await self._put_data_to_cache(hash_, data)

        return data

    async def _search_docs_in_elastic(self, query_body: dict) -> Optional[MODELS_TYPE]:
        try:
            doc = await self.elastic.search(body=query_body, index=self.index)
        except NotFoundError:
            return None
        return self.models.parse_obj(self.parse_es_response(doc))

    async def _get_doc_from_elastic(self, id_: str) -> Optional[MODEL_TYPE]:
        try:
            doc = await self.elastic.get(index=self.index, id=id_)
        except NotFoundError:
            return None
        return self.model.parse_obj(doc['_source'])

    async def _data_from_cache(self,
                               key: str,
                               many=False) -> Optional[Union[MODEL_TYPE, MODELS_TYPE]]:
        data = await self.redis.get(key)
        if not data:
            return None
        return self.models.parse_raw(data) if many else self.model.parse_raw(data)

    async def _put_data_to_cache(self, key: str, current: Union[MODEL_TYPE, MODELS_TYPE]):
        await self.redis.set(key, current.json(), ex=CACHE_EXPIRE_IN_SECONDS)

    @staticmethod
    def parse_es_response(data):
        return [record['_source'] for record in data['hits']['hits']]
