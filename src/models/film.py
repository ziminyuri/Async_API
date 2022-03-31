from typing import List, Optional

from pydantic import BaseModel

from .common import BaseOrjsonModel


class InnerModel(BaseOrjsonModel):
    id: str
    name: str


class Film(BaseOrjsonModel):
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


class Films(BaseModel):
    __root__: List[Film]
