from typing import List

from pydantic import BaseModel

from .common import InnerFilmModel


class PersonFilmModel(InnerFilmModel):
    role: str


class Person(BaseModel):
    id: str
    full_name: str
    roles: List[str]
    films: List[PersonFilmModel]
