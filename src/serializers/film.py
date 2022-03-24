from typing import List, Optional

from pydantic import BaseModel, Field


class FilmGenre(BaseModel):
    id: str
    name: str


class FilmPerson(BaseModel):
    id: str
    full_name: str = Field("", alias='name')


class FilmDetail(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    genres: List[FilmGenre]
    actors: List[FilmPerson]
    writers: List[FilmPerson]
    directors: List[FilmPerson]


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]


class Films(BaseModel):
    __root__: List[Film]
