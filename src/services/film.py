from functools import lru_cache

from aioredis import Redis
from fastapi import Depends

from db.base import AbstractRepository
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, Films
from services.base import BaseService


class FilmService(BaseService):
    pass


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        db: AbstractRepository = Depends(get_elastic)
) -> FilmService:
    return FilmService(redis=redis, db=db,
                       model=Film, models=Films, index='movies')
