from typing import Optional

from pydantic import BaseModel


class InnerFilmModel(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[str]
