from functools import lru_cache

from aioredis import Redis
from fastapi import Depends

from db.base import AbstractRepository
from db.elastic import get_elastic
from db.redis import get_redis
from models import Genre, Genres
from services.base import BaseService


class GenreService(BaseService):
    pass


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        db: AbstractRepository = Depends(get_elastic)
) -> GenreService:
    return GenreService(cache=redis, db=db,
                        model=Genre, models=Genres, index='genres')
