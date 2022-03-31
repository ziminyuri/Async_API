from typing import List

from pydantic import BaseModel

from .common import BaseOrjsonModel, InnerFilmModel


class PersonFilmModel(InnerFilmModel):
    role: str


class Person(BaseOrjsonModel):
    id: str
    full_name: str
    roles: List[str]
    films: List[PersonFilmModel]


class Persons(BaseModel):
    __root__: List[Person]
