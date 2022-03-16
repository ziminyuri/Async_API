from typing import Optional, List

import orjson
from pydantic import BaseModel

from helpers import orjson_dumps


class Film(BaseModel):
    id: str
    imdb_rating: Optional[str]
    genre: List[str] = []
    title: str
    description: Optional[str]
    director: List[str] = []
    actors_names: List[str] = []
    writers_names: List[str] = []
    actors: List[dict] = []
    writers: List[dict] = []

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
