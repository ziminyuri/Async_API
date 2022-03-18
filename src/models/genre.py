from typing import List

from pydantic import BaseModel

from .common import InnerFilmModel


class Genre(BaseModel):
    id: str
    name: str
    films: List[InnerFilmModel]
