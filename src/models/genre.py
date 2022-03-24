from typing import List

import orjson
from pydantic import BaseModel

from helpers import orjson_dumps

from .common import InnerFilmModel


class Genre(BaseModel):
    id: str
    name: str
    films: List[InnerFilmModel] = []

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Genres(BaseModel):
    __root__: List[Genre]
