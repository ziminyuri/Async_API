from typing import List, Optional

from pydantic import BaseModel, Field

from models.common import BaseOrjsonModel


class FilmGenre(BaseOrjsonModel):
    id: str
    name: str


class FilmPerson(BaseOrjsonModel):
    id: str
    full_name: str = Field('', alias='name')


class FilmDetail(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    genres: List[FilmGenre]
    actors: List[FilmPerson]
    writers: List[FilmPerson]
    directors: List[FilmPerson]


class Film(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: Optional[float]


class Films(BaseModel):
    __root__: List[Film]
