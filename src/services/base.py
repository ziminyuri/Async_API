from typing import Optional, Union

from aioredis import Redis
from elasticsearch.exceptions import NotFoundError

from db.base import AbstractRepository
from db.redis import get_key_for_list
from models import Film, Films, Genre, Genres, Person, Persons
from services.es_parser import PARAMS_TYPE

CACHE_EXPIRE_IN_SECONDS = 60 * 5

MODEL_TYPE = Union[Film, Person, Genre]
MODELS_TYPE = Union[Films, Persons, Genres]


class BaseService:
    def __init__(self, redis: Redis, db: AbstractRepository,
                 model: MODEL_TYPE, models: MODELS_TYPE, index: str):
        self.redis = redis
        self.db = db
        self.model = model
        self.models = models
        self.index = index

    async def get_by_id(self, id_: str) -> Optional[MODEL_TYPE]:
        hash_ = get_key_for_list(self.index, id_)
        data = await self._data_from_cache(hash_)

        if not data:
            data = await self._get_from_db(id_)
            if not data:
                return None
            await self._put_data_to_cache(hash_, data)

        return data

    async def get_by_params(self, params: PARAMS_TYPE) -> Optional[MODELS_TYPE]:
        hash_ = get_key_for_list(self.index, params.__dict__)

        data = await self._data_from_cache(hash_, many=True)
        if not data:
            data = await self._search_in_db(params)
            if not data:
                return None
            await self._put_data_to_cache(hash_, data)

        return data

    async def _search_in_db(self, params: PARAMS_TYPE) -> Optional[MODELS_TYPE]:
        try:
            doc = await self.db.search(index=self.index, params=params)
        except NotFoundError:
            return None
        return self.models.parse_obj(doc)

    async def _get_from_db(self, id_: str) -> Optional[MODEL_TYPE]:
        try:
            doc = await self.db.get(index=self.index, id_=id_)
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
