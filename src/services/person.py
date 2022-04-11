from functools import lru_cache

from aioredis import Redis
from fastapi import Depends

from db.base import AbstractRepository
from db.elastic import get_elastic
from db.redis import get_redis
from models import Person, Persons
from services.base import BaseService


class PersonService(BaseService):
    pass


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        db: AbstractRepository = Depends(get_elastic)
) -> PersonService:
    return PersonService(cache=redis, db=db,
                         model=Person, models=Persons, index='persons')
