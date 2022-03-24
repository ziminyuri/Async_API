from typing import List

import orjson
from pydantic import BaseModel

from helpers import orjson_dumps
from .common import InnerFilmModel


class PersonFilmModel(InnerFilmModel):
    role: str


class Person(BaseModel):
    id: str
    full_name: str
    roles: List[str]
    films: List[PersonFilmModel]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Persons(BaseModel):
    __root__: List[Person]
