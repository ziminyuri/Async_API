from typing import List

from pydantic import BaseModel

from .common import BaseOrjsonModel, InnerFilmModel


class Genre(BaseOrjsonModel):
    id: str
    name: str
    films: List[InnerFilmModel] = []


class Genres(BaseModel):
    __root__: List[Genre]
