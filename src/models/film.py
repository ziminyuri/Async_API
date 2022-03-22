from typing import List, Optional

import orjson
from pydantic import BaseModel

from helpers import orjson_dumps


class InnerModel(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: Optional[str]
    genres: List[InnerModel] = []
    title: str
    description: Optional[str]
    directors_names: List[str] = []
    actors_names: List[str] = []
    writers_names: List[str] = []
    directors: List[InnerModel] = []
    actors: List[InnerModel] = []
    writers: List[InnerModel] = []

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Films(BaseModel):
    __root__: List[Film]
