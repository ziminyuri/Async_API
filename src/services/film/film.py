from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, Films
from services.film.query import film_search_query

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    INDEX = 'movies'

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)

        if not film:
            film = await self._get_film(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film.id, film.json())

        return film

    async def get_by_query(self, query: str, page: int, size: int) -> Optional[Film]:
        cache_identifier = f"{query}:{page}:{size}"
        films = await self._film_from_cache(cache_identifier, many=True)

        if not films:
            films = await self._get_films_by_query(query, page, size)
            if not films:
                return None
            await self._put_film_to_cache(cache_identifier, films.json())

        return films

    async def _get_film(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index=self.INDEX, id=film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _get_films_by_query(self, query: str, page: int, size: int):
        try:
            doc = await self.elastic.search(index=self.INDEX,
                                            query=film_search_query(query),
                                            from_=self._get_offset(page, size),
                                            size=size)
        except NotFoundError:
            return None
        return Films.parse_obj(self.parse_es_response(doc))

    async def _film_from_cache(self, film_data: str, many=False) -> Optional[Film]:
        data = await self.redis.get(film_data)
        if not data:
            return None

        return Films.parse_raw(data) if many else Film.parse_raw(data)

    async def _put_film_to_cache(self, identifier: str, data: str):
        await self.redis.set(identifier, data, ex=FILM_CACHE_EXPIRE_IN_SECONDS)

    @staticmethod
    def _get_offset(page: int, size: int) -> int:
        return (page - 1) * size

    @staticmethod
    def parse_es_response(data):
        return [record['_source'] for record in data['hits']['hits']]


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
